import { TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { Router } from '@angular/router';
import { MatTableModule } from '@angular/material/table';
import { of } from 'rxjs';
import { UserComponent } from './user.component';
import { UserTokenService } from '../user-token.service';
import { RequestService } from '../request.service';
import { UserRole } from '../form.utility';

describe('UserComponent', () => {
  let routerSpy: jasmine.SpyObj<Router>;
  let userTokenServiceSpy: jasmine.SpyObj<UserTokenService>;
  let requestServiceSpy: jasmine.SpyObj<RequestService>;

  beforeEach(async () => {
    routerSpy = jasmine.createSpyObj('Router', ['navigateByUrl']);
    userTokenServiceSpy = jasmine.createSpyObj('UserTokenService', ['isGuest']);
    requestServiceSpy = jasmine.createSpyObj('RequestService', ['getUsers', 'getUserById']);

    const response = {
      status: '200 OK',
      rows: [],
      errors: [],
      token: ''
    }
    requestServiceSpy.getUsers.and.returnValue(of(response));

    await TestBed.configureTestingModule({
      imports: [
        MatTableModule,
        RouterTestingModule
      ],
      declarations: [
        UserComponent
      ],
      providers: [
        { provide: Router, useValue: routerSpy },
        { provide: UserTokenService, useValue: userTokenServiceSpy },
        { provide: RequestService, useValue: requestServiceSpy }
      ]
    }).compileComponents();
  });

  it('should render the table with entities', () => {
    const fixture = TestBed.createComponent(UserComponent);
    const component = fixture.componentInstance;
    const compiled = fixture.nativeElement as HTMLElement;

    const response = {
      status: '200 OK',
      rows: [
        {
          id: 1,
          name: 'michael',
          role: UserRole.Manager,
          added_at: '2022-05-23 09:45:10',
          updated_at: null
        },
        {
          id: 2,
          name: 'emily',
          role: UserRole.Member,
          added_at: '2022-05-23 09:50:35',
          updated_at: null
        }
      ],
      errors: [],
      token: ''
    }
    requestServiceSpy.getUsers.and.returnValue(of(response));
    component.getUsers();

    fixture.detectChanges();
    expect(compiled.querySelector('div.user table tbody')?.textContent)
      .toContain('michael');
  });

  it('should render the details of an entity', () => {
    const fixture = TestBed.createComponent(UserComponent);
    const component = fixture.componentInstance;
    const compiled = fixture.nativeElement as HTMLElement;

    const response = {
      status: '200 OK',
      rows: [
        {
          id: 1,
          name: 'michael',
          role: UserRole.Manager,
          added_at: '2022-05-23 09:45:10',
          updated_at: null
        }
      ],
      errors: [],
      token: ''
    }
    requestServiceSpy.getUserById.and.returnValue(of(response));
    component.getUserById(1);

    fixture.detectChanges();
    expect(compiled.querySelector('div.user ul')?.textContent)
      .toContain('Name: michael');
  });
});
