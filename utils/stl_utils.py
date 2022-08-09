import time

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import numpy as np
from stl import mesh
from matplotlib import cm, colors
import config
from config import *
from pathlib import Path


def loadSTL(filename):
    m = mesh.Mesh.from_file(filename)
    # shape = m.points.shape
    points = m.points.reshape(-1, 3)
    faces = np.arange(points.shape[0]).reshape(-1, 3)
    return points, faces


def stl_transformation(points, transformation_matrix, axis=0):
    # points shape : (n, xyz)

    points = np.c_[points, np.ones(len(points.shape[axis]))]
    points = points.T
    # points: [4, n]
    points = np.dot(transformation_matrix, points)
    points = points[0:3, :]
    points = points.T

    return points


def mapper(value, vmin=0,vmax=1, camp=cm.jet):
    norm = colors.Normalize(vmin=vmin, vmax=vmax, clip=True)
    mapper = cm.ScalarMappable(norm=norm, cmap=camp)
    return mapper.to_rgba(value)

# def color_code_value(value, value_min=0, value_max=1, color_min_hex=config.color_code_min_hex,
#                      color_max_hex=config.color_code_max_hex):
#     # R G B
#     color_min_dec = int(color_min_hex, 16)
#     color_max_dec = int(color_max_hex, 16)
#     offset = (color_max_dec - color_min_dec) * (value - value_min) / (value_max - value_min) + color_min_dec
#     color_code_dec = round(offset + color_max_dec)
#     color_code_hex = hex(color_code_dec)
#     R = int(color_code_hex[2:4], 16)  # '0xRRGGBB'
#     G = int(color_code_hex[4:6], 16)
#     B = int(color_code_hex[6:8], 16)
#     return R, G, B
