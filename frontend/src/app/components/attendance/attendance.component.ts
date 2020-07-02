import { Component, OnInit } from '@angular/core';
import { IAttendance } from 'src/app/interfaces/attendance';
import { AttendanceService } from 'src/app/services/attendance.service';

@Component({
  selector: 'app-attendance',
  templateUrl: './attendance.component.html',
  styleUrls: ['./attendance.component.css']
})
export class AttendanceComponent implements OnInit {

  public attendances: IAttendance[] = [];

  constructor(private _attendanceService: AttendanceService) { }

  ngOnInit(): void {
    this._attendanceService.getAttendanceList().subscribe(
      res => {
        // console.log(res);
        this.attendances = res;
      },
      err => {
        // console.log(err);
      }
    );
  }

}
