import { Routes } from '@angular/router';
import { HopHome } from './hop-home/hop-home';
import { StudioLandingComponent } from './studio-landing/studio-landing';

export const routes: Routes = [
  { path: '', component: StudioLandingComponent, pathMatch: 'full' },
  // Everything for House of Pips lives under /hop.
  { path: 'hop', component: HopHome, pathMatch: 'full', title: 'House of Pips | Slapcraft Games' },
  {
    path: 'hop/wiki',
    title: 'House of Pips Wiki | Slapcraft Games',
    loadChildren: () => import('./hop-wiki/hop-wiki.routes').then((m) => m.HOP_WIKI_ROUTES),
  },
  { path: '**', redirectTo: '' },
];
