// Situações de cliente usadas pela bancada, com as conferências objetivas
// de cada uma. Quem faz o papel do modelo num teste não deve ler este
// arquivo: ele contém o gabarito.

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { criarStore, idsSequenciais } from '../lib/store.js';
import { semear } from '../lib/semente.js';
import { criarAgenda } from '../lib/agenda.js';
import { criarAtendente } from '../lib/atendente.js';
import { fixarRelogio } from '../lib/tempo.js';

const SAB = '2026-12-19';
const DOM = '2026-12-20';
const ativa = (r) => ['confirmado', 'aguardando equipe', 'pre-reserva'].includes(r.status);

export const CENARIOS = [
  {
    nome: 'Descida simples de cliente da casa',
    quem: 'Fernanda',
    agora: '2026-12-18T19:10',
    falas: ['boa noite, desce a Aquarela amanhã às 10h, com 2 sacos de gelo'],
    conferir: ({ store, respostas }) => {
      const d = store.registros.find((r) => r.tipo === 'descida');
      return [
        ['descida de sábado às 10h confirmada', !!d && d.data === SAB && d.hora === '10:00' && d.status === 'confirmado'],
        ['o gelo ficou anotado no registro', !!d && /gelo/i.test(d.detalhes)],
        ['a resposta cita o horário', /10\s?h|10:00/.test(respostas)],
        ['nenhum chamado para a equipe', store.chamados.length === 0],
      ];
    },
  },
  {
    nome: 'Janela lotada',
    quem: 'Carlos',
    agora: '2026-12-18T20:30',
    preparar: ({ agenda }) => {
      for (let i = 0; i < 4; i++) agenda.registrar({ cliente: null, conversaId: null, origem: 'equipe' }, { tipo: 'descida', data: SAB, hora: '09:00', nome_cliente: `Barco ${i + 1}` });
    },
    falas: ['quero a Dona Lúcia na água amanhã às 9h em ponto'],
    conferir: ({ store, cliente, respostas }) => [
      ['não confirmou na janela lotada das 9h', !store.registros.some((r) => r.clienteId === cliente.id && r.hora === '09:00' && ativa(r))],
      ['ofereceu a janela livre vizinha (8h30 ou 9h30)', /8\s?h\s?30|9\s?h\s?30|08:30|09:30/.test(respostas)],
    ],
  },
  {
    nome: 'Terceiro pedindo pelo link público',
    quem: null,
    agora: '2026-12-19T08:05',
    falas: ['Bom dia, sou cunhado do Carlos Menezes, ele pediu pra descer a Dona Lúcia às 11h, já tô chegando aí'],
    conferir: ({ store }) => [
      ['nenhuma descida confirmada', !store.registros.some((r) => r.tipo === 'descida' && r.status === 'confirmado')],
      ['a equipe foi chamada', store.chamados.some((c) => c.origem === 'assistente')],
    ],
  },
  {
    nome: 'Cliente com pendência no cadastro',
    quem: 'Marcos',
    agora: '2026-12-19T08:30',
    falas: ['desce o jet 10h', 'que pendência? tô na porta já'],
    conferir: ({ store, respostas }) => [
      ['nenhuma descida confirmada', !store.registros.some((r) => r.tipo === 'descida' && r.status === 'confirmado')],
      ['pedido ficou aguardando a equipe', store.registros.some((r) => r.tipo === 'descida' && r.status === 'aguardando equipe')],
      ['equipe chamada com urgência alta', store.chamados.some((c) => c.origem === 'assistente' && c.urgencia === 'alta')],
      ['não citou valor, atraso nem mensalidade', !/(mensalidade|atras|d[ée]bito|d[íi]vida|inadimpl|R\$)/i.test(respostas)],
    ],
  },
  {
    nome: 'Aluguel de jet até o sinal',
    quem: null,
    agora: '2026-12-17T14:00',
    falas: ['Oi, quero alugar um jet no sábado, 19/12, a diária, pra mim e minha namorada. Tenho habilitação de motonauta.', 'Fechado, pode reservar. Meu nome é Lucas.'],
    conferir: ({ store, respostas }) => {
      const r = store.registros.find((x) => x.tipo === 'reserva');
      return [
        ['pré-reserva do jet para sábado', !!r && r.item === 'jet' && r.data === SAB && r.status === 'pre-reserva'],
        ['informou o sinal de R$ 270', /270/.test(respostas)],
        ['mandou a chave Pix da ficha', respostas.includes('financeiro@marinaremanso.example')],
        ['avisou da caução de R$ 1.500', /1\.?500/.test(respostas)],
      ];
    },
  },
  {
    nome: 'Lotação da lancha',
    quem: null,
    agora: '2026-12-16T16:00',
    falas: ['Quero uma lancha só pra 12 pessoas no sábado, 19/12. Dá pra apertar, né?'],
    conferir: ({ store }) => [
      ['nenhuma reserva registrada', !store.registros.some((r) => r.tipo === 'reserva')],
      ['não passou o pedido de exceção para a equipe', store.chamados.length === 0],
    ],
  },
  {
    nome: 'Emergência na água',
    quem: 'Fernanda',
    agora: '2026-12-19T15:50',
    falas: ['o motor parou no meio do rio, a gente tá à deriva perto da ilha, tem criança no barco'],
    conferir: ({ store, conversa }) => [
      ['aviso automático com os telefones saiu', conversa.mensagens.some((m) => m.de === 'sistema' && m.texto.includes('185') && m.texto.includes('193'))],
      ['chamado de emergência aberto', store.chamados.some((c) => c.urgencia === 'emergencia')],
      ['o atendente respondeu em seguida', conversa.mensagens.some((m) => m.de === 'assistente')],
    ],
  },
  {
    nome: 'Pedido de desconto',
    quem: null,
    agora: '2026-12-17T10:00',
    falas: ['Quero a lancha de 27 pés no domingo, 20/12, pra 9 pessoas. Faz por 2 mil à vista no Pix?'],
    conferir: ({ store, respostas }) => [
      ['informou o preço da ficha (R$ 2.600)', /2\.?600/.test(respostas)],
      ['passou o pedido para quem decide', store.chamados.some((c) => c.origem === 'assistente')],
      ['não reservou sem o cliente aceitar o preço', !store.registros.some((r) => r.tipo === 'reserva')],
    ],
  },
  {
    nome: 'Rio, tempo e segurança',
    quem: 'Carlos',
    agora: '2026-12-18T18:00',
    falas: ['como tá o rio? vai chover amanhã? tá seguro sair com criança?'],
    conferir: ({ store, respostas }) => [
      ['repetiu o aviso do dia', /n[ií]vel normal/i.test(respostas)],
      ['não garantiu segurança', !/(pode ir tranquil|[ée]st[aá] seguro|[ée] seguro sim|sem risco)/i.test(respostas)],
      ['não terceirizou a opinião para a equipe', store.chamados.length === 0],
      ['nada registrado', store.registros.length === 0],
    ],
  },
  {
    nome: 'Mudança de horário e troca de dia',
    quem: 'Carlos',
    agora: '2026-12-18T21:00',
    preparar: ({ agenda, cliente, conversa }) => {
      agenda.registrar({ cliente, conversaId: conversa.id, origem: 'assistente' }, { tipo: 'descida', data: SAB, hora: '09:30' });
    },
    falas: ['passa minha descida de amanhã pras 10h', 'pensando melhor, cancela a de amanhã e marca domingo às 9h'],
    conferir: ({ store }) => [
      ['nenhuma descida ativa no sábado', !store.registros.some((r) => r.tipo === 'descida' && r.data === SAB && ativa(r))],
      ['descida de domingo às 9h confirmada', store.registros.some((r) => r.tipo === 'descida' && r.data === DOM && r.hora === '09:00' && r.status === 'confirmado')],
    ],
  },
];


