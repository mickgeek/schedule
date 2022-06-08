import { Component, Inject } from '@angular/core';
import { Router } from '@angular/router';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { APP_CONFIG } from '../app.config';
import { TaskStatus, Task, TaskForm } from '../form.utility';
import { UserTokenService } from '../user-token.service';
import { RequestService } from '../request.service';
import { DateUtility } from '../date.utility';

@Component({
  selector: 'task',
  templateUrl: './task.component.html',
  styleUrls: ['./task.component.css']
})
export class TaskComponent {
  rawDates: string[] = [];
  dates: any = { years: [], months: [], days: [] }
  selectedDate: any = { year: null, month: null, day: null }

  tasks: Task[] = [];
  statuses: number[] = [TaskStatus.Opened, TaskStatus.Closed]
  columnDef: string[] = ['id', 'description', 'planned_at', 'status', 'added_at', 'updated_at', 'actions'];

  newEntityFormShown = false;
  newEntityForm = new FormGroup({
    planned_at: new FormControl(),
    description: new FormControl(null, [Validators.nullValidator, Validators.required, Validators.minLength(1)]),
    status: new FormControl(null, [Validators.nullValidator, Validators.required])
  });

  existEntityFormShown = false;
  existEntityForm = new FormGroup({
    id: new FormControl(),
    description: new FormControl(null, [Validators.nullValidator, Validators.required]),
    status: new FormControl(TaskStatus.Opened, [Validators.nullValidator, Validators.required])
  });

  constructor(
    @Inject(APP_CONFIG) private config: any,
    private router: Router,
    private userTokenService: UserTokenService,
    private requestService: RequestService
  ) {
    this.createRawDates();
    this.extractYears();
    this.selectedDate.year = this.dates.years[this.dates.years.length - 1];
    this.extractMonths(this.selectedDate.year);
    this.selectedDate.month = this.dates.months[this.dates.months.length - 1];
    this.extractDays(this.selectedDate.year, this.selectedDate.month);
    this.selectedDate.day = this.dates.days[this.dates.days.length - 1];

    this.getTasks(this.selectedDate.year, this.selectedDate.month, this.selectedDate.day);
  }

  ngDoCheck() {
    if (this.userTokenService.isGuest() === true) {
      this.router.navigateByUrl('authentication');
    }
  }

  createRawDates(beginningDate: string = this.config.beginningDate) {
    let dates = [];
    const current_date = Date.now();
    let iteratorDate = new Date(beginningDate);
    while (current_date >= iteratorDate.getTime()) {
      const date = iteratorDate.toISOString().slice(0, 10);
      dates.push(date);
      iteratorDate.setDate(iteratorDate.getDate() + 1);
    }

    this.rawDates = dates;
  }

  extractYears() {
    this.selectedDate.year = null;
    this.selectedDate.month = null;
    this.selectedDate.day = null;

    let years = [];
    for (const date of this.rawDates) {
      const parts = date.split('-');
      const year = Number(parts[0]);
      if (years.includes(year) === false) {
        years.push(year);
      }
    }

    this.dates.years = years;
  }

  extractMonths(year: number) {
    this.selectedDate.year = year;
    this.selectedDate.month = null;
    this.selectedDate.day = null;

    let months = [];
    for (const date of this.rawDates) {
      const parts = date.split('-');
      const month = Number(parts[1]);
      if (Number(parts[0]) === year && months.includes(month) === false) {
        months.push(month);
      }
    }

    this.dates.months = months;
  }

  extractDays(year: number, month: number) {
    this.selectedDate.year = year;
    this.selectedDate.month = month;
    this.selectedDate.day = null;

    let days = [];
    for (const date of this.rawDates) {
      const parts = date.split('-');
      const day = Number(parts[2]);
      if (Number(parts[0]) === year && Number(parts[1]) === month && days.includes(day) === false) {
        days.push(day);
      }
    }

    this.dates.days = days;
  }

  showNewEntityForm() {
    this.existEntityForm.reset();
    this.existEntityFormShown = false;

    const selectedDate = new Date(Date.UTC(this.selectedDate.year, this.selectedDate.month - 1, this.selectedDate.day));
    const plannedAt = selectedDate.toISOString().slice(0, 10);
    this.newEntityForm.reset({
      planned_at: plannedAt,
      description: null,
      status: TaskStatus.Opened
    });
    this.newEntityFormShown = true;
  }

  hideNewEntityForm() {
    this.newEntityForm.reset();
    this.newEntityFormShown = false;
  }

  showExistEntityForm(id: number | null = null, description: string | null = null, status: number | null = null) {
    this.newEntityForm.reset();
    this.newEntityFormShown = false;

    this.existEntityForm.reset({
      id: id,
      description: description,
      status: status
    });
    this.existEntityFormShown = true;
  }

  hideExistEntityForm() {
    this.existEntityForm.reset();
    this.existEntityFormShown = false;
  }

  getTasks(year: number, month: number, day: number) {
    const selectedDate = new Date(Date.UTC(year, month - 1, day));
    const plannedAt = selectedDate.toISOString().slice(0, 10);
    this.requestService.getTasks(plannedAt).subscribe((data: any) => {
      var tasks = [];
      for (const property in data.rows) {
        const row = data.rows[property];
        const task = new TaskForm(row.id, row.description, row.planned_at, row.status, row.added_at, row.updated_at, row.user_id);
        tasks.push(task);
      }
      this.tasks = tasks;

      this.hideNewEntityForm();
      this.hideExistEntityForm();

      this.selectedDate.year = year;
      this.selectedDate.month = month;
      this.selectedDate.day = day;
    });
  }

  putTask(newEntity: boolean = true) {
    if (newEntity === true && this.newEntityForm.valid === false) {
      return;
    }
    if (newEntity === false && this.existEntityForm.valid === false) {
      return;
    }

    const entityId = newEntity !== true ? this.existEntityForm.value['id'] : 0;
    const body = newEntity ? this.newEntityForm.value : this.existEntityForm.value;
    this.requestService.putTask(entityId, body).subscribe((data: any) => {
      this.getTasks(this.selectedDate.year, this.selectedDate.month, this.selectedDate.day);

      this.hideNewEntityForm();
      this.hideExistEntityForm();
    });
  }

  deleteTask(id: number) {
    this.requestService.deleteTask(id).subscribe((data: any) => {
      this.getTasks(this.selectedDate.year, this.selectedDate.month, this.selectedDate.day);
    });
  }

  convertMonth(month: number) {
    return DateUtility.convertMonth(month);
  }

  convertStatus(status: number) {
    switch (status) {
      case TaskStatus.Closed:
        return 'Closed';
        break;
      case TaskStatus.Opened:
        return 'Opened';
        break;
    }

    return 'unknown';
  }
}
