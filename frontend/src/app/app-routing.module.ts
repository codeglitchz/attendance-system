import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { AuthGuard } from './guards/auth.guard';

// components
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { RegisterComponent } from './components/register/register.component';
import { LoginComponent } from './components/login/login.component';
import { VideoFeedPreviewComponent } from './components/video-feed-preview/video-feed-preview.component';
import { VideoFeedListComponent } from './components/video-feed-list/video-feed-list.component';
import { StudentListComponent } from './components/student-list/student-list.component';
import { AttendanceComponent } from './components/attendance/attendance.component';
import { PageNotFoundComponent } from './components/page-not-found/page-not-found.component';


const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'login', component: LoginComponent },
  { path: 'video_feeds', component: VideoFeedListComponent, canActivate:[AuthGuard] },
  { path: 'video_feeds/preview/:feed_id', component: VideoFeedPreviewComponent, canActivate:[AuthGuard] },
  { path: 'students', component: StudentListComponent, canActivate:[AuthGuard] },
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
  VideoFeedListComponent, VideoFeedPreviewComponent, 
  StudentListComponent, 
  AttendanceComponent, 
  PageNotFoundComponent
]
