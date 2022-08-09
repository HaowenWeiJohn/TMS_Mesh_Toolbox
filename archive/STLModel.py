import time

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import numpy as np
from stl import mesh
from utils.stl_utils import *
from pathlib import Path


class STLModel:
    def __init__(self, stl_file_path=None, view_widget=None):
        self.stl_file_path = stl_file_path
        self.view_widget = view_widget
        self.points = None
        self.faces = None
        self.mesh_data = None
        self.stl_model = None
        self.stl_in_viewer = False

    def load_stl(self):
        if self.stl_file_path:
            self.points, self.faces = loadSTL(self.stl_file_path)
        else:
            print('file path is not specified')

    def set_view_widget(self, view_widget: gl.GLViewWidget):
        self.view_widget = view_widget

    def set_stl_file_path(self, stl_file_path):
        self.stl_file_path = stl_file_path

    def create_mesh_data(self, color=(1, 1, 1, 1), smooth=True, drawFaces=True, drawEdges=True, edgeColor=(0, 0, 0, 1)):
        self.mesh_data = gl.MeshData(vertexes=self.points, faces=self.faces)
        self.stl_model = gl.GLMeshItem(meshdata=self.mesh_data, color=color, smooth=smooth, drawFaces=drawFaces,
                                       drawEdges=drawEdges,
                                       edgeColor=edgeColor)
        # 'color': (1., 1., 1., 1.),
        # 'drawEdges': False,
        # 'drawFaces': True,
        # 'edgeColor': (0.5, 0.5, 0.5, 1.0),
        # 'shader': None,
        # 'smooth': True,
        # 'computeNormals': True,

    # def init_mesh_data(self, smooth=True, drawFaces=True, drawEdges=True, edgeColor=(0, 0, 0, 1)):
    #     mesh_data = gl.MeshData(vertexes=self.points, faces=self.faces)
    #     stl_model = gl.GLMeshItem(meshdata=self.mesh_data, smooth=smooth, drawFaces=drawFaces, drawEdges=drawEdges,
    #                                    edgeColor=edgeColor)
    #     return stl_model

    def set_stl(self):
        if self.view_widget and self.stl_model:
            self.view_widget.addItem(self.stl_model)

    def transform(self, transform_matrix, local=True):
        tr = QMatrix4x4(transform_matrix.flatten())
        self.stl_model.applyTransform(tr=tr, local=local)

    def scale(self, dx, dy, dz, local=False):
        self.stl_model.scale(x=dx, y=dy, z=dz, local=local)

    def set_points_faces(self, points, faces):
        self.points = points
        self.faces = faces

    def remove_stl(self):
        if self.view_widget and self.stl_model:  # gl.GLViewWidget
            self.view_widget.removeItem(self.stl_model)

    def set_all(self, stl_file_path, view_widget, color=(1, 1, 1, 1), remove_previous_model=True, smooth=True,
                drawFaces=True,
                drawEdges=True, edgeColor=(0, 0, 0, 1)):
        if remove_previous_model:
            self.remove_stl()

        self.set_stl_file_path(stl_file_path)
        self.set_view_widget(view_widget)
        self.load_stl()
        self.create_mesh_data(color=color, smooth=smooth, drawFaces=drawFaces, drawEdges=drawEdges, edgeColor=edgeColor)
        self.set_stl()
