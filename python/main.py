import sys
from PyQt4 import QtGui, QtCore
from image_widget import ImageWidget
from video import Video

class Communicate(QtCore.QObject):
    updateBW = QtCore.pyqtSignal(int)


class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()

        self.vid = Video(r'U:\Projects\_smalltests\toystory.mp4')
        self.vid.compute_averages(3)

        self.initUI()


    def initUI(self):
        vbox = QtGui.QVBoxLayout()

        # pic = QtGui.QLabel()
        # pic.setPixmap(QtGui.QPixmap(r"C:\Users\fischph\Pictures\vms-sorter.png"))
        # pic.setFrameStyle(1)

        self.pic = ImageWidget()
        self.pic.setImage(self.vid.get_frame(0.5))

        self.sld = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.sld.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld.setRange(0, 10000)
        self.sld.setValue(100)
        self.sld.valueChanged[int].connect(self.changeValue)


        vbox.addWidget(self.pic)
        vbox.addWidget(self.sld)

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
