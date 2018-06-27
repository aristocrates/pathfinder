#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
PyQT GUI for pathfinder

Written with reference to http://zetcode.com/gui/pyqt5
"""

import sys
import PyQt5

# events
from PyQt5.QtCore import QEvent
MouseMove           = QEvent.MouseMove
MouseButtonPress    = QEvent.MouseButtonPress
MouseButtonRelease  = QEvent.MouseButtonRelease
MouseButtonDblClick = QEvent.MouseButtonDblClick
from PyQt5.QtCore import Qt
LeftButton  = Qt.LeftButton
RightButton = Qt.RightButton

from PyQt5.QtWidgets import QApplication, QDesktopWidget, QWidget, QAction
from PyQt5.QtWidgets import QMainWindow, QMenu, QVBoxLayout
from PyQt5.QtSvg import QSvgWidget
from svgpathtools import svg2paths
class CenteredWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.center()
        self.setWindowTitle('Center')

        menubar  = self.menuBar()
        fileMenu = menubar.addMenu('File')

        openMenu   = QMenu("Open", self)
        openMapAct = QAction("Map", self)
        openMapAct.setStatusTip("Open background map")
        openMapAct.triggered.connect(self.open_map)
        openMenu.addAction(openMapAct)
        openDatAct = QAction("Data", self)
        openDatAct.setStatusTip("Open path data file")
        openDatAct.triggered.connect(self.open_path_data)
        openMenu.addAction(openDatAct)
        fileMenu.addMenu(openMenu)

        saveAct    = QAction("Save", self)
        saveAct.triggered.connect(self.save)
        fileMenu.addAction(saveAct)

        exitAct    = QAction("Exit", self)
        exitAct.triggered.connect(self.close)
        fileMenu.addAction(exitAct)

        svgMap     = QSvgWidget('Caltech_Map.svg')
        svgMap.setGeometry(50, 50, 759, 668)
        self.setCentralWidget(svgMap)

        paths, attributes = svg2paths('Caltech_Map.svg')
        xmin, xmax, ymin, ymax = paths[0].bbox()
        self.resize((xmax - xmin) / 1.25, (ymax - ymin) / 1.25)

        # self.graphicsView = PyQt5.QtWidgets.QGraphicsView()
        # self.graphicsView.setMouseTracking(True)
        svgMap.setMouseTracking(True)
        svgMap.installEventFilter(self)
        #self.graphicsView.viewport().installEventFilter(self)

    def open_map(self):
        pass

    def open_path_data(self):
        pass

    def save(self):
        pass

    # hash storing all mouse events
    mouse_events = [MouseMove, MouseButtonPress, MouseButtonRelease,
                    MouseButtonDblClick]
    mouse_buttons = [LeftButton, RightButton]
    def eventFilter(self, source, event):
        """
        Written with reference to https://stackoverflow.com/questions/35992088/why-mousemoveevent-does-nothing-in-pyqt5
        """
        print(event.type())
        # if event.type() == PyQt5.QtCore.QEvent.MouseMove:
        #     print("Mouse Move")
        # elif event.type() == PyQt5.QtCore.QEvent.MouseButtonPress:
        #     if event.buttons() == PyQt5.QtCore.Qt.LeftButton:
        #         print("Left press")
        #     elif event.buttons() == PyQt5.QtCore.Qt.RightButton:
        #         print("Right press")
        # elif event.type() == PyQt5.QtCore.QEvent.MouseButtonRelease:
        #     if event.buttons() == PyQt5.QtCore.Qt.LeftButton:
        #         print("Left release")
        #     elif event.buttons() == PyQt5.QtCore.Qt.RightButton:
        #         print("Right release")
        # elif event.type() == PyQt5.QtCore.QEvent.MouseButtonDblClick:
        #     print("Double click")
        return super(QMainWindow, self).eventFilter(source, event)

    # def mouseMoveEvent(self, event):
    #     print("Mouse move event")

    # def mousePressEvent(self, event):
    #     if event.button() == PyQt5.QtCore.Qt.LeftButton:
    #         print("Left press")
    #     elif event.button() == PyQt5.QtCore.Qt.RightButton:
    #         print("Right press")

    def center(self):
        frame_geo  = self.frameGeometry()
        center_pos = QDesktopWidget().availableGeometry().center()
        frame_geo.moveCenter(center_pos)
        self.move(frame_geo.topLeft())

if __name__ == "__main__":
    app = QApplication(sys.argv)

    center_frame = CenteredWindow()
    center_frame.show()

    sys.exit(app.exec_())
