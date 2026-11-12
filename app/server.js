// Ponto de entrada. Variáveis de ambiente em .env.example.

import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { criarApp } from './lib/app.js';

const aqui = path.dirname(fileURLToPath(import.meta.url));
const dir = process.env.DADOS_DIR || path.join(aqui, 'data');
const porta = Number(process.env.PORT || 3000);

const { app, store, atendente } = criarApp({ dir, semente: process.env.SEMENTE || 'vazio' });

const retomadas = atendente.retomar();
const servidor = app.listen(porta, () => {
  console.log(`Atendimento da ${store.config.nome} no ar: http://localhost:${porta}  (painel em /painel)`);
  console.log(`Modo: ${store.config.modo}${process.env.IA_FAKE === '1' ? ' · IA em modo de demonstração (sem custo)' : ''}`);
  if (retomadas) console.log(`${retomadas} conversa(s) com mensagem sem resposta foram retomadas.`);
  if (process.env.IA_FAKE !== '1' && !process.env.ANTHROPIC_API_KEY && !process.env.ANTHROPIC_AUTH_TOKEN) {
    console.warn('ATENÇÃO: ANTHROPIC_API_KEY não definida. O atendente vai falhar e chamar a equipe em toda mensagem.');
  }
});

function encerrar() {
  store.descarregar();
  servidor.close(() => process.exit(0));
  setTimeout(() => process.exit(0), 3000).unref();
}
process.on('SIGTERM', encerrar);
process.on('SIGINT', encerrar);
