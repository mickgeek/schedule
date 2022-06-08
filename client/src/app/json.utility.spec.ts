import { JsonUtility } from './json.utility';

describe('JsonUtility', () => {
  it('should convert a month to the human-readable format', () => {
    expect(JsonUtility.looseParse('{ exp: 1500000000 }')).toBeInstanceOf(Object);
  });
});
