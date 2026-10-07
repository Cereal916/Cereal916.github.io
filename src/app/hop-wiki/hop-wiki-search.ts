import { WikiSearchEntry } from './hop-wiki.models';

export interface WikiSearchResult {
  entry: WikiSearchEntry;
  snippet: string;
}

/** Lower case without accents, so "Español" matches "espanol". */
export function normalise(text: string): string {
  return (text || '')
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '');
}

const CATALOGUE_KINDS = new Set(['perk', 'supply', 'skill']);

function score(title: string, body: string, kind: string, words: string[]): number {
  let total = 0;
  for (const word of words) {
    const inTitle = title.indexOf(word);
    const inBody = body.indexOf(word);
    if (inTitle < 0 && inBody < 0) {
      return 0;
    }
    total += inTitle === 0 ? 40 : inTitle > 0 ? 25 : 0;
    total += inBody >= 0 ? 5 : 0;
  }
  return total + (CATALOGUE_KINDS.has(kind) ? 2 : 0);
}

function snippet(text: string, word: string): string {
  const start = Math.max(0, normalise(text).indexOf(word) - 40);
  const piece = text.slice(start, start + 140);
  return (start > 0 ? '…' : '') + piece + (start + 140 < text.length ? '…' : '');
}

/** Every word must appear; title matches rank above body matches. */
export function searchWiki(
  index: WikiSearchEntry[],
  query: string,
  limit = 12,
): WikiSearchResult[] {
  const words = normalise(query).split(/\s+/).filter(Boolean);
  if (!words.length) {
    return [];
  }
  return index
    .map((entry) => ({
      entry,
      value: score(normalise(entry.t), normalise(entry.x), entry.k, words),
    }))
    .filter((result) => result.value > 0)
    .sort((a, b) => b.value - a.value || a.entry.t.localeCompare(b.entry.t))
    .slice(0, limit)
    .map((result) => ({ entry: result.entry, snippet: snippet(result.entry.x, words[0]) }));
}
