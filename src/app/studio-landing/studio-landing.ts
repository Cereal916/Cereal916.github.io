import { Component } from '@angular/core';
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
  studioTagline = 'Forging High-Impact 2D Pixel Experiences';
  currentYear = new Date().getFullYear();

  activeProject: GameProject = {
    title: 'Project: Domino Smash (Working Title)',
    engine: 'Built with LÖVE (Love2D) & Lua',
    status: 'In Active Production — Targeting Steam',
    description:
      'An action-packed puzzle tactical game where kinetic chain reactions meet heavy combat mechanics. Destroy obstacles, forge physics-based combos, and crush adversaries utilizing precise pixel-perfect grid collisions.',
    features: [
      'Handcrafted retro pixel aesthetics tailored for desktop rendering',
      'Advanced 2D physics framework written completely from scratch in Lua',
      'Intricate chain-reaction logic system giving players total tactical control',
    ],
  };
}
