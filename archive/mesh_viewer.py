import time

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import numpy as np
from stl import mesh
import sys
import os
from PyQt5 import QtWidgets
from config import coil_stl_file
# Press the green button in the gutter to run the script.
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QLabel, QSystemTrayIcon, QMenu
from PyQt5.QtCore import Qt, QFile, QTextStream, QSettings

from pathlib import Path
# from matrix import trans_matrix


class MainWindow(QMainWindow):
    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.setGeometry(0, 0, 700, 900)
        self.setAcceptDrops(True)
        self.initUI()
        self.targetSTL = None

        self.coilSTL = None

        self.lastDir = None
        self.droppedFilename = None

        # self.coil_position_timer
        # self.emg_timer =

    def initUI(self):
        centerWidget = QWidget()
        self.setCentralWidget(centerWidget)

        layout = QVBoxLayout()
        centerWidget.setLayout(layout)

        self.viewer = gl.GLViewWidget()
        layout.addWidget(self.viewer, 1)

        self.viewer.setWindowTitle('STL Viewer')
        self.viewer.setCameraPosition(distance=100)

        g = gl.GLGridItem()
        g.setSize(200, 200)
        g.setSpacing(50, 50)
        self.viewer.addItem(g)

        btn = QPushButton(text="Load STL")
        btn.clicked.connect(self.showDialog)
        btn.setFont(QFont("Ricty Diminished", 14))
        layout.addWidget(btn)

    def showDialog(self):
        directory = Path("")
        if self.lastDir:
            directory = self.lastDir
        fname = QFileDialog.getOpenFileName(self, "Open file", str(directory), "STL (*.stl)")
        if fname[0]:
            self.showSTL(fname[0])
            self.lastDir = Path(fname[0]).parent

    def showSTL(self, filename):

        #############################
        if self.targetSTL:
            self.viewer.removeItem(self.targetSTL)
        self.points, self.faces = self.loadSTL(filename)
        self.meshdata = gl.MeshData(vertexes=self.points, faces=self.faces)
        self.targetSTL = gl.GLMeshItem(meshdata=self.meshdata, smooth=True, drawFaces=True, drawEdges=True, edgeColor=(0, 0, 0, 1))

        self.viewer.addItem(self.targetSTL)

        # self.color_timer.start()
        # self.add_coil_location()

    def add_coil_location(self, transformation_matrix=None):

        coil_stl = 'data/cube.stl'
        coil_points, coil_faces = self.loadSTL(coil_stl)
        coil_points = coil_points * 0.1
        transfer_points = coil_points.T
        transfer_points = np.c_[transfer_points, np.ones(36)]
        transfer_points = np.dot()

        coil_meshdata = gl.MeshData(vertexes=coil_points, faces=coil_faces)
        coilSTL = gl.GLMeshItem(meshdata=coil_meshdata)
        self.viewer.addItem(coilSTL)
        ###################################

    def loadSTL(self, filename):
        m = mesh.Mesh.from_file(filename)
        shape = m.points.shape
        points = m.points.reshape(-1, 3)
        faces = np.arange(points.shape[0]).reshape(-1, 3)
        return points, faces

    def dragEnterEvent(self, e):
        print("enter")
        mimeData = e.mimeData()
        mimeList = mimeData.formats()
        filename = None

        if "text/uri-list" in mimeList:
            filename = mimeData.data("text/uri-list")
            filename = str(filename, encoding="utf-8")
            filename = filename.replace("file:///", "").replace("\r\n", "").replace("%20", " ")
            filename = Path(filename)

        if filename.exists() and filename.suffix == ".stl":
            e.accept()
            self.droppedFilename = filename
        else:
            e.ignore()
            self.droppedFilename = None

    def dropEvent(self, e):
        if self.droppedFilename:
            self.showSTL(self.droppedFilename)

    # def update_face_color(self):
    #     # pass
    #     start_time = time.time()
    #     new_color = np.random.uniform(low=0, high=1, size=(self.faces.shape[0], 3))
    #     new_color = np.append(new_color, np.ones(shape=(self.faces.shape[0], 1)), axis=-1)
    #     self.meshdata.setFaceColors(new_color)
    #     self.currentSTL.meshDataChanged()
    #     finish_time = time.time()
    #     print(finish_time - start_time)
        # current_mesh = gl.GLMeshItem(meshdata=self.meshdata, smooth=True, drawFaces=True, drawEdges=True, edgeColor=(0, 1, 0, 1))
        # self.viewer.addItem(current_mesh)
        # self.currentSTL = current_mesh
    def load_coils(self):
        pass
        # self.coilSTL =



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(app=app)
    window.show()
    app.exec_()
