import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { SocialLinks } from '../social-links/social-links';

export const HOP_DEMO_URL =
  'https://store.steampowered.com/app/5319260/House_of_Pips_a_Domino_Roguelike_Demo/';
export const HOP_PLAYLIST_URL =
  'https://www.youtube.com/watch?v=fOqiFFHjgmo&list=PLaMPl9FW9Cug&pp=sAgC';

interface Screenshot {
  src: string;
  alt: string;
}

/** The House of Pips home on the studio site: demo, videos, wiki. */
@Component({
  selector: 'app-hop-home',
  imports: [RouterLink, SocialLinks],
  templateUrl: './hop-home.html',
  styleUrl: './hop-home.scss',
})
export class HopHome {
  protected readonly demoUrl = HOP_DEMO_URL;
  protected readonly playlistUrl = HOP_PLAYLIST_URL;
  protected readonly screenshots: Screenshot[] = [
    {
      src: 'hop/wiki-data/img/screens/table.png',
      alt: 'A House of Pips match against Rival at the table',
    },
    { src: 'hop/wiki-data/img/screens/draft.png', alt: 'Drafting perks between hands' },
    { src: 'hop/wiki-data/img/screens/perks-compendium.png', alt: 'The perk compendium' },
  ];
}
