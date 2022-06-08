import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { UserRole, User, UserForm } from '../form.utility';
import { UserTokenService } from '../user-token.service';
import { RequestService } from '../request.service';

@Component({
  selector: 'user',
  templateUrl: './user.component.html'
})
export class UserComponent {
  users: User[] = [];
  columnDef: string[] = ['id', 'name', 'role', 'added_at', 'updated_at', 'actions'];

  existEntityShown = false;
  user: User = new UserForm();

  constructor(
    private router: Router,
    private userTokenService: UserTokenService,
    private requestService: RequestService
  ) {
    this.getUsers();
  }

  ngDoCheck() {
    if (this.userTokenService.isGuest() === true) {
      this.router.navigateByUrl('authentication');
    }
  }

  getUsers() {
    this.requestService.getUsers().subscribe((data: any) => {
      var users = [];
      for (const property in data.rows) {
        const row = data.rows[property];
        const user = new UserForm(row.id, row.name, '', row.role, row.added_at, row.updated_at);
        users.push(user);
      }
      this.users = users;
    });
  }

  showExistEntity() {
    this.existEntityShown = true;
  }

  getUserById(id: number) {
    this.requestService.getUserById(id).subscribe((data: any) => {
      for (const property in data.rows) {
        const row = data.rows[property];
        const user = new UserForm(row.id, row.name, '', row.role, row.added_at, row.updated_at);
        this.user = user;

        this.showExistEntity();
      }
    });
  }

  convertRole(role: number) {
    switch (role) {
      case UserRole.Manager:
        return 'Manager';
        break;
      case UserRole.Member:
        return 'Member';
        break;
    }

    return 'unknown';
  }
}
