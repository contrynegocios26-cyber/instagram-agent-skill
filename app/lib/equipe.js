// Equipe de agentes de retaguarda. Cada agente olha os dados da marina e
// prepara sugestões (mensagens prontas, resumos, ideias) que alguém da
// equipe confere e envia. Nada sai sozinho para cliente nenhum.
//
// Os fatos são levantados por código. A IA só reescreve o texto no tom da
// marina; se ela falhar, ou no modo de demonstração, vale o texto-modelo.

import { novoId } from './store.js';
import { agora, carimbo, somarDias, diasEntre, dataPorExtenso, horaFalada, dataValida } from './tempo.js';
import { relatorio } from './relatorio.js';
import { custoEstimado } from './ia.js';

export const AGENTES = {
  operacao: { nome: 'Operação', oQue: 'Resumo do dia para a equipe da rampa: descidas, serviços, aluguéis e pendências.', quando: 'todo dia', semanal: false, comIA: false },
  relacionamento: {
    nome: 'Relacionamento',
    oQue: 'Lembretes de vencimento, revisão e documento, mensagem de pós-passeio e retomada de quem sumiu.',
    quando: 'todo dia',
    semanal: false,
    comIA: true,
  },
  vendas: { nome: 'Vendas', oQue: 'Retorno para quem perguntou de aluguel, vaga ou barco à venda e não fechou.', quando: 'todo dia', semanal: false, comIA: true },
  gerente: { nome: 'Gerente', oQue: 'Resumo da semana para o dono, com os números do atendimento e da rampa.', quando: 'toda semana', semanal: true, comIA: true },
  conteudo: { nome: 'Conteúdo', oQue: 'Três ideias de post para a semana, para a agência produzir.', quando: 'toda semana', semanal: true, comIA: true },
};

const INSTRUCAO = `Você escreve mensagens curtas de WhatsApp em nome de uma marina. Quem envia é uma pessoa da equipe, depois de conferir o texto.

Você recebe um JSON com "agente", "marina" e "itens". Cada item tem "chave", "tipo", "dados" e "rascunho". Reescreva cada rascunho no tom da marina (veja a ficha), mantendo todos os fatos do rascunho e dos dados.

Regras:
- Use só fatos que estão no item ou na ficha. Não invente preço, promoção, prazo, serviço nem motivo.
- Texto puro de WhatsApp: sem asteriscos, sem títulos. De duas a quatro linhas. O resumo da semana e as ideias de post podem ser mais longos.
- Nada de pressão, culpa ou urgência falsa. Lembrete de vencimento é só lembrete: não fale em atraso, multa ou cobrança.
- Não cite outros clientes nem embarcações de outros clientes.
- Mantenha datas, valores e links exatamente como vieram.
- No resumo da semana, comente só o que os números mostram. Número zero não ganha explicação inventada.
- Nas ideias de post, não use dados de clientes e não prometa nada que a ficha não diga.

Devolva um texto para cada chave recebida.`;

const FORMATO = {
  type: 'object',
  properties: {
    textos: {
      type: 'array',
      items: {
        type: 'object',
        properties: { chave: { type: 'string' }, texto: { type: 'string' } },
        required: ['chave', 'texto'],
        additionalProperties: false,
      },
    },
  },
  required: ['textos'],
  additionalProperties: false,
};

const primeiroNome = (nome) => String(nome || '').trim().split(/\s+/)[0] || '';
const ddmm = (iso) => iso.split('-').reverse().slice(0, 2).join('/');

/** Segunda-feira da semana de uma data. */
export function segundaDe(data) {
  const dia = new Date(`${data}T00:00:00Z`).getUTCDay();
  return somarDias(data, dia === 0 ? -6 : 1 - dia);
}

function tempoFalado(seg) {
  if (seg === null || seg === undefined) return 'sem dados';
  if (seg < 90) return `${Math.round(seg)} segundos`;
  if (seg < 5400) return `${Math.round(seg / 60)} minutos`;
  return `${(seg / 3600).toFixed(1).replace('.', ',')} horas`;
}

