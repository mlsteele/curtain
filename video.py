from curtain import Curtain, Canvas
import cv
import time


videos = ['videos/viz.mp4', 'videos/trippy.mp4', 'videos/ripples.mp4']
offset_x = 100
offset_y = 100
time_step = 0.0333
brightness = 0.05

if __name__ == '__main__':
    curtain = Curtain()
    canvas = Canvas()
    cv_videos = map(cv.CaptureFromFile, videos)
    current_video = 0
    current_time = 0
    while 1:
        canvas.clear(0, 0, 0)
        frame_image = cv.QueryFrame(cv_videos[current_video])
        if frame_image is not None:
            for x in xrange(0, 15):
                for y in xrange(0, 5):
                    px = frame_image[offset_x+(x*8), offset_y+(y*8)]
                    canvas.draw_pixel(x, y, (px[2]/255.0)*brightness, (px[1]/255.0)*brightness, (px[0]/255.0)*brightness)
        else:
            cv_videos[current_video] = cv.CaptureFromFile(videos[current_video])
        curtain.send_color_dict(canvas)
        if current_time > 15:
            current_time = 0
            current_video += 1
            current_video = current_video % len(videos)
        time.sleep(time_step)
        current_time += time_step
    sys.exit()
