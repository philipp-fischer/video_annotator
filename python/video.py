import sys
import cv2
import numpy as np


class Video:
    def __init__(self, filename):
        self.cap = cv2.VideoCapture(filename)
        self.framecount = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

        self.averages = []

    def get_frame(self, idx_or_floatpos):
        if isinstance(idx_or_floatpos, int):
            framenum = idx_or_floatpos
        else:
            framenum = min(int(self.framecount * idx_or_floatpos), self.framecount)

        print("Frame: ", framenum)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, framenum)
        success, image = self.cap.read()

        assert(success)
        return image

    def compute_averages(self, count):
        for idx in range(count):
            floatpos = idx / (count-1)
            frame = self.get_frame(floatpos)
            avg = np.mean(np.mean(frame, axis=0), axis=0).flatten().astype(np.uint8)  # Get RGB mean
            self.averages.append(avg)

    def get_averages(self):
        return self.averages
