from PyQt4 import QtGui, QtCore
import numpy as np
import cv2


class SliderWidget(QtGui.QWidget):
    def __init__(self):
        super(SliderWidget, self).__init__()

        self.averages = None
        self.ranges = None
        self.initUI()

    def initUI(self):
        self.setMinimumSize(100, 50)
        self.setMaximumHeight(50)

    def setAverages(self, averages):
        h, w = tuple(averages.shape[:2])
        self.averages = QtGui.QImage(averages.data, w, h, QtGui.QImage.Format_RGB888)
        self.averages.ndarray = averages

        self.update()

    def setRanges(self, ranges):
        self.ranges = ranges
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
            qp.drawImage(QtCore.QRectF(1, 1, w - 2, h // 2), self.averages)

        if self.ranges is not None:
            qp.setPen(QtCore.Qt.NoPen)
            qp.setBrush(QtGui.QColor(150, 0, 0))

            assert(isinstance(self.ranges, list))

            for range in self.ranges:
                k = range[0]
                if k == 'ad':
                    qp.setBrush(QtGui.QColor(200, 20, 20))
                elif k == 'preview':
                    qp.setBrush(QtGui.QColor(20, 200, 20))
                else:
                    qp.setBrush(QtGui.QColor(150, 150, 150))

                rect_from = range[1] * (w - 1)
                if len(range) > 2:
                    rect_to = range[2] * (w - 1)
                    qp.drawRect(rect_from, h // 2 + 1, rect_to-rect_from, h // 2 - 2)
                else:
                    y1 = h // 2 + 1
                    y2 = h - 2
                    y_mid = (y1+y2) // 2
                    qp.drawConvexPolygon(QtGui.QPolygon([QtCore.QPoint(rect_from, y1),
                                          QtCore.QPoint(rect_from, y2),
                                          QtCore.QPoint(rect_from + 10, y_mid)]))
                    # qp.drawRect(rect_from, h // 2 + 1, rect_to - rect_from, h // 2 - 2)

