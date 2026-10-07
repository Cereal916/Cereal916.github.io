import { TestBed } from '@angular/core/testing';
import { Router, provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { of, throwError } from 'rxjs';
import { HopWikiData } from './hop-wiki-data';
import { WikiManifest, WikiPage } from './hop-wiki.models';
import { HOP_WIKI_ROUTES } from './hop-wiki.routes';

const manifest: WikiManifest = {
  site: 'House of Pips Wiki',
  version: '0.25.0-pre.5',
  nav: [{ section: 'Playing', pages: [{ title: 'Domino rules', route: '/hop/wiki/rules' }] }],
  search: [],
  pages: ['/hop/wiki', '/hop/wiki/perks/tax', '/hop/wiki/rules'],
};

const pages: Record<string, WikiPage> = {
  'perks/tax': {
    route: '/hop/wiki/perks/tax',
    title: 'Perk Tax - House of Pips Wiki',
    description: 'Malus.',
    html: '<h1>Perk Tax</h1><p><a href="/hop/wiki/rules">Domino rules</a></p>',
    toc: [],
  },
  rules: {
    route: '/hop/wiki/rules',
    title: 'Domino rules',
    description: '',
    html: '<h1>Rules</h1>',
    toc: [],
  },
};

describe('House of Pips wiki pages', () => {
  let harness: RouterTestingHarness;

  beforeEach(async () => {
    TestBed.configureTestingModule({
      providers: [
        provideRouter([{ path: 'hop/wiki', children: HOP_WIKI_ROUTES }]),
        {
          provide: HopWikiData,
          useValue: {
            manifest: () => of(manifest),
            page: (slug: string) =>
              pages[slug] ? of(pages[slug]) : throwError(() => new Error('404')),
          },
        },
      ],
    });
    harness = await RouterTestingHarness.create();
  });

  it('renders a generated page and keeps wiki links inside the app', async () => {
    await harness.navigateByUrl('/hop/wiki/perks/tax');
    const root = harness.fixture.nativeElement as HTMLElement;
    expect(root.querySelector('.hop-wiki-content h1')?.textContent).toBe('Perk Tax');
    expect(root.querySelector('.wiki-sidebar a')?.textContent?.trim()).toBe('Domino rules');
    expect(document.title).toBe('Perk Tax - House of Pips Wiki | Slapcraft Games');

    root.querySelector<HTMLAnchorElement>('.hop-wiki-content a')!.click();
    await harness.fixture.whenStable();
    expect(TestBed.inject(Router).url).toBe('/hop/wiki/rules');
    expect(root.querySelector('.hop-wiki-content h1')?.textContent).toBe('Rules');
  });

  it('shows a not-found page for a missing slug', async () => {
    await harness.navigateByUrl('/hop/wiki/no-such-page');
    expect((harness.fixture.nativeElement as HTMLElement).textContent).toContain('Page not found');
  });
});
