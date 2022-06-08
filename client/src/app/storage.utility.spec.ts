import { StorageUtility } from './storage.utility';

describe('StorageUtility', () => {
  it('should get, set and delete the storage variable (JWT)', () => {
    expect(StorageUtility.getJwt()).toBeUndefined();
    StorageUtility.setJwt('test json web token');
    expect(StorageUtility.getJwt()).toEqual('test json web token');
    StorageUtility.removeJwt();
    expect(StorageUtility.getJwt()).toBeUndefined();
  });
});
