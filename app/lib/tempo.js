// Datas e horas sempre no relógio de parede da marina (fuso configurado).
// O Brasil não tem horário de verão, então a diferença entre dois horários
// de parede é a diferença real.

const DIAS = ['domingo', 'segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado'];
const DIAS_CURTOS = ['dom', 'seg', 'ter', 'qua', 'qui', 'sex', 'sáb'];

let relogioFixo = null; // usado só em teste: "2026-12-19T08:30"
let fuso = 'America/Sao_Paulo';

export function definirFuso(tz) {
  if (tz) fuso = tz;
}

export function fixarRelogio(iso) {
  relogioFixo = iso || null;
}

/** { data: 'YYYY-MM-DD', hora: 'HH:MM', minutos: n } no fuso da marina. */
export function agora() {
  if (relogioFixo) {
    const [data, hora] = relogioFixo.split('T');
    return { data, hora: hora.slice(0, 5), minutos: paraMinutos(hora.slice(0, 5)) };
  }
  const partes = new Intl.DateTimeFormat('en-CA', {
    timeZone: fuso,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hourCycle: 'h23',
  }).formatToParts(new Date());
  const p = Object.fromEntries(partes.map((x) => [x.type, x.value]));
  const data = `${p.year}-${p.month}-${p.day}`;
  const hora = `${p.hour}:${p.minute}`;
  return { data, hora, minutos: paraMinutos(hora) };
}

/** Carimbo ISO do instante real, para ordenar e medir tempo de resposta. */
export function carimbo() {
  if (relogioFixo) return new Date(`${relogioFixo}:00.000Z`).toISOString();
  return new Date().toISOString();
}

export function paraMinutos(hhmm) {
  const [h, m] = hhmm.split(':').map(Number);
  return h * 60 + m;
}

export function deMinutos(min) {
  const h = Math.floor(min / 60);
  const m = min % 60;
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}`;
}

const RE_DATA = /^\d{4}-\d{2}-\d{2}$/;
const RE_HORA = /^([01]\d|2[0-3]):[0-5]\d$/;

export function dataValida(s) {
  if (typeof s !== 'string' || !RE_DATA.test(s)) return false;
  const d = new Date(`${s}T00:00:00Z`);
  return !Number.isNaN(d.getTime()) && d.toISOString().slice(0, 10) === s;
}

export function horaValida(s) {
  return typeof s === 'string' && RE_HORA.test(s);
}

/** Aceita "9h", "9h30", "09:30", "9:30", "9" e devolve "09:30", ou null. */
export function normalizarHora(s) {
  if (typeof s !== 'string') return null;
  const m = s.trim().toLowerCase().match(/^(\d{1,2})(?:[:h](\d{2})?)?$/);
  if (!m) return null;
  const h = Number(m[1]);
  const min = m[2] ? Number(m[2]) : 0;
  if (h > 23 || min > 59) return null;
  return `${String(h).padStart(2, '0')}:${String(min).padStart(2, '0')}`;
}

export function somarDias(data, n) {
  const d = new Date(`${data}T00:00:00Z`);
  d.setUTCDate(d.getUTCDate() + n);
  return d.toISOString().slice(0, 10);
}

/** Dias inteiros entre duas datas (b - a). */
export function diasEntre(a, b) {
  return Math.round((new Date(`${b}T00:00:00Z`) - new Date(`${a}T00:00:00Z`)) / 86400000);
}

/** Minutos de relógio de parede entre dois pares data/hora (b - a). */
export function minutosEntre(dataA, horaA, dataB, horaB) {
  return diasEntre(dataA, dataB) * 1440 + paraMinutos(horaB) - paraMinutos(horaA);
}

export function diaDaSemana(data) {
  return DIAS[new Date(`${data}T00:00:00Z`).getUTCDay()];
}

export function fimDeSemana(data) {
  const d = new Date(`${data}T00:00:00Z`).getUTCDay();
  return d === 0 || d === 6;
}

/** "sábado, 19/12/2026" */
export function dataPorExtenso(data) {
  const [a, m, d] = data.split('-');
  return `${diaDaSemana(data)}, ${d}/${m}/${a}`;
}

/** "sáb 19/12" */
export function dataCurta(data) {
  const [, m, d] = data.split('-');
  const dia = DIAS_CURTOS[new Date(`${data}T00:00:00Z`).getUTCDay()];
  return `${dia} ${d}/${m}`;
}

/** "10h" ou "10h30" */
export function horaFalada(hhmm) {
  const [h, m] = hhmm.split(':');
  return m === '00' ? `${Number(h)}h` : `${Number(h)}h${m}`;
}
