// Dados iniciais. "exemplo" cria a Marina Remanso (fictícia) para demonstração
// e testes. "vazio" cria uma marina em branco, pronta para a ficha real.

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { novoId, novoToken } from './store.js';

const aqui = path.dirname(fileURLToPath(import.meta.url));
const ler = (nome) => fs.readFileSync(path.join(aqui, '..', 'dados-exemplo', nome), 'utf8');

export function configPadrao() {
  return {
    nome: 'Minha Marina',
    cidade: '',
    fuso: 'America/Sao_Paulo',
    modo: 'sombra', // 'sombra' | 'auto' | 'desligado'
    rampa: {
      abre: '08:00',
      ultimaDescida: '17:00',
      limiteSubida: '18:30',
      janelaMin: 30,
      capacidade: 4,
      antecedenciaMin: 60,
    },
    atendimentoHumano: { semana: ['08:00', '18:00'], fimDeSemana: ['07:00', '19:00'] },
    itensAluguel: [],
    preReservaMin: 120,
    emergencia: { telefone: '' },
    avisoDoDia: { texto: '', atualizadoEm: null },
    agencia: '',
  };
}

export function semear(store, tipo) {
  if (store.config) return false;
  if (tipo === 'exemplo') {
    store.config = {
      ...configPadrao(),
      nome: 'Marina Remanso',
      cidade: 'Porto Rico, PR',
      itensAluguel: [
        { id: 'jet', nome: 'Jet Sea-Doo', unidades: 2 },
        { id: 'lancha22', nome: 'Lancha 22 pés com piloto', unidades: 1 },
        { id: 'lancha27', nome: 'Lancha 27 pés com piloto', unidades: 1 },
      ],
      emergencia: { telefone: '(44) 90000-0000' },
      avisoDoDia: { texto: 'Rampa operando normalmente. Rio em nível normal. Previsão do tempo: não informada.', atualizadoEm: null },
    };
    store.ficha = ler('ficha.md');
    store.clientes = [
      { nome: 'Carlos Menezes', telefone: '44999001122', embarcacao: 'Lancha "Dona Lúcia", 24 pés', autorizados: 'Carlos; Lúcia (esposa)', pendencia: false },
      { nome: 'Paulo Andrade', telefone: '44999003344', embarcacao: 'Lancha "Serena", 29 pés', autorizados: 'Paulo', pendencia: false },
      { nome: 'Marcos Tavares', telefone: '44999005566', embarcacao: 'Jet "MT-07"', autorizados: 'Marcos', pendencia: true },
      { nome: 'Fernanda Rocha', telefone: '44999007788', embarcacao: 'Lancha "Aquarela", 21 pés', autorizados: 'Fernanda; Bruno (marido)', pendencia: false },
    ].map((c) => ({ id: novoId('cli'), token: novoToken(), obs: '', ...c }));
  } else {
    store.config = configPadrao();
    store.ficha = ler('ficha-modelo.md');
    store.clientes = [];
  }
  store.salvar('config');
  store.salvar('ficha');
  store.salvar('clientes');
  return true;
}
