import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { StudentService } from 'src/app/services/student.service';

@Component({
  selector: 'app-student-capture',
  templateUrl: './student-capture.component.html',
  styleUrls: ['./student-capture.component.css']
})
export class StudentCaptureComponent implements OnInit {

  @ViewChild("video")
  public video: ElementRef;

  @ViewChild("canvas")
  public canvas: ElementRef;

  errorMsg = "";
  public captures: Array<any>;
  public blobCaptures: Array<Blob>;
  public student_id: string;
  
  constructor(private _studentService: StudentService, private route: ActivatedRoute, private _router: Router) {
    this.captures = [];
    this.blobCaptures = [];
   }

  ngOnInit(): void {
    let id = this.route.snapshot.paramMap.get('student_id');
    this.student_id = id;
  }

  public ngAfterViewInit() {
    if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true, audio: false }).then(stream => {
            this.video.nativeElement.srcObject = stream;
            this.video.nativeElement.play();
        });
    }
  }
  
  public capture() {
    var context = this.canvas.nativeElement.getContext("2d").drawImage(this.video.nativeElement, 0, 0, 640, 480);
    this.captures.push(this.canvas.nativeElement.toDataURL("image/jpg"));
    this.canvas.nativeElement.toBlob(blob => {
      this.blobCaptures.push(blob);
    }, "image/jpg", 0.95);
    // console.log(this.captures);
    // console.log(this.blobCaptures);
  }

  public resetCaptures(){
    this.captures = [];
    this.blobCaptures = [] as Blob[];
  }

  public saveCaptures(){
    console.log(this.captures.length);
    if (this.captures.length < 5){
      this.errorMsg = "Minimum 5 face captures are required.";
    }else{
      for(var i = 0; i < this.blobCaptures.length; i++){
        console.log(this.blobCaptures[i]);
        const formData = new FormData();
        const file = new File([this.blobCaptures[i]], 'name.jpg', {type:'image/jpg'});
        formData.append('image', file);
        this._studentService.captureStudent(this.student_id, formData).subscribe(
          res => console.log(res),
          err => console.log(err)
        );
      }
      this.resetCaptures();
      // navigate to students/
      this._router.navigate(['../../'], {relativeTo: this.route});
      // train the images
      this._studentService.trainClassifier().subscribe(
        res => console.log(res),
        err => console.log(err)
      );
    }
  }

}
