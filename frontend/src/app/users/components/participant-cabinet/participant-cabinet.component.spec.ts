import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ParticipantCabinetComponent } from './participant-cabinet.component';

describe('ParticipantCabinetComponent', () => {
  let component: ParticipantCabinetComponent;
  let fixture: ComponentFixture<ParticipantCabinetComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ParticipantCabinetComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ParticipantCabinetComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
