import { HttpClient } from '@angular/common/http';
import { defer } from 'rxjs';
import { ENVIRONMENT, AppConfig } from './app.config';
import { UserTokenService } from './user-token.service';
import { RequestService } from './request.service';
import { TaskStatus } from './form.utility';

export function asyncData(data: any) {
  return defer(() => Promise.resolve(data));
}

describe('RequestService', () => {
  let httpClientSpy: jasmine.SpyObj<HttpClient>;
  let appConfigSpy: jasmine.SpyObj<AppConfig>;
  let userTokenServiceSpy: jasmine.SpyObj<UserTokenService>;
  let requestService: RequestService;

  beforeEach(() => {
    httpClientSpy = jasmine.createSpyObj('HttpClient', ['request']);
    appConfigSpy = jasmine.createSpyObj('AppConfig', [], ENVIRONMENT);
    userTokenServiceSpy = jasmine.createSpyObj('UserTokenService', ['getToken']);
    requestService = new RequestService(httpClientSpy, appConfigSpy, userTokenServiceSpy);

    userTokenServiceSpy.getToken.and.returnValue('test json web token');
  });

  it('should make the request to authenticate a user', (done: DoneFn) => {
    const response = {
      code: '200 OK',
      rows: [],
      errors: [],
      token: 'test json web token'
    }
    httpClientSpy.request.and.returnValue(asyncData(response));
    requestService.authenticate({ name: 'michael', password: 'michael' })
      .subscribe({
        next: (data: any) => {
          expect(data).toEqual(response);
          done();
        },
        error: done.fail
      });
  });

  it('should make the request to authenticate a user with the not valid name', (done: DoneFn) => {
    const response = {
      code: '200 OK',
      rows: [],
      errors: [{ name: 'Name is not valid.' }],
      token: ''
    }
    httpClientSpy.request.and.returnValue(asyncData(response));
    requestService.authenticate({ name: 'm', password: 'michael' })
      .subscribe({
        next: (data: any) => {
          expect(data).toEqual(response);
          done();
        },
        error: done.fail
      });
  });

  it('should make the request to authenticate a user with the not valid password', (done: DoneFn) => {
    const response = {
      code: '200 OK',
      rows: [],
      errors: [{ password: 'Password is not valid.' }],
      token: ''
    }
    httpClientSpy.request.and.returnValue(asyncData(response));
    requestService.authenticate({ name: 'michael', password: 'm' })
      .subscribe({
        next: (data: any) => {
          expect(data).toEqual(response);
          done();
        },
        error: done.fail
      });
  });

  it('should make the request to get tasks', (done: DoneFn) => {
    const response = {
      status: '200 OK',
      rows: [
        {
          id: 1,
          description: 'Edit the book of a jungle.',
          planned_at: '2022-05-15',
          status: 1,
          added_at: '2022-05-25 11:51:17',
          updated_at: null,
          user_id: 1
        },
        {
          id: 2,
          description: 'Delete personal files.',
          planned_at: '2022-05-15',
          status: 2,
          added_at: '2022-05-25 11:51:10',
          updated_at: '2022-05-26 09:38:34',
          user_id: 1
        },
      ],
      errors: [],
      token: ''
    }
    httpClientSpy.request.and.returnValue(asyncData(response));
    requestService.getTasks('2022-05-15')
      .subscribe({
        next: (data: any) => {
          expect(data).toEqual(response);
          done();
        },
        error: done.fail
      });
  });

  it('should make the request to get no tasks', (done: DoneFn) => {
    const response = {
      status: '200 OK',
      rows: [],
      errors: [],
      token: ''
    }
    httpClientSpy.request.and.returnValue(asyncData(response));
    requestService.getTasks('2022-05-20')
      .subscribe({
        next: (data: any) => {
          expect(data).toEqual(response);
          done();
        },
        error: done.fail
      });
  });

  it('should make the request to create a task', (done: DoneFn) => {
    const response = {
      status: '201 Created',
      rows: [{ id: 3 }],
      errors: [],
      token: ''
    }
    httpClientSpy.request.and.returnValue(asyncData(response));
    const body = {
      year: 2022,
      month: 5,
      day: 10,
      description: 'Modify the code algorithm.',
      status: TaskStatus.Opened
    }
    requestService.putTask(0, body)
      .subscribe({
        next: (data: any) => {
          expect(data).toEqual(response);
          done();
        },
        error: done.fail
      });
  });

  it('should make the request to update a task', (done: DoneFn) => {
    const response = {
      status: '200 OK',
      rows: [],
      errors: [],
      token: ''
    }
    httpClientSpy.request.and.returnValue(asyncData(response));
    const body = {
      year: 2022,
      month: 5,
      day: 10,
      description: 'Modify the code logic.',
      status: TaskStatus.Closed
    }
    requestService.putTask(3, body)
      .subscribe({
        next: (data: any) => {
          expect(data).toEqual(response);
          done();
        },
        error: done.fail
      });
  });

  it('should make the request to delete a task', (done: DoneFn) => {
    const response = {
      status: '200 OK',
      rows: [],
      errors: [],
      token: ''
    }
    httpClientSpy.request.and.returnValue(asyncData(response));
    requestService.deleteTask(3)
      .subscribe({
        next: (data: any) => {
          expect(data).toEqual(response);
          done();
        },
        error: done.fail
      });
  });

  it('should make the request to get users', (done: DoneFn) => {
    const response = {
      status: '200 OK',
      rows: [
        {
          id: 1,
          name: 'michael',
          role: 1,
          added_at: '2022-05-25 11:50:10',
          updated_at: null
        },
        {
          id: 2,
          name: 'emily',
          role: 2,
          added_at: '2022-05-25 11:50:10',
          updated_at: null
        },
      ],
      errors: [],
      token: ''
    }
    httpClientSpy.request.and.returnValue(asyncData(response));
    requestService.getUsers()
      .subscribe({
        next: (data: any) => {
          expect(data).toEqual(response);
          done();
        },
        error: done.fail
      });
  });

  it('should make the request to get no users', (done: DoneFn) => {
    const response = {
      status: '200 OK',
      rows: [],
      errors: [],
      token: ''
    }
    httpClientSpy.request.and.returnValue(asyncData(response));
    requestService.getUsers()
      .subscribe({
        next: (data: any) => {
          expect(data).toEqual(response);
          done();
        },
        error: done.fail
      });
  });

  it('should make the request to get a single user', (done: DoneFn) => {
    const response = {
      status: '200 OK',
      rows: [
        {
          id: 1,
          name: 'michael',
          role: 1,
          added_at: '2022-05-25 11:50:10',
          updated_at: null
        },
      ],
      errors: [],
      token: ''
    }
    httpClientSpy.request.and.returnValue(asyncData(response));
    requestService.getUserById(1)
      .subscribe({
        next: (data: any) => {
          expect(data).toEqual(response);
          done();
        },
        error: done.fail
      });
  });
});
