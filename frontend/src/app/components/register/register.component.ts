import { Component, OnInit } from '@angular/core';
import { AuthService } from 'src/app/services/auth.service';
import { FormBuilder, Validators, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {

  // registerUserModel = new User('', '');
  // registrationForm: FormGroup;
  submitted = false;
  errorMsg = '';
  responseMsg = '';
  passwordPattern = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;

  constructor(private _auth: AuthService, private fb: FormBuilder) { }

  ngOnInit(): void {
  }

  registrationForm = this.fb.group({
    username: ['', [Validators.required, Validators.minLength(4)]],
    password: ['', [Validators.required, Validators.pattern(this.passwordPattern)]]
  });

  get username(){
    return this.registrationForm.get('username');
  }

  get password(){
    return this.registrationForm.get('password');
  }

  registerUser(){
    // console.log(this.registrationForm.value);
    this.submitted = true;
    this._auth.registerUser(this.registrationForm.value).subscribe(
      res => {
        console.log('Success!', res);
        this.errorMsg = '';
        this.responseMsg = res.message;
      },
      err => {
        // console.log('Error!', err);
        this.responseMsg = '';
        this.errorMsg = err.error.message;
      }
    );
  }
}