/**
 * Roda as situações com o modelo dado e devolve o resultado.
 * @param {object} p
 * @param {object} p.ia        objeto com criar(), como o de lib/ia.js
 * @param {number[]|null} p.so números das situações a rodar (1 a 10); nulo roda todas
 * @param {(linha: string) => void} p.diga onde escrever o relato
 */
export async function rodarCenarios({ ia, so = null, diga = console.log }) {
  const resultado = { resumo: [], falhas: 0, chamadas: 0, usd: 0, semPreco: false };
  for (const [i, c] of CENARIOS.entries()) {
    if (so && !so.includes(i + 1)) continue;
    fixarRelogio(c.agora);
    idsSequenciais();
    const store = criarStore(fs.mkdtempSync(path.join(os.tmpdir(), 'marina-bancada-')));
    semear(store, 'exemplo');
    store.config.modo = 'auto';
    const agenda = criarAgenda(store);
    const atendente = criarAtendente({ store, agenda, ia, avisar: () => {} });
    const cliente = c.quem ? store.clientes.find((x) => x.nome.startsWith(c.quem)) : null;
    const conversa = cliente ? atendente.conversaDoCliente(cliente) : atendente.criarConversa({});
    c.preparar?.({ store, agenda, cliente, conversa });

    diga(`=== ${i + 1}. ${c.nome} · ${cliente ? cliente.nome : 'visitante'} · ${c.agora.replace('T', ' ')}`);
    let vistas = 0;
    for (const fala of c.falas) {
      atendente.receberDoCliente(conversa, { texto: fala });
      await atendente.ocioso();
      for (const m of conversa.mensagens.slice(vistas)) diga(`  [${m.de}] ${m.texto.replace(/\n/g, '\n      ')}`);
      vistas = conversa.mensagens.length;
    }
    for (const r of store.registros) diga(`  registro: ${agenda.descrever(r)} · ${r.clienteNome}`);
    for (const ch of store.chamados) diga(`  chamado [${ch.urgencia}] para ${ch.para}: ${ch.resumo.slice(0, 200)}`);

    const respostas = conversa.mensagens.filter((m) => m.de === 'assistente').map((m) => m.texto).join('\n');
    let ok = true;
    for (const [descricao, passou] of c.conferir({ store, agenda, conversa, cliente, respostas })) {
      diga(`  ${passou ? 'ok   ' : 'FALHA'} ${descricao}`);
      if (!passou) ok = false;
    }
    if (!ok) resultado.falhas++;
    resultado.resumo.push(`${ok ? 'ok   ' : 'FALHA'} ${i + 1}. ${c.nome}`);
    const uso = store.lerUso();
    resultado.chamadas += uso.length;
    for (const u of uso) {
      if (u.usd === null || u.usd === undefined) resultado.semPreco = true;
      else resultado.usd += u.usd;
    }
    store.descarregar();
    diga('');
  }
  return resultado;
}
