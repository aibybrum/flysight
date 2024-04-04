import { TestBed } from '@angular/core/testing';

import { JumpDataService } from './jump-data.service';

describe('JumpDataService', () => {
  let service: JumpDataService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(JumpDataService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
