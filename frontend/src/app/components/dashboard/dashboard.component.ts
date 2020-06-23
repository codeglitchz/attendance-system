import { Component, OnInit } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { DashboardService } from 'src/app/services/dashboard.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  dashboardResponseMsg = "";
  dashboardErrorMsg = "";

  constructor(private _dashboardService: DashboardService) { }

  ngOnInit(): void {
    this._dashboardService.getDashboard().subscribe(
      res => {
        // console.log(res);
        this.dashboardErrorMsg = "";
        this.dashboardResponseMsg = res.message;
      },
      err => {
        if (err instanceof HttpErrorResponse){
          // console.log(err);
          if (err.status === 401){
            // this._router.navigate(['/login']);
            this.dashboardResponseMsg = "";
            this.dashboardErrorMsg = err.error.message;
          }
        }
      }
    );
  }

}
