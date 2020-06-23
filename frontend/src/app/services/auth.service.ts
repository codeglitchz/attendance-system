import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Router } from '@angular/router';
import { User } from '../classes/user';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private _registerUrl = "http://localhost:5000/register";
  private _loginUrl = "http://localhost:5000/login";

  constructor(private http: HttpClient, private _router: Router) { }

  registerUser(user: User){
    return this.http.post<any>(this._registerUrl, user)
    // .pipe(
    //   catchError(this.errorHandler)
    // );
  }

  loginUser(user: User){
    return this.http.post<any>(this._loginUrl, user);
  }

  // errorHandler(error: HttpErrorResponse){
  //   return throwError(error);    
  // }

  loggedIn(){
    // returns true if access_token exists else false
    return !!localStorage.getItem('access_token');
  }

  logoutUser(){
    localStorage.removeItem('access_token');
    this._router.navigate(['/login']);
  }

  getToken(){
    // returns the token
    return localStorage.getItem('access_token');
  }
}
