import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageOlympiadsComponent } from './manage-olympiads.component';

describe('ManageOlynpiadsComponent', () => {
  let component: ManageOlympiadsComponent;
  let fixture: ComponentFixture<ManageOlympiadsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ManageOlympiadsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ManageOlympiadsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
