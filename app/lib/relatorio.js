// Números do piloto: o que o dono da marina precisa ver para decidir se
// continua, e o que a agência precisa para saber quanto custa atender.

import { fimDeSemana, paraMinutos } from './tempo.js';

function foraDoHorario(config, m) {
  const faixa = fimDeSemana(m.dataLocal) ? config.atendimentoHumano?.fimDeSemana : config.atendimentoHumano?.semana;
  if (!faixa || !m.horaLocal) return false;
  const t = paraMinutos(m.horaLocal);
  return t < paraMinutos(faixa[0]) || t >= paraMinutos(faixa[1]);
}

function percentil(ordenado, p) {
  if (!ordenado.length) return null;
  return ordenado[Math.min(ordenado.length - 1, Math.floor(p * ordenado.length))];
}

export function relatorio(store, { de, ate }) {
  const dentro = (data) => (!de || data >= de) && (!ate || data <= ate);
  const r = {
    periodo: { de: de || null, ate: ate || null },
    conversas: 0,
    mensagensCliente: 0,
    respostasAssistente: 0,
    respostasEquipe: 0,
    foraDoHorario: { mensagens: 0, respondidasPeloAssistente: 0 },
    tempoResposta: { amostras: 0, medianaSeg: null, p90Seg: null },
    tempoRespostaAssistente: { amostras: 0, medianaSeg: null, p90Seg: null },
    aprovacoes: { aprovadas: 0, editadas: 0 },
    conversasComEquipe: 0,
  };

  const tempos = [];
  const temposIA = [];
  for (const c of store.conversas.values()) {
    const msgs = c.mensagens.filter((m) => dentro(m.dataLocal));
    if (!msgs.length) continue;
    r.conversas++;
    if (msgs.some((m) => m.de === 'equipe')) r.conversasComEquipe++;
    let esperando = null; // primeira mensagem do cliente ainda sem resposta
    let aprovacaoAberta = false;
    for (const m of msgs) {
      if (m.de === 'cliente') {
        r.mensagensCliente++;
        if (foraDoHorario(store.config, m)) r.foraDoHorario.mensagens++;
        if (!esperando) esperando = m;
        aprovacaoAberta = false;
      } else if (m.de === 'assistente' || m.de === 'equipe') {
        if (m.de === 'assistente') r.respostasAssistente++;
        else r.respostasEquipe++;
        if (m.aprovadoPor && !aprovacaoAberta) {
          r.aprovacoes.aprovadas++;
          if (m.editado) r.aprovacoes.editadas++;
          aprovacaoAberta = true;
        }
        if (esperando) {
          const seg = (new Date(m.em) - new Date(esperando.em)) / 1000;
          tempos.push(seg);
          if (m.de === 'assistente') {
            temposIA.push(seg);
            if (foraDoHorario(store.config, esperando)) r.foraDoHorario.respondidasPeloAssistente++;
          }
          esperando = null;
        }
      }
    }
  }
  for (const [lista, alvo] of [
    [tempos, r.tempoResposta],
    [temposIA, r.tempoRespostaAssistente],
  ]) {
    lista.sort((a, b) => a - b);
    alvo.amostras = lista.length;
    alvo.medianaSeg = percentil(lista, 0.5);
    alvo.p90Seg = percentil(lista, 0.9);
  }

  const regs = store.registros.filter((x) => !x.rascunho && dentro((x.criadoEm || '').slice(0, 10)));
  const conta = (f) => regs.filter(f).length;
  const valida = (x) => x.status !== 'cancelado' && x.status !== 'recusado';
  r.descidas = {
    total: conta((x) => x.tipo === 'descida' && valida(x)),
    peloAssistente: conta((x) => x.tipo === 'descida' && valida(x) && x.origem === 'assistente'),
    pelaEquipe: conta((x) => x.tipo === 'descida' && valida(x) && x.origem === 'equipe'),
  };
  r.subidas = conta((x) => x.tipo === 'subida' && valida(x));
  r.servicos = conta((x) => x.tipo === 'servico' && valida(x));
  r.reservas = {
    preReservas: conta((x) => x.tipo === 'reserva' && x.status === 'pre-reserva'),
    confirmadas: conta((x) => x.tipo === 'reserva' && x.status === 'confirmado'),
  };
  r.leads = {
    aluguel: conta((x) => x.tipo === 'lead-aluguel'),
    vaga: conta((x) => x.tipo === 'lead-vaga'),
    venda: conta((x) => x.tipo === 'lead-venda'),
  };
  r.reclamacoes = conta((x) => x.tipo === 'reclamacao');

  const chs = store.chamados.filter((x) => !x.rascunho && dentro((x.criadoEm || '').slice(0, 10)));
  r.chamados = {
    total: chs.length,
    emergencia: chs.filter((x) => x.urgencia === 'emergencia').length,
    alta: chs.filter((x) => x.urgencia === 'alta').length,
    normal: chs.filter((x) => x.urgencia === 'normal').length,
    abertos: chs.filter((x) => x.status === 'aberto').length,
  };

  const uso = store.lerUso().filter((u) => dentro(u.dia));
  const soma = (k) => uso.reduce((t, u) => t + (u[k] || 0), 0);
  const entradaTotal = soma('entrada') + soma('cacheLeitura') + soma('cacheGravacao');
  const semPreco = uso.some((u) => u.usd === null || u.usd === undefined);
  const usd = semPreco ? null : uso.reduce((t, u) => t + u.usd, 0);
  r.ia = {
    chamadas: uso.length,
    tokensEntrada: soma('entrada'),
    tokensCacheLeitura: soma('cacheLeitura'),
    tokensCacheGravacao: soma('cacheGravacao'),
    tokensSaida: soma('saida'),
    parteLidaDoCache: entradaTotal ? soma('cacheLeitura') / entradaTotal : null,
    usd,
    usdPorResposta: usd !== null && r.respostasAssistente ? usd / r.respostasAssistente : null,
    modelos: [...new Set(uso.map((u) => u.modelo))],
  };
  return r;
}
