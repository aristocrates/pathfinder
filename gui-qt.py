#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
PyQT GUI for pathfinder

Written with reference to http://zetcode.com/gui/pyqt5
and https://github.com/baoboa/pyqt5/blob/master/examples/painting/svgviewer/svgviewer.py
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

from scroll import Zoom

# qt gui elements
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QWidget, QAction
from PyQt5.QtWidgets import QMainWindow, QMenu, QVBoxLayout
from PyQt5.QtCore import QFile, QSize
from PyQt5.QtGui import QBrush, QColor, QImage, QPainter, QPixmap, QPen
from PyQt5.QtWidgets import (QActionGroup, QFileDialog, QGraphicsItem, QGraphicsRectItem,
                             QGraphicsScene, QGraphicsView, QMessageBox)
from PyQt5.QtSvg import QSvgWidget, QGraphicsSvgItem
from PyQt5.QtOpenGL import QGL, QGLFormat, QGLWidget
from svgpathtools import svg2paths

class CenteredWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.center()
        self.setWindowTitle('Pathfinder Editor')

        self.currentPath = ''

        menubar  = self.menuBar()
        fileMenu = menubar.addMenu('File')

        openMenu   = QMenu("Open", self)
        openMapAct = QAction("Map", self)
        openMapAct.setStatusTip("Open background map")
        openMapAct.triggered.connect(self.open_map_image)
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

        self.view = SvgView()

        self.setCentralWidget(self.view)

        self.open_map_image('Caltech_Map.svg')

    def open_map_image(self, filename = None):
        """
        Taken from PyQt5 svgviewer.py example (see license.txt)
        """
        print("Ran open map image")
        if not filename:
            filename, _ = QFileDialog.getOpenFileName(self, "Open SVG File",
                                                      self.currentPath,
                                                      "SVG files (*.svg, *.svgz, *.svg.gz)")

        print(filename)

        if filename:
            svg_file = QFile(filename)
            if not svg_file.exists():
                QMessageBox.critical(self, "Open SVG File",
                                     "Could not open file '{}'".format(filename))
            else:
                self.view.openFile(svg_file)

                self.resize(self.view.sizeHint() + QSize(80, 80 + self.menuBar().height()))

    def open_path_data(self):
        pass

    def save(self):
        pass

    def center(self):
        frame_geo  = self.frameGeometry()
        center_pos = QDesktopWidget().availableGeometry().center()
        frame_geo.moveCenter(center_pos)
        self.move(frame_geo.topLeft())

class SvgView(QGraphicsView):
    """
    SVG display taken from the PyQt5 examples (see license.txt)
    """
    Native, OpenGL, Image = range(3)

    def __init__(self, parent=None):
        super(SvgView, self).__init__(parent)

        self.renderer = SvgView.Native
        self.svgItem = None
        self.backgroundItem = None
        self.outlineItem = None
        self.image = QImage()

        self.setScene(QGraphicsScene(self))
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        # Prepare background check-board pattern.
        tilePixmap = QPixmap(64, 64)
        tilePixmap.fill(Qt.white)
        tilePainter = QPainter(tilePixmap)
        color = QColor(220, 220, 220)
        tilePainter.fillRect(0, 0, 32, 32, color)
        tilePainter.fillRect(32, 32, 32, 32, color)
        tilePainter.end()

        self.setBackgroundBrush(QBrush(tilePixmap))

        # zoom tracker
        self.zoom = Zoom()

    def drawBackground(self, p, rect):
        p.save()
        p.resetTransform()
        p.drawTiledPixmap(self.viewport().rect(),
                self.backgroundBrush().texture())
        p.restore()

    def openFile(self, svg_file):
        if not svg_file.exists():
            return

        s = self.scene()

        if self.backgroundItem:
            drawBackground = self.backgroundItem.isVisible()
        else:
            drawBackground = False

        if self.outlineItem:
            drawOutline = self.outlineItem.isVisible()
        else:
            drawOutline = True

        s.clear()
        self.resetTransform()

        self.svgItem = QGraphicsSvgItem(svg_file.fileName())
        self.svgItem.setFlags(QGraphicsItem.ItemClipsToShape)
        self.svgItem.setCacheMode(QGraphicsItem.NoCache)
        self.svgItem.setZValue(0)

        self.backgroundItem = QGraphicsRectItem(self.svgItem.boundingRect())
        self.backgroundItem.setBrush(Qt.white)
        self.backgroundItem.setPen(QPen(Qt.NoPen))
        self.backgroundItem.setVisible(drawBackground)
        self.backgroundItem.setZValue(-1)

        self.outlineItem = QGraphicsRectItem(self.svgItem.boundingRect())
        outline = QPen(Qt.black, 2, Qt.DashLine)
        outline.setCosmetic(True)
        self.outlineItem.setPen(outline)
        self.outlineItem.setBrush(QBrush(Qt.NoBrush))
        self.outlineItem.setVisible(drawOutline)
        self.outlineItem.setZValue(1)

        s.addItem(self.backgroundItem)
        s.addItem(self.svgItem)
        s.addItem(self.outlineItem)

        s.setSceneRect(self.outlineItem.boundingRect().adjusted(-10, -10, 10, 10))

    def setHighQualityAntialiasing(self, highQualityAntialiasing):
        if QGLFormat.hasOpenGL():
            self.setRenderHint(QPainter.HighQualityAntialiasing,
                    highQualityAntialiasing)

    def setViewBackground(self, enable):
        if self.backgroundItem:
            self.backgroundItem.setVisible(enable)

    def setViewOutline(self, enable):
        if self.outlineItem:
            self.outlineItem.setVisible(enable)

    def paintEvent(self, event):
        if self.renderer == SvgView.Image:
            if self.image.size() != self.viewport().size():
                self.image = QImage(self.viewport().size(),
                        QImage.Format_ARGB32_Premultiplied)

            imagePainter = QPainter(self.image)
            QGraphicsView.render(self, imagePainter)
            imagePainter.end()

            p = QPainter(self.viewport())
            p.drawImage(0, 0, self.image)
        else:
            super(SvgView, self).paintEvent(event)

    def mouseMoveEvent(self, event):
        super(SvgView, self).mouseMoveEvent(event)

    def mousePressEvent(self, event):
        super(SvgView, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        super(SvgView, self).mouseReleaseEvent(event)

    def wheelEvent(self, event):
        self.zoom.change_scroll(event.angleDelta().y())
        factor = pow(1.1, self.zoom.zoom_delta())
        self.scale(factor, factor)
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    center_frame = CenteredWindow()
    center_frame.show()

    sys.exit(app.exec_())
