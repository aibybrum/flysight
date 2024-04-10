import { Component } from '@angular/core';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss'
})
export class LoginComponent {
  email: string = '';
  password: string = '';

  onSubmit() {
    // TODO: Implement login logic
  }

  onForgotPassword() {
    // TODO: Implement forgot password logic
  }

  onSignup() {
    //
  }
}
