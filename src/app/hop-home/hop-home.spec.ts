import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { HopHome } from './hop-home';

describe('HopHome', () => {
  it('offers the demo, the wiki and the YouTube playlist', async () => {
    TestBed.configureTestingModule({ providers: [provideRouter([])] });
    const fixture = TestBed.createComponent(HopHome);
    await fixture.whenStable();
    const root = fixture.nativeElement as HTMLElement;
    const hrefs = Array.from(root.querySelectorAll('.hop-actions a')).map((link) =>
      link.getAttribute('href'),
    );
    expect(hrefs).toEqual([
      'https://store.steampowered.com/app/5319260/House_of_Pips_a_Domino_Roguelike_Demo/',
      '/hop/wiki',
    ]);
    expect(root.querySelector('iframe')?.getAttribute('src')).toBe(
      'https://www.youtube-nocookie.com/embed/fOqiFFHjgmo?list=PLaMPl9FW9Cug',
    );
    expect(root.querySelector('.video-link a')?.getAttribute('href')).toBe(
      'https://www.youtube.com/watch?v=fOqiFFHjgmo&list=PLaMPl9FW9Cug&pp=sAgC',
    );
    expect(root.querySelector('app-social-links')).toBeTruthy();
  });
});
