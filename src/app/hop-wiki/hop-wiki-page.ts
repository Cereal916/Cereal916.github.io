import { ViewportScroller } from '@angular/common';
import {
  Component,
  ElementRef,
  Injector,
  ViewEncapsulation,
  afterNextRender,
  computed,
  inject,
  signal,
} from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { DomSanitizer, Meta, Title } from '@angular/platform-browser';
import { ActivatedRoute, Router } from '@angular/router';
import { catchError, distinctUntilChanged, map, of, switchMap } from 'rxjs';
import { HopWikiData, WIKI_ROUTE, slugFor } from './hop-wiki-data';
import { WikiPage } from './hop-wiki.models';
import { normalise } from './hop-wiki-search';

interface PerkFilter {
  rarity: string;
  kind: string;
  text: string;
}

@Component({
  selector: 'app-hop-wiki-page',
  templateUrl: './hop-wiki-page.html',
  styleUrl: './hop-wiki-page.scss',
  encapsulation: ViewEncapsulation.None,
})
export class HopWikiPage {
  private readonly router = inject(Router);
  private readonly route = inject(ActivatedRoute);
  private readonly title = inject(Title);
  private readonly meta = inject(Meta);
  private readonly scroller = inject(ViewportScroller);
  private readonly host = inject<ElementRef<HTMLElement>>(ElementRef);
  private readonly injector = inject(Injector);
  private readonly sanitizer = inject(DomSanitizer);
  private filter: PerkFilter = { rarity: '', kind: '', text: '' };

  protected readonly page = signal<WikiPage | null>(null);
  protected readonly missing = signal(false);
  protected readonly home = WIKI_ROUTE;
  // Trusted on purpose: the bodies are generated from this site's own
  // Markdown in hop-wiki/ by hop-wiki/build.py and served from here, and they
  // carry the perk filter controls and data attributes Angular's sanitizer
  // would strip.
  protected readonly body = computed(() => {
    const page = this.page();
    return page ? this.sanitizer.bypassSecurityTrustHtml(page.html) : '';
  });

  constructor() {
    const data = inject(HopWikiData);
    this.route.url
      .pipe(
        map((segments) => slugFor(segments.map((segment) => segment.path).join('/'))),
        distinctUntilChanged(),
        switchMap((slug) => data.page(slug).pipe(catchError(() => of(null)))),
        takeUntilDestroyed(),
      )
      .subscribe((page) => this.show(page));
  }

  private show(page: WikiPage | null): void {
    this.page.set(page);
    this.missing.set(page === null);
    this.filter = { rarity: '', kind: '', text: '' };
    this.title.setTitle(
      page ? `${page.title} | Slapcraft Games` : 'Page not found | House of Pips Wiki',
    );
    this.meta.updateTag({
      name: 'description',
      content: page?.description ?? 'House of Pips player wiki.',
    });
    // The body arrives after navigation ends, so a deep link's fragment is
    // honoured once it is on screen.
    afterNextRender(
      () => {
        const fragment = this.route.snapshot.fragment;
        if (fragment && this.applyRarityFragment(fragment)) {
          return;
        }
        if (fragment) {
          this.scroller.scrollToAnchor(fragment);
        } else {
          this.scroller.scrollToPosition([0, 0]);
        }
      },
      { injector: this.injector },
    );
  }

  protected tocLink(id: string): string {
    return `${this.page()?.route ?? WIKI_ROUTE}#${id}`;
  }

  protected onClick(event: MouseEvent): void {
    const target = event.target as HTMLElement;
    const chip = target.closest<HTMLElement>("[data-filter='rarity']");
    if (chip) {
      this.setRarity(chip.dataset['value'] ?? '');
      return;
    }
    const link = target.closest('a');
    const href = link?.getAttribute('href') ?? '';
    const plain =
      event.button === 0 && !event.ctrlKey && !event.metaKey && !event.shiftKey && !event.altKey;
    if (link && plain && !link.target && href.startsWith(WIKI_ROUTE)) {
      // Wiki links stay in the single-page app; the router scrolls to any
      // fragment once the page is drawn.
      event.preventDefault();
      void this.router.navigateByUrl(href);
    }
  }

  protected onInput(event: Event): void {
    const field = event.target as HTMLInputElement;
    if (field.dataset['filter'] === 'text') {
      this.filter.text = normalise(field.value.trim());
      this.applyFilter();
    }
  }

  protected onChange(event: Event): void {
    const field = event.target as HTMLSelectElement;
    if (field.dataset['filter'] === 'kind') {
      this.filter.kind = field.value;
      this.applyFilter();
    }
  }

  /** /hop/wiki/perks#malus shows only that rarity, as its link promises. */
  private applyRarityFragment(fragment: string): boolean {
    const chip = this.host.nativeElement.querySelector<HTMLElement>(
      `.filters [data-filter='rarity'][data-value='${CSS.escape(fragment)}']`,
    );
    if (!chip) {
      return false;
    }
    this.setRarity(fragment);
    this.scroller.scrollToAnchor(fragment);
    return true;
  }

  private setRarity(value: string): void {
    this.filter.rarity = value;
    this.host.nativeElement
      .querySelectorAll<HTMLElement>("[data-filter='rarity']")
      .forEach((chip) => {
        chip.setAttribute('aria-pressed', chip.dataset['value'] === value ? 'true' : 'false');
      });
    this.applyFilter();
  }

  private applyFilter(): void {
    const root = this.host.nativeElement;
    let shown = 0;
    root.querySelectorAll<HTMLElement>('.perk-tile').forEach((tile) => {
      const visible =
        (!this.filter.rarity || tile.dataset['rarity'] === this.filter.rarity) &&
        (!this.filter.kind || tile.dataset['kind'] === this.filter.kind) &&
        (!this.filter.text || (tile.dataset['text'] ?? '').includes(this.filter.text));
      tile.hidden = !visible;
      shown += visible ? 1 : 0;
    });
    root.querySelectorAll<HTMLElement>('.perk-group').forEach((group) => {
      group.hidden = !group.querySelector('.perk-tile:not([hidden])');
    });
    const empty = root.querySelector<HTMLElement>('#perk-empty');
    if (empty) {
      empty.hidden = shown > 0;
    }
  }
}
