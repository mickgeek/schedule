import { Injectable } from '@angular/core';
import { StorageUtility } from './storage.utility';
import { JsonUtility } from './json.utility';
import { UserRole } from './form.utility';

@Injectable()
export class UserTokenService {
  #payload: any = {
    exp: 0,
    iss: '',
    jti: 0,
    role: 0,
  }

  getToken() {
    return StorageUtility.getJwt();
  }

  setToken(value: string) {
    StorageUtility.setJwt(value);
  }

  removeToken() {
    StorageUtility.removeJwt();
  }

  #resetPayload() {
    this.#payload = {
      exp: 0,
      iss: '',
      jti: 0,
      role: 0,
    }
  }

  refreshAuthentication() {
    this.#resetPayload();
    const token = this.getToken();
    if (token !== undefined) {
      this.decodeToken(token);
      if (this.isTokenExpired() === true) {
        this.removeToken();
        this.#resetPayload();
      }
    }
  }

  decodeTokenPart(part: []) {
    let utf8decoder = new TextDecoder();
    let u8arr = new Uint8Array(part);
    return utf8decoder.decode(u8arr);
  }

  decodeToken(token: string = '') {
    try {
      const parts = token.split('.');
      const payload = JsonUtility.looseParse(this.decodeTokenPart(eval(atob(parts[1]))));
      this.#payload = {
        exp: payload.exp,
        iss: payload.iss,
        jti: payload.jti,
        role: payload.role,
      }
    } catch (event) {
      throw new Error('Token is not valid.');
    }
  }

  isTokenExpired() {
    return (Math.round(Date.now() / 1000) > this.#payload.exp) ? true : false;
  }

  getName() {
    this.refreshAuthentication();
    if (this.#payload.iss !== '') {
      return this.#payload.iss;
    }
    return 'unknown';
  }

  isManager() {
    this.refreshAuthentication();
    if (this.#payload.role === UserRole.Manager) {
      return true;
    }
    return false;
  }

  isMember() {
    this.refreshAuthentication();
    if (this.#payload.role === UserRole.Member) {
      return true;
    }
    return false;
  }

  isGuest() {
    this.refreshAuthentication();
    if (this.#payload.role === 0) {
      return true;
    }
    return false;
  }
}
