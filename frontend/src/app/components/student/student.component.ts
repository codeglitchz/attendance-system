import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';

import { faTrashAlt } from '@fortawesome/free-regular-svg-icons';

import { IStudent } from 'src/app/interfaces/student';
import { StudentService } from 'src/app/services/student.service';

@Component({
  selector: 'app-student',
  templateUrl: './student.component.html',
  styleUrls: ['./student.component.css']
})
export class StudentComponent implements OnInit {

  studentForm: FormGroup;
  public students: IStudent[] = [];
  trashIcon = faTrashAlt;
  addResponseMsg = '';
  delResponseMsg = '';

  constructor(private _studentService: StudentService, private fb: FormBuilder) { }

  ngOnInit(): void {
    this.studentForm = this.fb.group({
      name: ['', Validators.required]
    })
    this._studentService.getStudentList().subscribe(
      res => {
        // console.log(res);
        this.students = res;
      },
      err => {
        // console.log(err);
      }
    );
  }

  get name(){
    return this.studentForm.get('name');
  }

  addStudent(){
    console.log(this.studentForm.value);
    this._studentService.addStudent(this.studentForm.value).subscribe(
      res => {
        this.students.push(res);
        this.delResponseMsg = '';
        this.addResponseMsg = `'${res.name}' has been added successfully`;
        
      }
    );
  }

  deleteStudent(student_id, index){
    console.log(student_id);
    this._studentService.deleteStudent(student_id).subscribe(
      res => {
        // console.log(res);
        this.addResponseMsg = '';
        this.delResponseMsg = res.message;
        // remove entry from html
        this.students.splice(index, 1);
      },
      err => {
        // console.log(err);
      }
    );
  }

}
