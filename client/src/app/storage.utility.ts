export class StorageUtility {
  static getJwt() {
    return localStorage['jwt'];
  }

  static setJwt(value: string) {
    localStorage['jwt'] = value;
  }

  static removeJwt() {
    delete localStorage['jwt'];
  }
}
