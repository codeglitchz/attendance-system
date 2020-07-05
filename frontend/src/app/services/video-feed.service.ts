import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { IVideoFeed } from '../interfaces/video-feed';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class VideoFeedService {
  _feedListUrl = "http://localhost:5000/video_feeds";
  _feedAddUrl = "http://localhost:5000/video_feeds/add"
  _feedStartUrl = "http://localhost:5000/video_feeds/start";
  _feedStopUrl = "http://localhost:5000/video_feeds/stop";
  _feedDeleteUrl = "http://localhost:5000/video_feeds/delete";
 
  constructor(private http: HttpClient) { }

  getFeedList(): Observable<IVideoFeed[]>{
    return this.http.get<IVideoFeed[]>(this._feedListUrl);
  }

  addVideoFeed(_feed){
    return this.http.post<any>(this._feedAddUrl, _feed);
  }

  deleteVideoFeed(feed_id){
    return this.http.delete<any>(this._feedDeleteUrl + "/" + feed_id);
  }

  start_feed(feed_id){
    // todo: pass a parameter called feed_id & append it to url
    return this.http.get<any>(this._feedStartUrl + "/" + feed_id.toString());
  }

  stop_feed(feed_id){
    // todo: pass a parameter called feed_id & append it to url
    return this.http.get<any>(this._feedStopUrl + "/" + feed_id.toString());
  }
}
