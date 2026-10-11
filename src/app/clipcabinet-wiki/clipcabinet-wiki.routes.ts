import { Routes } from '@angular/router';
import { ClipCabinetWiki } from './clipcabinet-wiki';
import { WIKI_GUIDES } from './clipcabinet-guides';

export const CLIPCABINET_WIKI_ROUTES: Routes = [
  ...WIKI_GUIDES.map((page) => ({
    path: page.slug,
    pathMatch: 'full' as const,
    component: ClipCabinetWiki,
    title: page.label + ' | ClipCabinet Wiki | Slapcraft Games',
    data: { pageId: page.slug },
  })),
  { path: '**', redirectTo: '' },
];
