##### Standard Lib Imports #######
import configparser
import sys
import os
import numpy as np
import threading
import math

###### Style Imports #######
import qdarkstyle
import qdarkgraystyle
import qtmodern.styles

###### Project Imports ########
from src.MohrCirclePropogator import MohrCirclePropogator as mcp
from src.MohrCirclePropogator import MohrCircle3DValues as mc3dVals
import pyqtcss
from Forms.engCalcUI import Ui_MainWindow
from src.planetary_data import planetaryData as plDat
from src.OrbitPropagator import OrbitPropogator as OP
from src.VectorCoesConverter import Vector2CoesConverter
from src.CoordinateTransforms import CoordinateTransforms
from src.CoesToState import CoesToStateVectors
from src.General import OrbitalElements


##### QT Imports  ############# 
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QColorDialog
import PyQt5

###### MatPlotLib Imports #########
import matplotlib as mpl
mpl.use('QT5Agg')
import matplotlib.pyplot as plt
import pyqtgraph.opengl as gl







plt.rcParams.update({
    "lines.color": "white",
    "patch.edgecolor": "white",
    "text.color": "black",
    "axes.facecolor": "white",
    "axes.edgecolor": "lightgray",
    "axes.labelcolor": "white",
    "xtick.color": "white",
    "ytick.color": "white",
    "grid.color": "lightgray",
    "figure.facecolor": "#5C5C5C",
    "figure.edgecolor": "black",
    "savefig.facecolor": "black",
    "savefig.edgecolor": "black"})


###### Global Vars ######
restart = False
highResScreen = False
EXIT_CODE_REBOOT = -11231351
theme = None
CONFIG_FILE_DIR = os.path.join("Resources", "config.ini")


