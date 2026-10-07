import { ViewportScroller } from '@angular/common';
import {
  Component,
  ElementRef,
  HostListener,
  ViewEncapsulation,
  computed,
  inject,
  signal,
  viewChild,
} from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import {
  IsActiveMatchOptions,
  Router,
  RouterLink,
  RouterLinkActive,
  RouterOutlet,
} from '@angular/router';
import { catchError, of } from 'rxjs';
import { HopWikiData, WIKI_DATA, WIKI_ROUTE } from './hop-wiki-data';
import { searchWiki } from './hop-wiki-search';

const EXACT: IsActiveMatchOptions = {
  paths: 'exact',
  queryParams: 'ignored',
  fragment: 'ignored',
  matrixParams: 'ignored',
};
const SECTION: IsActiveMatchOptions = {
  paths: 'subset',
  queryParams: 'ignored',
  fragment: 'ignored',
  matrixParams: 'ignored',
};

@Component({
  selector: 'app-hop-wiki-layout',
  imports: [RouterLink, RouterLinkActive, RouterOutlet],
  templateUrl: './hop-wiki-layout.html',
  styleUrl: './hop-wiki-layout.scss',
  // The page bodies arrive as generated HTML, so the wiki's styles are
  // global and scoped by the .hop-wiki class instead.
  encapsulation: ViewEncapsulation.None,
})
export class HopWikiLayout {
  private readonly router = inject(Router);
  private readonly host = inject<ElementRef<HTMLElement>>(ElementRef);

  protected readonly data = WIKI_DATA;
  protected readonly home = WIKI_ROUTE;
  protected readonly manifest = toSignal(
    inject(HopWikiData)
      .manifest()
      .pipe(catchError(() => of(null))),
  );
  protected readonly menuOpen = signal(false);
  protected readonly query = signal('');
  protected readonly searchOpen = signal(false);
  protected readonly active = signal(-1);
  protected readonly results = computed(() =>
    searchWiki(this.manifest()?.search ?? [], this.query()),
  );
  private readonly searchBox = viewChild<ElementRef<HTMLInputElement>>('searchBox');

  constructor() {
    // Headings land below the sticky header when a link jumps to them.
    inject(ViewportScroller).setOffset([0, 96]);
  }

  protected activeOptions(route: string): IsActiveMatchOptions {
    return route === WIKI_ROUTE ? EXACT : SECTION;
  }

  // A bare #fragment would resolve against <base href> and leave the wiki.
  protected skipToContent(event: Event): void {
    event.preventDefault();
    this.host.nativeElement.querySelector<HTMLElement>('#wiki-content')?.focus();
  }

  protected toggleMenu(): void {
    this.menuOpen.update((open) => !open);
  }

  protected closeMenu(): void {
    this.menuOpen.set(false);
  }

  protected onSearch(value: string): void {
    this.query.set(value);
    this.active.set(-1);
    this.searchOpen.set(true);
  }

  protected onSearchKey(event: KeyboardEvent): void {
    const count = this.results().length;
    if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
      event.preventDefault();
      if (count) {
        this.active.update(
          (index) => (index + (event.key === 'ArrowDown' ? 1 : -1) + count) % count,
        );
      }
    } else if (event.key === 'Enter') {
      const result = this.results()[Math.max(0, this.active())];
      if (result) {
        this.open(result.entry.u);
      }
    } else if (event.key === 'Escape') {
      this.onSearch('');
      this.searchOpen.set(false);
    }
  }

  protected openResult(event: MouseEvent, url: string): void {
    if (event.button === 0 && !event.ctrlKey && !event.metaKey && !event.shiftKey) {
      event.preventDefault();
      this.open(url);
    }
  }

  private open(url: string): void {
    this.searchOpen.set(false);
    this.query.set('');
    this.closeMenu();
    void this.router.navigateByUrl(url);
  }

  @HostListener('document:click', ['$event'])
  protected onDocumentClick(event: MouseEvent): void {
    const search = this.host.nativeElement.querySelector('.wiki-search');
    if (search && !search.contains(event.target as Node)) {
      this.searchOpen.set(false);
    }
  }

  @HostListener('document:keydown', ['$event'])
  protected onDocumentKey(event: KeyboardEvent): void {
    const typing = /input|textarea|select/i.test(
      (event.target as HTMLElement | null)?.tagName ?? '',
    );
    if (event.key === '/' && !typing) {
      event.preventDefault();
      this.searchBox()?.nativeElement.focus();
    }
  }
}
