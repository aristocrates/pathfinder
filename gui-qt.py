#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
PyQT GUI for pathfinder

Written with reference to http://zetcode.com/gui/pyqt5
"""

import sys
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QWidget, QAction
from PyQt5.QtWidgets import QMainWindow, QMenu
from PyQt5.QtSvg import QSvgWidget

class CenteredWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.resize(667, 500)
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

    def open_map(self):
        pass

    def open_path_data(self):
        pass

    def save(self):
        pass

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
