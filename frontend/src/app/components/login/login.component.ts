import { Component, OnInit } from '@angular/core';
import { AuthService } from 'src/app/services/auth.service';
import { Router } from '@angular/router';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  // loginUserModel = new User('', '');
  loginForm: FormGroup;
  submitted = false;
  errorMsg = '';

  constructor(private _auth: AuthService, private _router: Router, private fb: FormBuilder) { }

  ngOnInit(): void {
    this.loginForm = this.fb.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    })
  }

  get username(){
    return this.loginForm.get('username');
  }

  get password(){
    return this.loginForm.get('password');
  }

  loginUser(){
    this.submitted = true;
    // console.log(this.loginForm.value);
    this._auth.loginUser(this.loginForm.value).subscribe(
      res => {
        // console.log('Success!', res);
        this.errorMsg = '';

        localStorage.setItem('access_token', res.access_token);
        this._router.navigate(['/dashboard']);
      },
      err => {
        // console.log('Error!', err);
        this.errorMsg = err.error.message;
      }
    );
  }
}
