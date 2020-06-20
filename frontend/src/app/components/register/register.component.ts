import { Component, OnInit } from '@angular/core';
import { AuthService } from 'src/app/services/auth.service';
import { User } from 'src/app/classes/user';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {

  // registerUserData = {};
  registerUserModel = new User('', '');
  submitted = false;
  errorMsg = '';
  responseMsg = '';

  constructor(private _auth: AuthService) { }

  ngOnInit(): void {
  }

  registerUser(){
    // console.log(this.registerUserModel);
    this.submitted = true;
    this._auth.registerUser(this.registerUserModel).subscribe(
      res => {
        console.log('Success!', res);
        this.errorMsg = '';
        this.responseMsg = res.message;
      },
      err => {
        console.log('Error!', err);
        this.responseMsg = '';
        this.errorMsg = err.error.message;
      }
    );
  }
}
