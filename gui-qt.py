#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
PyQT GUI for pathfinder
"""

import sys
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QWidget, QAction
from PyQt5.QtWidgets import QMainWindow, QMenu

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

        openAct = QAction("Open", self)
        fileMenu.addAction(openAct)

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
