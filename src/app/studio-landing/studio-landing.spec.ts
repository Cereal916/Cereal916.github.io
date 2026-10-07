import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { StudioLandingComponent } from './studio-landing';

describe('StudioLandingComponent', () => {
  let component: StudioLandingComponent;
  let fixture: ComponentFixture<StudioLandingComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StudioLandingComponent],
      providers: [provideRouter([])],
    }).compileComponents();

    fixture = TestBed.createComponent(StudioLandingComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('announces the demo and links the House of Pips pages', () => {
    const root = fixture.nativeElement as HTMLElement;
    const hrefs = (selector: string) =>
      Array.from(root.querySelectorAll(selector)).map((link) => link.getAttribute('href'));
    const demo =
      'https://store.steampowered.com/app/5319260/House_of_Pips_a_Domino_Roguelike_Demo/';
    expect(root.querySelector('.demo-announcement')?.textContent).toContain('demo is out now');
    expect(hrefs('.demo-announcement a')).toEqual([demo, '/hop']);
    expect(hrefs('.card-actions a')).toEqual([demo, '/hop', '/hop/wiki']);
  });

  it('puts the studio social links in the header', () => {
    const root = fixture.nativeElement as HTMLElement;
    expect(root.querySelector('.studio-nav app-social-links')).toBeTruthy();
  });
});
