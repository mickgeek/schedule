import { UserTokenService } from './user-token.service';

describe('UserTokenService', () => {
  // header = { typ: 'JWT', alg: 'HS256' }
  // payload = { exp: 5000000000, iss: 'michael', jti: 1, role: 1 }
  const managerToken = 'WzEyMywgMzksIDExNiwgMTIxLCAxMTIsIDM5LCA1OCwgMzIsIDM5LCA3NCwgODcsIDg0LCAzOSwgNDQsIDMyLCAzOSwgOTcsIDEwOCwgMTAzLCAzOSwgNTgsIDMyLCAzOSwgNzIsIDgzLCA1MCwgNTMsIDU0LCAzOSwgMTI1XQ==.WzEyMywgMzksIDEwMSwgMTIwLCAxMTIsIDM5LCA1OCwgMzIsIDUzLCA0OCwgNDgsIDQ4LCA0OCwgNDgsIDQ4LCA0OCwgNDgsIDQ4LCA0NCwgMzIsIDM5LCAxMDUsIDExNSwgMTE1LCAzOSwgNTgsIDMyLCAzOSwgMTA5LCAxMDUsIDk5LCAxMDQsIDk3LCAxMDEsIDEwOCwgMzksIDQ0LCAzMiwgMzksIDEwNiwgMTE2LCAxMDUsIDM5LCA1OCwgMzIsIDQ5LCA0NCwgMzIsIDM5LCAxMTQsIDExMSwgMTA4LCAxMDEsIDM5LCA1OCwgMzIsIDQ5LCAxMjVd.w9po9v1t9k6-2mOFSwlVVQbt4AZF32vdyoKQwEen8D4=';

  // header = { typ: 'JWT', alg: 'HS256' }
  // payload = { exp: 1500000000, iss: 'michael', jti: 1, role: 1 }
const notActualToken = 'WzEyMywgMzksIDExNiwgMTIxLCAxMTIsIDM5LCA1OCwgMzIsIDM5LCA3NCwgODcsIDg0LCAzOSwgNDQsIDMyLCAzOSwgOTcsIDEwOCwgMTAzLCAzOSwgNTgsIDMyLCAzOSwgNzIsIDgzLCA1MCwgNTMsIDU0LCAzOSwgMTI1XQ==.WzEyMywgMzksIDEwMSwgMTIwLCAxMTIsIDM5LCA1OCwgMzIsIDQ5LCA1MywgNDgsIDQ4LCA0OCwgNDgsIDQ4LCA0OCwgNDgsIDQ4LCA0NCwgMzIsIDM5LCAxMDUsIDExNSwgMTE1LCAzOSwgNTgsIDMyLCAzOSwgMTA5LCAxMDUsIDk5LCAxMDQsIDk3LCAxMDEsIDEwOCwgMzksIDQ0LCAzMiwgMzksIDEwNiwgMTE2LCAxMDUsIDM5LCA1OCwgMzIsIDQ5LCA0NCwgMzIsIDM5LCAxMTQsIDExMSwgMTA4LCAxMDEsIDM5LCA1OCwgMzIsIDQ5LCAxMjVd.CsIU1xc7oV_K1Ey8k9Lw5Xelc0IDi7nmPqqFsTe9BqA='

  // header = { typ: 'JWT', alg: 'HS256' }
  // payload = { exp: 5000000000, iss: 'emily', jti: 2, role: 2 }
  const memberToken = 'WzEyMywgMzksIDExNiwgMTIxLCAxMTIsIDM5LCA1OCwgMzIsIDM5LCA3NCwgODcsIDg0LCAzOSwgNDQsIDMyLCAzOSwgOTcsIDEwOCwgMTAzLCAzOSwgNTgsIDMyLCAzOSwgNzIsIDgzLCA1MCwgNTMsIDU0LCAzOSwgMTI1XQ==.WzEyMywgMzksIDEwMSwgMTIwLCAxMTIsIDM5LCA1OCwgMzIsIDUzLCA0OCwgNDgsIDQ4LCA0OCwgNDgsIDQ4LCA0OCwgNDgsIDQ4LCA0NCwgMzIsIDM5LCAxMDUsIDExNSwgMTE1LCAzOSwgNTgsIDMyLCAzOSwgMTAxLCAxMDksIDEwNSwgMTA4LCAxMjEsIDM5LCA0NCwgMzIsIDM5LCAxMDYsIDExNiwgMTA1LCAzOSwgNTgsIDMyLCA1MCwgNDQsIDMyLCAzOSwgMTE0LCAxMTEsIDEwOCwgMTAxLCAzOSwgNTgsIDMyLCA1MCwgMTI1XQ==.g3SyBMB07HcwUrPYFDFkCQvz0PfodT6kl3Ilp_zGppU='

  it('should have the guest role', () => {
    const userTokenService = new UserTokenService();
    expect(userTokenService.isGuest()).toBeTrue();
  });

  it('should have the guest role (without the token variable declaring)', () => {
    const userTokenService = new UserTokenService();
    spyOn(userTokenService, 'getToken').and.returnValue(undefined);
    expect(userTokenService.isGuest()).toBeTrue();
  });

  it('should have the manager role', () => {
    const userTokenService = new UserTokenService();
    spyOn(userTokenService, 'getToken').and.returnValue(managerToken);
    expect(userTokenService.isManager()).toBeTrue();
  });

  it('should have the manager name', () => {
    const userTokenService = new UserTokenService();
    spyOn(userTokenService, 'getToken').and.returnValue(managerToken);
    expect(userTokenService.getName()).toContain('michael');
  });

  it('should have the guest role (with the not actual token)', () => {
    const userTokenService = new UserTokenService();
    spyOn(userTokenService, 'getToken').and.returnValue(notActualToken);
    expect(userTokenService.isMember()).toBeFalse();
    expect(userTokenService.isGuest()).toBeTrue();
  });

  it('should return the error exception (with the not valid token)', () => {
    const userTokenService = new UserTokenService();
    spyOn(userTokenService, 'getToken').and.returnValue('test json web token');
    expect(function() { userTokenService.decodeToken() }).toThrowError();
  });

  it('should have the member role', () => {
    const userTokenService = new UserTokenService();
    spyOn(userTokenService, 'getToken').and.returnValue(memberToken);
    expect(userTokenService.isMember()).toBeTrue();
  });
});
