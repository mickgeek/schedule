import { NgModule, Injectable } from '@angular/core';
import { RouterModule, Routes, CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router } from '@angular/router';
import { IndexComponent } from './index/index.component';
import { AuthenticationComponent } from './authentication/authentication.component';
import { UserComponent } from './user/user.component';
import { TaskComponent } from './task/task.component';
import { ErrorNotFoundComponent } from './error-not-found/error-not-found.component';
import { UserTokenService } from './user-token.service';

@Injectable()
class CanActivateAuthentication implements CanActivate {
  constructor(private router: Router, private userTokenService: UserTokenService) { }

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
    return true;
  }
}

@Injectable()
class CanActivateUser implements CanActivate {
  constructor(private router: Router, private userTokenService: UserTokenService) { }

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
    if (this.userTokenService.isGuest() === true) {
      return this.router.parseUrl('authentication');
    }
    if (this.userTokenService.isManager() === true) {
      return true;
    }

    return false;
  }
}

@Injectable()
class CanActivateTask implements CanActivate {
  constructor(private router: Router, private userTokenService: UserTokenService) { }

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
    if (this.userTokenService.isGuest() === true) {
      return this.router.parseUrl('authentication');
    }
    if (this.userTokenService.isMember() === true) {
      return true;
    }
    if (this.userTokenService.isManager() === true) {
      return true;
    }

    return false;
  }
}

const routes: Routes = [
  { path: 'authentication', component: AuthenticationComponent, canActivate: [CanActivateAuthentication] },
  { path: 'users', component: UserComponent, canActivate: [CanActivateUser] },
  { path: 'tasks', component: TaskComponent, canActivate: [CanActivateTask] },
  { path: '', component: IndexComponent },
  { path: '**', component: ErrorNotFoundComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
  providers: [CanActivateAuthentication, CanActivateUser, CanActivateTask],
})
export class RoutingModule { }
