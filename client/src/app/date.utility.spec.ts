import { DateUtility } from './date.utility';

describe('DateUtility', () => {
  it('should convert a month to the human-readable format', () => {
    expect(DateUtility.convertMonth(7)).toEqual('July');
  });
});
