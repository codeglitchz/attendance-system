import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { VideoFeedPreviewComponent } from './video-feed-preview.component';

describe('VideoFeedPreviewComponent', () => {
  let component: VideoFeedPreviewComponent;
  let fixture: ComponentFixture<VideoFeedPreviewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ VideoFeedPreviewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(VideoFeedPreviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
