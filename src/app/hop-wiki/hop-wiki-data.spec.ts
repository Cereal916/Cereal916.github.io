import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { firstValueFrom } from 'rxjs';
import { HopWikiData, slugFor } from './hop-wiki-data';

describe('HopWikiData', () => {
  let data: HopWikiData;
  let http: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    data = TestBed.inject(HopWikiData);
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  it('loads pages from the base-relative data folder once', async () => {
    const first = firstValueFrom(data.page('perks/tax'));
    const second = firstValueFrom(data.page('perks/tax'));
    http.expectOne('hop/wiki-data/pages/perks/tax.json').flush({
      route: '/hop/wiki/perks/tax',
      title: 'Perk Tax',
      description: '',
      html: '',
      toc: [],
    });
    expect((await first).title).toBe('Perk Tax');
    expect((await second).title).toBe('Perk Tax');
  });

  it('never requests a slug outside the generated names', async () => {
    await expect(firstValueFrom(data.page('../manifest'))).rejects.toThrow();
    http.expectNone(() => true);
  });

  it('maps route paths to page slugs', () => {
    expect(slugFor('')).toBe('index');
    expect(slugFor('perks/tax')).toBe('perks/tax');
    expect(slugFor('/rules/')).toBe('rules');
  });
});
