#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
PyQT GUI for pathfinder

Written with reference to http://zetcode.com/gui/pyqt5
and https://github.com/baoboa/pyqt5/blob/master/examples/painting/svgviewer/svgviewer.py
"""
import sys
import PyQt5
import json

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
from grid import Grid

# qt gui elements
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QWidget, QAction
from PyQt5.QtWidgets import QMainWindow, QMenu, QVBoxLayout
from PyQt5.QtCore import QFile, QSize
from PyQt5.QtGui import QBrush, QColor, QImage, QPainter, QPixmap, QPen, QCursor
from PyQt5.QtWidgets import (QActionGroup, QFileDialog, QGraphicsItem, QGraphicsRectItem,
                             QGraphicsScene, QGraphicsView, QMessageBox)
from PyQt5.QtSvg import QSvgWidget, QGraphicsSvgItem
from PyQt5.QtOpenGL import QGL, QGLFormat, QGLWidget

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
        saveAsAct  = QAction("Save as", self)
        saveAsAct.triggered.connect(self.saveAs)
        fileMenu.addAction(saveAsAct)

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
        if not filename:
            filename, _ = QFileDialog.getOpenFileName(self, "Open SVG File",
                                                      self.currentPath,
                                                      "SVG files (*.svg *.svgz *.svg.gz)")
        if filename:
            svg_file = QFile(filename)
            if not svg_file.exists():
                QMessageBox.critical(self, "Open SVG File",
                                     "Could not open file '{}'".format(filename))
            else:
                self.view.openFile(svg_file)

                self.resize(self.view.sizeHint() + QSize(80, 80 + self.menuBar().height()))

    def open_path_data(self, filename = None):
        if not filename:
            filename, _ = QFileDialog.getOpenFileName(self, "Open path data",
                                                      self.currentPath,
                                                      "All files (*.*)")

        if filename:
            path_file = QFile(filename)
            if not path_file.exists():
                QMessageBox.critical(self, "Open path data",
                                     "Could not open file '{}'".format(filename))
            else:
                pass

    def save(self, filename = None):
        self.view.svgItem.save(filename)

    def saveAs(self):
        pass

    def center(self):
        frame_geo  = self.frameGeometry()
        center_pos = QDesktopWidget().availableGeometry().center()
        frame_geo.moveCenter(center_pos)
        self.move(frame_geo.topLeft())

def fillCircle(scene, x, y, r, color):
    """
    Adds a circle into a graphics scene
    """
    return scene.addEllipse(x - r, y - r, r * 2, r * 2,
                        pen = QColor(0, 0, 0, 0), brush = color)

class MapItem(QGraphicsSvgItem):
    """
    Captures mouse events with coordinates relative to the actual map
    """
    def __init__(self, *args):
        super(MapItem, self).__init__(*args)
        self.draw_active = False
        self.r = None
        self.BLACK = QColor(0, 0, 0)
        self.BLUE  = QColor(0, 0, 255)
        self.grid_point_stack = []

    def removeItem(self, item):
        self.scene().removeItem(item)

    def setRadius(self, rad):
        self.r = rad

    def save(self, filename):
        if not filename:
            pass

        if filename:
            grid_point_data = {"enabled": self.grid.enabledPoints(),
                               "int": self.grid.enabledPointsAsInt()}
            with open(filename, "w") as f:
                json.dump(grid_point_data, f)

    def makeGrid(self, num_x, num_y, width, height):
        self.num_x = num_x
        self.num_y = num_y
        self.width = width
        self.height = height
        self.grid = Grid(self.num_x, self.num_y, self.width, self.height)

    def drawGridPoints(self, points, color):
        for p in points:
            added_ellipse = fillCircle(self.scene(), p[0], p[1], 0.2, color)
            self.grid_point_stack[-1].append(added_ellipse)

    def undoDraw(self):
        """
        Undoes all grid drawing from the last click and drag
        """
        if len(self.grid_point_stack) > 0:
            last_draw_points = self.grid_point_stack.pop()
            self.grid.disablePoints(last_draw_points)
            for point in last_draw_points:
                self.removeItem(point)

    def resetGrid(self):
        self.grid.clearEnabled()

    def mouseMoveEvent(self, event):
        if self.draw_active:
            x = event.pos().x()
            y = event.pos().y()
            pointsWithinR    = self.grid.pointsWithinRadius((x, y), self.r)
            pointsToActivate = self.grid.notEnabledIn(pointsWithinR)
            self.grid.setEnabledPoints(pointsWithinR)
            self.drawGridPoints(pointsToActivate, self.BLUE)
        super(MapItem, self).mouseMoveEvent(event)

    def mousePressEvent(self, event):
        super(MapItem, self).mousePressEvent(event)
        if event.button() == RightButton:
            self.draw_active = True
            self.grid_point_stack.append([])
            # TODO: add call to mouseMoveEvent or factor out highlighting code
            # into another function so that single clicks still add points
            event.accept()

    def mouseReleaseEvent(self, event):
        self.draw_active = False
        super(MapItem, self).mouseReleaseEvent(event)

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

        self.TRANSLUCENT_WHITE = QColor(255, 255, 255, 180)
        # Prepare background check-board pattern.
        tilePixmap = QPixmap(64, 64)
        tilePixmap.fill(Qt.white)
        tilePainter = QPainter(tilePixmap)
        color = QColor(220, 220, 220)
        tilePainter.fillRect(0, 0, 32, 32, color)
        tilePainter.fillRect(32, 32, 32, 32, color)
        tilePainter.end()

        self.setBackgroundBrush(QBrush(tilePixmap))
        self.num_x = 1000
        self.num_y = 1500

        # zoom tracker
        self.zoom = Zoom()

        # position tracker
        self.x = self.width() / 2
        self.y = self.height() / 2
        self.r = 10
        # scales when zooming
        #self.r_mult = 1

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

        self.svgItem = MapItem(svg_file.fileName())
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

        self.svgItem.setRadius(self.r)
        self.svgItem.makeGrid(self.num_x, self.num_y,
                              self.svgItem.boundingRect().width(),
                              self.svgItem.boundingRect().height())
        self.svgItem.resetGrid()

        s.setSceneRect(self.outlineItem.boundingRect().adjusted(-10, -10, 10, 10))
        self.cursor_circle = fillCircle(self.outlineItem.scene(), self.x, self.y,
                                        self.r,
                                        self.TRANSLUCENT_WHITE)

    def setHighQualityAntialiasing(self, highQualityAntialiasing):
        if QGLFormat.hasOpenGL():
            self.setRenderHint(QPainter.HighQualityAntialiasing,
                    highQualityAntialiasing)

    def removeItem(self, item):
        self.scene().removeItem(item)

    def setRadius(self, r):
        self.r = r
        self.svgItem.setRadius(r)

    def setViewBackground(self, enable):
        if self.backgroundItem:
            self.backgroundItem.setVisible(enable)

    def setViewOutline(self, enable):
        if self.outlineItem:
            self.outlineItem.setVisible(enable)

    def paintEvent(self, event):
        super(SvgView, self).paintEvent(event)
        p = QPainter(self.viewport())

    def updateCursorCircle(self):
        self.removeItem(self.cursor_circle)
        transformedPos = self.mapToScene(self.pos)
        x = transformedPos.x()
        y = transformedPos.y()
        self.cursor_circle = fillCircle(self.outlineItem.scene(), x, y,
                                        self.r,
                                        self.TRANSLUCENT_WHITE)

    def mouseMoveEvent(self, event):
        super(SvgView, self).mouseMoveEvent(event)
        self.pos = event.pos() #QCursor.pos()
        self.updateCursorCircle()

    def wheelEvent(self, event):
        self.zoom.change_scroll(event.angleDelta().y())
        factor = pow(1.1, self.zoom.zoom_delta())
        self.scale(factor, factor)
        # TODO: test floating point problems with this implementation
        # (repeatedly zoom in and out and see if it becomes inaccurate)
        #self.r_mult = self.r_mult * factor
        self.updateCursorCircle()
        event.accept()

    def keyPressEvent(self, event):
        super(SvgView, self).keyPressEvent(event)
        if event.key() == Qt.Key_Plus:
            self.setRadius(self.r * 1.2)
            self.updateCursorCircle()
        elif event.key() == Qt.Key_Minus:
            self.setRadius(self.r / 1.2)
            self.updateCursorCircle()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    center_frame = CenteredWindow()
    center_frame.show()

    sys.exit(app.exec_())
