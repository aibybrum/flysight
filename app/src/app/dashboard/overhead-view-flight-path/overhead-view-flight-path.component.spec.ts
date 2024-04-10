import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OverheadViewFlightPathComponent } from './overhead-view-flight-path.component';

describe('OverheadViewFlightPathComponent', () => {
  let component: OverheadViewFlightPathComponent;
  let fixture: ComponentFixture<OverheadViewFlightPathComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [OverheadViewFlightPathComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(OverheadViewFlightPathComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
