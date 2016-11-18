from PyQt4 import QtGui, QtCore
import numpy as np
import cv2


class SliderWidget(QtGui.QWidget):
    def __init__(self):
        super(SliderWidget, self).__init__()

        self.initUI()

    def initUI(self):
        self.setMinimumSize(100, 30)
        # self.value = 75
        # self.num = [75, 150, 225, 300, 375, 450, 525, 600, 675]

    def setAverages(self, averages):
        self.averages = averages
        self.update()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

    def drawWidget(self, qp):
        #font = QtGui.QFont('Serif', 7, QtGui.QFont.Light)
        #qp.setFont(font)

        size = self.size()
        w = size.width()
        h = size.height()

        qp.setPen(QtGui.QColor(0, 0, 0))
        qp.setBrush(QtGui.QColor(255, 255, 255))
        qp.drawRect(0, 0, w-1, h-1)

        qp.setPen(QtGui.QPen)
        qp.setBrush(QtGui.QColor(30, 255, 30))
        qp.drawRect(0, 0, w - 1, h - 1)


        if self.curimage is not None:
            assert(isinstance(self.curimage, QtGui.QImage))
            offx = (w - self.curimage.width()) // 2
            offy = (h - self.curimage.height()) // 2
            qp.drawImage(QtCore.QPointF(offx, offy), self.curimage)
            # qp.drawImage(QtCore.QRectF(0, 0, w, h), self.curimage)