class Ui(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        global theme
        global EXIT_CODE_REBOOT
        global CONFIG_FILE_DIR
        self.EXIT_CODE_REBOOT = EXIT_CODE_REBOOT
        self.plotLineWidth = 15
        self.scatterPlotPointSize = 60
        self.theme = theme
        self.configFileDir = CONFIG_FILE_DIR
        self.currentOrbitNames = []
        self.currentOrbits = {}
        self.orbitPropogatorThread = threading.Thread()
        self.finished = False
        self.timer = QtCore.QTimer()
        self.counter = 0
        self.trajectoryColor = (1, 1, 1, 1)
        self.tleColor = (1, 1, 1, 1)

        self.setupUi(self)
        # uic.loadUi(os.path.join("Forms", "engCalcForm.ui"), self)
        self.show()
        
        self.calculate3DMohrCircle

        self.calculateGradeButton.clicked.connect(self.calculateGrade)
        self.clearGradeEdits.clicked.connect(self.clearGradeCalculator)
        self.interpolateButton.clicked.connect(self.interpolate)
        self.clearInterpolateEditsButton.clicked.connect(self.clearInterpolateEdits)
        self.calculateMohrCircleBtn.clicked.connect(self.calculateMohrCircleBtn_clicked)
        self.calculate3DMohrCircleBtn.clicked.connect(self.calculate3DMohrCircle)
        self.actionToggle_4K_Screen_Parameter.triggered.connect(self.on_actionToggle_4K_Screen_Parameter)
        self.actionNoColorTheme.triggered.connect(self.on_actionNoColorTheme)
        self.actionClassic_Dark.triggered.connect(self.on_actionClassicDark)
        self.actionDark_Blue.triggered.connect(self.on_actionDarkBlue)
        self.actionDark_Orange.triggered.connect(self.on_actionDarkOarnge)
        self.actionDark_Yellow.triggered.connect(self.on_actionDarkYellow)
        self.actionDark_Black.triggered.connect(self.on_actionDarkBlack)
        self.actionDark_GrayGreen.triggered.connect(self.on_actionDarkGrayGreen)
        self.initializeOrbitParamsBtn.clicked.connect(self.initializeOrbitParams)
        self.propogateOrbitBtn.clicked.connect(self.propogateOrbit)
        self.addOrbitBtn.clicked.connect(self.addOrbit)
        self.orbitListViewRemoveBtn.clicked.connect(self.removeOrbit)
        self.orbitListViewClearBtn.clicked.connect(self.clearOrbits)
        self.propogateMultOrbitsBtn.clicked.connect(self.propogateMultipleOrbits)
        self.planetaryBodyComboBox.currentTextChanged.connect(self.updateCelestialBodyRadius)
        self.enterPVBtn.clicked.connect(self.change2PVTab)
        self.enterCoeBtn.clicked.connect(self.change2CoeTab)
        self.initializePvVectorsBtn.clicked.connect(self.initializePvVectorsFromCoes)
        self.orbitColorBtn.clicked.connect(self.getColor)
        self.convertVectorCoesBtn.clicked.connect(self.vectorCoesConverter)
        self.transformOrbitVectorsBtn.clicked.connect(self.transformOrbitVectors)


        self.initializePlots()
        self.planetaryBodyComboBox.addItems(plDat.getAvailableBodies())
        self.vecCoesConverterCombobx.addItems(plDat.getAvailableBodies())
        frames = CoordinateTransforms.validFrames
        frames.append("Manually Input Matrix Values")
        self.transformMatrixComboBx.addItems(frames)
        self.orbitPBar.setValue(0)




    def getColor(self):
        color = QColorDialog.getColor()
        newcolors = []
        for colors in color.getRgb():
            newcolors.append(round(colors/255, 1))

        self.trajectoryColor = tuple(newcolors)


    def change2PVTab(self):
        self.orbitParmStacked.setCurrentIndex(0)


    def change2CoeTab(self):
        self.orbitParmStacked.setCurrentIndex(1)


    def initializePlots(self):
        self.linearStressPlot.setsquare(True)
        self.chart.setsquare(True)
        self.mohrCirclePlot3D.setsquare(True)
        # self.orbitPlot.setsquare(True)

        self.mohrCirclePlot3D.canvas.ax.set_facecolor("#C4C4C4")
        self.mohrCirclePlot3D.canvas.ax.grid()
        self.mohrCirclePlot3D.canvas.ax.grid(b=True, which='major', color='black', linewidth=1)
        self.mohrCirclePlot3D.canvas.ax.grid(b=True, which='minor', color='black', linewidth=0.1)
        self.mohrCirclePlot3D.canvas.ax.get_yaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
        self.mohrCirclePlot3D.canvas.ax.get_xaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())

        self.chart.canvas.ax.set_facecolor("#C4C4C4")
        self.chart.canvas.ax.grid(b=True, which='major', color='black', linewidth=0.6)
        self.chart.canvas.ax.grid(b=True, which='minor', color='black', linewidth=0.1)
        self.chart.canvas.ax.get_yaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
        self.chart.canvas.ax.get_xaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())

        self.linearStressPlot.canvas.ax.set_facecolor("#C4C4C4")
        self.linearStressPlot.canvas.ax.grid()
        self.linearStressPlot.canvas.ax.grid(b=True, which='major', color='black', linewidth=1)
        self.linearStressPlot.canvas.ax.grid(b=True, which='minor', color='black', linewidth=0.1)
        self.linearStressPlot.canvas.ax.get_yaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
        self.linearStressPlot.canvas.ax.get_xaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())


    def calculateGrade(self):
        totalWeight = 0
        totalPoints = 0
        overallGrade = 0

        if  self.gradeEdit1.text() and self.gradeWeightEdit1.text():
            totalPoints = float(self.gradeEdit1.text()) * float(self.gradeWeightEdit1.text())
            totalWeight = float(self.gradeWeightEdit1.text())

        if  self.gradeEdit2.text() and self.gradeWeightEdit2.text():
            totalPoints = totalPoints + float(self.gradeEdit2.text()) * float(self.gradeWeightEdit2.text())
            totalWeight = totalWeight + float(self.gradeWeightEdit2.text())

        if  self.gradeEdit3.text() and self.gradeWeightEdit3.text():
            totalPoints = totalPoints + float(self.gradeEdit3.text()) * float(self.gradeWeightEdit3.text())
            totalWeight = totalWeight + float(self.gradeWeightEdit3.text())

        if  self.gradeEdit4.text() and self.gradeWeightEdit4.text():
            totalPoints = totalPoints + float(self.gradeEdit4.text()) * float(self.gradeWeightEdit4.text())
            totalWeight = totalWeight + float(self.gradeWeightEdit4.text())

        if  self.gradeEdit5.text() and self.gradeWeightEdit5.text():
            totalPoints = totalPoints + float(self.gradeEdit5.text()) * float(self.gradeWeightEdit5.text())
            totalWeight = totalWeight + float(self.gradeWeightEdit5.text())

        if  self.gradeEdit6.text() and self.gradeWeightEdit6.text():
            totalPoints = totalPoints + float(self.gradeEdit6.text()) * float(self.gradeWeightEdit6.text())
            totalWeight = totalWeight + float(self.gradeWeightEdit6.text())

        if  self.gradeEdit7.text() and self.gradeWeightEdit7.text():
            totalPoints = totalPoints + float(self.gradeEdit7.text()) * float(self.gradeWeightEdit7.text())
            totalWeight = totalWeight + float(self.gradeWeightEdit7.text())

        if  self.gradeEdit8.text() and self.gradeWeightEdit8.text():
            totalPoints = totalPoints + float(self.gradeEdit8.text()) * float(self.gradeWeightEdit8.text())
            totalWeight = totalWeight + float(self.gradeWeightEdit8.text())

        if  self.gradeEdit9.text() and self.gradeWeightEdit9.text():
            totalPoints = totalPoints + float(self.gradeEdit9.text()) * float(self.gradeWeightEdit9.text())
            totalWeight = totalWeight + float(self.gradeWeightEdit9.text())

        if  self.gradeEdit10.text() and self.gradeWeightEdit10.text():
            totalPoints = totalPoints + float(self.gradeEdit10.text()) * float(self.gradeWeightEdit10.text())
            totalWeight = totalWeight + float(self.gradeWeightEdit10.text())

        if  self.gradeEdit11.text() and self.gradeWeightEdit11.text():
            totalPoints = totalPoints + float(self.gradeEdit11.text()) * float(self.gradeWeightEdit11.text()) 
            totalWeight = totalWeight + float(self.gradeWeightEdit11.text())

        if totalWeight != 0:
            overallGrade = round(totalPoints / totalWeight, 3)
        
        self.overallGradeLabel.setText("Overall grade achieved with entered grades is: {} and a total weight of: {}".format(overallGrade, totalWeight))

        if self.neededGradeEdit.text() and totalWeight != 0:
            remainingWeight = 100 - totalWeight
            requestedGrade = float(self.neededGradeEdit.text())
            neededGrade = round((requestedGrade - (totalPoints / (100 * totalWeight)) * totalWeight) / (remainingWeight/100))
            self.neededGradeLabel.setText("Overall grade needed on remaining assignments to get a grade of, {}, is: {}".format(requestedGrade, neededGrade))

        if self.remainAssGradeEdit.text() and totalWeight != 0:
            remainingWeight = 100 - totalWeight
            remainingGrade = float(self.remainAssGradeEdit.text())
            projectedGrade = round(overallGrade / 100 * totalWeight + remainingGrade / 100 * remainingWeight, 3)
            self.remainingGradeLabel.setText("Overall grade wtih, {}, on remaining assignments is: {}".format(remainingGrade, projectedGrade))


    def clearGradeCalculator(self):
        self.gradeEdit1.clear()
        self.gradeEdit2.clear() 
        self.gradeEdit3.clear() 
        self.gradeEdit4.clear() 
        self.gradeEdit5.clear() 
        self.gradeEdit6.clear() 
        self.gradeEdit7.clear() 
        self.gradeEdit8.clear() 
        self.gradeEdit9.clear() 
        self.gradeEdit10.clear() 
        self.gradeEdit11.clear() 
        self.gradeWeightEdit1.clear()
        self.gradeWeightEdit2.clear()
        self.gradeWeightEdit3.clear()
        self.gradeWeightEdit4.clear()
        self.gradeWeightEdit5.clear()
        self.gradeWeightEdit6.clear()
        self.gradeWeightEdit7.clear()
        self.gradeWeightEdit8.clear()
        self.gradeWeightEdit9.clear()
        self.gradeWeightEdit10.clear()
        self.gradeWeightEdit11.clear()
        self.remainAssGradeEdit.clear()
        self.neededGradeEdit.clear()
        self.overallGradeLabel.setText("Overall grade achieved with entered grades is: and a total weight of: ")
        self.neededGradeLabel.setText("Overall grade needed on remaining assignments to get a grade of, , is: ")
        self.remainingGradeLabel.setText("Overall grade wtih, , on remaining assignments is: ")


    def interpolate(self):
        if self.interpolateX1Edit.text() and self.interpolateX2Edit.text() \
            and self.interpolateX3Edit.text() and self.interpolateY1Edit.text() \
            and self.interpolateY3Edit.text():

            x1 = float(self.interpolateX1Edit.text())
            x2 = float(self.interpolateX2Edit.text())
            x3 = float(self.interpolateX3Edit.text())
            y1 = float(self.interpolateY1Edit.text())
            y3 = float(self.interpolateY3Edit.text())

            y2 = ((x2 - x1)*(y3 - y1) / (x3 - x1) + y1)

            self.interpolateY2Edit.setText(str(round(y2, 4)))
            

    def clearInterpolateEdits(self):
        self.interpolateX1Edit.clear()
        self.interpolateX2Edit.clear()
        self.interpolateX3Edit.clear()
        self.interpolateY1Edit.clear()
        self.interpolateY2Edit.clear()
        self.interpolateY3Edit.clear()


    def calculateMohrCircleBtn_clicked(self):
        if self.sigmaXEdit.text():
            sigmaX = float(self.sigmaXEdit.text())
        else:
            sigmaX = 0

        if self.sigmaYEdit.text():
            sigmaY = float(self.sigmaYEdit.text())
        else:
            sigmaY = 0

        if self.tauXyEdit.text():
            tauXY = float(self.tauXyEdit.text())
        else:
            tauXY  = 0
        
        if self.thetaRealEdit.text():
            thetaReal = float(self.thetaRealEdit.text())
        else:
            thetaReal = 0

        if sigmaY == 0 and sigmaX == 0:
            print("Both Stresses cannont be zero")
            return

        mohrCirle = mcp(sigmaX, sigmaY, tauXY, thetaReal)
        # mohrCirle = mcp(5, 20, 15, 10)  # Debug to bypass typing in values
        mohrCirle.calculateMohrCircleValues()
        circle =  mohrCirle.getCicleValues()
        q1 = mohrCirle.getQ1()
        q2 = mohrCirle.getQ2()
        prinStress = mohrCirle.getPrincipalStresses()
        calcPoint = mohrCirle.getCalculatedPoint()
        maxTau = mohrCirle.getMaxTau()
        center = mohrCirle.getCenter()
        pStressPlanes = mohrCirle.getPrincipalStressPlaneAngles()
        shearStressPlanes = mohrCirle.getShearStressPlanes()
        radius = mohrCirle.getRadius()


        self.chart.canvas.ax.clear()
        self.chart.canvas.ax.set_facecolor("#C4C4C4")
        self.chart.canvas.ax.grid(b=True, which='major', color='black', linewidth=0.6)
        self.chart.canvas.ax.grid(b=True, which='minor', color='black', linewidth=0.1)
        self.chart.canvas.ax.get_yaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
        self.chart.canvas.ax.get_xaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
        self.chart.canvas.ax.plot(circle[0], circle[1], 15, color="black")
        self.chart.canvas.ax.plot([prinStress[0], prinStress[1]], [0, 0], color="black")
        self.chart.canvas.ax.plot([center, center], [maxTau, -maxTau], color="black")
        self.chart.canvas.ax.scatter(q1[0], q1[1], 60, color='blue', label="Q1")
        self.chart.canvas.ax.scatter(q2[0], q2[1], 60, color="red", label="Q2")
        self.chart.canvas.ax.scatter(prinStress[0], 0, 60, color="orange", label = "Sigma I")
        self.chart.canvas.ax.scatter(prinStress[1], 0, 60, color="purple", label = "Sigma II")
        self.chart.canvas.ax.plot([q1[0], q2[0]], [q1[1], q2[1]], color = "blue", linestyle="dashed")
        self.chart.canvas.ax.scatter(calcPoint[0], calcPoint[1], 60, color="green", label="Calculated")
        self.chart.canvas.ax.legend(loc="upper right", prop={'size':8})
        self.chart.canvas.ax.set_xlim(center - 1.2*radius, center + 1.8 * radius)
        self.chart.canvas.ax.set_ylim(maxTau + 0.4*maxTau, -maxTau - 0.4*maxTau)
        self.chart.canvas.ax.set_xlabel("Normal Stress")
        self.chart.canvas.ax.set_ylabel("Shear Stress")
        self.chart.canvas.draw()

        stressVals = mohrCirle.getNormalAndShearStressValues()
        thetaVals = mohrCirle.getThetaVals()
        thetaVals = np.degrees(np.transpose(thetaVals))

        self.linearStressPlot.canvas.ax.clear()
        self.linearStressPlot.canvas.ax.set_facecolor("#C4C4C4")
        self.linearStressPlot.canvas.ax.grid()
        self.linearStressPlot.canvas.ax.grid(b=True, which='major', color='black', linewidth=1)
        self.linearStressPlot.canvas.ax.grid(b=True, which='minor', color='black', linewidth=0.1)
        self.linearStressPlot.canvas.ax.get_yaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
        self.linearStressPlot.canvas.ax.get_xaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
        self.linearStressPlot.canvas.ax.plot(thetaVals, stressVals[0], color='Red', label="Normal Stress")
        self.linearStressPlot.canvas.ax.plot(thetaVals, stressVals[1], color='green', label="Shear Stress")
        self.linearStressPlot.canvas.ax.plot([0, 361], [0, 0], color='black', linewidth=2)
        self.linearStressPlot.canvas.ax.set_xlabel("Theta [deg]")
        self.linearStressPlot.canvas.ax.set_xlim(0, 360)
        self.linearStressPlot.canvas.ax.legend(loc="upper right", prop={'size':8})
        self.linearStressPlot.canvas.draw()

        self.sigma1Lbl.setText(str(round(prinStress[0], 4)))
        self.sigma11Lbl.setText(str(round(prinStress[1], 4)))
        self.maxTauLbl.setText(str(round(maxTau, 4)))
        self.q1Lbl.setText(str(q1))
        self.q2Lbl.setText(str(q2))
        self.maxPrinStressPlaneLbl.setText(str(round(pStressPlanes[0], 4)))
        self.minPrinStressPlaneLbl.setText(str(round(pStressPlanes[1], 4)))
        self.maxShearStressPlaneLbl.setText(str(round(shearStressPlanes[0], 4)))
        self.minShearStressPlaneLbl.setText(str(round(shearStressPlanes[1], 4)))
        self.sigmaLbl.setText(str(round(calcPoint[0], 4)))
        self.tauLbl.setText(str(round(calcPoint[1], 4)))


    def calculate3DMohrCircle(self):
        # Calculates 3D Mohr Circle
        vals = mc3dVals

        if self.sigmaX3dEdit.text():
            vals.sigmaX = float(self.sigmaX3dEdit.text())
        else:
            vals.sigmaX = 0
        
        if self.sigmaY3dEdit.text():
            vals.sigmaY = float(self.sigmaY3dEdit.text())
        else:
            vals.sigmaY = 0

        if self.sigmaZ3dEdit.text():
            vals.sigmaZ = float(self.sigmaZ3dEdit.text())
        else:
            vals.sigmaZ = 0

        if self.tauxy3dEdit.text():
            vals.tauXY = float(self.tauxy3dEdit.text())
        else:
            vals.tauXY = 0
        
        if self.tauxz3dEdit.text():
            vals.tauXZ = float(self.tauxz3dEdit.text())
        else:
            vals.tauXZ = 0

        if self.tauyz3dEdit.text():
            vals.tauYZ = float(self.tauyz3dEdit.text())
        else:
            vals.tauYZ = 0

        # Some Debugs to bypass entry boxes
        # vals.sigmaX = 30
        # vals.sigmaY = 40
        # vals.sigmaZ = 50
        # vals.tauXY = 40
        # vals.tauXZ = 40
        # vals.tauYZ = 40
        
        # Null vals in constructor TODO: change constructor setup
        circle3d = mcp(1, 1, 1, 1)
        vals = circle3d.calculateMohrCircle3D(vals)

        self.mohrCirclePlot3D.canvas.ax.clear()
        self.mohrCirclePlot3D.canvas.ax.set_facecolor("#C4C4C4")
        self.mohrCirclePlot3D.canvas.ax.grid()
        self.mohrCirclePlot3D.canvas.ax.grid(b=True, which='major', color='black', linewidth=1)
        self.mohrCirclePlot3D.canvas.ax.grid(b=True, which='minor', color='black', linewidth=0.1)
        self.mohrCirclePlot3D.canvas.ax.get_yaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
        self.mohrCirclePlot3D.canvas.ax.get_xaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
        self.mohrCirclePlot3D.canvas.ax.plot(vals.circle1X, vals.circle1Y, self.plotLineWidth, color='red')
        self.mohrCirclePlot3D.canvas.ax.plot(vals.circle2X, vals.circle2Y, self.plotLineWidth, color='blue')
        self.mohrCirclePlot3D.canvas.ax.plot(vals.circle3X, vals.circle3Y, self.plotLineWidth, color='green')
        self.mohrCirclePlot3D.canvas.ax.scatter(vals.sigmaI, 0, self.scatterPlotPointSize, color='yellow', label="SigmaI")
        self.mohrCirclePlot3D.canvas.ax.scatter(vals.sigmaII, 0, self.scatterPlotPointSize, color='black', label="SigmaII")
        self.mohrCirclePlot3D.canvas.ax.scatter(vals.sigmaIII, 0, self.scatterPlotPointSize, color='brown', label="SigmaIII")
        self.mohrCirclePlot3D.canvas.ax.scatter(vals.C1, vals.maxTau1, self.scatterPlotPointSize, color="red", marker="*", label="Max TauI")
        self.mohrCirclePlot3D.canvas.ax.scatter(vals.C2, vals.maxTau2, self.scatterPlotPointSize, color="blue", marker="*", label="Max TauII")
        self.mohrCirclePlot3D.canvas.ax.scatter(vals.C3, vals.maxTau3, self.scatterPlotPointSize, color="green", marker="*", label="Max TauIII")
        self.mohrCirclePlot3D.canvas.ax.plot([vals.sigmaIII, vals.sigmaI], [0, 0], self.plotLineWidth, color="black", linewidth=2)
        self.mohrCirclePlot3D.canvas.ax.legend(loc='upper right', prop={'size':9})
        self.mohrCirclePlot3D.canvas.ax.set_xlabel("Normal Stress")
        self.mohrCirclePlot3D.canvas.ax.set_ylabel("Shear Stress")
        # self.mohrCirclePlot3D.canvas.ax.set_xlim(vals.sigmaIII - abs(vals.sigmaIII*0.1), vals.sigmaI * 1.2)

        # Set the on screen labels
        self.sigmaI3dLbl.setText(str(round(vals.sigmaI,4)))
        self.sigmaII3dLbl.setText(str(round(vals.sigmaII,4)))
        self.sigmaIII3dLbl.setText(str(round(vals.sigmaIII,4)))
        self.maxTauI3dLbl.setText(str(round(vals.maxTau1,4)))
        self.maxTauII3dLbl.setText(str(round(vals.maxTau2,4)))
        self.maxTauIII3dLbl.setText(str(round(vals.maxTau3,4)))
        self.vm3dLbl.setText(str(round(vals.vonMissesStress, 4)))
        self.hydrostaticStress3D.setText(str(round(vals.hydrostaticStress, 5)))

        self.mohrCirclePlot3D.canvas.draw()


    def on_actionNoColorTheme(self):
        self.theme = "none"
        self.writeThemeConfig()

    
    def on_actionClassicDark(self):
        self.theme = "Classic Dark"
        self.writeThemeConfig()


    def on_actionDarkBlue(self):
        self.theme = "Dark Blue"
        self.writeThemeConfig()


    def on_actionDarkOarnge(self):
        self.theme = "Dark Orange"
        self.writeThemeConfig()


    def on_actionDarkYellow(self):
        self.theme = "Dark Yellow"
        self.writeThemeConfig()

    
    def on_actionDarkBlack(self):
        self.theme = "Dark Black"
        self.writeThemeConfig()


    def on_actionDarkGrayGreen(self):
        self.theme = "Dark GrayGreen"
        self.writeThemeConfig()

    
    def writeThemeConfig(self):

        with open(self.configFileDir, "r") as configFile:
            config = configparser.ConfigParser()
            config.read_file(configFile)

        config.set("Screen_Settings", "theme", self.theme)

        with open(self.configFileDir, "w") as configFile2:
            config.write(configFile2)

        self.shutdown(self.EXIT_CODE_REBOOT)


    def on_actionToggle_4K_Screen_Parameter(self):

        with open(self.configFileDir, "r") as configFile:
            config = configparser.ConfigParser()
            config.read_file(configFile)


        if config.getboolean("Screen_Settings", "4k_Resolution"):
            config.set("Screen_Settings", "4k_Resolution", "False")
        else:
            config.set("Screen_Settings", "4k_Resolution", "True")

        
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Manual Restart Required for QT DPI Change!")
        msgBox.setWindowTitle("Program Shutdown Requested")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        returnValue = msgBox.exec()

        if returnValue == QMessageBox.Ok:
            with open(self.configFileDir, "w") as configFile2:
                config.write(configFile2)

            self.shutdown(120)


    def shutdown(self, exitCode):
        return QtCore.QCoreApplication.exit(exitCode)



    def initializeOrbitParams(self):
        body = self.planetaryBodyComboBox.currentText()
        cb = plDat.Earth

        if body == "Sun":
            cb = plDat.Sun

        rmag = cb.radius + 1000
        vmag = np.sqrt(cb.mu / rmag)

        self.orbitInitP1Edit.setText(str(round(rmag, 5)))
        self.orbitInitP2Edit.setText(str(round(rmag * 0.1, 5)))
        self.orbitInitP3Edit.setText(str(round(rmag * -0.5, 5)))
        self.orbitInitV1Edit.setText(str(0))
        self.orbitInitV2Edit.setText(str(round(vmag, 5)))
        self.orbitInitV3Edit.setText(str(round(vmag * 0.8, 5)))


    def removeOrbit(self):
        orbits = self.orbitListViewEdit.selectedItems()
        for orbit in orbits:
            self.currentOrbitNames.remove(orbit.text())
            self.currentOrbits.pop(orbit.text(), None)
        
        self.orbitListViewEdit.clear()
        self.orbitListViewEdit.addItems(self.currentOrbitNames)
    

    def clearOrbits(self):
        self.orbitListViewEdit.clear()
        self.currentOrbitNames.clear()
        self.currentOrbits.clear()


    def addOrbit(self):
        if not self.orbitInitP1Edit.text() or \
            not self.orbitInitP2Edit.text() or \
            not self.orbitInitP3Edit.text():
            return

        if not self.orbitInitV1Edit.text() or \
            not self.orbitInitV2Edit.text() or \
            not self.orbitInitV3Edit.text():
            return
        
        if not self.orbitTimeEdit.text(): return
        if not self.orbitTimeStepEdit.text(): return
        if not self.orbitNameEdit.text(): return

        if self.planetaryBodyComboBox.currentText() not in plDat.bodyList: return

        r1 = float(self.orbitInitP1Edit.text())
        r2 = float(self.orbitInitP2Edit.text())
        r3 = float(self.orbitInitP3Edit.text())

        v1 = float(self.orbitInitV1Edit.text())
        v2 = float(self.orbitInitV2Edit.text())
        v3 = float(self.orbitInitV3Edit.text())

        r0 = [r1, r2, r3]
        v0 = [v1, v2, v3]

        cb = plDat.Earth
        body = self.planetaryBodyComboBox.currentText()

        if body == "Sun":
            cb = plDat.Sun
        
        timeStep = float(self.orbitTimeStepEdit.text())
        time = float(self.orbitTimeEdit.text()) * 3600

        params = OrbitParams
        params.rVec = r0
        params.vVec = v0
        params.timelength = time
        params.timeStep = timeStep
        params.color = self.trajectoryColor
        params.cb = cb
        op = OP(params)

        name = self.orbitNameEdit.text()
        self.currentOrbitNames.append(name)
        self.orbitListViewEdit.addItem(name)
        self.currentOrbits[name] = op
        


    def propogateOrbit(self):
        if not self.orbitInitP1Edit.text() or \
            not self.orbitInitP2Edit.text() or \
            not self.orbitInitP3Edit.text():
            return

        if not self.orbitInitV1Edit.text() or \
            not self.orbitInitV2Edit.text() or \
            not self.orbitInitV3Edit.text():
            return
        
        if not self.orbitTimeEdit.text(): return
        if not self.orbitTimeStepEdit.text(): return

        if self.planetaryBodyComboBox.currentText() not in plDat.bodyList: return


        r1 = float(self.orbitInitP1Edit.text())
        r2 = float(self.orbitInitP2Edit.text())
        r3 = float(self.orbitInitP3Edit.text())

        v1 = float(self.orbitInitV1Edit.text())
        v2 = float(self.orbitInitV2Edit.text())
        v3 = float(self.orbitInitV3Edit.text())

        r0 = [r1, r2, r3]
        v0 = [v1, v2, v3]

        cb = plDat.Earth
        body = self.planetaryBodyComboBox.currentText()

        if body == "Sun":
            cb = plDat.Sun
        
        timeStep = float(self.orbitTimeStepEdit.text())
        time = float(self.orbitTimeEdit.text()) * 3600

        params = OrbitParams
        params.rVec = r0
        params.vVec = v0
        params.timelength = time
        params.timeStep = timeStep
        params.color = self.trajectoryColor
        params.cb = cb
        op = OP(params)
        op.propogateOrbit()
        rs = op.getRadiusArray()


        # print(self.trajectoryColor)
        self.orbitPlot.clear()

        # Create the celestial body
        radius = np.linalg.norm([0, cb.radius, 0])
        md = gl.MeshData.sphere(rows=200, cols=300, radius=radius)
        m1 = gl.GLMeshItem(meshdata=md,smooth=True,color=cb.qtColor,shader="balloon",glOptions="additive")
        # m1.translate(10000, 5000, 12000)
        self.orbitPlot.plot.addItem(m1)

        # Plot the initial point
        initialPoint = gl.GLScatterPlotItem(pos=np.array([rs[0,0], rs[0,1], rs[0,2]]), size=np.array([13]), color=(1,0,0,1.5))
        self.orbitPlot.plot.addItem(initialPoint)

        # Plot the trajectory
        orbit1 = np.array([rs[:,0], rs[:,1], rs[:,2]]).transpose()
        orbit = gl.GLLinePlotItem(pos=orbit1, color=self.trajectoryColor, antialias=True) # (0.8, 0.5, 0.6, 1))
        self.orbitPlot.plot.addItem(orbit)

        # Adjust the plot
        self.orbitPlot.plot.setCameraPosition(distance=cb.radius*10)
        self.orbitPlot.zgrid.scale(np.max(orbit1),np.max(orbit1),np.max(orbit1))
        self.orbitPlot.scaleAxis(cb.radius*2)
        self.orbitPlot.createAxis()
        # self.orbitPlot.createGrid(np.max(orbit1)) # Doesn't Work ?



    def showMultipleOrbits(self):
        self.finished = False
        
        self.orbitPlot.clear()

        firstPass = True

        for orbit, params in self.currentOrbits.items():

            if firstPass:
                # Create the celestial body
                radius = np.linalg.norm([0, params.body.radius, 0])
                md = gl.MeshData.sphere(rows=200, cols=300, radius=radius)
                m1 = gl.GLMeshItem(meshdata=md,smooth=True,color=params.body.qtColor,shader="balloon",glOptions="additive")
                m1.translate(10000, 5000, 12000)
                self.orbitPlot.plot.addItem(m1)
                firstPass = False
            
            rs = params.getRadiusArray()

            # Plot the initial point
            initialPoint = gl.GLScatterPlotItem(pos=np.array([rs[0,0], rs[0,1], rs[0,2]]), size=np.array([13]), color=(1,0,0,1.5))
            self.orbitPlot.plot.addItem(initialPoint)

            # Plot the trajectory
            orbit1 = np.array([rs[:,0], rs[:,1], rs[:,2]]).transpose()
            orbit = gl.GLLinePlotItem(pos=orbit1, color=params.color, antialias=True)
            self.orbitPlot.plot.addItem(orbit)

            # Adjust the plot
            self.orbitPlot.plot.setCameraPosition(distance=params.body.radius*10)
            self.orbitPlot.zgrid.scale(np.max(orbit1),np.max(orbit1),np.max(orbit1))
            self.orbitPlot.scaleAxis(params.body.radius*2)
            self.orbitPlot.createAxis()


    def propogateMultipleOrbits(self):
        if not self.orbitPropogatorThread.is_alive():
            self.counter = 0
            self.orbitPBar.setMaximum(len(self.currentOrbitNames))
            self.orbitPBar.setValue(0)
            self.orbitPropogatorThread = threading.Thread(target=self.propogateMultipleOrbitsThread)
            self.orbitPropogatorThread.start()

        else:
            print("Thread already started shouldn't be here")
        
        self.timer.singleShot(500, self.checkOrbitThread)


    def checkOrbitThread(self):

        if not self.orbitPropogatorThread.is_alive():
            if self.finished:
                self.orbitPBar.setValue(self.counter)
                self.showMultipleOrbits()
        else:
            self.orbitPBar.setValue(self.counter)
            self.timer.singleShot(200, self.checkOrbitThread)
            

    def propogateMultipleOrbitsThread(self):
        for orbit in self.currentOrbitNames:
            self.currentOrbits[orbit].propogateOrbit()
            self.counter += 1
        
        self.finished = True

    
    def updateCelestialBodyRadius(self):
        cb = plDat.getPlanetData(self.planetaryBodyComboBox.currentText())
        self.orbitRadiusLbl.setText(str(cb.radius))


    def initializePvVectorsFromCoes(self):
        annomoly = 0
        trueAnnomoly = 0
        eccentricity = 0
        inclination = 0
        raan = 0
        argPerig = 0

        if self.annomolyEdit.text():
            annomoly = float(self.annomolyEdit.text())

        if self.trueAnomolyEdit.text():
            trueAnnomoly = float(self.trueAnomolyEdit.text())

        if self.eccentricityEdit.text():
            eccentricity = float(self.eccentricityEdit.text())

        if self.InclinationEdit.text():
            inclination = float(self.InclinationEdit.text())

        if self.raanEdit.text():
            raan = float(self.raanEdit.text())

        if self.argOfPerigEdit.text():
            argPerig = float(self.argOfPerigEdit.text())

        cb = plDat.getPlanetData(self.planetaryBodyComboBox.currentText())

        oe = OrbitalElements()
        oe.trueAnomoly = trueAnnomoly
        oe.eccentricity = eccentricity
        oe.inclination = inclination
        oe.semiMajorAxis = annomoly
        oe.argOfPerigee = argPerig
        oe.rightAscension = raan


        stateConverter = CoesToStateVectors(oe, mu=cb.mu)
        r, v = stateConverter.getRandV()

        self.orbitInitP1Edit.setText(str(round(r[0], 5)))
        self.orbitInitP2Edit.setText(str(round(r[1], 5)))
        self.orbitInitP3Edit.setText(str(round(r[2], 5)))

        self.orbitInitV1Edit.setText(str(round(v[0], 5)))
        self.orbitInitV2Edit.setText(str(round(v[1], 5)))
        self.orbitInitV3Edit.setText(str(round(v[2], 5)))


    def vectorCoesConverter(self):
        mu = plDat.getPlanetData(self.vecCoesConverterCombobx.currentText()).mu

        if self.vecCoesConverterUseCanonicalChckBx.isChecked():
            mu = 1

        if self.calculateCoesChckbx.isChecked():
            if self.r1VecCoesConverterEdit.text() and self.r2VecCoesConverterEdit.text() and self.r3VecCoesConverterEdit.text() \
                and self.v1VecCoesConverterEdit.text() and self.v2VecCoesConverterEdit.text() and self.v3VecCoesConverterEdit.text():

                r1 = float(self.r1VecCoesConverterEdit.text())
                r2 = float(self.r2VecCoesConverterEdit.text())
                r3 = float(self.r3VecCoesConverterEdit.text())

                v1 = float(self.v1VecCoesConverterEdit.text())
                v2 = float(self.v2VecCoesConverterEdit.text())
                v3 = float(self.v3VecCoesConverterEdit.text())

                v = [v1, v2, v3]
                r = [r1, r2, r3]

                converter = Vector2CoesConverter(r, v, mu=mu)

                self.inclinationCoesConvertEdit.setText(str(round(converter.getInclination(), 5)))
                self.raanCoesConvertEdit.setText(str(round(converter.getRaan(), 5)))
                self.argPerigCoesConvertEdit.setText(str(round(converter.getArgOfPerig(), 5)))
                self.trueAnomalyCoesConvertEdit.setText(str(round(converter.getTrueAnomaly(), 5)))
                self.eccentricityCoesconvertEdit.setText(str(round(converter.getEccentricity(), 5)))
                self.semiMajorAxisCoesConvertEdit.setText(str(round(converter.getSemiMajorAxis(), 5)))
                self.semiLatusRectumCoesConverterEdit.setText(str(round(converter.getSemiLatusRectum(), 5)))
        

        if self.calculateRVchckbx.isChecked():
            if self.inclinationCoesConvertEdit.text() and self.raanCoesConvertEdit.text() and self.argPerigCoesConvertEdit.text() \
                and self.trueAnomalyCoesConvertEdit.text() and self.eccentricityCoesconvertEdit.text() \
                and self.semiMajorAxisCoesConvertEdit.text() and self.semiLatusRectumCoesConverterEdit.text():

                semiMajorAxis = float(self.semiMajorAxisCoesConvertEdit.text())
                inclination = float(self.inclinationCoesConvertEdit.text())
                raan = float(self.raanCoesConvertEdit.text())
                argPerig = float(self.argPerigCoesConvertEdit.text())
                trueAnom = float(self.trueAnomalyCoesConvertEdit.text())
                eccentricity = float(self.eccentricityCoesconvertEdit.text())
                latusRectum = float(self.semiLatusRectumCoesConverterEdit.text())

                oe = OrbitalElements()
                oe.trueAnomoly = trueAnom
                oe.eccentricity = eccentricity
                oe.inclination = inclination
                oe.semiMajorAxis = semiMajorAxis
                oe.argOfPerigee = argPerig
                oe.rightAscension = raan
                oe.semiLatusRectum = latusRectum


                stateConverter = CoesToStateVectors(oe, mu=mu)
                r, v = stateConverter.getRandV()

                self.r1VecCoesConverterEdit.setText(str(round(r[0], 5)))
                self.r2VecCoesConverterEdit.setText(str(round(r[1], 5)))
                self.r3VecCoesConverterEdit.setText(str(round(r[2], 5)))

                self.v1VecCoesConverterEdit.setText(str(round(v[0], 5)))
                self.v2VecCoesConverterEdit.setText(str(round(v[1], 5)))
                self.v3VecCoesConverterEdit.setText(str(round(v[2], 5)))


    
    def transformOrbitVectors(self):
        orbitElementsDefined = False
        latLstDefined = False
        userDefineMatrix = False
        selectedTransform = self.transformMatrixComboBx.currentText()

        if self.transformRaanEdit.text() and self.transformInclinationEdit.text() and self.transformAopEdit.text() \
            and self.r1TTransformEdit.text() and self.r2TTransformEdit.text() and self.r3TTransformEdit.text \
            and self.v1TTransformEdit.text() and self.v2TTransformEdit.text() and self.v3TTransformEdit.text():

            orbitElementsDefined = True
            raan = float(self.transformRaanEdit.text())
            aop = float(self.transformAopEdit.text())
            inclination = float(self.transformInclinationEdit.text())

        if self.transformLatEdit.text() and self.transformLstEdit.text():
            latLstDefined = True

        if self.transformMatric11Edit.text() and self.transformMatric12Edit.text() and self.transformMatric13Edit.text() \
            and self.transformMatric21Edit.text() and self.transformMatric22Edit.text() and self.transformMatric23Edit.text() \
            and self.transformMatric31Edit.text() and self.transformMatric32Edit.text() and self.transformMatric33Edit.text():
            
            userDefineMatrix = True


        r1 = float(self.r1TTransformEdit.text())
        r2 = float(self.r2TTransformEdit.text())
        r3 = float(self.r3TTransformEdit.text())

        v1 = float(self.v1TTransformEdit.text())
        v2 = float(self.v2TTransformEdit.text())
        v3 = float(self.v3TTransformEdit.text())

        r = np.array([r1, r2, r3])
        v = np.array([v1, v2, v3])

        matrix = np.empty((3,3), float)


        if selectedTransform == "Inertial -> Perifocal" and orbitElementsDefined:
            matrix = CoordinateTransforms.getInertial2PerifocalTransform(raan, aop, inclination)

        elif selectedTransform == "Perifocal -> Inertial" and orbitElementsDefined:
            matrix = CoordinateTransforms.getPerifocal2InertialTransform(raan, aop, inclination)

        elif selectedTransform == "Perifocal -> Geocentric" and orbitElementsDefined:
            matrix = CoordinateTransforms.getPerifcoal2GeocentricTransform(raan, aop, inclination)

        elif selectedTransform == "Geocentric -> Perifocal" and orbitElementsDefined:
            matrix = CoordinateTransforms.getGeocentric2PerifocalTransform(raan, aop, inclination)

        elif selectedTransform == "Manually Input Matrix Values" and userDefineMatrix:
            m11 = float(self.transformMatric11Edit.text())
            m12 = float(self.transformMatric12Edit.text())
            m13 = float(self.transformMatric13Edit.text())
            m21 = float(self.transformMatric21Edit.text())
            m22 = float(self.transformMatric22Edit.text())
            m23 = float(self.transformMatric23Edit.text())
            m31 = float(self.transformMatric31Edit.text())
            m32 = float(self.transformMatric32Edit.text())
            m33 = float(self.transformMatric33Edit.text())

            matrix = np.array([[m11, m12, m13], [m21, m22, m23], [m31, m32, m33]])

        elif selectedTransform == "Topocentric-Horizon -> Geocentric" and latLstDefined:
            latitude = math.radians(float(self.transformLatEdit.text()))
            lst = math.radians(float(self.transformLstEdit.text()))

            matrix = CoordinateTransforms.getTopoHorizon2Geocentric(latitude, lst)

        elif selectedTransform == "Geocentric -> Topocentric-Horizon" and latLstDefined:
            latitude = float(self.transformLatEdit.text())
            lst = float(self.transformLstEdit.text())

            matrix = CoordinateTransforms.getGeocentric2TopoHorizon(latitude, lst)

        else:
            print("Invalid transform type: {}".format(selectedTransform))


        if (orbitElementsDefined or latLstDefined or userDefineMatrix):
            r = np.matmul(matrix, r)
            v = np.matmul(matrix, v)

            self.r1PrimeTransformEdit.setText(str(round(r[0], 4)))
            self.r2PrimeTransformEdit.setText(str(round(r[1], 4)))
            self.r3PrimeTransformEdit.setText(str(round(r[2], 4)))

            self.v1PrimeTransformEdit.setText(str(round(v[0], 4)))
            self.v2PrimeTransformEdit.setText(str(round(v[1], 4)))
            self.v3PrimeTransformEdit.setText(str(round(v[2], 4)))

            self.transformMatric11Edit.setText(str(round(matrix[0][0], 5)))
            self.transformMatric12Edit.setText(str(round(matrix[0][1], 5)))
            self.transformMatric13Edit.setText(str(round(matrix[0][2], 5)))
            self.transformMatric21Edit.setText(str(round(matrix[1][0], 5)))
            self.transformMatric22Edit.setText(str(round(matrix[1][1], 5)))
            self.transformMatric23Edit.setText(str(round(matrix[1][2], 5)))
            self.transformMatric31Edit.setText(str(round(matrix[2][0], 5)))
            self.transformMatric32Edit.setText(str(round(matrix[2][1], 5)))
            self.transformMatric33Edit.setText(str(round(matrix[2][2], 5)))













