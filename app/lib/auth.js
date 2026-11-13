// Sessões assinadas (HMAC), sem banco: o painel usa cookie HttpOnly e o
// chat do cliente usa uma chave que o navegador guarda e manda no cabeçalho.

import crypto from 'node:crypto';

const b64 = (buf) => Buffer.from(buf).toString('base64url');

// Cada tipo de sessão (painel, chat, foto) é assinado com uma chave própria,
// derivada do segredo, e leva o seu uso dentro. Assim a chave que o chat
// entrega a qualquer visitante nunca vale como login do painel.
const chaveDe = (segredo, uso) => crypto.createHmac('sha256', segredo).update(`uso:${uso}`).digest();

export function assinar(dados, segredo, validadeSeg, uso) {
  if (!uso) throw new Error('assinar: informe o uso da chave');
  const corpo = b64(JSON.stringify({ ...dados, u: uso, exp: Math.floor(Date.now() / 1000) + validadeSeg }));
  const mac = crypto.createHmac('sha256', chaveDe(segredo, uso)).update(corpo).digest('base64url');
  return `${corpo}.${mac}`;
}

export function verificar(token, segredo, uso) {
  if (!uso) throw new Error('verificar: informe o uso da chave');
  if (typeof token !== 'string' || token.length > 2000) return null;
  const [corpo, mac] = token.split('.');
  if (!corpo || !mac) return null;
  const esperado = crypto.createHmac('sha256', chaveDe(segredo, uso)).update(corpo).digest('base64url');
  const a = Buffer.from(mac);
  const b = Buffer.from(esperado);
  if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) return null;
  try {
    const dados = JSON.parse(Buffer.from(corpo, 'base64url').toString('utf8'));
    if (dados.u !== uso) return null;
    if (typeof dados.exp !== 'number' || dados.exp < Date.now() / 1000) return null;
    return dados;
  } catch {
    return null;
  }
}

export function senhaConfere(informada, correta) {
  if (typeof informada !== 'string' || !correta) return false;
  const h = (s) => crypto.createHash('sha256').update(s).digest();
  return crypto.timingSafeEqual(h(informada), h(correta));
}

export function lerCookies(req) {
  const out = {};
  for (const par of (req.headers.cookie || '').split(';')) {
    const i = par.indexOf('=');
    if (i > 0) out[par.slice(0, i).trim()] = decodeURIComponent(par.slice(i + 1).trim());
  }
  return out;
}

/** Limite de frequência em memória: no máximo `max` eventos por janela. */
export function criarLimite() {
  const baldes = new Map();
  setInterval(() => {
    const agora = Date.now();
    for (const [k, v] of baldes) if (v.every((t) => agora - t > 3600_000)) baldes.delete(k);
  }, 600_000).unref();
  return function permitido(chave, max, janelaMs) {
    const agora = Date.now();
    const lista = (baldes.get(chave) || []).filter((t) => agora - t < janelaMs);
    if (lista.length >= max) {
      baldes.set(chave, lista);
      return false;
    }
    lista.push(agora);
    baldes.set(chave, lista);
    return true;
  };
}
