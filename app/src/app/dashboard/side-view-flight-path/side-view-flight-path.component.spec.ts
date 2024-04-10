import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SideViewFlightPathComponent } from './side-view-flight-path.component';

describe('SideViewFlightPathComponent', () => {
  let component: SideViewFlightPathComponent;
  let fixture: ComponentFixture<SideViewFlightPathComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [SideViewFlightPathComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(SideViewFlightPathComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
