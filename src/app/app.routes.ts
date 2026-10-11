import { Routes } from '@angular/router';
import { HopHome } from './hop-home/hop-home';
import { StudioLandingComponent } from './studio-landing/studio-landing';

export const routes: Routes = [
  { path: '', component: StudioLandingComponent, pathMatch: 'full', title: 'Slapcraft Games' },
  // Everything for House of Pips lives under /hop.
  { path: 'hop', component: HopHome, pathMatch: 'full', title: 'House of Pips | Slapcraft Games' },
  {
    path: 'hop/wiki',
    title: 'House of Pips Wiki | Slapcraft Games',
    loadChildren: () => import('./hop-wiki/hop-wiki.routes').then((m) => m.HOP_WIKI_ROUTES),
  },
  { path: 'clipcabinet', redirectTo: 'clipcabinet/wiki', pathMatch: 'full' },
  {
    path: 'clipcabinet/wiki',
    title: 'ClipCabinet Wiki | Slapcraft Games',
    loadChildren: () => import('./clipcabinet-wiki/clipcabinet-wiki.routes').then((m) => m.CLIPCABINET_WIKI_ROUTES),
  },
  { path: '**', redirectTo: '' },
];
