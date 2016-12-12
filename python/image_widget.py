from PyQt4 import QtGui, QtCore
import numpy as np
import cv2


class ImageWidget(QtGui.QWidget):
    def __init__(self):
        super(ImageWidget, self).__init__()

        self.curimage = None
        self.initUI()

    def initUI(self):
        self.setMinimumSize(100, 100)

    def setImage(self, image):
        # w = 300
        # h = 300
        # total = np.zeros((h, w, 4), np.uint8)
        # total[100:105, :, :] = 255
        total = image[:, :, ::-1].copy()
        w = image.shape[1]
        h = image.shape[0]

        # cv2.imwrite('out.png', total)

        self.setMinimumSize(w, h)

        self.curimage = QtGui.QImage(total.data, w, h, QtGui.QImage.Format_RGB888)
        self.curimage.ndarray = total
        self.update()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

    def drawWidget(self, qp):
        size = self.size()
        w = size.width()
        h = size.height()

        qp.setPen(QtGui.QColor(0, 0, 0))
        qp.setBrush(QtGui.QColor(30, 30, 30))
        qp.drawRect(0, 0, w-1, h-1)

        if self.curimage is not None:
            assert(isinstance(self.curimage, QtGui.QImage))
            offx = (w - self.curimage.width()) // 2
            offy = (h - self.curimage.height()) // 2
            qp.drawImage(QtCore.QPointF(offx, offy), self.curimage)
            # qp.drawImage(QtCore.QRectF(0, 0, w, h), self.curimage)
        else:
            text = "Drop video here"
            qp.setFont(QtGui.QFont("Arial", 14))
            fm = QtGui.QFontMetrics(qp.font())
            pixelsWide = fm.width(text)
            qp.setPen(QtGui.QColor(255, 255, 255))
            qp.drawText((w-pixelsWide)//2, (h+fm.height())//2, text)
