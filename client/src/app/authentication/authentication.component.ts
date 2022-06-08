import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { UserTokenService } from '../user-token.service';
import { RequestService } from '../request.service';

@Component({
  selector: 'authentication',
  templateUrl: './authentication.component.html'
})
export class AuthenticationComponent {
  userName = this.userTokenService.getName();
  isGuest = this.userTokenService.isGuest();

  form = new FormGroup({
    name: new FormControl(null, [Validators.nullValidator, Validators.required]),
    password: new FormControl(null, [Validators.nullValidator, Validators.required])
  });

  constructor(
    private router: Router,
    private userTokenService: UserTokenService,
    private requestService: RequestService
  ) { }

  doAuthentication() {
    if (this.form.valid === false) {
      return;
    }

    this.requestService.authenticate(this.form.value).subscribe((data: any) => {
      if (data.errors.length > 0) {
        this.form.setErrors(data.errors[0]);
        return;
      }

      this.userTokenService.setToken(data.token);
      this.router.navigateByUrl('tasks');
    });
  }

  clearAuthenticationData() {
    this.userTokenService.removeToken();
    this.router.navigateByUrl('');
  }
}