def readINI():
    global theme
    highResScreen = False
    global CONFIG_FILE_DIR

    with open(CONFIG_FILE_DIR, "r") as configFile:
        config = configparser.ConfigParser()
        config.read_file(configFile)

        highResScreen = config.getboolean("Screen_Settings", "4k_Resolution")
        theme = config.get("Screen_Settings", "theme")
    

    if highResScreen:
        setHighResScreenParams()


def setHighResScreenParams():
    if QtCore.QCoreApplication.instance() == None:
        if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
            PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

        if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
            PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

        os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"


def setTheme(app):
    global theme

    if theme == "Classic Dark":
        qtmodern.styles.dark(app)
    
    elif theme == "Dark Blue":
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    
    elif theme == "Dark Orange":
        app.setStyleSheet(pyqtcss.get_style("dark_orange"))

    elif theme == "Dark Yellow":
        app.setStyleSheet(qdarkgraystyle.load_stylesheet())

    elif theme == "Dark Black":
        app.setStyle("Fusion")
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53,53,53))
        palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Base, QtGui.QColor(15,15,15))
        palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53,53,53))
        palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53,53,53))
        palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
        palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(142,45,197).lighter())
        palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
        app.setPalette(palette)

    elif theme == "Dark GrayGreen":
        app.setStyle("Fusion")
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(12, 60, 12))
        palette.setColor(QtGui.QPalette.Base, QtGui.QColor(15, 15, 15))
        palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
        palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(142, 45, 197).lighter())
        palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
        app.setPalette(palette)

    elif theme == "none":
        app.setStyleSheet("")



def main():
    global theme
    exitCode = 0

    while True:
        readINI()
        
        app = QtCore.QCoreApplication.instance()
        

        if app == None:
            app = QtWidgets.QApplication(sys.argv)

        setTheme(app)
        
        window = Ui()
        exitCode = app.exec_()
        del window
        del app
        
        if exitCode != EXIT_CODE_REBOOT:
            break









if __name__ == "__main__":
    main()
