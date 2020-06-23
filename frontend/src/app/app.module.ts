import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

// components
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { RegisterComponent } from './components/register/register.component';
import { LoginComponent } from './components/login/login.component';
import { VideoFeedComponent } from './components/video-feed/video-feed.component';
import { StudentsComponent } from './components/students/students.component';
import { AttendanceComponent } from './components/attendance/attendance.component';

// other imports
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { TokenInterceptorService } from './services/token-interceptor.service';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

@NgModule({
  declarations: [
    AppComponent,
    RegisterComponent,
    LoginComponent,
    VideoFeedComponent,
    DashboardComponent,
    StudentsComponent,
    AttendanceComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule,
    HttpClientModule,
    NgbModule
  ],
  providers: [ { provide: HTTP_INTERCEPTORS, useClass: TokenInterceptorService, multi: true } ],
  bootstrap: [AppComponent]
})
export class AppModule { }
