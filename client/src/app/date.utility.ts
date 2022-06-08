export class DateUtility {
  static namedMonths: string[] = [
    'January', 'February', 'March',
    'April', 'May', 'June',
    'July', 'August', 'September',
    'October', 'November', 'December'
  ];

  static convertMonth(month: number) {
    return DateUtility.namedMonths[month - 1];
  }
}
