import { UserRole, UserForm, TaskStatus, TaskForm } from './form.utility';

describe('UserRole', () => {
  it('should check to exists the user roles', () => {
    expect(UserRole.Manager).toEqual(1);
    expect(UserRole.Member).toEqual(2);
  });

  it('should create the value object with user data', () => {
    const userForm = new UserForm(1, 'michael', 'test password hash', 1, '2022-05-25 11:50:10', null);
    expect(userForm.id).toEqual(1);
    expect(userForm.name).toEqual('michael');
    expect(userForm.password_hash).toEqual('test password hash');
    expect(userForm.added_at).toEqual('2022-05-25 11:50:10');
    expect(userForm.updated_at).toEqual(null);
  });

  it('should check to exists the task statuses', () => {
    expect(TaskStatus.Opened).toEqual(1);
    expect(TaskStatus.Closed).toEqual(2);
  });

  it('should create the value object with user data', () => {
    const taskForm = new TaskForm(1, 'Edit the book of a jungle.', '2022-05-15', 1, '2022-05-25 11:51:17', null, 1);
    expect(taskForm.id).toEqual(1);
    expect(taskForm.description).toEqual('Edit the book of a jungle.');
    expect(taskForm.planned_at).toEqual('2022-05-15');
    expect(taskForm.status).toEqual(1);
    expect(taskForm.added_at).toEqual('2022-05-25 11:51:17');
    expect(taskForm.updated_at).toEqual(null);
    expect(taskForm.user_id).toEqual(1);
  });
});
