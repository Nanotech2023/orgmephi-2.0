import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddContestModalComponent } from './add-contest-modal.component';

describe('AddContestModalComponent', () => {
  let component: AddContestModalComponent;
  let fixture: ComponentFixture<AddContestModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AddContestModalComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AddContestModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
