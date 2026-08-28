import { ComponentFixture, TestBed } from '@angular/core/testing';
import { StudioLanding } from './studio-landing';

describe('StudioLanding', () => {
  let component: StudioLanding;
  let fixture: ComponentFixture<StudioLanding>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StudioLanding],
    }).compileComponents();

    fixture = TestBed.createComponent(StudioLanding);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
