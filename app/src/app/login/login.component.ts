import { Component } from '@angular/core';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  username: string = '';
  password: string = '';
  showSignup: boolean = true;

  onSubmit() {
    // TODO: Implement login logic
  }

  onForgotPassword() {
    // TODO: Implement forgot password logic
  }

  onSignup() {
    this.showSignup = true;
  }
}