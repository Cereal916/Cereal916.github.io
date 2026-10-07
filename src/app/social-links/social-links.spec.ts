import { Component } from '@angular/core';
import { TestBed } from '@angular/core/testing';
import { SocialLinks } from './social-links';

@Component({
  imports: [SocialLinks],
  template: '<app-social-links /><app-social-links />',
})
class TwoCopies {}

describe('SocialLinks', () => {
  it('links YouTube, Instagram and the Steam developer page in new tabs', async () => {
    const fixture = TestBed.createComponent(SocialLinks);
    await fixture.whenStable();
    const links = Array.from((fixture.nativeElement as HTMLElement).querySelectorAll('a'));
    expect(links.map((link) => link.getAttribute('href'))).toEqual([
      'https://www.youtube.com/@slapcraftgames',
      'https://www.instagram.com/slapcraftgames/',
      'https://store.steampowered.com/developer/slapcraft?snr=1_5_9__2000',
    ]);
    for (const link of links) {
      expect(link.target).toBe('_blank');
      expect(link.rel).toContain('noopener');
      expect(link.getAttribute('aria-label')).toMatch(/^Slapcraft Games on /);
    }
  });

  it('draws every mark without url(#id) references the base href would break', async () => {
    const fixture = TestBed.createComponent(TwoCopies);
    await fixture.whenStable();
    const marks = Array.from((fixture.nativeElement as HTMLElement).querySelectorAll('svg'));
    expect(marks.length).toBe(6);
    for (const mark of marks) {
      expect(mark.querySelector('mask, clipPath, defs, [id]')).toBeNull();
      expect(mark.innerHTML).not.toContain('url(');
    }
  });
});
