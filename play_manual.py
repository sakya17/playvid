import cv2
import datetime
import ffmpeg
import os
import sys
import time

from dateutil import parser


_CURRENT_PATH = os.getcwd()
_FPS = 25
_PLAYSPEED = 25


class Video:

  def __init__(self, file_name: str):
    self.file_name = file_name
    self.video_capture = cv2.VideoCapture(self.file_name)
    streams = ffmpeg.probe(self.file_name)['streams']
    self._video_stream = [s for s in streams if s['codec_type'] == 'video'][0]
    video_creation_time = self._video_stream['tags']['creation_time']
    try:
      self.video_creation_time = time.mktime(
          datetime.datetime.fromisoformat(video_creation_time).timetuple()
      )
    except ValueError:
      self.video_creation_time = time.mktime(
          parser.isoparse(video_creation_time).timetuple()
      )
    self.video_duration = self._video_stream['duration']
    self.video_duration_ts = self._video_stream['duration_ts']
    self.video_nb_frames = self._video_stream['nb_frames']

    self.current_frame = 0

    self.is_playing = False
    self.is_close = False
  

def single_video():
  video_file = os.path.join(_CURRENT_PATH, sys.argv[1])

  video = Video(video_file)

  output_f = open(video_file + '_out.csv', 'w')

  is_focused = True
  is_quit = False
  is_first_frame = True

  while(video.video_capture.isOpened()):
    if is_first_frame or video.is_playing:
      success, frame = video.video_capture.read()
      video.current_frame += 1

    if is_first_frame:
      output_f.write('{},{}\n'.format(
          os.path.basename(video.file_name),
          video.video_creation_time,
      ))
      is_first_frame = False

    frame = cv2.resize(frame, (800, 400))

    if success:
      cv2.imshow('Video Player', frame)
    
    pressed_button = cv2.waitKey(_PLAYSPEED) & 0xFF

    if pressed_button == ord('q'):
      is_quit = True
    elif pressed_button == ord('z'):
      is_focused = True
    elif pressed_button == ord('x'):
      is_focused = False
    elif pressed_button == ord(' '):
      video.is_playing = not video.is_playing
    
    if video.is_playing:
      output_f.write('{},{}\n'.format(video.current_frame, 1 if is_focused else 0))
    
    video.is_close = cv2.getWindowProperty('Video Player', cv2.WND_PROP_VISIBLE) < 1
    if is_quit or video.is_close:
      break
    
  video.video_capture.release()


def manual_videos():
  file_1 = os.path.join(_CURRENT_PATH, sys.argv[1])
  file_2 = os.path.join(_CURRENT_PATH, sys.argv[2])

  video_1 = Video(file_1)
  video_2 = Video(file_2)

  output_f = open(file_1 + '_out.csv', 'w')

  is_record = False
  is_focused = True
  is_quit = False
  is_first_frame = True

  while(video_1.video_capture.isOpened() and video_2.video_capture.isOpened()):
    if is_first_frame or video_1.is_playing:
      success_1, frame_1 = video_1.video_capture.read()
      video_1.current_frame += 1
    if is_first_frame or video_2.is_playing:
      success_2, frame_2 = video_2.video_capture.read()
      video_2.current_frame += 1

    if is_first_frame:
      output_f.write('{},{},{},{}\n'.format(
          os.path.basename(video_1.file_name),
          video_1.video_creation_time,
          os.path.basename(video_2.file_name),
          video_2.video_creation_time,
      ))
      is_first_frame = False

    frame_2 = cv2.resize(frame_2, (800, 400))
    frame_1 = cv2.resize(frame_1, (800, 400))

    if success_1 and success_2:
      cv2.imshow('Video Player 1', frame_1)
      cv2.imshow('Video Player 2', frame_2)
    
    pressed_button = cv2.waitKey(_PLAYSPEED) & 0xFF

    if pressed_button == ord('q'):
      is_quit = True
    elif pressed_button == ord('r'):
      is_record = True
    elif pressed_button == ord('s'):
      is_record = False
    elif pressed_button == ord('z'):
      is_focused = True
    elif pressed_button == ord('x'):
      is_focused = False
    elif pressed_button == ord('1'):
      video_1.is_playing = not video_1.is_playing
    elif pressed_button == ord('2'):
      video_2.is_playing = not video_2.is_playing
    elif pressed_button == ord(' '):
      video_1.is_playing = not video_1.is_playing
      video_2.is_playing = not video_2.is_playing
    
    if video_1.is_playing and video_2.is_playing and is_record:
      output_f.write('{},{},{}\n'.format(video_1.current_frame, video_2.current_frame, 1 if is_focused else 0))
    
    video_1.is_close = cv2.getWindowProperty('Video Player 1', cv2.WND_PROP_VISIBLE) < 1
    video_2.is_close = cv2.getWindowProperty('Video Player 2', cv2.WND_PROP_VISIBLE) < 1
    if is_quit or video_1.is_close or video_2.is_close:
      break
    
  video_1.video_capture.release()
  video_2.video_capture.release()


if __name__ == '__main__':
  if len(sys.argv) >= 3:
    manual_videos()
  else:
    single_video()
