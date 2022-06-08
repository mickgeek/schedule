import { TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { Router } from '@angular/router';
import { of } from 'rxjs';
import { AuthenticationComponent } from './authentication.component';
import { UserTokenService } from '../user-token.service';
import { RequestService } from '../request.service';

describe('AuthenticationComponent', () => {
  let routerSpy: jasmine.SpyObj<Router>;
  let userTokenServiceSpy: jasmine.SpyObj<UserTokenService>;
  let requestServiceSpy: jasmine.SpyObj<RequestService>;

  beforeEach(async () => {
    routerSpy = jasmine.createSpyObj('Router', ['navigateByUrl']);
    userTokenServiceSpy = jasmine.createSpyObj('UserTokenService', ['setToken', 'getName', 'isGuest']);
    requestServiceSpy = jasmine.createSpyObj('RequestService', ['authenticate']);

    await TestBed.configureTestingModule({
      imports: [
        RouterTestingModule
      ],
      declarations: [
        AuthenticationComponent
      ],
      providers: [
        { provide: Router, useValue: routerSpy },
        { provide: UserTokenService, useValue: userTokenServiceSpy },
        { provide: RequestService, useValue: requestServiceSpy }
      ]
    }).compileComponents();
  });

  it('should render to guest the form', () => {
    userTokenServiceSpy.getName.and.returnValue('unknown');
    userTokenServiceSpy.isGuest.and.returnValue(true);

    const fixture = TestBed.createComponent(AuthenticationComponent);
    const component = fixture.componentInstance;
    const compiled = fixture.nativeElement as HTMLElement;

    const response = {
      status: '200 OK',
      rows: [],
      errors: [],
      token: 'test json web token'
    }
    requestServiceSpy.authenticate.and.returnValue(of(response));

    fixture.detectChanges();
    expect(compiled.querySelector('div.authentication form')?.textContent)
      .not.toBeUndefined();
  });

  it('should render to authenticated user the button to clear authentication data', () => {
    userTokenServiceSpy.getName.and.returnValue('michael');
    userTokenServiceSpy.isGuest.and.returnValue(false);

    const fixture = TestBed.createComponent(AuthenticationComponent);
    const component = fixture.componentInstance;
    const compiled = fixture.nativeElement as HTMLElement;

    fixture.detectChanges();
    expect(compiled.querySelector('div.authentication button')?.textContent)
      .toContain('Clear Authentication Data');
  });

  it('should render the validation error (the name field)', () => {
    userTokenServiceSpy.getName.and.returnValue('michael');
    userTokenServiceSpy.isGuest.and.returnValue(true);

    const fixture = TestBed.createComponent(AuthenticationComponent);
    const component = fixture.componentInstance;
    const compiled = fixture.nativeElement as HTMLElement;

    const response = {
      status: '200 OK',
      rows: [],
      errors: [{ name: 'Name is not valid.' }],
      token: ''
    }
    requestServiceSpy.authenticate.and.returnValue(of(response));

    component.form.setValue({
      name: 'michael',
      password: 'm'
    });
    component.form.markAsTouched();
    component.doAuthentication();

    fixture.detectChanges();
    expect(compiled.querySelector('div.authentication form .error-warning')?.textContent)
      .toContain('Name is not valid.');
  });

  it('should render the validation error (the password field)', () => {
    userTokenServiceSpy.getName.and.returnValue('michael');
    userTokenServiceSpy.isGuest.and.returnValue(true);

    const fixture = TestBed.createComponent(AuthenticationComponent);
    const component = fixture.componentInstance;
    const compiled = fixture.nativeElement as HTMLElement;

    const response = {
      status: '200 OK',
      rows: [],
      errors: [{ password: 'Password is not valid.' }],
      token: ''
    }
    requestServiceSpy.authenticate.and.returnValue(of(response));

    component.form.setValue({
      name: 'm',
      password: 'michael'
    });
    component.form.markAsTouched();
    component.doAuthentication();

    fixture.detectChanges();
    expect(compiled.querySelector('div.authentication form .error-warning')?.textContent)
      .toContain('Password is not valid.');
  });
});
