from threading import Thread

import cv2

from src import NerdyConstants

"""USB camera stream class for optimized FPS modified by tedfoodlin"""
__author__ = "pyimagesearch @http://www.pyimagesearch.com/"


class WebcamVideoStream:
    def __init__(self, src=-1):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        # adjust camera settings
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, NerdyConstants.FRAME_X)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, NerdyConstants.FRAME_Y)
        self.stream.set(cv2.CAP_PROP_EXPOSURE, -8.0)

        (self.grabbed, self.frame) = self.stream.read()

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True