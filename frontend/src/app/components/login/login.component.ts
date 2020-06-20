import { Component, OnInit } from '@angular/core';
import { User } from 'src/app/classes/user';
import { AuthService } from 'src/app/services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  // loginUserData = {};
  loginUserModel = new User('', '');
  submitted = false;
  errorMsg = '';

  constructor(private _auth: AuthService, private _router: Router) { }

  ngOnInit(): void {
  }

  loginUser(){
    this.submitted = true;
    // console.log(this.loginUserModel);
    this._auth.loginUser(this.loginUserModel).subscribe(
      res => {
        console.log('Success!', res);
        this.errorMsg = '';

        localStorage.setItem('access_token', res.access_token);
        this._router.navigate(['/special']);
      },
      err => {
        console.log('Error!', err);
        this.errorMsg = err.error.message;
      }
    );
  }
}
