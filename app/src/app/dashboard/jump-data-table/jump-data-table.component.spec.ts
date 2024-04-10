import { ComponentFixture, TestBed } from '@angular/core/testing';

import { JumpDataTableComponent } from './jump-data-table.component';

describe('JumpDataTableComponent', () => {
  let component: JumpDataTableComponent;
  let fixture: ComponentFixture<JumpDataTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [JumpDataTableComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(JumpDataTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
