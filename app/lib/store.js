// Persistência em arquivos JSON, um processo só. Tudo fica em memória e é
// gravado em disco de forma atômica (arquivo temporário + rename) logo após
// cada mudança. Suficiente para o piloto de uma marina; os dados são legíveis
// e fáceis de exportar ou apagar.

import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

// Nos testes de bancada os ids são sequenciais, para que repetir a mesma
// conversa produza exatamente os mesmos pedidos ao modelo.
let sequencia = null;
export function idsSequenciais() {
  sequencia = 0;
}

export function novoId(prefixo) {
  if (sequencia !== null) return `${prefixo}_${String(++sequencia).padStart(6, '0')}`;
  return `${prefixo}_${crypto.randomBytes(5).toString('hex')}`;
}

export function novoToken() {
  return crypto.randomBytes(16).toString('base64url');
}

function lerJson(arquivo, padrao) {
  try {
    return JSON.parse(fs.readFileSync(arquivo, 'utf8'));
  } catch (e) {
    if (e.code === 'ENOENT') return padrao;
    throw new Error(`Arquivo de dados corrompido: ${arquivo} (${e.message})`);
  }
}

function gravarAtomico(arquivo, texto) {
  const tmp = `${arquivo}.${process.pid}.tmp`;
  fs.writeFileSync(tmp, texto);
  fs.renameSync(tmp, arquivo);
}

export function criarStore(dir) {
  fs.mkdirSync(path.join(dir, 'conversas'), { recursive: true });
  fs.mkdirSync(path.join(dir, 'fotos'), { recursive: true });

  const arq = (nome) => path.join(dir, nome);
  const sujos = new Set();
  let timer = null;

  const s = {
    dir,
    config: lerJson(arq('config.json'), null),
    ficha: fs.existsSync(arq('ficha.md')) ? fs.readFileSync(arq('ficha.md'), 'utf8') : null,
    clientes: lerJson(arq('clientes.json'), []),
    registros: lerJson(arq('registros.json'), []),
    chamados: lerJson(arq('chamados.json'), []),
    rascunhos: lerJson(arq('rascunhos.json'), []),
    sugestoes: lerJson(arq('sugestoes.json'), []),
    equipe: lerJson(arq('equipe.json'), {}),
    conversas: new Map(),
  };

  for (const f of fs.readdirSync(arq('conversas'))) {
    if (!f.endsWith('.json')) continue;
    const c = lerJson(path.join(arq('conversas'), f), null);
    if (c && c.id) s.conversas.set(c.id, c);
  }

  function gravar(chave) {
    if (chave === 'config') gravarAtomico(arq('config.json'), JSON.stringify(s.config, null, 2));
    else if (chave === 'ficha') gravarAtomico(arq('ficha.md'), s.ficha ?? '');
    else if (chave === 'clientes') gravarAtomico(arq('clientes.json'), JSON.stringify(s.clientes, null, 2));
    else if (chave === 'registros') gravarAtomico(arq('registros.json'), JSON.stringify(s.registros, null, 2));
    else if (chave === 'chamados') gravarAtomico(arq('chamados.json'), JSON.stringify(s.chamados, null, 2));
    else if (chave === 'rascunhos') gravarAtomico(arq('rascunhos.json'), JSON.stringify(s.rascunhos));
    else if (chave === 'sugestoes') gravarAtomico(arq('sugestoes.json'), JSON.stringify(s.sugestoes, null, 2));
    else if (chave === 'equipe') gravarAtomico(arq('equipe.json'), JSON.stringify(s.equipe, null, 2));
    else if (chave.startsWith('conversa:')) {
      const id = chave.slice(9);
      const c = s.conversas.get(id);
      const destino = path.join(arq('conversas'), `${id}.json`);
      if (c) gravarAtomico(destino, JSON.stringify(c));
      else fs.rmSync(destino, { force: true });
    }
  }

  // Erro de gravação (disco cheio, permissão) não pode derrubar o processo
  // de dentro de um timer: a chave continua marcada e a gravação é tentada
  // de novo em instantes.
  s.descarregar = () => {
    if (timer) clearTimeout(timer);
    timer = null;
    let falhou = false;
    for (const chave of [...sujos]) {
      try {
        gravar(chave);
        sujos.delete(chave);
      } catch (e) {
        falhou = true;
        console.error(`[dados] não consegui gravar "${chave}": ${e.message}`);
      }
    }
    if (falhou && !timer) {
      timer = setTimeout(s.descarregar, 5000);
      timer.unref?.();
    }
    return !falhou;
  };

  /** Marca uma coleção como alterada: 'config', 'ficha', 'clientes',
   *  'registros', 'chamados', 'rascunhos', 'sugestoes', 'equipe' ou
   *  'conversa:<id>'. */
  s.salvar = (chave) => {
    sujos.add(chave);
    if (!timer) timer = setTimeout(s.descarregar, 50);
  };

  s.registrarUso = (linha) => {
    try {
      fs.appendFileSync(arq('uso.jsonl'), `${JSON.stringify(linha)}\n`);
    } catch (e) {
      console.error(`[dados] não consegui gravar o uso da IA: ${e.message}`);
    }
  };

  // Uma linha cortada (queda no meio da gravação) é pulada, não impede a partida.
  s.lerUso = () => {
    let texto;
    try {
      texto = fs.readFileSync(arq('uso.jsonl'), 'utf8');
    } catch (e) {
      if (e.code === 'ENOENT') return [];
      throw e;
    }
    const linhas = [];
    for (const l of texto.split('\n')) {
      if (!l) continue;
      try {
        linhas.push(JSON.parse(l));
      } catch {
        /* linha incompleta */
      }
    }
    return linhas;
  };

  /** Segredo de sessão: vem do ambiente ou é criado e guardado na pasta de dados. */
  s.segredo = () => {
    if (process.env.SESSION_SECRET) return process.env.SESSION_SECRET;
    const f = arq('segredo.txt');
    if (!fs.existsSync(f)) fs.writeFileSync(f, crypto.randomBytes(32).toString('hex'), { mode: 0o600 });
    return fs.readFileSync(f, 'utf8').trim();
  };

  s.caminhoFoto = (nome) => path.join(arq('fotos'), path.basename(nome));

  return s;
}
