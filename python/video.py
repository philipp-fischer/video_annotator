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
            framenum = min(int(self.framecount * idx_or_floatpos), self.framecount - 5)

        # print("Get Frame %d/%d" % (framenum, self.framecount))

        self.cap.set(cv2.CAP_PROP_POS_FRAMES, framenum)
        success, image = self.cap.read()

        assert success
        return image

    def compute_averages(self, count):
        averages_list = []
        print("Computing frame averages...")
        last_notify = -1
        for idx in range(count):
            floatpos = idx / (count-1)
            if int(floatpos * 10) > last_notify:
                last_notify = int(floatpos * 10)
                print("%d%%" % (floatpos*100))

            frame = self.get_frame(floatpos)
            avg = np.mean(np.mean(frame, axis=0), axis=0).flatten().astype(np.uint8)  # Get RGB mean
            averages_list.append(avg)

        # Create an RGB image (1xN pixels)
        self.averages = np.stack(averages_list).reshape((1, count, 3))[:, :, ::-1].copy()
        print("Done.")

    def get_averages(self):
        return self.averages
