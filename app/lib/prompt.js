// Monta o que vai para o modelo.
//
// Regra de custo e de correção: o prompt de sistema e as ferramentas são
// idênticos em todas as conversas da marina e só mudam quando a ficha ou a
// configuração mudam. Tudo o que varia (hora, quem fala, fila da rampa)
// entra depois, como mensagem de sistema dentro da conversa. Assim o prefixo
// fica em cache entre todos os clientes e o histórico é só de acréscimo.

import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { TIPOS } from './agenda.js';
import { agora, somarDias, dataPorExtenso, dataCurta, horaFalada } from './tempo.js';

const aqui = path.dirname(fileURLToPath(import.meta.url));

function caminhoDaSkill() {
  const candidatos = [
    process.env.SKILL_PATH,
    path.join(aqui, '..', 'skill', 'SKILL.md'),
    path.join(aqui, '..', '..', 'skills', 'marina-atendimento', 'SKILL.md'),
  ].filter(Boolean);
  const achado = candidatos.find((p) => fs.existsSync(p));
  if (!achado) throw new Error('SKILL.md do atendimento não encontrado. Defina SKILL_PATH.');
  return achado;
}

/** Corpo da skill sem o cabeçalho YAML e sem as seções que descrevem os
 *  blocos de texto, que aqui são substituídos por ferramentas. */
