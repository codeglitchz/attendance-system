import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';

import { faTrashAlt } from '@fortawesome/free-regular-svg-icons';

import { IStudent } from 'src/app/interfaces/student';
import { StudentService } from 'src/app/services/student.service';

@Component({
  selector: 'app-student-list',
  templateUrl: './student-list.component.html',
  styleUrls: ['./student-list.component.css']
})
export class StudentListComponent implements OnInit {

  trashIcon = faTrashAlt;

  studentForm: FormGroup;
  public formIsCollapsed = true;
  public students: IStudent[] = [];
  
  addResponseMsg = '';
  delResponseMsg = '';

  constructor(
    private _studentService: StudentService, private fb: FormBuilder, 
    private _router: Router, private route: ActivatedRoute) { }

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
        this.captureFaces(res.id)
        // this.students.push(res);
        // this.delResponseMsg = '';
        // this.addResponseMsg = `'${res.name}' has been added successfully`;
        
      }
    );
  }

  captureFaces(student_id){
    this._router.navigate(['capture/' + student_id], {relativeTo: this.route});
  }

  deleteStudent(student_id, index){
    // console.log(student_id);
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
