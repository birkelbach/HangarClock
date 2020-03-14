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
import urllib.request

class Clock(QLabel):
    def __init__(self, parent=None):
        super(Clock, self).__init__(parent)
        self.gmt = False
        self.seconds = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.setTime)
        self.timer.start(1000)
        self.setTime()

    def setTime(self):
        if self.gmt:
            now = time.gmtime()
        else:
            now = time.localtime()
        if self.seconds:
            self.setText(time.strftime("%H:%M:%S", now))
        else:
            self.setText(time.strftime("%H:%M", now))

class DateLabel(QLabel):
    def __init__(self, parent=None):
        super(DateLabel, self).__init__(parent)

        self.timer = QTimer()
        self.timer.timeout.connect(self.setDate)
        self.timer.start(1000)
        self.setDate()

    def setDate(self):
        self.setText(time.strftime("%B %d, %Y"))

class MetarList(QLabel):
    def __init__(self, station_list, timeout = 10000, parent=None):
        super(MetarList, self).__init__(parent)
        self.stations = []
        for station in station_list:
            d = {}
            d["id"] = station
            d["text"] = self.getMetar(station)
            d["updated"] = time.time()
            self.stations.append(d)

        self.timer = QTimer()
        self.timer.timeout.connect(self.setNext)
        self.timer.start(timeout)
        self.nextIndex = 0
        self.setNext()

    def getMetar(self, id):
        link = "https://tgftp.nws.noaa.gov/data/observations/metar/stations/{}.TXT".format(id)
        f = urllib.request.urlopen(link)
        lines = f.readlines()
        return lines[1].decode()

    def setNext(self):
        self.setText(self.stations[self.nextIndex]["text"])
        self.nextIndex += 1
        if self.nextIndex == len(self.stations):
            self.nextIndex = 0
        now = time.time()
        if now - self.stations[self.nextIndex]["updated"] > 300:
            self.stations[self.nextIndex]["text"] = self.getMetar(self.stations[self.nextIndex]["id"])
            self.stations[self.nextIndex]["updated"] = now


class Main(QMainWindow):
    def __init__(self, config, parent=None):
        super(Main, self).__init__(parent)

        self.setObjectName("Hangar Clock")
        #self.showFullScreen()
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

        self.fixedFont = QFont("FreeMono", 60, QFont.Bold)

        self.label1 = QLabel()
        self.label1.setStyleSheet("background-color: rgba(255,255,255,0%); color : white;")
        self.label1.setFont(self.fixedFont)
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setText(time.strftime("%Z"))
        self.vleft.addWidget(self.label1)

        self.label2 = QLabel()
        self.label2.setStyleSheet("background-color: rgba(255,255,255,0%); color : white;")
        self.label2.setFont(self.fixedFont)
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setText(time.strftime("GMT"))
        self.vright.addWidget(self.label2)


        self.clockFont = QFont("DSEG7 Classic Mini", 200, QFont.Bold)

        self.clock1 = Clock()
        self.clock1.setStyleSheet("QLabel { background-color : rgba(255,255,255,0%); color : red; }")
        self.clock1.setFont(self.clockFont)
        self.vleft.addWidget(self.clock1)

        self.clock2 = Clock()
        self.clock2.color = QColor(Qt.green)
        self.clock2.setStyleSheet("QLabel { background-color : rgba(255,255,255,0%); color : green; }")
        self.clock2.setFont(self.clockFont)
        self.clock2.gmt = True
        self.vright.addWidget(self.clock2)

        self.monthFont = QFont("FreeMono", 100, QFont.Bold)

        self.labelDate = DateLabel()
        self.labelDate.setStyleSheet("background-color: rgba(255,255,255,0%); color : blue;")
        self.labelDate.setFont(self.monthFont)
        self.labelDate.setAlignment(Qt.AlignCenter)
        self.labelDate.setText(time.strftime("%B %d, %Y"))
        self.vout.addWidget(self.labelDate)
        self.spacerItemMonth = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.vout.addItem(self.spacerItemMonth)

        self.metarFont = QFont("FreeMono", 70, QFont.Bold)

        self.metar = MetarList(["KDWH", "KCLL", "KIAH", "KHOU", "KTME", "KDTO"])
        self.metar.setStyleSheet("background-color: rgba(255,255,255,0%; color : white;)")
        self.metar.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.metar.setFont(self.metarFont)
        self.metar.setAlignment(Qt.AlignCenter)
        self.metar.setWordWrap(True)
        self.vout.addWidget(self.metar)

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
