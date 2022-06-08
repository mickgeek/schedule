export class JsonUtility {
  static looseParse(value: string) {
    return Function('"use strict"; return (' + value + ')')();
  }
}
