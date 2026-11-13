// Persistência em arquivos JSON, um processo só. Tudo fica em memória e é
// gravado em disco de forma atômica (arquivo temporário + rename) logo após
// cada mudança. Suficiente para o piloto de uma marina; os dados são legíveis
// e fáceis de exportar ou apagar.

import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

export function novoId(prefixo) {
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

  s.descarregar = () => {
    if (timer) clearTimeout(timer);
    timer = null;
    for (const chave of [...sujos]) {
      sujos.delete(chave);
      gravar(chave);
    }
  };

  /** Marca uma coleção como alterada: 'config', 'ficha', 'clientes',
   *  'registros', 'chamados', 'rascunhos', 'sugestoes', 'equipe' ou
   *  'conversa:<id>'. */
  s.salvar = (chave) => {
    sujos.add(chave);
    if (!timer) timer = setTimeout(s.descarregar, 50);
  };

  s.registrarUso = (linha) => {
    fs.appendFileSync(arq('uso.jsonl'), `${JSON.stringify(linha)}\n`);
  };

  s.lerUso = () => {
    try {
      return fs
        .readFileSync(arq('uso.jsonl'), 'utf8')
        .split('\n')
        .filter(Boolean)
        .map((l) => JSON.parse(l));
    } catch (e) {
      if (e.code === 'ENOENT') return [];
      throw e;
    }
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
