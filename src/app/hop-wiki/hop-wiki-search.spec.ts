import { normalise, searchWiki } from './hop-wiki-search';
import { WikiSearchEntry } from './hop-wiki.models';

const index: WikiSearchEntry[] = [
  {
    t: 'Domino rules',
    u: '/hop/wiki/rules',
    s: 'Playing',
    k: 'page',
    x: 'Open ends, the boneyard and the hammer.',
  },
  {
    t: 'Boneyard Lantern',
    u: '/hop/wiki/supplies#boneyard_lantern',
    s: 'Supply',
    k: 'supply',
    x: 'Reveals one bone.',
  },
  {
    t: 'Perk Tax',
    u: '/hop/wiki/perks/tax',
    s: 'Malus',
    k: 'perk',
    x: 'Each perk bonus loses 1 point.',
  },
];

describe('searchWiki', () => {
  it('ranks title matches above body matches', () => {
    const results = searchWiki(index, 'boneyard');
    expect(results.map((result) => result.entry.t)).toEqual(['Boneyard Lantern', 'Domino rules']);
  });

  it('requires every word and ignores accents and case', () => {
    expect(searchWiki(index, 'PERK bönus').map((result) => result.entry.u)).toEqual([
      '/hop/wiki/perks/tax',
    ]);
    expect(searchWiki(index, 'perk lantern')).toEqual([]);
    expect(normalise('Español')).toBe('espanol');
  });

  it('returns nothing for an empty query and quotes a snippet', () => {
    expect(searchWiki(index, '   ')).toEqual([]);
    expect(searchWiki(index, 'hammer')[0].snippet).toContain('hammer');
  });
});
