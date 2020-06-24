import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { IStudent } from '../interfaces/student';
import { HttpClient } from '@angular/common/http';



@Injectable({
  providedIn: 'root'
})
export class StudentService {

  _studentListUrl = "http://localhost:5000/students";
  _studentDeleteUrl = "http://localhost:5000/students/delete";
  _studentAddUrl = "http://localhost:5000/students/add";

  constructor(private http: HttpClient) { }

  getStudentList(): Observable<IStudent[]>{
    return this.http.get<IStudent[]>(this._studentListUrl);
  }

  addStudent(student){
    return this.http.post<any>(this._studentAddUrl, student);
  }

  deleteStudent(student_id){
    return this.http.delete<any>(this._studentDeleteUrl + "/" + student_id);
  }

}
