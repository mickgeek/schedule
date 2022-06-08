export enum UserRole {
  Manager = 1,
  Member = 2
}

export interface User {
  id: number;
  name: string;
  password_hash: string;
  role: UserRole.Manager | UserRole.Member | number;
  added_at: string;
  updated_at: string | null;
}

export class UserForm implements User {
  #id: number;
  #name: string;
  #password_hash: string;
  #role: UserRole.Manager | UserRole.Member | number;
  #added_at: string;
  #updated_at: string | null;

  constructor(
    id: number = 0,
    name: string = '',
    password_hash: string = '',
    role: number = 0,
    added_at: string = '',
    updated_at: string | null = null
  ) {
    this.#id = id;
    this.#name = name;
    this.#password_hash = password_hash;
    this.#role = role;
    this.#added_at = added_at;
    this.#updated_at = updated_at;
  }

  get id() {
    return this.#id;
  }

  set id(value) {
    this.#id = value;
  }

  get name() {
    return this.#name;
  }

  set name(value) {
    this.#name = value;
  }

  get password_hash() {
    return this.#password_hash;
  }

  set password_hash(value) {
    this.#password_hash = value;
  }

  get role() {
    return this.#role;
  }

  set role(value) {
    this.#role = value;
  }

  get added_at() {
    return this.#added_at;
  }

  set added_at(value) {
    this.#added_at = value;
  }

  get updated_at() {
    return this.#updated_at;
  }

  set updated_at(value) {
    this.#updated_at = value;
  }
}

export enum TaskStatus {
  Opened = 1,
  Closed = 2
}

export interface Task {
  id: number;
  description: string;
  planned_at: string;
  status: TaskStatus.Opened | TaskStatus.Closed | number;
  added_at: string;
  updated_at: string | null;
  user_id: number;
}

export class TaskForm implements Task {
  #id: number;
  #description: string;
  #planned_at: string;
  #status: TaskStatus.Opened | TaskStatus.Closed | number;
  #added_at: string;
  #updated_at: string | null;
  #user_id: number;

  constructor(
    id: number = 0,
    description: string = '',
    planned_at: string = '',
    status: number = 0,
    added_at: string = '',
    updated_at: string | null = null,
    user_id: number = 0
  ) {
    this.#id = id;
    this.#description = description;
    this.#planned_at = planned_at;
    this.#status = status;
    this.#added_at = added_at;
    this.#updated_at = updated_at;
    this.#user_id = user_id;
  }

  get id() {
    return this.#id;
  }

  set id(value) {
    this.#id = value;
  }

  get description() {
    return this.#description;
  }

  set description(value) {
    this.#description = value;
  }

  get planned_at() {
    return this.#planned_at;
  }

  set planned_at(value) {
    this.#planned_at = value;
  }

  get status() {
    return this.#status;
  }

  set status(value) {
    this.#status = value;
  }

  get added_at() {
    return this.#added_at;
  }

  set added_at(value) {
    this.#added_at = value;
  }

  get updated_at() {
    return this.#updated_at;
  }

  set updated_at(value) {
    this.#updated_at = value;
  }

  get user_id() {
    return this.#user_id;
  }

  set user_id(value) {
    this.#user_id = value;
  }
}
