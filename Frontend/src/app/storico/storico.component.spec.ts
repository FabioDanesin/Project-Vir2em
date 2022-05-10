import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StoricoComponent } from './storico.component';

describe('StoricoComponent', () => {
  let component: StoricoComponent;
  let fixture: ComponentFixture<StoricoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ StoricoComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(StoricoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
