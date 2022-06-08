import { Component } from '@angular/core';
import { UserTokenService } from './user-token.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  isManager = this.userTokenService.isManager();
  isMember = this.userTokenService.isMember();
  isGuest = this.userTokenService.isGuest();

  constructor(private userTokenService: UserTokenService) { }

  ngDoCheck() {
    this.isManager = this.userTokenService.isManager();
    this.isMember = this.userTokenService.isMember();
    this.isGuest = this.userTokenService.isGuest();
  }
}
