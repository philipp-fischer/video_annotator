import os
import sys
from PyQt4 import QtGui, QtCore
from image_widget import ImageWidget
from slider_widget import SliderWidget
from video import Video
from ranges import Ranges
import json


class VideoAnnotator(QtGui.QWidget):
    def __init__(self):
        super(VideoAnnotator, self).__init__()

        self.vid = Video(r'O:\WinTV\Recording\Robin_Hood_20160110_2015.ts')
        # self.vid.compute_averages(1000)
        self.vid.compute_averages(50)

        self.pic = None
        self.sld = None
        self.sld2 = None

        self.ranges = None

        # Number of distinct viewable video positions (slider granularity)
        self.num_positions = 50000

        self.initUI()

    def initUI(self):
        vbox = QtGui.QVBoxLayout()

        # Create the widget that displays the video frame
        self.pic = ImageWidget()
        self.pic.setImage(self.vid.get_frame(0.0))

        # A horizontal slider to scroll through the video
        self.sld = QtGui.QSlider(QtCore.Qt.Horizontal)
        # self.sld.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld.setRange(0, self.num_positions)
        self.sld.setValue(100)
        self.sld.valueChanged[int].connect(self.change_slider_value)

        # A special widget that displays the marked ranges and average frame colors
        # (Is also called slider, because it should later take over the role of the conventional slider)
        self.sld2 = SliderWidget()
        self.sld2.setAverages(self.vid.get_averages())

        # sample_ranges = {
        #     'ads': [[195799/239854, 215379/239854], [10000/239854]],
        #     'previews': [[1000/239854, 5000/239854]]
        # }
        # print(sample_ranges)
        # self.sld2.setRanges(sample_ranges, )

        # The ranges class manages the marked video ranges and sends them to the widget when changed
        self.ranges = Ranges(update_function=self.sld2.setRanges)
        self.load_or_save_ranges(save=False)

        # Put everything together and show it
        vbox.addWidget(self.pic)
        vbox.addWidget(self.sld)
        vbox.addWidget(self.sld2)

        self.setLayout(vbox)
        self.setWindowTitle('Video Annotator')
        self.show()

    def current_position(self, slider_value=None):
        if slider_value is None:
            return self.sld.value() / self.num_positions
        else:
            return slider_value / self.num_positions

    def change_slider_value(self, value):
        self.pic.setImage(self.vid.get_frame(self.current_position(value)))

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
        elif e.key() == QtCore.Qt.Key_Backspace:
            self.ranges.remove_last_element()
        elif e.key() == QtCore.Qt.Key_A:
            self.ranges.add_range_start('ad', self.current_position())
        elif e.key() == QtCore.Qt.Key_Q:
            self.ranges.add_range_start('preview', self.current_position())
        elif e.key() == QtCore.Qt.Key_D:
            self.ranges.add_range_end(self.current_position())

    def load_or_save_ranges(self, save=False):
        filename = os.path.splitext(self.vid.get_filename())[0] + '_annotation.txt'
        if save:
            with open(filename, 'w') as f:
                json.dump(self.ranges.get_ranges(), f)
        else:
            if os.path.isfile(filename):
                with open(filename, 'r') as f:
                    range_data = json.load(f)
                    self.ranges.set_ranges(range_data)


    def closeEvent(self, e):
        self.load_or_save_ranges(save=True)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    va = VideoAnnotator()
    sys.exit(app.exec_())
