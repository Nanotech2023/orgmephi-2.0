import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ContestRegistrationComponent } from './contest-registration.component';

describe('ContestRegistrationComponent', () => {
  let component: ContestRegistrationComponent;
  let fixture: ComponentFixture<ContestRegistrationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ContestRegistrationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ContestRegistrationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
