import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';

interface GameProject {
  title: string;
  engine: string;
  status: string;
  description: string;
  features: string[];
}

@Component({
  selector: 'app-studio-landing',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './studio-landing.html',
  styleUrls: ['./studio-landing.scss'],
})
export class StudioLandingComponent {
  studioName = 'Slapcraft Games';
  studioEmail = 'SlapcraftGames@gmail.com';
  studioTagline = 'Forging High-Impact 2D Pixel Experiences';
  currentYear = new Date().getFullYear();
  contactHighlighted = signal(false);

  highlightContact(): void {
    const contact = document.getElementById('contact-email');

    contact?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    this.contactHighlighted.set(false);

    window.setTimeout(() => {
      this.contactHighlighted.set(true);
    });

    window.setTimeout(() => {
      this.contactHighlighted.set(false);
    }, 3000);
  }

  activeProject: GameProject = {
    title: 'Project: Domino Delirium',
    engine: 'In development with LÖVE (Love2D) and Lua',
    status: 'In Development — Planned for Steam',
    description:
      'A roguelike-inspired domino game in development, where scoring abilities, perks, and changing house rules shape each match. Build your strategy, grow stronger, and outplay your rival.',
    features: [
      'A retro pixel-art presentation designed for desktop play',
      'Replayable matches shaped by changing rules and upgrades',
      'Unlockable perks designed to expand strategic options',
    ],
  };
}
