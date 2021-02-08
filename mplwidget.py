from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QSizePolicy, QHBoxLayout, QVBoxLayout

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from mpl_toolkits.mplot3d import Axes3D

# Ensure using PyQt5 backend
import matplotlib
matplotlib.use('QT5Agg')


class MplCanvas(Canvas):
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        Canvas.__init__(self, self.fig)
        Canvas.updateGeometry(self)
        Canvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        Canvas.updateGeometry(self)


class MplPlotWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.vbl = QtWidgets.QVBoxLayout()         # Set box for plotting
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)
        self.keepFigSquare = False
        self.widthScaleFactor = 0
        self.canvas.draw()
        
    def setsquare(self, square):
        self.keepFigSquare = square

    def setWidthScaleFactor(self, factor):
        self.widthScaleFactor = factor

    def resizeEvent(self, event):
        # Create a square base size of 10x10 and scale it to the new size
        # maintaining aspect ratio.
        if self.keepFigSquare: 
            new_size = QtCore.QSize(10, 10)
            new_size.scale(event.size(), QtCore.Qt.KeepAspectRatio)
            self.resize(new_size)

        if self.widthScaleFactor != 0:
            new_size = QtCore.QSize(10, 10 - 10 * self.widthScaleFactor)
            new_size.scale(event.size(), QtCore.Qt.KeepAspectRatio)
            self.resize(new_size)



class MplCanvas3D(Canvas):
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.fig.subplots_adjust(left=0.01, bottom=0.01, right=1.05, top=1.05)
        Canvas.__init__(self, self.fig)
        Canvas.updateGeometry(self)
        Canvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        Canvas.updateGeometry(self)


class MplPlotWidget3D(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.canvas = MplCanvas3D()
        # self.navToolbar = MyNavigationToolbar(self, self.canvas)
        self.vbl = QtWidgets.QVBoxLayout()         # Set box for plotting
        self.vbl.addWidget(self.canvas)
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)
        self.keepFigSquare = False
        self.widthScaleFactor = 0
        self.canvas.draw()
    
        
    def setsquare(self, square):
        self.keepFigSquare = square

    def setWidthScaleFactor(self, factor):
        self.widthScaleFactor = factor

    def resizeEvent(self, event):
        # Create a square base size of 10x10 and scale it to the new size
        # maintaining aspect ratio.
        if self.keepFigSquare: 
            new_size = QtCore.QSize(10, 10)
            new_size.scale(event.size(), QtCore.Qt.KeepAspectRatio)
            self.resize(new_size)

        if self.widthScaleFactor != 0:
            new_size = QtCore.QSize(10, 10 - 10 * self.widthScaleFactor)
            new_size.scale(event.size(), QtCore.Qt.KeepAspectRatio)
            self.resize(new_size)




class MyNavigationToolbar(NavigationToolbar) :
    def __init__(self, parent, canvas, direction = 'h' ) :

        self.canvas = canvas
        QWidget.__init__( self, parent )

        if direction=='h' :
            self.layout = QHBoxLayout( self )
        else :
            self.layout = QVBoxLayout( self )

        # self.layout.setMargin( 2 )
        # self.layout.setSpacing( 0 )

        NavigationToolbar.__init__(self, self, self.canvas, self)


    def set_message( self, s ):
        pass
