import sys
from PyQt4 import QtGui, QtCore
from image_widget import ImageWidget
from slider_widget import SliderWidget
from video import Video

class Communicate(QtCore.QObject):
    updateBW = QtCore.pyqtSignal(int)


class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()

        self.vid = Video(r'U:\Projects\_smalltests\toystory.mp4')
        self.vid.compute_averages(100)

        self.pic = None
        self.sld = None
        self.sld2 = None

        self.initUI()

    def initUI(self):
        vbox = QtGui.QVBoxLayout()

        self.pic = ImageWidget()
        self.pic.setImage(self.vid.get_frame(0.0))

        self.sld = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.sld.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld.setRange(0, 10000)
        self.sld.setValue(100)
        self.sld.valueChanged[int].connect(self.changeValue)

        self.sld2 = SliderWidget()
        self.sld2.setAverages(self.vid.get_averages())

        vbox.addWidget(self.pic)
        vbox.addWidget(self.sld)
        vbox.addWidget(self.sld2)

        self.setLayout(vbox)
        self.setWindowTitle('Video Annotator')
        self.show()

    def changeValue(self, value):
        self.pic.setImage(self.vid.get_frame(value / 10000))


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
