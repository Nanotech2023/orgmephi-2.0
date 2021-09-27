import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ContestPassingComponent } from './contest-passing.component';

describe('ContestPassingComponent', () => {
  let component: ContestPassingComponent;
  let fixture: ComponentFixture<ContestPassingComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ContestPassingComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ContestPassingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
