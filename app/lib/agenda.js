// Regras da rampa e do aluguel. É este módulo, e não o modelo de IA, que
// decide se um horário existe, se a janela tem vaga e se há unidade livre.
// O atendente só pode dizer "confirmado" depois que registrar() devolve ok.
//
// Tudo o que um turno do atendente faz fica em rascunho até o turno ser
// confirmado (na hora, no modo automático; na aprovação, no modo sombra):
// - registro novo nasce com `rascunho: <turno>` e não aparece para ninguém;
// - mudança em registro que já vale fica em `pendente` e só é aplicada na
//   confirmação. Até lá o registro continua valendo como estava.
// Enquanto isso, o rascunho e a mudança pendente seguram a vaga que pedem,
// para que outra conversa não a leve.

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
  let aoInvalidar = () => {};

  function tocar(reg, por, oQue) {
    reg.atualizadoEm = carimbo();
    reg.historico = reg.historico || [];
    reg.historico.push({ em: reg.atualizadoEm, por, oQue });
    store.salvar('registros');
  }

  /** Como o registro fica para o turno que tem uma mudança pendente nele. */
  const efetivo = (reg, turnoId) => (turnoId && reg.pendente?.turnoId === turnoId ? { ...reg, ...reg.pendente.campos } : reg);

  /** Para contar vagas valem as duas formas: a que está valendo e a pendente. */
  const formas = (reg) => (reg.pendente ? [reg, { ...reg, ...reg.pendente.campos }] : [reg]);

  // ---------- rampa ----------

  function gradeDoDia() {
    const r = rampa();
    const ini = paraMinutos(r.abre);
    const fim = paraMinutos(r.ultimaDescida);
    const out = [];
    for (let m = ini; m <= fim; m += r.janelaMin) out.push(deMinutos(m));
    return out;
  }

  // Pedido do link público que ainda espera a equipe não segura vaga: é de
  // alguém cuja identidade ninguém confirmou, e quatro deles lotariam a janela.
  const ocupaRampa = (r) => r.status === 'confirmado' || (r.status === 'aguardando equipe' && !r.publico);

  function ocupadas(data, hora, ignorarId) {
    return store.registros.filter((x) => x.tipo === 'descida' && x.id !== ignorarId && formas(x).some((v) => v.data === data && v.hora === hora && ocupaRampa(v)))
      .length;
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

  function motivoSubidaInvalida(data, hora, forcar) {
    if (!dataValida(data)) return 'Data inválida. Use AAAA-MM-DD.';
    if (!horaValida(hora)) return 'Informe a hora prevista da volta no formato HH:MM.';
    if (data < agora().data) return 'Essa data já passou.';
    if (paraMinutos(hora) > paraMinutos(rampa().limiteSubida) && !forcar) {
      return `A volta às ${horaFalada(hora)} passa do limite de subida (${horaFalada(rampa().limiteSubida)}). Avise o cliente e chame encaminhar para a operação.`;
    }
    return null;
  }

  // ---------- aluguel ----------

  // Pré-reserva segura a unidade pelo prazo combinado. Vencida, só continua
  // segurando se o cliente mandou comprovante e a equipe ainda não conferiu.
  const seguraUnidade = (r) => r.status === 'confirmado' || (r.status === 'pre-reserva' && (r.comprovante || !r.expiraEm || r.expiraEm > carimbo()));

  function reservasDoItem(itemId, data, ignorarId) {
    return store.registros.filter((x) => x.tipo === 'reserva' && x.item === itemId && x.id !== ignorarId && formas(x).some((v) => v.data === data && seguraUnidade(v))).length;
  }

  function disponibilidadeAluguel(data) {
    return (cfg().itensAluguel || []).map((it) => {
      const usadas = reservasDoItem(it.id, data);
      return { id: it.id, nome: it.nome, unidades: it.unidades, livres: Math.max(0, it.unidades - usadas) };
    });
  }

  function semUnidade(itemId, data, ignorarId) {
    const item = (cfg().itensAluguel || []).find((i) => i.id === itemId);
    return !!item && reservasDoItem(itemId, data, ignorarId) >= item.unidades;
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

  /** Registros futuros e em aberto de quem está na conversa, como o turno os vê. */
  function ativosDe(ctx) {
    const hoje = agora().data;
    return store.registros
      .filter((x) => !x.rascunho || x.rascunho === ctx.turnoId)
      .map((x) => efetivo(x, ctx.turnoId))
      .filter((x) => doDono(x, ctx) && ATIVOS.has(x.status) && (!x.data || x.data >= hoje))
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
    const origem = ctx.origem || 'assistente';
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
      origem,
      // Pedido feito pelo link público: nome e embarcação são só o que a pessoa disse.
      publico: !c && origem === 'assistente',
      conversaId: ctx.conversaId || null,
      criadoEm: ts,
      criadoDia: agora().data,
      atualizadoEm: ts,
      historico: [{ em: ts, por: ctx.por || origem, oQue: 'criado' }],
      ...extra,
    };
    if (ctx.turnoId) reg.rascunho = ctx.turnoId;
    store.registros.push(reg);
    store.salvar('registros');
    return reg;
  }

  /** Muda um registro: na hora, se ele é do próprio turno ou se não há turno;
   *  como pendência, se ele já vale e o turno ainda pode ser descartado. */
  function mudar(reg, ctx, campos, oQue) {
    if (ctx.turnoId && reg.rascunho !== ctx.turnoId) {
      const anteriores = reg.pendente?.turnoId === ctx.turnoId ? reg.pendente.campos : {};
      reg.pendente = { turnoId: ctx.turnoId, campos: { ...anteriores, ...campos }, oQue, por: ctx.por || 'assistente' };
      store.salvar('registros');
      return;
    }
    Object.assign(reg, campos);
    tocar(reg, ctx.por || ctx.origem || 'assistente', oQue);
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
    const reg = store.registros.find((x) => x.id === id && (!x.rascunho || x.rascunho === ctx.turnoId));
    if (!reg) return { erro: 'Registro não encontrado. Use um id listado em "Registros em aberto" no contexto.' };
    if (ctx.origem !== 'equipe' && !doDono(reg, ctx)) return { erro: 'Esse registro não pertence a esta conversa.' };
    const visto = efetivo(reg, ctx.turnoId);
    if (!ATIVOS.has(visto.status)) return { erro: `Esse registro está ${visto.status} e não pode mais ser alterado.` };
    return { reg, visto };
  }

  function ok(reg, avisos = []) {
    return { ok: true, registro_id: reg.id, status: reg.status, resumo: descrever(reg), avisos };
  }

  function registrar(ctx, entrada) {
    const tipo = entrada.tipo;
    if (!TIPOS.includes(tipo)) return { ok: false, erro: `Tipo desconhecido: ${tipo}.` };
    const a = agora();
    const aberta = (v) => v.tipo === 'descida' && doDono(v, ctx) && ATIVOS.has(v.status) && v.etapa !== 'guardada';
    const visiveis = () => store.registros.filter((x) => !x.rascunho || x.rascunho === ctx.turnoId);

    if (tipo === 'descida') {
      const motivo = motivoDescidaInvalida(entrada.data, entrada.hora, { forcar: ctx.forcar });
      if (motivo) return { ok: false, erro: motivo };
      const jaTem = visiveis()
        .map((x) => efetivo(x, ctx.turnoId))
        .find((v) => aberta(v) && v.data === entrada.data);
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
      const motivo = motivoSubidaInvalida(data, entrada.hora, ctx.forcar);
      if (motivo) return { ok: false, erro: motivo };
      const { status, avisos } = statusPorIdentidade(ctx, entrada.status);
      const descida = visiveis().find((x) => {
        const v = efetivo(x, ctx.turnoId);
        return aberta(v) && v.data === data;
      });
      const reg = base(ctx, { ...entrada, data }, { status, refId: descida ? descida.id : null });
      if (descida && status === 'confirmado') mudar(descida, ctx, { voltaPrevista: entrada.hora }, `volta prevista ${entrada.hora}`);
      return ok(reg, avisos);
    }

    if (tipo === 'alteracao') {
      const { reg, visto, erro } = alvoDoDono(ctx, entrada.registro_id);
      if (erro) return { ok: false, erro };
      const novaData = entrada.data || visto.data;
      const novaHora = entrada.hora || visto.hora;
      const mudouQuando = novaData !== visto.data || novaHora !== visto.hora;
      let motivo = null;
      if (visto.tipo === 'descida') {
        if (mudouQuando) motivo = motivoDescidaInvalida(novaData, novaHora, { ignorarId: reg.id, forcar: ctx.forcar });
      } else if (visto.tipo === 'subida') {
        motivo = motivoSubidaInvalida(novaData, novaHora, ctx.forcar);
      } else if (novaData !== null && !dataValida(novaData)) {
        motivo = 'Data inválida. Use AAAA-MM-DD.';
      } else if (novaData && novaData < a.data) {
        motivo = 'Essa data já passou.';
      } else if (novaHora !== null && !horaValida(novaHora)) {
        motivo = 'Hora inválida. Use o formato HH:MM.';
      } else if (visto.tipo === 'reserva' && novaData !== visto.data && semUnidade(visto.item, novaData, reg.id)) {
        motivo = `Sem unidade livre de ${nomeDoItem(visto.item)} em ${dataPorExtenso(novaData)}.`;
      }
      if (motivo) return { ok: false, erro: motivo };
      const campos = { data: novaData, hora: novaHora };
      if (entrada.detalhes) campos.detalhes = entrada.detalhes.slice(0, 500);
      mudar(reg, ctx, campos, `alterado para ${novaData || ''} ${novaHora || ''}`.trim());
      return ok(efetivo(reg, ctx.turnoId));
    }

    if (tipo === 'cancelamento') {
      const { reg, visto, erro } = alvoDoDono(ctx, entrada.registro_id);
      if (erro) return { ok: false, erro };
      const campos = { status: 'cancelado' };
      if (entrada.detalhes) campos.motivo = entrada.detalhes.slice(0, 300);
      mudar(reg, ctx, campos, 'cancelado');
      return { ok: true, registro_id: reg.id, status: 'cancelado', resumo: `${visto.tipo} cancelado(a)`, avisos: [] };
    }

    if (tipo === 'servico') {
      if (!entrada.detalhes) return { ok: false, erro: 'Descreva o serviço em detalhes (ex.: "lavagem simples, R$ 80").' };
      const data = entrada.data || a.data;
      if (!dataValida(data)) return { ok: false, erro: 'Data inválida. Use AAAA-MM-DD.' };
      if (data < a.data) return { ok: false, erro: 'Essa data já passou.' };
      if (entrada.hora && !horaValida(entrada.hora)) return { ok: false, erro: 'Hora inválida. Use o formato HH:MM.' };
      const { status, avisos } = statusPorIdentidade(ctx, entrada.status);
      const reg = base(ctx, { ...entrada, data }, { status, refId: entrada.registro_id || null });
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
      if (entrada.hora && !horaValida(entrada.hora)) return { ok: false, erro: 'Hora inválida. Use o formato HH:MM.' };
      if (semUnidade(item.id, entrada.data)) {
        return { ok: false, erro: `Sem unidade livre de ${item.nome} em ${dataPorExtenso(entrada.data)}. Ofereça outra data ou outro item.` };
      }
      const minutos = cfg().preReservaMin || 120;
      const status = ctx.origem === 'equipe' ? entrada.status || 'confirmado' : 'pre-reserva';
      const reg = base(ctx, entrada, { status, item: item.id, expiraEm: status === 'pre-reserva' ? prazoDaPreReserva() : null });
      const avisos =
        status === 'pre-reserva'
          ? [`Pré-reserva válida por ${minutos} minutos à espera do sinal. Quem confirma o pagamento é a equipe; não diga que está confirmada.`]
          : [];
      return ok(reg, avisos);
    }

    // interessados e reclamação
    const status = tipo === 'reclamacao' ? 'aguardando equipe' : 'interesse';
    const reg = base(ctx, { ...entrada, data: dataValida(entrada.data) ? entrada.data : null, hora: horaValida(entrada.hora) ? entrada.hora : null }, { status });
    return ok(reg);
  }

  function prazoDaPreReserva() {
    return new Date(new Date(carimbo()).getTime() + (cfg().preReservaMin || 120) * 60000).toISOString();
  }

  // ---------- turno em rascunho ----------

  const doTurno = (r, turnoId) => r.rascunho === turnoId || r.pendente?.turnoId === turnoId;

  /** Antes de aprovar uma resposta que esperou: o que ela registrou ainda cabe? */
  function validarTurno(turnoId) {
    const a = agora();
    for (const r of store.registros) {
      if (!doTurno(r, turnoId)) continue;
      const v = efetivo(r, turnoId);
      if (!ATIVOS.has(v.status)) continue;
      if (v.tipo === 'descida' && v.status === 'confirmado' && minutosEntre(a.data, a.hora, v.data, v.hora) < 0) {
        return `A descida de ${dataPorExtenso(v.data)} às ${horaFalada(v.hora)} já passou do horário. Descarte esta resposta e fale com o cliente.`;
      }
      if (v.tipo === 'reserva') {
        if (v.data < a.data) return 'A data da reserva já passou. Descarte esta resposta e fale com o cliente.';
        // A pré-reserva em rascunho pode ter vencido e a unidade ter ido para outra pessoa.
        const semSegurar = !seguraUnidade(v);
        if (semSegurar && semUnidade(v.item, v.data, r.id)) return `${nomeDoItem(v.item)} foi reservado por outra pessoa enquanto esta resposta esperava. Descarte e fale com o cliente.`;
      }
    }
    return null;
  }

  function confirmarTurno(turnoId) {
    let mudou = false;
    for (const r of store.registros) {
      if (r.rascunho === turnoId) {
        delete r.rascunho;
        // O prazo da pré-reserva conta de quando o cliente recebe a resposta.
        if (r.tipo === 'reserva' && r.status === 'pre-reserva') r.expiraEm = prazoDaPreReserva();
        mudou = true;
      }
      if (r.pendente?.turnoId === turnoId) {
        const { campos, oQue, por } = r.pendente;
        delete r.pendente;
        Object.assign(r, campos);
        tocar(r, por, oQue);
        mudou = true;
      }
    }
    for (const c of store.chamados) {
      if (c.rascunho !== turnoId) continue;
      delete c.rascunho;
      // Chamado que atualiza outro, para a mesma pessoa, fecha o anterior.
      const velho = c.substitui ? store.chamados.find((x) => x.id === c.substitui) : null;
      if (velho && velho.status === 'aberto') {
        velho.status = 'resolvido';
        velho.resolvidoEm = carimbo();
        velho.resolvidoPor = 'atualizado por um chamado mais novo';
      }
      store.salvar('chamados');
    }
    if (mudou) store.salvar('registros');
  }

  function descartarTurno(turnoId) {
    const antes = store.registros.length;
    store.registros = store.registros.filter((r) => r.rascunho !== turnoId);
    let mudou = store.registros.length !== antes;
    for (const r of store.registros) {
      if (r.pendente?.turnoId === turnoId) {
        delete r.pendente;
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
      if (r.pendente) turnos.add(r.pendente.turnoId);
    }
    for (const c of store.chamados) if (c.rascunho) turnos.add(c.rascunho);
    for (const t of turnos) descartarTurno(t);
    return turnos.size;
  }

  // ---------- ações da equipe ----------

  function porId(id) {
    return store.registros.find((x) => x.id === id) || null;
  }

  /** A equipe mexeu num registro que um turno em rascunho queria mudar: o
   *  rascunho perde o sentido e é desfeito; quem cuida das respostas é avisado. */
  function soltar(reg) {
    if (!reg.pendente) return;
    const turnoId = reg.pendente.turnoId;
    descartarTurno(turnoId);
    aoInvalidar(turnoId);
  }

  function liberar(id, por, { forcar = false } = {}) {
    const reg = porId(id);
    if (!reg || reg.rascunho) return { ok: false, erro: 'Registro não encontrado.' };
    if (reg.status !== 'aguardando equipe') return { ok: false, erro: `Registro está ${reg.status}.` };
    soltar(reg);
    if (reg.tipo === 'descida' && !forcar && ocupadas(reg.data, reg.hora, reg.id) >= rampa().capacidade) {
      return { ok: false, lotada: true, erro: `A janela das ${horaFalada(reg.hora)} já está lotada. Libere como encaixe ou combine outro horário.` };
    }
    reg.status = 'confirmado';
    tocar(reg, por, forcar ? 'liberado pela equipe como encaixe' : 'liberado pela equipe');
    return { ok: true, registro: reg };
  }

  function recusar(id, por, motivo) {
    const reg = porId(id);
    if (!reg || reg.rascunho) return { ok: false, erro: 'Registro não encontrado.' };
    if (!ATIVOS.has(reg.status)) return { ok: false, erro: `Registro está ${reg.status}.` };
    soltar(reg);
    reg.status = reg.tipo === 'reserva' || reg.status === 'confirmado' ? 'cancelado' : 'recusado';
    if (motivo) reg.motivo = String(motivo).slice(0, 300);
    tocar(reg, por, `${reg.status} pela equipe`);
    return { ok: true, registro: reg };
  }

  function mudarEtapa(id, etapa, por) {
    const reg = porId(id);
    if (!reg || reg.rascunho || reg.tipo !== 'descida') return { ok: false, erro: 'Descida não encontrada.' };
    if (!['agendada', 'na_agua', 'guardada'].includes(etapa)) return { ok: false, erro: 'Etapa inválida.' };
    if (reg.status !== 'confirmado') return { ok: false, erro: `Descida está ${reg.status}.` };
    soltar(reg);
    reg.etapa = etapa;
    tocar(reg, por, `etapa: ${etapa}`);
    return { ok: true, registro: reg };
  }

  function confirmarPagamento(id, por) {
    const reg = porId(id);
    if (!reg || reg.rascunho || reg.tipo !== 'reserva') return { ok: false, erro: 'Reserva não encontrada.' };
    if (reg.status !== 'pre-reserva') return { ok: false, erro: `Reserva está ${reg.status}.` };
    soltar(reg);
    if (!seguraUnidade(reg) && semUnidade(reg.item, reg.data, reg.id)) {
      return { ok: false, erro: `Esta pré-reserva venceu e ${nomeDoItem(reg.item)} foi reservado por outra pessoa nesse dia. Combine outra data com o cliente.` };
    }
    reg.status = 'confirmado';
    reg.expiraEm = null;
    tocar(reg, por, 'pagamento confirmado');
    return { ok: true, registro: reg };
  }

  function concluir(id, por) {
    const reg = porId(id);
    if (!reg || reg.rascunho) return { ok: false, erro: 'Registro não encontrado.' };
    soltar(reg);
    reg.status = 'concluido';
    tocar(reg, por, 'concluído');
    return { ok: true, registro: reg };
  }

  /** O cliente mandou foto com pré-reserva aberta: pode ser o comprovante.
   *  A unidade fica segura até a equipe conferir, mesmo depois do prazo. */
  function marcarComprovante(conversaId) {
    let n = 0;
    for (const r of store.registros) {
      if (r.tipo === 'reserva' && r.status === 'pre-reserva' && !r.rascunho && r.conversaId === conversaId && !r.comprovante) {
        r.comprovante = true;
        tocar(r, 'sistema', 'foto recebida depois da pré-reserva');
        n++;
      }
    }
    return n;
  }

  const vencida = (x) => x.status === 'pre-reserva' && !!x.expiraEm && x.expiraEm < carimbo();

  /** Tudo o que a equipe precisa ver de um dia. */
  function quadro(data) {
    const doDia = store.registros.filter((x) => x.data === data && !x.rascunho && x.status !== 'cancelado' && x.status !== 'recusado');
    const porHora = (a, b) => (a.hora || '').localeCompare(b.hora || '');
    const descidas = doDia.filter((x) => x.tipo === 'descida').sort(porHora);
    const janelas = janelasDoDia(data);
    // Descida marcada num horário que saiu da grade (a configuração mudou)
    // continua aparecendo: o quadro mostra todo horário que tem barco.
    const horas = [...new Set(descidas.map((d) => d.hora))].sort().map((hora) => {
      const j = janelas.find((x) => x.hora === hora);
      return j || { hora, ocupadas: ocupadas(data, hora), capacidade: rampa().capacidade, livres: 0, foraDaGrade: true };
    });
    return {
      data,
      dia: dataPorExtenso(data),
      janelas,
      horas,
      descidas,
      subidas: doDia.filter((x) => x.tipo === 'subida' && x.status !== 'concluido').sort(porHora),
      servicos: doDia.filter((x) => x.tipo === 'servico' && x.status !== 'concluido').sort(porHora),
      reservas: doDia.filter((x) => x.tipo === 'reserva').map((x) => ({ ...x, itemNome: nomeDoItem(x.item), vencida: vencida(x) })),
      aluguel: disponibilidadeAluguel(data),
    };
  }

  /** Pedidos que esperam decisão da equipe, em qualquer data futura. */
  function pendentes() {
    const hoje = agora().data;
    return store.registros
      .filter((x) => !x.rascunho && (!x.data || x.data >= hoje))
      .filter((x) => x.status === 'aguardando equipe' || vencida(x))
      .map((x) => ({
        ...x,
        itemNome: x.item ? nomeDoItem(x.item) : null,
        vencida: vencida(x),
        janelaLotada: x.tipo === 'descida' && x.status === 'aguardando equipe' && ocupadas(x.data, x.hora, x.id) >= rampa().capacidade,
      }));
  }

  function leads() {
    return store.registros
      .filter((x) => !x.rascunho && (x.tipo.startsWith('lead-') || x.tipo === 'reclamacao') && x.status !== 'concluido')
      .sort((a, b) => b.criadoEm.localeCompare(a.criadoEm));
  }

  /** Descidas futuras cujo horário não existe na grade atual da rampa. */
  function foraDaGrade() {
    const hoje = agora().data;
    const grade = gradeDoDia();
    return store.registros.filter((x) => x.tipo === 'descida' && !x.rascunho && x.data >= hoje && ATIVOS.has(x.status) && !grade.includes(x.hora)).length;
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
    validarTurno,
    confirmarTurno,
    descartarTurno,
    limparRascunhos,
    porId,
    liberar,
    recusar,
    mudarEtapa,
    confirmarPagamento,
    concluir,
    marcarComprovante,
    quadro,
    pendentes,
    leads,
    foraDaGrade,
    definirAoInvalidar: (fn) => {
      aoInvalidar = fn;
    },
  };
}
