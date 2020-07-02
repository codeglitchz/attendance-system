import { TestBed } from '@angular/core/testing';

import { AttendanceService } from './attendance.service';

describe('AttendanceService', () => {
  let service: AttendanceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AttendanceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
