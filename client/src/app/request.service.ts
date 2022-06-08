import { Injectable, Inject } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { APP_CONFIG, AppConfig } from './app.config';
import { UserTokenService } from './user-token.service';

@Injectable()
export class RequestService {
  constructor(
    private httpClient: HttpClient,
    @Inject(APP_CONFIG) private config: AppConfig,
    private userTokenService: UserTokenService
  ) { }

  authenticate(body: any) {
    const url = this.config.serverEndpoint + '/authenticate';
    const request = this.httpClient.request('POST', url, { body: body, observe: 'body', responseType: 'json' })

    return request
  }

  getTasks(plannedAt: string) {
    const url = this.config.serverEndpoint + '/tasks';
    const httpParams = {
      planned_at: plannedAt,
      jwt: this.userTokenService.getToken() !== undefined ? this.userTokenService.getToken() : ''
    };
    const request = this.httpClient.request('GET', url, { params: httpParams, observe: 'body', responseType: 'json' })

    return request
  }

  putTask(id: number, body: any) {
    const url = id === 0 ? this.config.serverEndpoint + '/tasks' : this.config.serverEndpoint + `/tasks/${id}`;
    const httpParams = {
      jwt: this.userTokenService.getToken() !== undefined ? this.userTokenService.getToken() : ''
    };
    const request = this.httpClient.request('PUT', url, { params: httpParams, body: body, observe: 'body', responseType: 'json' })

    return request
  }

  deleteTask(id: number) {
    const url = this.config.serverEndpoint + `/tasks/${id}`;
    const httpParams = {
      jwt: this.userTokenService.getToken() !== undefined ? this.userTokenService.getToken() : ''
    };
    const request = this.httpClient.request('DELETE', url, { params: httpParams, observe: 'body', responseType: 'json' })

    return request
  }

  getUsers() {
    const url = this.config.serverEndpoint + '/users';
    const httpParams = {
      jwt: this.userTokenService.getToken() !== undefined ? this.userTokenService.getToken() : ''
    };
    const request = this.httpClient.request('GET', url, { params: httpParams, observe: 'body', responseType: 'json' })

    return request
  }

  getUserById(id: number) {
    const url = this.config.serverEndpoint + `/users/${id}`;
    const httpParams = {
      jwt: this.userTokenService.getToken() !== undefined ? this.userTokenService.getToken() : ''
    };
    const request = this.httpClient.request('GET', url, { params: httpParams, observe: 'body', responseType: 'json' })

    return request
  }
}
