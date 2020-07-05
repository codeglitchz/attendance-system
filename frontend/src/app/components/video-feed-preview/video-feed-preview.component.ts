import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { VideoFeedService } from 'src/app/services/video-feed.service';

@Component({
  selector: 'app-video-feed-preview',
  templateUrl: './video-feed-preview.component.html',
  styleUrls: ['./video-feed-preview.component.css']
})
export class VideoFeedPreviewComponent implements OnInit {

  public feed_id: string;
  public _feedUrl: string;
  public is_active: boolean;

  constructor(private _videoFeedService: VideoFeedService, private route: ActivatedRoute) { }

  ngOnInit(): void {
    let id = this.route.snapshot.paramMap.get('feed_id');
    this.feed_id = id;
    this._videoFeedService.getVideoFeed(id).subscribe(
      res => {
        console.log(res);
        this.is_active = res.is_active;
        // preview feed as it is
        // this._feedUrl = res.url;
        // run recognization & preview
        this._feedUrl = this._videoFeedService._feedPreviewUrl + "/" + id;

      },
      err => {
        // console.log(err);
      }
    );
  }

}
