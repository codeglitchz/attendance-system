import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';

import { faVideo, faCircle, faPlay, faStop } from '@fortawesome/free-solid-svg-icons';
import { faTrashAlt } from '@fortawesome/free-regular-svg-icons';

import { IVideoFeed } from 'src/app/interfaces/video-feed';
import { VideoFeedService } from 'src/app/services/video-feed.service';

@Component({
  selector: 'app-video-feed-list',
  templateUrl: './video-feed-list.component.html',
  styleUrls: ['./video-feed-list.component.css']
})
export class VideoFeedListComponent implements OnInit {

  videoIcon = faVideo;
  circleIcon = faCircle;
  playIcon = faPlay;
  stopIcon = faStop;
  trashIcon = faTrashAlt;

  videoFeedForm: FormGroup;
  public formIsCollapsed = true;
  public feeds: IVideoFeed[] = [];
 
  addResponseMsg = '';
  delResponseMsg = '';

  constructor(private _videoFeedService: VideoFeedService, private fb: FormBuilder) { }

  ngOnInit(): void {
    this.videoFeedForm = this.fb.group({
      id: ['', Validators.required],
      url: ['', Validators.required]
    })
    this._videoFeedService.getFeedList().subscribe(
      res => {
        // console.log(res);
        this.feeds = res;
      },
      err => {
        // console.log(err);
      }
    );
  }

  get id(){
    return this.videoFeedForm.get('id');
  }

  get url(){
    return this.videoFeedForm.get('url');
  }

  addVideoFeed(){
    console.log(this.videoFeedForm.value);
    this._videoFeedService.addVideoFeed(this.videoFeedForm.value).subscribe(
      res => {
        this.feeds.push(res);
        this.delResponseMsg = '';
        this.addResponseMsg = `Video feed for Classroom '${res.id}' has been added successfully`;
      }
    );
  }

  deleteVideoFeed(feed_id, index){
    // console.log(feed_id);
    this._videoFeedService.deleteVideoFeed(feed_id).subscribe(
      res => {
        // console.log(res);
        this.addResponseMsg = '';
        this.delResponseMsg = res.message;
        // remove entry from html
        this.feeds.splice(index, 1);
      },
      err => {
        // console.log(err);
      }
    );
  }

  // toggle video feed on or off
  toggleVideoFeed(feed_id){
    let is_active: Boolean;
    for (var feed of this.feeds) {
      if (feed.id == feed_id){
        is_active = feed.is_active
        if(is_active == true){
          // stop the feed
          this._videoFeedService.stop_feed(feed_id).subscribe(
            res => console.log(res),
            err => console.log(err)
          );
          return feed.is_active = false;
        }else{
          // start the feed again
          this._videoFeedService.start_feed(feed_id).subscribe(
            res => console.log(res),
            err => console.log(err)
          );
          return feed.is_active = true;
        }
      }
    }
    // return this.is_active = !this.is_active;
  }

  // generateUrl
  generatePreviewUrl(feed_id){
    return "/video_feeds/preview/" + feed_id.toString();
  }

}
