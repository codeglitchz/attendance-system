import { Component, OnInit } from '@angular/core';

import { VideoFeedService } from 'src/app/services/video-feed.service';

@Component({
  selector: 'app-video-feed-preview',
  templateUrl: './video-feed-preview.component.html',
  styleUrls: ['./video-feed-preview.component.css']
})
export class VideoFeedPreviewComponent implements OnInit {

  public _feedUrl = "http://localhost:5000/video_feeds/1"; // + "/" + _id.toString()

  constructor(private _videoFeedService: VideoFeedService) { }

  ngOnInit(): void {
  }

  get_is_active(){
    // get is_active of the given id parameter in the route
    return true;
  }

}
