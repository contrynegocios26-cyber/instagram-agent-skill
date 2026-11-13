// Regras da rampa e do aluguel. É este módulo, e não o modelo de IA, que
// decide se um horário existe, se a janela tem vaga e se há unidade livre.
// O atendente só pode dizer "confirmado" depois que registrar() devolve ok.

import { novoId } from './store.js';
import {
  agora,
  carimbo,
  dataValida,
  horaValida,
  paraMinutos,
  deMinutos,
  minutosEntre,
  dataPorExtenso,
  dataCurta,
  horaFalada,
} from './tempo.js';

export const TIPOS = [
  'descida',
  'subida',
  'alteracao',
  'cancelamento',
  'servico',
  'reserva',
  'lead-aluguel',
  'lead-vaga',
  'lead-venda',
  'reclamacao',
];

const ATIVOS = new Set(['confirmado', 'aguardando equipe', 'pre-reserva']);

export function criarAgenda(store) {
  const cfg = () => store.config;
  const rampa = () => cfg().rampa;

  function tocar(reg, por, oQue) {
    reg.atualizadoEm = carimbo();
    reg.historico = reg.historico || [];
    reg.historico.push({ em: reg.atualizadoEm, por, oQue });
    store.salvar('registros');
  }

  // ---------- rampa ----------

  function gradeDoDia() {
    const r = rampa();
    const ini = paraMinutos(r.abre);
    const fim = paraMinutos(r.ultimaDescida);
    const out = [];
    for (let m = ini; m <= fim; m += r.janelaMin) out.push(deMinutos(m));
    return out;
  }

  function ocupadas(data, hora, ignorarId) {
    return store.registros.filter(
      (x) =>
        x.tipo === 'descida' &&
        x.data === data &&
        x.hora === hora &&
        x.id !== ignorarId &&
        (x.status === 'confirmado' || x.status === 'aguardando equipe'),
    ).length;
  }

  function janelasDoDia(data) {
    const cap = rampa().capacidade;
    return gradeDoDia().map((hora) => {
      const o = ocupadas(data, hora);
      return { hora, ocupadas: o, capacidade: cap, livres: Math.max(0, cap - o) };
    });
  }

  function janelasLivresProximas(data, hora, ignorarId) {
    const a = agora();
    const cap = rampa().capacidade;
    const alvo = paraMinutos(hora);
    const livres = gradeDoDia().filter((h) => {
      if (ocupadas(data, h, ignorarId) >= cap) return false;
      return minutosEntre(a.data, a.hora, data, h) >= rampa().antecedenciaMin;
    });
    const antes = livres.filter((h) => paraMinutos(h) < alvo).pop();
    const depois = livres.find((h) => paraMinutos(h) > alvo);
    return [antes, depois].filter(Boolean);
  }

  /** Confere um horário de descida. Devolve null se pode, ou o motivo. */
  function motivoDescidaInvalida(data, hora, { ignorarId, forcar } = {}) {
    if (!dataValida(data)) return 'Data inválida. Use o formato AAAA-MM-DD.';
    if (!horaValida(hora)) return 'Hora inválida. Use o formato HH:MM.';
    const r = rampa();
    const a = agora();
    const grade = gradeDoDia();
    if (!grade.includes(hora)) {
      const m = paraMinutos(hora);
      if (m < paraMinutos(r.abre)) {
        return `A rampa abre às ${horaFalada(r.abre)}. A primeira janela de descida é ${horaFalada(r.abre)}.`;
      }
      if (m > paraMinutos(r.ultimaDescida)) {
        return `A última janela de descida é ${horaFalada(r.ultimaDescida)}.`;
      }
      const perto = grade.filter((h) => Math.abs(paraMinutos(h) - m) < r.janelaMin);
      return `As descidas são em janelas de ${r.janelaMin} minutos. Janelas mais próximas: ${perto.map(horaFalada).join(' e ')}.`;
    }
    const falta = minutosEntre(a.data, a.hora, data, hora);
    if (falta < 0) return 'Esse horário já passou.';
    if (forcar) return null;
    if (falta < r.antecedenciaMin) {
      const prox = janelasLivresProximas(data, hora, ignorarId);
      const dica = prox.length ? ` Próxima janela válida com vaga: ${horaFalada(prox[prox.length - 1])}.` : '';
      return `Antecedência mínima de ${r.antecedenciaMin} minutos não cumprida (faltam ${falta} min para a janela).${dica} Encaixe fora da regra só com a equipe.`;
    }
    if (ocupadas(data, hora, ignorarId) >= r.capacidade) {
      const prox = janelasLivresProximas(data, hora, ignorarId);
      const dica = prox.length
        ? ` Janelas livres mais próximas: ${prox.map(horaFalada).join(' e ')}.`
        : ' Não há outra janela livre nesse dia.';
      return `A janela das ${horaFalada(hora)} de ${dataPorExtenso(data)} está lotada (${r.capacidade}/${r.capacidade}).${dica}`;
    }
    return null;
  }

  // ---------- aluguel ----------

  function reservasDoItem(itemId, data, ignorarId) {
    return store.registros.filter(
      (x) =>
        x.tipo === 'reserva' &&
        x.item === itemId &&
        x.data === data &&
        x.id !== ignorarId &&
        (x.status === 'pre-reserva' || x.status === 'confirmado'),
    ).length;
  }

  function disponibilidadeAluguel(data) {
    return (cfg().itensAluguel || []).map((it) => {
      const usadas = reservasDoItem(it.id, data);
      return { id: it.id, nome: it.nome, unidades: it.unidades, livres: Math.max(0, it.unidades - usadas) };
    });
  }

  // ---------- resumos para o atendente ----------

  function resumoRampa(data) {
    const js = janelasDoDia(data);
    const comGente = js.filter((j) => j.ocupadas > 0);
    if (!comGente.length) return 'todas as janelas livres';
    const partes = comGente.map((j) => `${j.hora} ${j.ocupadas}/${j.capacidade}${j.livres === 0 ? ' LOTADA' : ''}`);
    return `${partes.join(' · ')} · demais janelas livres`;
  }

  function resumoAluguel(data) {
    const d = disponibilidadeAluguel(data);
    if (!d.length) return 'sem itens de aluguel cadastrados';
    return d
      .map((i) => (i.livres === 0 ? `${i.nome} [${i.id}]: sem unidade livre` : `${i.nome} [${i.id}]: ${i.livres} de ${i.unidades} livre(s)`))
      .join(' · ');
  }

  function consultar(data) {
    if (!dataValida(data)) return { ok: false, erro: 'Data inválida. Use AAAA-MM-DD.' };
    const r = rampa();
    return {
      ok: true,
      data,
      dia: dataPorExtenso(data),
      rampa: {
        descidas: `${r.abre} a ${r.ultimaDescida}, janelas de ${r.janelaMin} min, ${r.capacidade} por janela`,
        limite_subida: r.limiteSubida,
        ocupacao: resumoRampa(data),
      },
      aluguel: resumoAluguel(data),
    };
  }

  // ---------- consulta de registros ----------

  function doDono(reg, ctx) {
    if (ctx.cliente) return reg.clienteId === ctx.cliente.id;
    return !reg.clienteId && reg.conversaId === ctx.conversaId;
  }

  /** Registros futuros e em aberto de quem está na conversa. */
  function ativosDe(ctx) {
    const hoje = agora().data;
    return store.registros
      .filter((x) => doDono(x, ctx) && ATIVOS.has(x.status) && (!x.data || x.data >= hoje))
      .filter((x) => !x.rascunho || x.rascunho === ctx.turnoId)
      .filter((x) => x.etapa !== 'guardada')
      .filter((x) => ['descida', 'subida', 'servico', 'reserva'].includes(x.tipo))
      .sort((a, b) => `${a.data}${a.hora || ''}`.localeCompare(`${b.data}${b.hora || ''}`));
  }

  function descrever(reg) {
    const quando = reg.data ? `${dataCurta(reg.data)}${reg.hora ? ` ${horaFalada(reg.hora)}` : ''}` : 'sem data';
    const item = reg.tipo === 'reserva' ? ` ${nomeDoItem(reg.item)}` : '';
    const det = reg.detalhes ? ` (${reg.detalhes})` : '';
    return `${reg.tipo}${item} ${quando}${det}, ${reg.status}`;
  }

  function nomeDoItem(id) {
    return (cfg().itensAluguel || []).find((i) => i.id === id)?.nome || id;
  }

  // ---------- gravação ----------

  function base(ctx, entrada, extra) {
    const c = ctx.cliente;
    const ts = carimbo();
    const reg = {
      id: novoId('reg'),
      tipo: entrada.tipo,
      clienteId: c ? c.id : null,
      clienteNome: c ? c.nome : entrada.nome_cliente || 'Visitante',
      embarcacao: c ? c.embarcacao : entrada.embarcacao || '',
      data: entrada.data || null,
      hora: entrada.hora || null,
      item: null,
      detalhes: (entrada.detalhes || '').slice(0, 500),
      telefone: c ? c.telefone || '' : String(entrada.telefone || '').replace(/\D/g, '').slice(0, 15),
      status: 'confirmado',
      origem: ctx.origem || 'assistente',
      conversaId: ctx.conversaId || null,
      criadoEm: ts,
      atualizadoEm: ts,
      historico: [{ em: ts, por: ctx.por || ctx.origem || 'assistente', oQue: 'criado' }],
      ...extra,
    };
    if (ctx.turnoId) reg.rascunho = ctx.turnoId;
    store.registros.push(reg);
    store.salvar('registros');
    return reg;
  }

  /** Status que a identidade de quem pede permite. */
  function statusPorIdentidade(ctx, pedido) {
    const avisos = [];
    if (ctx.origem === 'equipe') return { status: pedido || 'confirmado', avisos };
    if (pedido === 'aguardando equipe') return { status: 'aguardando equipe', avisos };
    if (!ctx.cliente) {
      avisos.push(
        'Conversa pelo link público (sem cadastro): o pedido ficou como "aguardando equipe". Não confirme o horário; a equipe confirma com o titular. Chame encaminhar para a operação.',
      );
      return { status: 'aguardando equipe', avisos };
    }
    if (ctx.cliente.pendencia) {
      avisos.push(
        'Cadastro com pendência: o pedido ficou como "aguardando equipe". Siga a política da ficha, sem citar valor nem atraso, e chame encaminhar com urgência alta para quem está trabalhando agora.',
      );
      return { status: 'aguardando equipe', avisos };
    }
    return { status: 'confirmado', avisos };
  }

  function alvoDoDono(ctx, id) {
    const reg = store.registros.find((x) => x.id === id);
    if (!reg) return { erro: 'Registro não encontrado. Use um id listado em "Registros ativos" no contexto.' };
    if (ctx.origem !== 'equipe' && !doDono(reg, ctx)) return { erro: 'Esse registro não pertence a esta conversa.' };
    if (!ATIVOS.has(reg.status)) return { erro: `Esse registro está ${reg.status} e não pode mais ser alterado.` };
    return { reg };
  }

  /** Guarda os valores antigos para desfazer se o turno for descartado. */
  function guardarAntes(reg, ctx) {
    if (!ctx.turnoId || reg.rascunho === ctx.turnoId) return;
    if (reg.antes && reg.antes.turnoId === ctx.turnoId) return;
    reg.antes = {
      turnoId: ctx.turnoId,
      campos: { data: reg.data, hora: reg.hora, detalhes: reg.detalhes, status: reg.status, voltaPrevista: reg.voltaPrevista ?? null },
    };
  }

  function ok(reg, avisos = []) {
    return { ok: true, registro_id: reg.id, status: reg.status, resumo: descrever(reg), avisos };
  }

  function registrar(ctx, entrada) {
    const tipo = entrada.tipo;
    if (!TIPOS.includes(tipo)) return { ok: false, erro: `Tipo desconhecido: ${tipo}.` };
    const a = agora();

    if (tipo === 'descida') {
      const motivo = motivoDescidaInvalida(entrada.data, entrada.hora, { forcar: ctx.forcar });
      if (motivo) return { ok: false, erro: motivo };
      const jaTem = store.registros.find(
        (x) => x.tipo === 'descida' && doDono(x, ctx) && x.data === entrada.data && ATIVOS.has(x.status) && x.etapa !== 'guardada',
      );
      if (jaTem && ctx.origem !== 'equipe') {
        return {
          ok: false,
          erro: `Já existe uma descida desta embarcação em ${dataPorExtenso(jaTem.data)} às ${horaFalada(jaTem.hora)} (id ${jaTem.id}, ${jaTem.status}). Para mudar o horário use tipo "alteracao" com esse registro_id.`,
        };
      }
      const { status, avisos } = statusPorIdentidade(ctx, entrada.status);
      const reg = base(ctx, entrada, { status, etapa: 'agendada' });
      return ok(reg, avisos);
    }

    if (tipo === 'subida') {
      const data = entrada.data || a.data;
      if (!dataValida(data)) return { ok: false, erro: 'Data inválida. Use AAAA-MM-DD.' };
      if (!horaValida(entrada.hora)) return { ok: false, erro: 'Informe a hora prevista da volta no formato HH:MM.' };
      if (paraMinutos(entrada.hora) > paraMinutos(rampa().limiteSubida) && !ctx.forcar) {
        return {
          ok: false,
          erro: `A volta às ${horaFalada(entrada.hora)} passa do limite de subida (${horaFalada(rampa().limiteSubida)}). Avise o cliente e chame encaminhar para a operação.`,
        };
      }
      const { status, avisos } = statusPorIdentidade(ctx, entrada.status);
      const descida = store.registros.find(
        (x) => x.tipo === 'descida' && doDono(x, ctx) && x.data === data && ATIVOS.has(x.status) && x.etapa !== 'guardada',
      );
      const reg = base(ctx, { ...entrada, data }, { status, refId: descida ? descida.id : null });
      if (descida && status === 'confirmado') {
        guardarAntes(descida, ctx);
        descida.voltaPrevista = entrada.hora;
        tocar(descida, ctx.por || 'assistente', `volta prevista ${entrada.hora}`);
      }
      return ok(reg, avisos);
    }

    if (tipo === 'alteracao') {
      const { reg, erro } = alvoDoDono(ctx, entrada.registro_id);
      if (erro) return { ok: false, erro };
      const novaData = entrada.data || reg.data;
      const novaHora = entrada.hora || reg.hora;
      if (reg.tipo === 'descida' && (novaData !== reg.data || novaHora !== reg.hora)) {
        const motivo = motivoDescidaInvalida(novaData, novaHora, { ignorarId: reg.id, forcar: ctx.forcar });
        if (motivo) return { ok: false, erro: motivo };
      }
      if (reg.tipo === 'reserva' && novaData !== reg.data) {
        const item = (cfg().itensAluguel || []).find((i) => i.id === reg.item);
        if (item && reservasDoItem(reg.item, novaData, reg.id) >= item.unidades) {
          return { ok: false, erro: `Sem unidade livre de ${item.nome} em ${dataPorExtenso(novaData)}.` };
        }
      }
      guardarAntes(reg, ctx);
      reg.data = novaData;
      reg.hora = novaHora;
      if (entrada.detalhes) reg.detalhes = entrada.detalhes.slice(0, 500);
      tocar(reg, ctx.por || 'assistente', `alterado para ${novaData} ${novaHora || ''}`.trim());
      return ok(reg);
    }

    if (tipo === 'cancelamento') {
      const { reg, erro } = alvoDoDono(ctx, entrada.registro_id);
      if (erro) return { ok: false, erro };
      guardarAntes(reg, ctx);
      reg.status = 'cancelado';
      if (entrada.detalhes) reg.motivo = entrada.detalhes.slice(0, 300);
      tocar(reg, ctx.por || 'assistente', 'cancelado');
      return { ok: true, registro_id: reg.id, status: 'cancelado', resumo: `${reg.tipo} cancelado(a)`, avisos: [] };
    }

    if (tipo === 'servico') {
      if (!entrada.detalhes) return { ok: false, erro: 'Descreva o serviço em detalhes (ex.: "lavagem simples, R$ 80").' };
      const { status, avisos } = statusPorIdentidade(ctx, entrada.status);
      const reg = base(ctx, { ...entrada, data: entrada.data || a.data }, { status, refId: entrada.registro_id || null });
      return ok(reg, avisos);
    }

    if (tipo === 'reserva') {
      const item = (cfg().itensAluguel || []).find((i) => i.id === entrada.item_aluguel);
      if (!item) {
        const ids = (cfg().itensAluguel || []).map((i) => i.id).join(', ') || 'nenhum cadastrado';
        return { ok: false, erro: `Informe item_aluguel. Itens válidos: ${ids}.` };
      }
      if (!dataValida(entrada.data)) return { ok: false, erro: 'Informe a data da reserva no formato AAAA-MM-DD.' };
      if (entrada.data < a.data) return { ok: false, erro: 'Essa data já passou.' };
      if (reservasDoItem(item.id, entrada.data) >= item.unidades) {
        return { ok: false, erro: `Sem unidade livre de ${item.nome} em ${dataPorExtenso(entrada.data)}. Ofereça outra data ou outro item.` };
      }
      const minutos = cfg().preReservaMin || 120;
      const expira = new Date(new Date(carimbo()).getTime() + minutos * 60000).toISOString();
      const status = ctx.origem === 'equipe' ? entrada.status || 'confirmado' : 'pre-reserva';
      const reg = base(ctx, entrada, { status, item: item.id, expiraEm: status === 'pre-reserva' ? expira : null });
      const avisos =
        status === 'pre-reserva'
          ? [`Pré-reserva válida por ${minutos} minutos à espera do sinal. Quem confirma o pagamento é a equipe; não diga que está confirmada.`]
          : [];
      return ok(reg, avisos);
    }

    // leads e reclamação
    const status = tipo === 'reclamacao' ? 'aguardando equipe' : 'interesse';
    const reg = base(ctx, entrada, { status });
    return ok(reg);
  }

  // ---------- turno em rascunho ----------

  function confirmarTurno(turnoId) {
    let mudou = false;
    for (const r of store.registros) {
      if (r.rascunho === turnoId) {
        delete r.rascunho;
        mudou = true;
      }
      if (r.antes && r.antes.turnoId === turnoId) {
        delete r.antes;
        mudou = true;
      }
    }
    for (const c of store.chamados) {
      if (c.rascunho === turnoId) {
        delete c.rascunho;
        store.salvar('chamados');
      }
    }
    if (mudou) store.salvar('registros');
  }

  function descartarTurno(turnoId) {
    const antes = store.registros.length;
    store.registros = store.registros.filter((r) => r.rascunho !== turnoId);
    let mudou = store.registros.length !== antes;
    for (const r of store.registros) {
      if (r.antes && r.antes.turnoId === turnoId) {
        Object.assign(r, r.antes.campos);
        if (r.voltaPrevista === null) delete r.voltaPrevista;
        delete r.antes;
        mudou = true;
      }
    }
    if (mudou) store.salvar('registros');
    const antesC = store.chamados.length;
    store.chamados = store.chamados.filter((c) => c.rascunho !== turnoId);
    if (store.chamados.length !== antesC) store.salvar('chamados');
  }

  /** Na partida: nada pode sobrar em rascunho de um processo anterior. */
  function limparRascunhos() {
    const turnos = new Set();
    for (const r of store.registros) {
      if (r.rascunho) turnos.add(r.rascunho);
      if (r.antes) turnos.add(r.antes.turnoId);
    }
    for (const c of store.chamados) if (c.rascunho) turnos.add(c.rascunho);
    for (const t of turnos) descartarTurno(t);
    return turnos.size;
  }

  // ---------- ações da equipe ----------

  function porId(id) {
    return store.registros.find((x) => x.id === id) || null;
  }

  function liberar(id, por) {
    const reg = porId(id);
    if (!reg) return { ok: false, erro: 'Registro não encontrado.' };
    if (reg.status !== 'aguardando equipe') return { ok: false, erro: `Registro está ${reg.status}.` };
    reg.status = 'confirmado';
    tocar(reg, por, 'liberado pela equipe');
    return { ok: true, registro: reg };
  }

  function recusar(id, por, motivo) {
    const reg = porId(id);
    if (!reg) return { ok: false, erro: 'Registro não encontrado.' };
    if (!ATIVOS.has(reg.status)) return { ok: false, erro: `Registro está ${reg.status}.` };
    reg.status = reg.tipo === 'reserva' || reg.status === 'confirmado' ? 'cancelado' : 'recusado';
    if (motivo) reg.motivo = String(motivo).slice(0, 300);
    tocar(reg, por, `${reg.status} pela equipe`);
    return { ok: true, registro: reg };
  }

  function mudarEtapa(id, etapa, por) {
    const reg = porId(id);
    if (!reg || reg.tipo !== 'descida') return { ok: false, erro: 'Descida não encontrada.' };
    if (!['agendada', 'na_agua', 'guardada'].includes(etapa)) return { ok: false, erro: 'Etapa inválida.' };
    if (reg.status !== 'confirmado') return { ok: false, erro: `Descida está ${reg.status}.` };
    reg.etapa = etapa;
    tocar(reg, por, `etapa: ${etapa}`);
    return { ok: true, registro: reg };
  }

  function confirmarPagamento(id, por) {
    const reg = porId(id);
    if (!reg || reg.tipo !== 'reserva') return { ok: false, erro: 'Reserva não encontrada.' };
    if (reg.status !== 'pre-reserva') return { ok: false, erro: `Reserva está ${reg.status}.` };
    reg.status = 'confirmado';
    reg.expiraEm = null;
    tocar(reg, por, 'pagamento confirmado');
    return { ok: true, registro: reg };
  }

  function concluir(id, por) {
    const reg = porId(id);
    if (!reg) return { ok: false, erro: 'Registro não encontrado.' };
    reg.status = 'concluido';
    tocar(reg, por, 'concluído');
    return { ok: true, registro: reg };
  }

  /** Tudo o que a equipe precisa ver de um dia. */
  function quadro(data) {
    const doDia = store.registros.filter((x) => x.data === data && !x.rascunho && x.status !== 'cancelado' && x.status !== 'recusado');
    const porHora = (a, b) => (a.hora || '').localeCompare(b.hora || '');
    const agoraIso = carimbo();
    return {
      data,
      dia: dataPorExtenso(data),
      janelas: janelasDoDia(data),
      descidas: doDia.filter((x) => x.tipo === 'descida').sort(porHora),
      subidas: doDia.filter((x) => x.tipo === 'subida' && x.status !== 'concluido').sort(porHora),
      servicos: doDia.filter((x) => x.tipo === 'servico' && x.status !== 'concluido').sort(porHora),
      reservas: doDia
        .filter((x) => x.tipo === 'reserva')
        .map((x) => ({ ...x, itemNome: nomeDoItem(x.item), vencida: x.status === 'pre-reserva' && x.expiraEm && x.expiraEm < agoraIso })),
      aluguel: disponibilidadeAluguel(data),
    };
  }

  /** Pedidos que esperam decisão da equipe, em qualquer data futura. */
  function pendentes() {
    const hoje = agora().data;
    const agoraIso = carimbo();
    return store.registros
      .filter((x) => !x.rascunho && (!x.data || x.data >= hoje))
      .filter((x) => x.status === 'aguardando equipe' || (x.status === 'pre-reserva' && x.expiraEm && x.expiraEm < agoraIso))
      .map((x) => ({ ...x, itemNome: x.item ? nomeDoItem(x.item) : null, vencida: x.status === 'pre-reserva' }));
  }

  function leads() {
    return store.registros
      .filter((x) => !x.rascunho && (x.tipo.startsWith('lead-') || x.tipo === 'reclamacao') && x.status !== 'concluido')
      .sort((a, b) => b.criadoEm.localeCompare(a.criadoEm));
  }

  return {
    gradeDoDia,
    janelasDoDia,
    disponibilidadeAluguel,
    resumoRampa,
    resumoAluguel,
    consultar,
    registrar,
    ativosDe,
    descrever,
    nomeDoItem,
    confirmarTurno,
    descartarTurno,
    limparRascunhos,
    porId,
    liberar,
    recusar,
    mudarEtapa,
    confirmarPagamento,
    concluir,
    quadro,
    pendentes,
    leads,
  };
}
