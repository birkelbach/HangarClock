#!/usr/bin/env python3

#  Copyright (c) 2020 Phil Birkelbach
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import time

class Clock(QWidget):
    def __init__(self, parent=None):
        super(Clock, self).__init__(parent)
        self.font = QFont("DSEG7 Classic Mini")
        self.fontSize = 30
        self.margin = 20
        self.color = QColor(Qt.red)
        self.gmt = False
        self.seconds = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

    def getTime(self):
        if self.gmt:
            now = time.gmtime()
        else:
            now = time.localtime()
        if self.seconds:
            return time.strftime("%H:%M:%S", now)
        else:
            return time.strftime("%H:%M", now)

    def resizeEvent(self, event):
        # Starting place for font size
        #self.font.setPixelSize(self.height())
        self.font.setPixelSize(self.fontSize)
        # qm = QFontMetrics(self.font)
        # # Allowed width
        # # aw = self.width() - self.margin * 2
        # aw = self.width()
        # # # If it's too wide then resize it
        # while qm.width(self.getTime(), -1) >= aw:
        #     self.font.setPixelSize(self.font.pixelSize() * 0.9)
        #     qm = QFontMetrics(self.font)


    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        pen = QPen()
        pen.setWidth(1)
        pen.setCapStyle(Qt.FlatCap)
        p.setPen(pen)

        # Draw Value
        pen.setColor(self.color)
        p.setPen(pen)
        p.setFont(self.font)
        p.drawText(QRectF(self.rect()), self.getTime(), QTextOption(Qt.AlignCenter))
        #p.drawRect(0,0,self.width(), self.height())


class Main(QMainWindow):
    def __init__(self, config, parent=None):
        super(Main, self).__init__(parent)

        self.setObjectName("Hangar Clock")
        #mainWindow.showFullScreen()
        self.showMaximized()
        self.w = QWidget(self)
        self.w.setStyleSheet("QWidget { background: black; }")
        # w.setGeometry(0, 0, self.screenWidth, self.screenHeight)
        self.setCentralWidget(self.w)
        self.vout = QVBoxLayout(self.w)
        self.htop = QHBoxLayout()
        self.vout.addLayout(self.htop)
        self.vleft = QVBoxLayout()
        self.vright = QVBoxLayout()
        self.htop.addLayout(self.vleft)
        self.htop.addLayout(self.vright)

        self.fixedFont = QFont("FreeMono", 30, QFont.Bold)

        self.label1 = QLabel()
        self.label1.setStyleSheet("background-color: rgba(255,255,255,0%)")
        self.label1.setFont(self.fixedFont)
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setText(time.strftime("%Z"))
        self.vleft.addWidget(self.label1)

        self.label2 = QLabel()
        self.label2.setStyleSheet("background-color: rgba(255,255,255,0%)")
        self.label2.setFont(self.fixedFont)
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setText(time.strftime("GMT"))
        self.vright.addWidget(self.label2)

        self.clock1 = Clock()
        self.clock1.fontSize = 250
        self.vleft.addWidget(self.clock1)

        self.clock2 = Clock()
        self.clock2.color = QColor(Qt.green)
        self.clock2.fontSize = 250
        self.clock2.gmt = True
        self.vright.addWidget(self.clock2)

        self.metarFont = QFont("FreeMono", 70, QFont.Bold)

        self.labelMetar = QLabel()
        self.labelMetar.setStyleSheet("background-color: rgba(255,255,255,0%)")
        self.labelMetar.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.labelMetar.setFont(self.metarFont)
        self.labelMetar.setAlignment(Qt.AlignCenter)
        self.labelMetar.setWordWrap(True)
        self.labelMetar.setText("KCLL 091753Z 17008KT 7SM -RA OVC020 20/18 A3022 RMK AO2 SLP231 P0002 60002 T02000178 10200 20183 50006")
        self.vout.addWidget(self.labelMetar)

        self.spacerItemLeft = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.vleft.addItem(self.spacerItemLeft)

        self.spacerItemRight = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.vright.addItem(self.spacerItemRight)



def main():
    app = QApplication(sys.argv)
    mainWindow = Main({})
    # Main program loop
    result = app.exec_()

if __name__ == "__main__":
    main()
