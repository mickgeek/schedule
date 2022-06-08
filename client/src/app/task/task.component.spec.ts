import { TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { Router } from '@angular/router';
import { MatTableModule } from '@angular/material/table';
import { of } from 'rxjs';
import { TaskComponent } from './task.component';
import { APP_CONFIG, ENVIRONMENT } from '../app.config';
import { UserTokenService } from '../user-token.service';
import { RequestService } from '../request.service';
import { TaskStatus } from '../form.utility';

describe('TaskComponent', () => {
  let routerSpy: jasmine.SpyObj<Router>;
  let userTokenServiceSpy: jasmine.SpyObj<UserTokenService>;
  let requestServiceSpy: jasmine.SpyObj<RequestService>;

  const responseWithNoData = {
    status: '200 OK',
    rows: [],
    errors: [],
    token: ''
  }
  const responseWithData = {
    status: '200 OK',
    rows: [
      {
        id: 1,
        description: 'Pack the box with gifts.',
        planned_at: '2022-05-15',
        status: TaskStatus.Opened,
        added_at: '2022-05-15 09:45:10',
        updated_at: null,
        user_id: 1
      },
      {
        id: 2,
        description: 'Repair the kid chair.',
        planned_at: '2022-05-15',
        status: TaskStatus.Opened,
        added_at: '2022-05-15 12:40:55',
        updated_at: null,
        user_id: 1
      }
    ],
    errors: [],
    token: ''
  }
  const responseWithUpdatedData = {
    status: '200 OK',
    rows: [
      {
        id: 1,
        description: 'Pack the box with gifts.',
        planned_at: '2022-05-15',
        status: TaskStatus.Opened,
        added_at: '2022-05-15 09:45:10',
        updated_at: null,
        user_id: 1
      },
      {
        id: 2,
        description: 'Update the third page.',
        planned_at: '2022-05-15',
        status: TaskStatus.Opened,
        added_at: '2022-05-15 15:45:10',
        updated_at: '2022-05-16 15:18:30',
        user_id: 1
      }
    ],
    errors: [],
    token: ''
  }
  const responseWithDeletedData = {
    status: '200 OK',
    rows: [
      {
        id: 1,
        description: 'Pack the box with gifts.',
        planned_at: '2022-05-15',
        status: TaskStatus.Opened,
        added_at: '2022-05-15 09:45:10',
        updated_at: null,
        user_id: 1
      }
    ],
    errors: [],
    token: ''
  }

  beforeEach(async () => {
    routerSpy = jasmine.createSpyObj('Router', ['navigateByUrl']);
    userTokenServiceSpy = jasmine.createSpyObj('UserTokenService', ['isGuest']);
    requestServiceSpy = jasmine.createSpyObj('RequestService', ['getTasks', 'putTask', 'deleteTask']);
    requestServiceSpy.getTasks.and.returnValue(of(responseWithNoData));

    await TestBed.configureTestingModule({
      imports: [
        MatTableModule,
        RouterTestingModule
      ],
      declarations: [
        TaskComponent
      ],
      providers: [
        { provide: APP_CONFIG, useValue: ENVIRONMENT },
        { provide: Router, useValue: routerSpy },
        { provide: UserTokenService, useValue: userTokenServiceSpy },
        { provide: RequestService, useValue: requestServiceSpy }
      ]
    }).compileComponents();
  });

  it('should render the navigation with selected buttons', () => {
    requestServiceSpy.getTasks.and.returnValue(of(responseWithNoData));

    const fixture = TestBed.createComponent(TaskComponent);
    const component = fixture.componentInstance;
    const compiled = fixture.nativeElement as HTMLElement;

    component.createRawDates('2022-01-15');
    component.extractYears();
    component.selectedDate.year = 2022;
    component.extractMonths(component.selectedDate.year);
    component.selectedDate.month = 5;
    component.extractDays(component.selectedDate.year, component.selectedDate.month);
    component.selectedDate.day = 7;

    fixture.detectChanges();
    expect(compiled.querySelector('div nav span.years .mat-button-disabled')?.textContent)
      .toContain('2022');
    expect(compiled.querySelector('div nav span.months .mat-button-disabled')?.textContent)
      .toContain('May');
    expect(compiled.querySelector('div nav span.days .mat-button-disabled')?.textContent)
      .toContain('7');
  });

  it('should render the table with no data by default', () => {
    requestServiceSpy.getTasks.and.returnValue(of(responseWithNoData));

    const fixture = TestBed.createComponent(TaskComponent);
    const component = fixture.componentInstance;
    const compiled = fixture.nativeElement as HTMLElement;

    fixture.detectChanges();
    expect(compiled.querySelector('div.task table tbody')?.textContent)
      .toBe('No data');
  });

  it('should render the table with entities', () => {
    requestServiceSpy.getTasks.and.returnValue(of(responseWithData));

    const fixture = TestBed.createComponent(TaskComponent);
    const component = fixture.componentInstance;
    const compiled = fixture.nativeElement as HTMLElement;

    component.selectedDate = { year: 2022, month: 5, day: 15 }
    component.getTasks(2022, 5, 15);
    fixture.detectChanges();
    expect(compiled.querySelector('div.task table tbody')?.textContent)
      .toContain('Pack the box with gifts.');
  });

  it('should create a new entity (render the form of a new entity)', () => {
    const fixture = TestBed.createComponent(TaskComponent);
    const component = fixture.componentInstance;
    const compiled = fixture.nativeElement as HTMLElement;

    requestServiceSpy.getTasks.and.returnValue(of(responseWithNoData));
    fixture.detectChanges();
    expect(compiled.querySelector('div.task table tbody')?.textContent)
      .toContain('No data');

    component.showNewEntityForm();
    fixture.detectChanges();
    expect(compiled.querySelector('div.task h3')?.textContent)
      .toContain('New Entity');

    // create an entity and get dummy entities
    const responseOfNewEntity = {
      status: '201 Created',
      rows: [{ id: 2 }],
      errors: [],
      token: ''
    }
    requestServiceSpy.putTask.and.returnValue(of(responseOfNewEntity));
    requestServiceSpy.getTasks.and.returnValue(of(responseWithData));

    component.newEntityForm.setValue({
      planned_at: '2022-05-15',
      description: 'Pack the box with gifts.',
      status: TaskStatus.Opened
    });
    component.putTask(true);

    component.getTasks(2022, 5, 15);
    fixture.detectChanges();
    expect(compiled.querySelector('div.task table tbody')?.textContent)
      .toContain('Pack the box with gifts.');
  });

  it('should update an exist entity (render the form of an exist entity)', () => {
    const fixture = TestBed.createComponent(TaskComponent);
    const component = fixture.componentInstance;
    const compiled = fixture.nativeElement as HTMLElement;

    requestServiceSpy.getTasks.and.returnValue(of(responseWithData));
    component.getTasks(2022, 5, 15);
    fixture.detectChanges();
    expect(compiled.querySelector('div.task table tbody')?.textContent)
      .toContain('Pack the box with gifts.');

    component.showExistEntityForm();
    fixture.detectChanges();
    expect(compiled.querySelector('div.task h3')?.textContent)
      .toContain('Exist Entity');

    // put an entity and get dummy entities
    const responseOfExistEntity = {
      status: '200 OK',
      rows: [],
      errors: [],
      token: ''
    }
    requestServiceSpy.putTask.and.returnValue(of(responseOfExistEntity));
    requestServiceSpy.getTasks.and.returnValue(of(responseWithUpdatedData));

    component.existEntityForm.setValue({
      id: 2,
      description: 'Update the third page.',
      status: TaskStatus.Opened
    });
    component.putTask(false);

    component.getTasks(2022, 5, 15)
    fixture.detectChanges();
    expect(compiled.querySelector('div.task table tbody')?.textContent)
      .toContain('Update the third page.');
  });

  it('should delete an exist entity', () => {
    const fixture = TestBed.createComponent(TaskComponent);
    const component = fixture.componentInstance;
    const compiled = fixture.nativeElement as HTMLElement;

    requestServiceSpy.getTasks.and.returnValue(of(responseWithData));
    component.getTasks(2022, 5, 15);
    fixture.detectChanges();
    expect(compiled.querySelector('div.task table tbody')?.textContent)
      .toContain('Repair the kid chair.');

    const responseOfDeletedEntity = {
      status: '200 OK',
      rows: [],
      errors: [],
      token: ''
    }
    requestServiceSpy.deleteTask.and.returnValue(of(responseOfDeletedEntity));
    requestServiceSpy.getTasks.and.returnValue(of(responseWithDeletedData));
    component.deleteTask(2);
    component.getTasks(2022, 5, 15);
    fixture.detectChanges();
    expect(compiled.querySelector('div.task table tbody')?.textContent)
      .not.toContain('Repair the kid chair.');
  });
});
