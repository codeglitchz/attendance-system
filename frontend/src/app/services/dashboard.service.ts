import { Injectable, Injector } from '@angular/core';
import { HttpClient, HttpBackend } from '@angular/common/http';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class DashboardService {

  private _dashboardUrl = "http://localhost:5000/dashboard";
  private _httpWithoutHeaders: HttpClient;

  constructor(private _injector: Injector, private http: HttpClient, private handler: HttpBackend) { 
    this._httpWithoutHeaders = new HttpClient(handler);
  }

  getDashboard(){
    let _authService = this._injector.get(AuthService);
    if (_authService.loggedIn()){
      return this.http.get<any>(this._dashboardUrl);
    }
    return this._httpWithoutHeaders.get<any>(this._dashboardUrl);
  }
}
