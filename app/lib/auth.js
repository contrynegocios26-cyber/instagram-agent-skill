// Sessões assinadas (HMAC), sem banco: o painel usa cookie HttpOnly e o
// chat do cliente usa uma chave que o navegador guarda e manda no cabeçalho.

import crypto from 'node:crypto';

const b64 = (buf) => Buffer.from(buf).toString('base64url');

export function assinar(dados, segredo, validadeSeg) {
  const corpo = b64(JSON.stringify({ ...dados, exp: Math.floor(Date.now() / 1000) + validadeSeg }));
  const mac = crypto.createHmac('sha256', segredo).update(corpo).digest('base64url');
  return `${corpo}.${mac}`;
}

export function verificar(token, segredo) {
  if (typeof token !== 'string' || token.length > 2000) return null;
  const [corpo, mac] = token.split('.');
  if (!corpo || !mac) return null;
  const esperado = crypto.createHmac('sha256', segredo).update(corpo).digest('base64url');
  const a = Buffer.from(mac);
  const b = Buffer.from(esperado);
  if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) return null;
  try {
    const dados = JSON.parse(Buffer.from(corpo, 'base64url').toString('utf8'));
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
