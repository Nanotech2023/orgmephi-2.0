import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ContestAssignmentComponent } from './contest-assignment.component';

describe('ContestAssignmentComponent', () => {
  let component: ContestAssignmentComponent;
  let fixture: ComponentFixture<ContestAssignmentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ContestAssignmentComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ContestAssignmentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
