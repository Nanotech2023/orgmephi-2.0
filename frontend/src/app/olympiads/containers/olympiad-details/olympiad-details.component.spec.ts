import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OlympiadDetailsComponent } from './olympiad-details.component';

describe('OlympiadDetailsComponent', () => {
  let component: OlympiadDetailsComponent;
  let fixture: ComponentFixture<OlympiadDetailsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ OlympiadDetailsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(OlympiadDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
