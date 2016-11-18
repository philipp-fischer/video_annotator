from PyQt4 import QtGui, QtCore
import numpy as np
import cv2


class SliderWidget(QtGui.QWidget):
    def __init__(self):
        super(SliderWidget, self).__init__()

        self.averages = None
        self.initUI()

    def initUI(self):
        self.setMinimumSize(100, 50)
        self.setMaximumHeight(50)

    def setAverages(self, averages):
        h, w = tuple(averages.shape[:2])
        self.averages = QtGui.QImage(averages.data, w, h, QtGui.QImage.Format_RGB888)
        self.averages.ndarray = averages

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
        qp.setBrush(QtGui.QColor(0, 0, 0))
        qp.drawRect(0, 0, w-1, h-1)

        if self.averages is not None:
            qp.drawImage(QtCore.QRectF(1, 1, w - 1, h // 2), self.averages)


