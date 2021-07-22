import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ParticipantRegistrationFormEducationComponent } from './participant-registration-form-education.component';

describe('ParticipantRegistrationFormEducationComponent', () => {
  let component: ParticipantRegistrationFormEducationComponent;
  let fixture: ComponentFixture<ParticipantRegistrationFormEducationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ParticipantRegistrationFormEducationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ParticipantRegistrationFormEducationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
