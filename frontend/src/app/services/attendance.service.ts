import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';

import { IAttendance } from '../interfaces/attendance';

@Injectable({
  providedIn: 'root'
})
export class AttendanceService {

  _attendanceListUrl = "http://localhost:5000/attendance";

  constructor(private http: HttpClient) { }

  getAttendanceList(): Observable<IAttendance[]>{
    return this.http.get<IAttendance[]>(this._attendanceListUrl);
  }
}