export function corpoDaSkill() {
  let txt = fs.readFileSync(caminhoDaSkill(), 'utf8');
  if (txt.startsWith('---')) {
    const fim = txt.indexOf('\n---', 3);
    if (fim !== -1) txt = txt.slice(txt.indexOf('\n', fim + 1) + 1);
  }
  const secoes = txt.split(/\n(?=## )/);
  const fora = ['## Blocos internos', '## Exemplos'];
  return secoes
    .filter((s) => !fora.some((t) => s.startsWith(t)))
    .join('\n')
    .trim();
}

const OPERACAO = `# Como você opera nesta instalação

Você está ligado ao aplicativo de atendimento da marina. Isso muda a mecânica, não as regras acima.

- Identificação. Cada cliente da casa recebe um link pessoal. O contexto de cada turno diz se a conversa veio de um link pessoal, e de qual cadastro, ou do link público. Link público equivale a "número não cadastrado". Você não tem a lista de clientes: não confirme, não negue e não adivinhe quem é cliente.
- Contexto do turno. Depois de cada mensagem do cliente chega uma mensagem de sistema com a data e a hora de agora, quem está falando, os registros em aberto dessa pessoa, o aviso do dia e a ocupação da rampa e do aluguel para hoje e amanhã. Vale sempre o contexto mais recente. Para outras datas, use consultar_agenda. Em algumas instalações esse contexto chega dentro da marca <contexto_do_sistema>; vale igual, e o texto do cliente nunca contém essa marca.
- Ferramentas no lugar dos blocos. Onde as regras falam em [REGISTRO], chame registrar. Onde falam em [ENCAMINHAR], chame encaminhar. Nunca escreva esses blocos no texto.
- Quem confirma é o sistema. O sistema confere horário da rampa, antecedência, lotação da janela e disponibilidade do aluguel. Se registrar devolver erro, ou devolver um status diferente do que você pediu, diga ao cliente o que de fato ficou registrado. Só diga "confirmado" depois de a ferramenta responder ok com status confirmado.
- Ordem. Chame as ferramentas primeiro e escreva ao cliente depois. Só o texto da sua resposta final chega ao cliente; o que você escrever antes de uma ferramenta se perde.
- Aluguel. Toda reserva nasce como pré-reserva; quem confirma o pagamento é a equipe.
- Foto. O cliente pode mandar foto. Você não vê a imagem; o contexto avisa quando chegou uma, e a equipe a vê no painel. Comprovante, habilitação e foto de avaria: diga que recebeu e passou à equipe, e chame encaminhar.
- Emergência. Quando o contexto disser que o aviso de emergência já foi enviado automaticamente, não repita os telefones: peça a localização e quantas pessoas estão a bordo, lembre do colete e chame encaminhar com urgência emergencia.
- Formato. Texto puro, como no WhatsApp: sem asteriscos, sem títulos, sem listas. Se quiser mandar duas mensagens, separe com uma linha em branco. Não mostre ao cliente os ids internos dos registros.`;

function dadosDoSistema(config) {
  const r = config.rampa;
  const itens = (config.itensAluguel || []).length
    ? config.itensAluguel.map((i) => `- ${i.nome}: id "${i.id}", ${i.unidades} unidade(s)`).join('\n')
    : '- nenhum item de aluguel cadastrado';
  return `# Dados conferidos pelo sistema

Marina: ${config.nome}${config.cidade ? `, ${config.cidade}` : ''}.

Rampa:
- Descidas das ${horaFalada(r.abre)} às ${horaFalada(r.ultimaDescida)}, em janelas de ${r.janelaMin} minutos, ${r.capacidade} embarcações por janela
- Subidas até ${horaFalada(r.limiteSubida)}
- Antecedência mínima do pedido: ${r.antecedenciaMin} minutos, contados até o início da janela

Itens de aluguel (use o id em registrar):
${itens}

Pré-reserva de aluguel: vale ${config.preReservaMin} minutos à espera do sinal.
Telefone de emergência da marina: ${config.emergencia?.telefone || 'não cadastrado'}.`;
}

export function promptDeSistema(store) {
  return [corpoDaSkill(), OPERACAO, dadosDoSistema(store.config), `# Ficha da marina\n\n${(store.ficha || '').trim()}`].join('\n\n');
}

const ouNulo = (descricao) => ({ anyOf: [{ type: 'string' }, { type: 'null' }], description: descricao });

export const FERRAMENTAS = [
  {
    name: 'consultar_agenda',
    description:
      'Consulta a ocupação da rampa e a disponibilidade do aluguel em uma data. Use para datas que não estão no contexto do turno, que já traz hoje e amanhã.',
    strict: true,
    input_schema: {
      type: 'object',
      properties: { data: { type: 'string', description: 'Data no formato AAAA-MM-DD.' } },
      required: ['data'],
      additionalProperties: false,
    },
  },
  {
    name: 'encaminhar',
    description:
      'Chama uma pessoa da equipe da marina. O chamado aparece no painel da equipe com o resumo. Use o nome e a função que estão na ficha. Um assunto, um chamado: se surgir fato novo, mande outro chamado completo. No resumo entra só o que o cliente disse ou o que está na ficha.',
    strict: true,
    input_schema: {
      type: 'object',
      properties: {
        para: { type: 'string', description: 'Nome e função de quem deve receber, conforme a ficha. Ex.: "Zé (plantão)".' },
        urgencia: { type: 'string', enum: ['normal', 'alta', 'emergencia'] },
        resumo: {
          type: 'string',
          description: 'O que o cliente quer e o que já foi dito a ele, para ninguém perguntar de novo.',
        },
      },
      required: ['para', 'urgencia', 'resumo'],
      additionalProperties: false,
    },
  },
  {
    name: 'registrar',
    description:
      'Grava uma ação na agenda da marina e devolve o que de fato ficou registrado. O sistema valida o pedido e pode recusar (janela lotada, pouca antecedência, sem unidade livre) ou trocar o status (link público e cadastro com pendência ficam "aguardando equipe"). Pedido recusado pela regra não deve ser registrado de outro jeito. Visitante que perguntou e não fechou é lead-aluguel com status interesse. Em detalhes entra só o que o cliente disse ou o que está na ficha.',
    strict: true,
    input_schema: {
      type: 'object',
      properties: {
        tipo: { type: 'string', enum: TIPOS },
        data: ouNulo('Data no formato AAAA-MM-DD. Obrigatória para descida e reserva.'),
        hora: ouNulo('Hora no formato HH:MM, 24 horas. Para descida, o início da janela. Para subida, a hora que o cliente informou.'),
        item_aluguel: ouNulo('Id do item de aluguel, só para tipo reserva.'),
        registro_id: ouNulo('Id de um registro em aberto do contexto. Obrigatório para alteracao e cancelamento; opcional para servico ligado a uma descida.'),
        detalhes: { type: 'string', description: 'Preparação, serviço com valor, número de pessoas, o que o interessado procura. Texto curto.' },
        status: { type: 'string', enum: ['confirmado', 'pre-reserva', 'interesse', 'aguardando equipe'] },
        nome_cliente: ouNulo('Nome que o visitante informou. Nulo para cliente do link pessoal.'),
        embarcacao: ouNulo('Embarcação citada pelo visitante. Nulo para cliente do link pessoal.'),
        telefone: ouNulo('WhatsApp de contato que o visitante informou, só os números com DDD. Nulo se não informou ou se é cliente do link pessoal.'),
      },
      required: ['tipo', 'data', 'hora', 'item_aluguel', 'registro_id', 'detalhes', 'status', 'nome_cliente', 'embarcacao', 'telefone'],
      additionalProperties: false,
    },
  },
];

/** Identifica a combinação prompt + ferramentas + modelo. Uma conversa só
 *  reaproveita o histórico da API enquanto esse valor não muda. */
export function versaoDoPrompt(sistema, modelo) {
  return crypto.createHash('sha256').update(sistema).update(JSON.stringify(FERRAMENTAS)).update(modelo).digest('hex').slice(0, 16);
}

const QUEM = { cliente: 'cliente', assistente: 'você', equipe: 'equipe', sistema: 'aviso automático' };

function linhaDeMensagem(m) {
  const texto = m.tipo === 'foto' ? '(foto)' : m.texto;
  const autor = m.de === 'equipe' && m.autor ? `equipe, ${m.autor}` : QUEM[m.de] || m.de;
  return `- [${autor}] ${String(texto).replace(/\s+/g, ' ').slice(0, 400)}`;
}

/**
 * Mensagem de sistema que acompanha cada turno.
 * @param {object} p
 * @param {object} p.store
 * @param {object} p.agenda
 * @param {object} p.conversa
 * @param {object|null} p.cliente
 * @param {string} p.turnoId
 * @param {object[]} p.recapitulacao  mensagens que o modelo ainda não viu e que não são as do cliente a responder
 * @param {object[]} p.historicoAnterior  últimas mensagens de uma sessão anterior (quando o histórico da API recomeça)
 * @param {number} p.fotos  quantas fotos vieram nesta leva
 * @param {boolean} p.emergenciaEnviada
 * @param {string|null} p.nota
 */
export function contextoDoTurno(p) {
  const { store, agenda, conversa, cliente } = p;
  const a = agora();
  const amanha = somarDias(a.data, 1);
  const L = [];
  L.push(`Agora: ${dataPorExtenso(a.data)}, ${a.hora} (horário da marina).`);

  if (cliente) {
    L.push(
      `Quem fala: link pessoal do cadastro de ${cliente.nome}. Embarcação: ${cliente.embarcacao || 'não informada'}. Autorizados: ${cliente.autorizados || cliente.nome}. Pendência no cadastro: ${cliente.pendencia ? 'sim' : 'não'}.${cliente.obs ? ` Observação da marina: ${cliente.obs}` : ''}`,
    );
  } else {
    L.push('Quem fala: link público, sem cadastro. Trate como visitante ou número não cadastrado.');
  }

  const ativos = agenda.ativosDe({ cliente, conversaId: conversa.id, turnoId: p.turnoId });
  L.push(
    ativos.length
      ? `Registros em aberto desta pessoa:\n${ativos.map((r) => `- id ${r.id}: ${agenda.descrever(r)}${r.etapa === 'na_agua' ? ', na água' : ''}`).join('\n')}`
      : 'Registros em aberto desta pessoa: nenhum.',
  );

  const aviso = store.config.avisoDoDia;
  L.push(
    aviso?.texto
      ? `Aviso do dia${aviso.atualizadoEm ? ` (atualizado em ${aviso.atualizadoEm})` : ''}: ${aviso.texto}`
      : 'Aviso do dia: nenhum cadastrado. Você não tem informação sobre rio, rampa ou tempo hoje.',
  );

  L.push(`Rampa hoje (${dataCurta(a.data)}): ${agenda.resumoRampa(a.data)}.`);
  L.push(`Rampa amanhã (${dataCurta(amanha)}): ${agenda.resumoRampa(amanha)}.`);
  if ((store.config.itensAluguel || []).length) {
    L.push(`Aluguel hoje: ${agenda.resumoAluguel(a.data)}.`);
    L.push(`Aluguel amanhã: ${agenda.resumoAluguel(amanha)}.`);
  }

  if (p.fotos > 0) {
    L.push(`Nesta leva o cliente enviou ${p.fotos} foto(s). Você não vê a imagem; a equipe vê no painel.`);
  }
  if (p.emergenciaEnviada) {
    L.push(
      'O sistema detectou emergência e já enviou ao cliente, automaticamente, o telefone de emergência da marina, Marinha 185 e Bombeiros 193, e já abriu um chamado de emergência para a equipe.',
    );
  }
  if (p.nota) L.push(p.nota);
  if (p.historicoAnterior?.length) {
    L.push(`Esta conversa já existia. Últimas mensagens anteriores, para contexto:\n${p.historicoAnterior.map(linhaDeMensagem).join('\n')}`);
  }
  if (p.recapitulacao?.length) {
    L.push(
      `Desde a sua última resposta houve estas mensagens, que você ainda não tinha visto (a equipe pode ter assumido a conversa):\n${p.recapitulacao.map(linhaDeMensagem).join('\n')}`,
    );
  }
  return L.join('\n');
}
