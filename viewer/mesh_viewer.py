import copy
import random

import pyqtgraph.opengl as gl

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import numpy as np
from stl import mesh
import sys
from PyQt5 import QtWidgets
# Press the green button in the gutter to run the script.
from PyQt5.QtCore import QTimer
from pathlib import Path
# from matrix import trans_matrix
from archive.STLModel import STLModel
import pickle
import scipy.io
from utils.stl_utils import loadSTL, mapper


class MainWindow(QMainWindow):
    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.setGeometry(0, 0, 700, 900)
        self.setAcceptDrops(True)

        self.initUI()

        self.stl_model = STLModel()
        self.coils = []
        self.lastDir = None
        self.droppedFilename = None
        self.load_coil_model()

        self.coil = STLModel()

        self.coil_stream_timer = QTimer()
        # self.inference_timer.setInterval(0.2)  # for 5 KHz refresh rate


        self.emg_stream = QTimer()
        self.tms_stream = QTimer()



    def initUI(self):
        centerWidget = QWidget()
        self.setCentralWidget(centerWidget)

        layout = QVBoxLayout()
        centerWidget.setLayout(layout)

        self.viewer = gl.GLViewWidget()
        layout.addWidget(self.viewer, 1)

        self.viewer.setWindowTitle('STL Viewer')
        self.viewer.setCameraPosition(distance=150)

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
        self.stl_model.set_all(color=(130/225, 129/225, 70/225, 1),stl_file_path=filename, view_widget=self.viewer, drawEdges=False)

    def load_coil(self):
        coil_mat = scipy.io.loadmat('../data/coil_positions/coil_mat.mat')
        self.coil.set_points_faces(coil_mat['P'], coil_mat['t'] - 1)

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

    def load_coil_model(self):

        coil_pos = scipy.io.loadmat('../data/coil_positions/coil_mat.mat')
        points, faces = loadSTL(filename='../stl_models/sphere_coil.stl')
        coil_model = STLModel()
        with open('../data/coil_positions/aapo_tms.pickle', 'rb') as fp:
            trans_matrices = pickle.load(fp)
        with open('../data/evoked_response/aapo_evoked_responses.pickle', 'rb') as fp:
            evoked_responses = pickle.load(fp)

        for evoked_response, trans_matrix in zip(evoked_responses, trans_matrices.values()):
            coil_model.set_points_faces(coil_pos['P'], coil_pos['t']-1)
            coil_model.set_view_widget(self.viewer)

            ######### generate random
            pick_range = evoked_response['evoked_response'][:, 200:300]
            rgba = mapper(value=np.max(pick_range)-np.min(pick_range), vmax=400, vmin=0)
            #########
            coil_model.create_mesh_data(drawEdges=False, color=rgba) # R G B
            coil_model.transform(trans_matrix, local=False)
            coil_model.scale(10, 10, 10, local=True)
            coil_model.set_stl()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(app=app)
    window.show()
    app.exec_()
