import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable, shareReplay, throwError } from 'rxjs';
import { WikiManifest, WikiPage } from './hop-wiki.models';

/** Relative to the site's <base href>, so it works at every route depth. */
export const WIKI_DATA = 'hop/wiki-data/';
export const WIKI_ROUTE = '/hop/wiki';

// Page slugs are generated names such as "rules" or "perks/tax"; anything else
// never reaches the network.
const SLUG = /^[a-z0-9_-]+(\/[a-z0-9_-]+)*$/;

@Injectable({ providedIn: 'root' })
export class HopWikiData {
  private readonly http = inject(HttpClient);
  private manifestRequest?: Observable<WikiManifest>;
  private readonly pageRequests = new Map<string, Observable<WikiPage>>();

  manifest(): Observable<WikiManifest> {
    this.manifestRequest ??= this.http
      .get<WikiManifest>(`${WIKI_DATA}manifest.json`)
      .pipe(shareReplay(1));
    return this.manifestRequest;
  }

  page(slug: string): Observable<WikiPage> {
    if (!SLUG.test(slug)) {
      return throwError(() => new Error(`Unknown wiki page: ${slug}`));
    }
    let request = this.pageRequests.get(slug);
    if (!request) {
      request = this.http.get<WikiPage>(`${WIKI_DATA}pages/${slug}.json`).pipe(shareReplay(1));
      this.pageRequests.set(slug, request);
    }
    return request;
  }
}

/** The page slug for a route path below /hop/wiki ("" is the home page). */
export function slugFor(path: string): string {
  return path.replace(/^\/+|\/+$/g, '') || 'index';
}
