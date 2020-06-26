import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { AuthGuard } from './guards/auth.guard';

// components
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { RegisterComponent } from './components/register/register.component';
import { LoginComponent } from './components/login/login.component';
import { VideoFeedComponent } from './components/video-feed/video-feed.component';
import { StudentComponent } from './components/student/student.component';
import { AttendanceComponent } from './components/attendance/attendance.component';
import { PageNotFoundComponent } from './components/page-not-found/page-not-found.component';


const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'login', component: LoginComponent },
  { path: 'video_feed', component: VideoFeedComponent, canActivate:[AuthGuard] },
  { path: 'students', component: StudentComponent, canActivate:[AuthGuard] },
  { path: 'attendance', component: AttendanceComponent, canActivate:[AuthGuard] },
  { path: '**', component: PageNotFoundComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
export const routingComponents = [
  DashboardComponent, 
  RegisterComponent, LoginComponent, 
  VideoFeedComponent, StudentComponent, AttendanceComponent, 
  PageNotFoundComponent
]
