import cv2
import datetime
import ffmpeg
import os
import sys
import time

# from dateutil import parser


_CURRENT_PATH = os.getcwd()
_FPS = 25
_PLAYSPEED = 25


class Video:

  def __init__(self, file_name: str):
    self.file_name = file_name
    self.video_capture = cv2.VideoCapture(self.file_name)
    streams = ffmpeg.probe(self.file_name)['streams']
    self._video_stream = [s for s in streams if s['codec_type'] == 'audio'][0]
    video_creation_time = self._video_stream['tags']['creation_time']
    self.video_creation_time = time.mktime(
        datetime.datetime.fromisoformat(video_creation_time).timetuple()
    )
    self.video_duration = self._video_stream['duration']
    self.video_duration_ts = self._video_stream['duration_ts']
    self.video_nb_frames = self._video_stream['nb_frames']
  

if __name__ == '__main__':
  file_1 = os.path.join(_CURRENT_PATH, sys.argv[1])
  file_2 = os.path.join(_CURRENT_PATH, sys.argv[2])

  video_1 = Video(file_1)
  video_2 = Video(file_2)

  output_f = open(file_1 + '_out.csv', 'w')

  start_time_delta = int(video_1.video_creation_time - video_2.video_creation_time)

  if start_time_delta > 0:
    earlier_video = video_2
    later_video = video_1
  else:
    earlier_video = video_1
    later_video = video_2
    start_time_delta = -start_time_delta

  earlier_cap = earlier_video.video_capture
  later_cap = later_video.video_capture

  skipping_frame = start_time_delta * _FPS

  for _ in range(skipping_frame):
    earlier_cap.read()

  output_f.write('{},{},{},{},{} seconds,{} frames\n'.format(
      os.path.basename(earlier_video.file_name),
      earlier_video.video_creation_time,
      os.path.basename(later_video.file_name),
      later_video.video_creation_time,
      start_time_delta,
      skipping_frame,
  ))

  time = 1
  is_focused = True
  is_quit = False
  is_close_1 = False
  is_close_2 = False

  while(earlier_cap.isOpened() and later_cap.isOpened()):
    success_1, frame_1 = earlier_cap.read()
    success_2, frame_2 = later_cap.read()

    frame_2 = cv2.resize(frame_2, (500, 250))
    frame_1 = cv2.resize(frame_1, (500, 250))

    if success_1 and success_2:
      cv2.imshow('Video Player 1', frame_1)
      cv2.imshow('Video Player 2', frame_2)
    
    pressed_button = cv2.waitKey(_PLAYSPEED) & 0xFF

    if pressed_button == ord('q'):
      is_quit = True
    elif pressed_button == ord('z'):
      is_focused = True
    elif pressed_button == ord('x'):
      is_focused = False
    
    output_f.write('{},{}\n'.format(time, 1 if is_focused else 0))
    time += 1
    
    is_close_1 = cv2.getWindowProperty('Video Player 1', cv2.WND_PROP_VISIBLE) < 1
    is_close_2 = cv2.getWindowProperty('Video Player 2', cv2.WND_PROP_VISIBLE) < 1
    if is_quit or is_close_1 or is_close_2:
      break
    
  earlier_cap.release()
  later_cap.release()
