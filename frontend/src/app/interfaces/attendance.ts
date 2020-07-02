import { Time } from '@angular/common';
import { IStudent } from './student';

export interface IAttendance {
    date: Date,
    students: IStudent[],
    time: Time
}