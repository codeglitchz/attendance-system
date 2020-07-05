import { TestBed } from '@angular/core/testing';

import { VideoFeedService } from './video-feed.service';

describe('VideoFeedService', () => {
  let service: VideoFeedService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(VideoFeedService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