export function criarEquipe({ store, agenda, ia, avisar = () => {}, urlBase = '' }) {
  const cfg = () => store.config;
  const rodando = new Set();

  const existe = (chave) => store.sugestoes.find((s) => s.chave === chave);

  // ---------- fatos de cada agente ----------

  function fatosOperacao() {
    const a = agora();
    const q = agenda.quadro(a.data);
    const L = [`Rampa de ${dataPorExtenso(a.data)} · ${cfg().nome}`];
    if (cfg().avisoDoDia?.texto) L.push(`Aviso do dia: ${cfg().avisoDoDia.texto}`);
    L.push('', `Descidas: ${q.descidas.length}`);
    for (const d of q.descidas) {
      L.push(`${horaFalada(d.hora)} · ${d.embarcacao || d.clienteNome}${d.detalhes ? ` · ${d.detalhes}` : ''}${d.status === 'aguardando equipe' ? ' · AGUARDANDO LIBERAÇÃO' : ''}`);
    }
    if (q.servicos.length) {
      L.push('', `Serviços pedidos: ${q.servicos.length}`);
      for (const s of q.servicos) L.push(`${s.embarcacao || s.clienteNome} · ${s.detalhes}`);
    }
    if (q.reservas.length) {
      L.push('', `Aluguel: ${q.reservas.length}`);
      for (const r of q.reservas) L.push(`${r.itemNome} · ${r.clienteNome} · ${r.status === 'pre-reserva' ? 'aguardando o sinal' : r.status}`);
    }
    const pend = agenda.pendentes().length;
    const abertos = store.chamados.filter((c) => c.status === 'aberto' && !c.rascunho).length;
    if (pend || abertos) L.push('', `Esperando a equipe: ${pend} pedido(s) e ${abertos} chamado(s). Veja o painel.`);
    return [
      {
        chave: `briefing:${a.data}`,
        tipo: 'briefing',
        titulo: `Resumo da rampa de ${ddmm(a.data)}`,
        para: { quem: 'equipe', nome: 'Equipe da rampa', telefone: cfg().contatos?.equipe || '' },
        modelo: L.join('\n'),
        atualiza: true,
      },
    ];
  }

  function proximoVencimento(dia, hoje) {
    const [ano, mes] = hoje.split('-').map(Number);
    const noMes = (a, m) => {
      const ultimo = new Date(Date.UTC(a, m, 0)).getUTCDate();
      return `${a}-${String(m).padStart(2, '0')}-${String(Math.min(dia, ultimo)).padStart(2, '0')}`;
    };
    const este = noMes(ano, mes);
    if (este >= hoje) return este;
    return mes === 12 ? noMes(ano + 1, 1) : noMes(ano, mes + 1);
  }

  function fatosRelacionamento() {
    const hoje = agora().data;
    const r = cfg().relacionamento;
    const marina = cfg().nome;
    const fatos = [];
    for (const cli of store.clientes) {
      if (cli.semLembretes) continue;
      const nome = primeiroNome(cli.nome);
      const barco = cli.embarcacao || 'sua embarcação';
      const para = { quem: 'cliente', nome: cli.nome, telefone: cli.telefone || '', clienteId: cli.id };

      if (Number.isInteger(cli.mensalidadeDia) && !cli.pendencia) {
        const venc = proximoVencimento(cli.mensalidadeDia, hoje);
        if (diasEntre(hoje, venc) <= r.diasAntesVencimento) {
          fatos.push({
            chave: `venc:${cli.id}:${venc}`,
            tipo: 'vencimento',
            titulo: `Vencimento em ${ddmm(venc)} · ${cli.nome}`,
            para,
            dados: { cliente: nome, embarcacao: barco, vencimento: ddmm(venc) },
            modelo: `Olá, ${nome}! Aqui é da ${marina}. Só um lembrete: a mensalidade da vaga da ${barco} vence dia ${ddmm(venc)}. Qualquer dúvida, estamos por aqui.`,
            exige: [ddmm(venc)],
          });
        }
      }
      for (const [campo, tipo, dias, frase] of [
        ['revisaoEm', 'revisao', r.diasAntesRevisao, (d) => `a revisão do motor da ${barco} está prevista para ${d}`],
        ['documentoVence', 'documento', r.diasAntesDocumento, (d) => `o documento da ${barco} vence em ${d}. Vale conferir antes da próxima saída`],
      ]) {
        const data = cli[campo];
        if (!dataValida(data)) continue;
        const falta = diasEntre(hoje, data);
        if (falta < 0 || falta > dias) continue;
        fatos.push({
          chave: `${tipo}:${cli.id}:${data}`,
          tipo,
          titulo: `${tipo === 'revisao' ? 'Revisão' : 'Documento'} em ${ddmm(data)} · ${cli.nome}`,
          para,
          dados: { cliente: nome, embarcacao: barco, data: ddmm(data) },
          modelo: `Olá, ${nome}! Aqui é da ${marina}. Só lembrando: ${frase(ddmm(data))}.`,
          exige: [ddmm(data)],
        });
      }

      const descidas = store.registros.filter((x) => x.tipo === 'descida' && x.clienteId === cli.id && x.status === 'confirmado' && !x.rascunho);
      const passadas = descidas.filter((x) => x.data <= hoje).map((x) => x.data).sort();
      const temFutura = descidas.some((x) => x.data > hoje);
      const ultima = passadas.at(-1);
      if (ultima && !temFutura && diasEntre(ultima, hoje) >= r.diasSumido) {
        const link = urlBase && cli.token ? `${urlBase}/c/${cli.token}` : '';
        fatos.push({
          chave: `sumido:${cli.id}:${hoje.slice(0, 7)}`,
          tipo: 'retomada',
          titulo: `Sem sair desde ${ddmm(ultima)} · ${cli.nome}`,
          para,
          dados: { cliente: nome, embarcacao: barco, ultimaSaida: ddmm(ultima), link },
          modelo: `Olá, ${nome}! Aqui é da ${marina}. Faz um tempo que a ${barco} não vai pra água. Quando quiser sair, é só pedir a descida${link ? ` pelo seu link: ${link}` : ' por aqui'}.`,
          exige: link ? [link] : [],
        });
      }
    }

    // Pós-passeio: um por cliente a cada 30 dias, para não virar rotina chata.
    for (const reg of store.registros) {
      if (reg.tipo !== 'descida' || reg.etapa !== 'guardada' || !reg.clienteId) continue;
      const dias = diasEntre(reg.data, hoje);
      if (dias < 1 || dias > 2) continue;
      const cli = store.clientes.find((c) => c.id === reg.clienteId);
      if (!cli || cli.semLembretes) continue;
      const recente = store.sugestoes.some((s) => s.tipo === 'pos-passeio' && s.para?.clienteId === cli.id && diasEntre(s.criadoEm.slice(0, 10), hoje) < 30);
      if (recente || fatos.some((f) => f.tipo === 'pos-passeio' && f.para.clienteId === cli.id)) continue;
      const link = cfg().linkAvaliacao || '';
      const nome = primeiroNome(cli.nome);
      fatos.push({
        chave: `pos:${reg.id}`,
        tipo: 'pos-passeio',
        titulo: `Pós-passeio de ${ddmm(reg.data)} · ${cli.nome}`,
        para: { quem: 'cliente', nome: cli.nome, telefone: cli.telefone || '', clienteId: cli.id },
        dados: { cliente: nome, dia: ddmm(reg.data), linkAvaliacao: link },
        modelo: `Olá, ${nome}! Aqui é da ${marina}. Como foi o passeio de ${ddmm(reg.data)}? Se puder, conte pra gente como foi o atendimento${link ? `: ${link}` : '.'}`,
        exige: link ? [link] : [],
      });
    }
    return fatos;
  }

  function fatosVendas() {
    const hoje = agora().data;
    const marina = cfg().nome;
    const frases = {
      'lead-aluguel': (r) => `Você perguntou sobre aluguel${r.data ? ` para ${ddmm(r.data)}` : ''}. Ainda tem interesse? Posso ver a disponibilidade pra você.`,
      'lead-vaga': () => 'Você perguntou sobre vaga para guardar embarcação. Quer marcar uma visita para conhecer a marina?',
      'lead-venda': () => 'Você se interessou por uma embarcação à venda aqui. Quer combinar um horário para ver de perto?',
    };
    return store.registros
      .filter((r) => frases[r.tipo] && r.status === 'interesse' && !r.rascunho)
      .filter((r) => {
        const dias = diasEntre(r.criadoEm.slice(0, 10), hoje);
        return dias >= 1 && dias <= 14;
      })
      .map((r) => {
        const nome = r.clienteNome && r.clienteNome !== 'Visitante' ? primeiroNome(r.clienteNome) : '';
        return {
          chave: `lead:${r.id}`,
          tipo: 'retorno',
          titulo: `Retorno · ${r.clienteNome} · ${r.tipo.replace('lead-', '')}`,
          para: { quem: 'interessado', nome: r.clienteNome, telefone: r.telefone || '', clienteId: r.clienteId || null, conversaId: r.conversaId || null },
          dados: { nome, interesse: r.tipo.replace('lead-', ''), data: r.data ? ddmm(r.data) : '', oQueDisse: r.detalhes },
          modelo: `Olá${nome ? `, ${nome}` : ''}! Aqui é da ${marina}. ${frases[r.tipo](r)}`,
          exige: [],
        };
      });
  }

  function fatosGerente() {
    const segunda = segundaDe(agora().data);
    const de = somarDias(segunda, -7);
    const ate = somarDias(segunda, -1);
    const n = relatorio(store, { de, ate });
    const abertos = store.chamados.filter((c) => c.status === 'aberto' && !c.rascunho).length;
    const semRetorno = store.registros.filter((r) => r.tipo.startsWith('lead-') && r.status === 'interesse' && !r.rascunho).length;
    const L = [
      `Resumo da semana (${ddmm(de)} a ${ddmm(ate)}) · ${cfg().nome}`,
      '',
      `Atendimento: ${n.conversas} conversas e ${n.mensagensCliente} mensagens de clientes.`,
      `Respostas: ${n.respostasAssistente} do assistente e ${n.respostasEquipe} da equipe. Resposta típica em ${tempoFalado(n.tempoResposta.medianaSeg)}.`,
      `Fora do horário: ${n.foraDoHorario.mensagens} mensagens, ${n.foraDoHorario.respondidasPeloAssistente} respondidas na hora pelo assistente.`,
      `Rampa: ${n.descidas.total} descidas agendadas, ${n.descidas.peloAssistente} pelo assistente. ${n.servicos} serviços pedidos.`,
      `Aluguel: ${n.reservas.confirmadas} reservas confirmadas e ${n.reservas.preReservas} à espera do sinal. ${n.leads.aluguel + n.leads.vaga + n.leads.venda} interessados registrados.`,
      `Chamados para a equipe: ${n.chamados.total}${n.chamados.emergencia ? `, sendo ${n.chamados.emergencia} de emergência` : ''}.`,
      `Agora: ${abertos} chamado(s) em aberto e ${semRetorno} interessado(s) sem retorno.`,
    ];
    if (n.ia.usd !== null && n.ia.chamadas) L.push(`Custo da IA na semana: US$ ${n.ia.usd.toFixed(2).replace('.', ',')} (estimativa).`);
    return [
      {
        chave: `semana:${de}`,
        tipo: 'resumo',
        titulo: `Resumo da semana de ${ddmm(de)} a ${ddmm(ate)}`,
        para: { quem: 'dono', nome: 'Dono da marina', telefone: cfg().contatos?.dono || '' },
        dados: { periodo: `${ddmm(de)} a ${ddmm(ate)}`, numeros: n, chamadosAbertosAgora: abertos, interessadosSemRetorno: semRetorno },
        modelo: L.join('\n'),
        exige: [],
      },
    ];
  }

  function fatosConteudo() {
    const segunda = segundaDe(agora().data);
    const n = relatorio(store, { de: somarDias(segunda, -7), ate: somarDias(segunda, -1) });
    const marina = cfg().nome;
    const itens = (cfg().itensAluguel || []).map((i) => i.nome);
    const modelo = [
      `Ideias de post da semana de ${ddmm(segunda)} · ${marina}`,
      '',
      '1. Reels: um dia na rampa',
      'Mostre, em 20 segundos, o caminho do pedido até o barco na água: a mensagem chegando, o trator, a descida. Sem narração, só legenda na tela.',
      `Legenda: Do pedido à água, sem fila e sem ligação. Assim é sair pelo ${marina}.`,
      '',
      '2. Carrossel: como pedir a descida pelo link',
      'Quatro telas: abrir o link, escrever o horário, receber a confirmação, chegar com o barco pronto.',
      'Legenda: Seu barco na água no horário que você pediu. Salve este post para a próxima saída.',
      '',
      '3. Story: enquete do fim de semana',
      'Enquete "Sábado ou domingo no rio?" e uma caixinha para perguntas sobre a marina.',
      itens.length ? `Feche lembrando o que dá para alugar: ${itens.join(', ')}.` : 'Feche convidando para conhecer a marina.',
    ].join('\n');
    return [
      {
        chave: `conteudo:${segunda}`,
        tipo: 'conteudo',
        titulo: `Ideias de post da semana de ${ddmm(segunda)}`,
        para: { quem: 'agencia', nome: 'Agência', telefone: '' },
        dados: { marina, cidade: cfg().cidade, aluguel: itens, descidasNaSemanaPassada: n.descidas.total, mes: agora().data.slice(5, 7) },
        modelo,
        exige: [],
      },
    ];
  }

  const COLETA = { operacao: fatosOperacao, relacionamento: fatosRelacionamento, vendas: fatosVendas, gerente: fatosGerente, conteudo: fatosConteudo };

  // ---------- redação com IA ----------

  async function redigir(id, fatos) {
    const { saida, usage, model } = await ia.redigir({
      sistema: `${INSTRUCAO}\n\n# Ficha da marina\n\n${(store.ficha || '').trim()}`,
      dados: { agente: AGENTES[id].nome, marina: cfg().nome, itens: fatos.map((f) => ({ chave: f.chave, tipo: f.tipo, dados: f.dados, rascunho: f.modelo })) },
      schema: FORMATO,
    });
    store.registrarUso({
      dia: agora().data,
      em: carimbo(),
      agente: id,
      modelo: model || ia.modelo,
      entrada: usage?.input_tokens ?? 0,
      saida: usage?.output_tokens ?? 0,
      cacheLeitura: usage?.cache_read_input_tokens ?? 0,
      cacheGravacao: usage?.cache_creation_input_tokens ?? 0,
      usd: custoEstimado(model || ia.modelo, usage),
    });
    const textos = new Map();
    for (const t of Array.isArray(saida?.textos) ? saida.textos : []) {
      const fato = fatos.find((f) => f.chave === t.chave);
      const texto = typeof t.texto === 'string' ? t.texto.replace(/\*\*(.+?)\*\*/g, '$1').trim() : '';
      // Só aceita o texto da IA se ele preservou o que não pode mudar
      // (data de vencimento, link). Senão vale o texto-modelo.
      if (fato && texto && texto.length <= 2500 && (fato.exige || []).every((trecho) => texto.includes(trecho))) textos.set(t.chave, texto);
    }
    return textos;
  }

  // ---------- execução ----------

  async function rodar(id, { por = 'agenda' } = {}) {
    if (!AGENTES[id]) return { ok: false, erro: 'Agente desconhecido.' };
    if (rodando.has(id)) return { ok: false, erro: 'Este agente já está trabalhando.' };
    rodando.add(id);
    try {
      const fatos = COLETA[id]().filter((f) => {
        const anterior = existe(f.chave);
        return !anterior || (f.atualiza && anterior.status === 'pendente' && anterior.texto !== f.modelo) || (f.atualiza && anterior.status !== 'pendente' && por !== 'agenda');
      });
      let textos = new Map();
      let erro = null;
      if (fatos.length && AGENTES[id].comIA && ia.redigir) {
        try {
          textos = await redigir(id, fatos);
        } catch (e) {
          erro = e.message;
          console.error(`[equipe] ${id}: a IA falhou, usando os textos-modelo. ${e.message}`);
        }
      }
      let criadas = 0;
      for (const f of fatos) {
        const anterior = existe(f.chave);
        const texto = textos.get(f.chave) || f.modelo;
        if (anterior && anterior.status === 'pendente') {
          anterior.texto = texto;
          anterior.criadoEm = carimbo();
        } else {
          store.sugestoes.push({
            id: novoId('sug'),
            agente: id,
            tipo: f.tipo,
            chave: anterior ? `${f.chave}:${novoId('r').slice(2)}` : f.chave,
            titulo: f.titulo,
            para: f.para,
            texto,
            viaIA: textos.has(f.chave),
            criadoEm: carimbo(),
            status: 'pendente',
          });
        }
        criadas++;
      }
      const a = agora();
      store.equipe[id] = { ultimaData: a.data, ultimaSemana: segundaDe(a.data), ultimaEm: `${dataPorExtenso(a.data)}, ${a.hora}`, criadas, erro, por };
      store.salvar('sugestoes');
      store.salvar('equipe');
      avisar();
      return { ok: true, criadas, viaIA: textos.size > 0, erro };
    } finally {
      rodando.delete(id);
    }
  }

  function deveRodar(id) {
    const c = cfg().agentes?.[id];
    if (!c?.ativo) return false;
    const a = agora();
    if (a.hora < c.hora) return false;
    const est = store.equipe[id];
    if (AGENTES[id].semanal) return est?.ultimaSemana !== segundaDe(a.data);
    return est?.ultimaData !== a.data;
  }

  /** Chamado de minuto em minuto: roda quem está na hora e ainda não rodou. */
  async function tique() {
    const feitos = [];
    for (const id of Object.keys(AGENTES)) {
      if (!deveRodar(id)) continue;
      try {
        const r = await rodar(id);
        if (r.ok) feitos.push(id);
      } catch (e) {
        console.error(`[equipe] ${id}:`, e);
      }
    }
    return feitos;
  }

  // ---------- sugestões ----------

  function pendentes() {
    return store.sugestoes.filter((s) => s.status === 'pendente').sort((a, b) => b.criadoEm.localeCompare(a.criadoEm));
  }

  function concluir(id, { acao, texto, por }) {
    const s = store.sugestoes.find((x) => x.id === id);
    if (!s) return { ok: false, erro: 'Sugestão não encontrada.' };
    if (s.status !== 'pendente') return { ok: false, erro: 'Esta sugestão já foi tratada.' };
    if (!['feita', 'descartada'].includes(acao)) return { ok: false, erro: 'Ação inválida.' };
    if (typeof texto === 'string' && texto.trim()) s.texto = texto.trim().slice(0, 3000);
    s.status = acao;
    s.feitaPor = por;
    s.feitaEm = carimbo();
    store.salvar('sugestoes');
    avisar();
    return { ok: true, sugestao: s };
  }

  function resumo() {
    return Object.entries(AGENTES).map(([id, a]) => ({
      id,
      nome: a.nome,
      oQue: a.oQue,
      quando: a.quando,
      ativo: !!cfg().agentes?.[id]?.ativo,
      hora: cfg().agentes?.[id]?.hora || '',
      ultimaEm: store.equipe[id]?.ultimaEm || null,
      criadas: store.equipe[id]?.criadas ?? null,
      erro: store.equipe[id]?.erro || null,
      pendentes: store.sugestoes.filter((s) => s.agente === id && s.status === 'pendente').length,
    }));
  }

  return { rodar, tique, deveRodar, pendentes, concluir, resumo };
}
