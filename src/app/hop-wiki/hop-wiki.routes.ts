import { Routes } from '@angular/router';
import { HopWikiLayout } from './hop-wiki-layout';
import { HopWikiPage } from './hop-wiki-page';

// /hop/wiki is the home page; every other page lives one or two segments
// below it, for example /hop/wiki/rules or /hop/wiki/perks/tax.
export const HOP_WIKI_ROUTES: Routes = [
  {
    path: '',
    component: HopWikiLayout,
    children: [
      { path: '', component: HopWikiPage },
      { path: '**', component: HopWikiPage },
    ],
  },
];
