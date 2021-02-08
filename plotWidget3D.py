from matplotlib.pyplot import axes
import pyqtgraph.opengl as gl
import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5 import QtCore
import numpy as np
import OpenGL.GL as ogl


class PlotWidget3D(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.hLayout = QHBoxLayout()
        self.setLayout(self.hLayout)
        self.plot = gl.GLViewWidget()
        self.hLayout.addWidget(self.plot)


        self.axis = Custom3DAxis(self.plot, color=(0.5,0.5,10.5,0.6))
        self.createAxis()

        ## create three grids, add each to the view
        self.xgrid = gl.GLGridItem()
        self.ygrid = gl.GLGridItem()
        self.zgrid = gl.GLGridItem()
        self.xgrid.rotate(90, 0, 1, 0)
        self.ygrid.rotate(90, 1, 0, 0)
        self.translateGrid(-10)
        self.plot.addItem(self.xgrid)
        self.plot.addItem(self.ygrid)
        self.plot.addItem(self.zgrid)

        self.plot.setCameraPosition(distance=40)


    def createAxis(self):
        self.axis.add_labels()
        self.plot.addItem(self.axis)

    def createGrid(self, factor):
        self.xgrid = gl.GLGridItem()
        self.ygrid = gl.GLGridItem()
        self.zgrid = gl.GLGridItem()
        self.rotateGrid()
        self.scaleGrid(factor)
        self.translateGrid(-factor)
        self.plot.addItem(self.xgrid)
        self.plot.addItem(self.ygrid)
        self.plot.addItem(self.zgrid)
    
    def scaleGrid(self, factor):
        self.xgrid.scale(factor, factor, factor)
        self.ygrid.scale(factor, factor, factor)
        self.zgrid.scale(factor, factor, factor)

    def rotateGrid(self):
        self.xgrid.rotate(90, 0, 1, 0)
        self.ygrid.rotate(90, 1, 0, 0)

    def translateGrid(self, factor):
        self.xgrid.translate(factor, 0, 0)
        self.ygrid.translate(0, factor, 0)
        self.zgrid.translate(0, 0, factor)

    
    def scaleAxis(self, factor):
        self.axis.setSize(x=factor, y=factor, z=factor)


    def clear(self):
        self.plot.clear()





class CustomTextItem(gl.GLGraphicsItem.GLGraphicsItem):
    def __init__(self, X, Y, Z, text):
        gl.GLGraphicsItem.GLGraphicsItem.__init__(self)
        self.text = text
        self.X = X
        self.Y = Y
        self.Z = Z

    def setGLViewWidget(self, GLViewWidget):
        self.GLViewWidget = GLViewWidget

    def setText(self, text):
        self.text = text
        self.update()

    def setX(self, X):
        self.X = X
        self.update()

    def setY(self, Y):
        self.Y = Y
        self.update()

    def setZ(self, Z):
        self.Z = Z
        self.update()

    def paint(self):
        self.GLViewWidget.qglColor(QtCore.Qt.white)
        self.GLViewWidget.renderText(self.X, self.Y, self.Z, self.text)


class Custom3DAxis(gl.GLAxisItem):
    """Class defined to extend 'gl.GLAxisItem'."""
    def __init__(self, parent, color=(0,0,0,.6)):
        gl.GLAxisItem.__init__(self)
        self.parent = parent
        self.c = color

    def add_labels(self):
        """Adds axes labels."""
        x,y,z = self.size()
        #X label
        self.xLabel = CustomTextItem(X=x, Y=-y/20, Z=-z/20, text="X")
        self.xLabel.setGLViewWidget(self.parent)
        self.parent.addItem(self.xLabel)
        #Y label
        self.yLabel = CustomTextItem(X=-x/20, Y=y, Z=-z/20, text="Y")
        self.yLabel.setGLViewWidget(self.parent)
        self.parent.addItem(self.yLabel)
        #Z label
        self.zLabel = CustomTextItem(X=-x/20, Y=-y/20, Z=z, text="Z")
        self.zLabel.setGLViewWidget(self.parent)
        self.parent.addItem(self.zLabel)

    def add_tick_values(self, xticks=[], yticks=[], zticks=[]):
        """Adds ticks values."""
        x,y,z = self.size()
        xtpos = np.linspace(0, x, len(xticks))
        ytpos = np.linspace(0, y, len(yticks))
        ztpos = np.linspace(0, z, len(zticks))
        #X label
        for i, xt in enumerate(xticks):
            val = CustomTextItem(X=xtpos[i], Y=-y/20, Z=-z/20, text=str(xt))
            val.setGLViewWidget(self.parent)
            self.parent.addItem(val)
        #Y label
        for i, yt in enumerate(yticks):
            val = CustomTextItem(X=-x/20, Y=ytpos[i], Z=-z/20, text=str(yt))
            val.setGLViewWidget(self.parent)
            self.parent.addItem(val)
        #Z label
        for i, zt in enumerate(zticks):
            val = CustomTextItem(X=-x/20, Y=-y/20, Z=ztpos[i], text=str(zt))
            val.setGLViewWidget(self.parent)
            self.parent.addItem(val)

    def paint(self):
        self.setupGLState()
        if self.antialias:
            ogl.glEnable(ogl.GL_LINE_SMOOTH)
            ogl.glHint(ogl.GL_LINE_SMOOTH_HINT, ogl.GL_NICEST)
        ogl.glBegin(ogl.GL_LINES)

        x,y,z = self.size()
        #Draw Z
        ogl.glColor4f(1, 0, 0, 1)
        ogl.glVertex3f(0, 0, 0)
        ogl.glVertex3f(0, 0, z)
        #Draw Y
        ogl.glColor4f(0, 1, 0, 1)
        ogl.glVertex3f(0, 0, 0)
        ogl.glVertex3f(0, y, 0)
        #Draw X
        ogl.glColor4f(0, 0, 1, 1)
        ogl.glVertex3f(0, 0, 0)
        ogl.glVertex3f(x, 0, 0)
        ogl.glEnd()
