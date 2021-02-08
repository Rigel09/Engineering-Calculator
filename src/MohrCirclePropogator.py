import numpy as np
import math
from matplotlib import pyplot as plt
import matplotlib as mpl
from numpy.linalg.linalg import eigvals

class MohrCircle3DValues:
    nSteps = 100
    sigmaX = 0
    sigmaY = 0
    sigmaZ = 0
    tauXY =  0
    tauXZ = 0
    tauYZ = 0
    sigmaI = 0
    sigmaII = 0
    sigmaIII = 0
    maxTau1 = 0
    maxTau2 = 0
    maxTau3 = 0
    R1 = 0
    R2 = 0
    R3 = 0
    C1 = 0
    C2 = 0
    C3 = 0
    thetaVals = np.empty((0,0))
    circle1X = np.empty((0,0))
    circle1Y = np.empty((0,0))
    circle2X = np.empty((0,0))
    circle2Y = np.empty((0,0))
    circle3X = np.empty((0,0))
    circle3Y = np.empty((0,0))
    vonMissesStress = 0
    hydrostaticStress = 0


class MohrCirclePropogator():
    def __init__(self, sigmaX: float, sigmaY: float, tauXy: float, theta: float) -> None:
        super().__init__()
        self.nsteps = 100
        self.scatterPlotPointSize = 60
        self.plotLineWidth = 15
        self.sigmaX = sigmaX
        self.sigmaY = sigmaY
        self.tauXy = tauXy
        self.theta = theta
        self.q1 = ()
        self.q2 = ()
        self.sigmal  = 0
        self.sigmall = 0
        self.maxTau = 0
        self.sigmaPoint = 0
        self.tauPoint = 0
        self.circleXValues = np.empty([0, 0])
        self.circleYValues = np.empty([0, 0])
        self.principalStressPlane = 0
        self.shearStressPlane = np.empty([1, 1])
        self.normalStressVals = np.empty([1, 1])
        self.shearStressVals = 0
        self.thetaVals = np.empty([0, 0])



    def getCicleValues(self) -> tuple:
        return (self.circleXValues, self.circleYValues)

    def getQ1(self) -> tuple:
        return self.q1

    def getQ2(self) -> tuple:
        return self.q2

    def getCalculatedPoint(self) -> tuple:
        return (self.sigmaPoint, self.tauPoint)
    
    def getPrincipalStresses(self) -> tuple:
        return (self.sigmal, self.sigmall)

    def getMaxTau(self) -> float:
        return self.maxTau

    def getPrincipalStressPlaneAngles(self) -> float:
        return self.principalStressPlane

    def getShearStressPlanes(self) -> float:
        return self.shearStressPlane

    def getNormalAndShearStressValues(self) -> list:
        return [self.normalStressVals, self.shearStressVals]

    def getCenter(self) -> tuple:
        return self.center

    def getRadius(self) -> float:
        return self.radius

    def getThetaVals(self) -> np.array:
        return self.thetaVals
    


    
    def calculateMohrCircleValues(self) -> None:
        # First calculate Center 
        self.center = (self.sigmaX + self.sigmaY) / 2

        # Calculate Radius 
        self.radius = np.sqrt(((self.sigmaX - self.sigmaY)/2)**2 + self.tauXy**2)
        
        # Generate Circle
        # theta goes from 0 to 2pi
        self.thetaVals = np.linspace(0, 2*np.pi, 100)

        # compute circle x y coords
        self.circleXValues = self.center + self.radius*np.cos(self.thetaVals)
        self.circleYValues = self.radius*np.sin(self.thetaVals)

        # Compute Principal Stresses and max shear stress
        self.sigmal = self.center + self.radius
        self.sigmall = self.center - self.radius
        self.maxTau = self.radius

        # Compute Q1 and Q2
        self.q1 = (self.sigmaX, self.tauXy)
        self.q2 = (self.sigmaY, -self.tauXy)

        # Calculate normal and shear stress at given point
        self.sigmaPoint = self.center + (self.sigmaX - self.sigmaY) / 2 * np.cos(np.radians(2 * self.theta)) + self.tauXy * np.sin(np.radians(2 * self.theta))
        self.tauPoint = -(self.sigmaX - self.sigmaY) / 2 * np.sin(np.radians(2 * self.theta)) + self.tauXy * np.cos(np.radians(2 * self.theta))

        # Calculate Angle between X axis and Q1
        thetaP1 = math.degrees(math.atan(2 * self.tauXy / (self.sigmaX - self.sigmaY))) / 2
        thetaP2 = thetaP1 + 90

        self.principalStressPlane = (thetaP1, thetaP2)

        thetaS1 = math.degrees(math.atan(-(self.sigmaX - self.sigmaY)/ ( 2 * self.tauXy))) / 2
        thetaS2 = thetaS1 + 90
        self.shearStressPlane = (thetaS1, thetaS2)

        self.normalStressVals = self.radius + (self.sigmaX - self.sigmaY) / 2 * np.cos(2 * self.thetaVals) + self.tauXy * np.sin(2 * self.thetaVals)
        self.shearStressVals = -(self.sigmaX - self.sigmaY) / 2 * np.sin(2 * self.thetaVals) + self.tauXy * np.cos(2 * self.thetaVals)




    def plotMohrCircle2D(self) -> None:
        # Plot 2D Version of Mohr Circle
        fig, ax = plt.subplots(1,2)

        ax[0].set_facecolor("#C4C4C4")
        ax[0].grid(b=True, which='major', color='black', linewidth=0.6)
        ax[0].grid(b=True, which='minor', color='black', linewidth=0.1)
        ax[0].get_yaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
        ax[0].get_xaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
        ax[0].plot(self.circleXValues, self.circleYValues, 15, color="black")
        ax[0].plot([self.sigmal, self.sigmall], [0, 0], color="black")
        ax[0].plot([self.center, self.center], [self.maxTau, -self.maxTau], color="black")
        ax[0].scatter(self.q1[0], self.q1[1], 60, color='blue', label="Q1")
        ax[0].scatter(self.q2[0], self.q2[1], 60, color="red", label="Q2")
        ax[0].scatter(self.sigmal, 0, 60, color="orange", label = "Sigma I")
        ax[0].scatter(self.sigmall, 0, 60, color="purple", label = "Sigma II")
        ax[0].plot([self.q1[0], self.q2[0]], [self.q1[1], self.q2[1]], color = "blue", linestyle="dashed")
        ax[0].scatter(self.sigmaPoint, self.tauPoint, 60, color="green", label="Calculated")
        ax[0].legend(loc="upper right", prop={'size':8})
        ax[0].set_xlim(self.center - 1.2*self.radius, self.center + 1.8 * self.radius)
        ax[0].set_ylim(self.maxTau + 0.4*self.maxTau, -self.maxTau - 0.4*self.maxTau)
        ax[0].set_xlabel("Normal Stress")
        ax[0].set_ylabel("Shear Stress")

        thetaVals = np.degrees(np.transpose(self.thetaVals))


        ax[1].set_facecolor("#C4C4C4")
        ax[1].grid()
        ax[1].grid(b=True, which='major', color='black', linewidth=1)
        ax[1].grid(b=True, which='minor', color='black', linewidth=0.1)
        ax[1].get_yaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
        ax[1].get_xaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
        ax[1].plot(thetaVals, self.normalStressVals, color='Red', label="Normal Stress")
        ax[1].plot(thetaVals, self.shearStressVals, color='green', label="Shear Stress")
        ax[1].plot([0, 361], [0, 0], color='black', linewidth=2)
        ax[1].set_xlabel("Theta [deg]")
        ax[1].set_xlim(0, 360)
        ax[1].legend(loc="upper right", prop={'size':8})

        plt.show()




    def calculateMohrCircle3D(self, args: MohrCircle3DValues) -> None:

        # Calculate the Stress Matrix
        stressMatrix = np.array([[args.sigmaX, args.tauXY, args.tauXZ],
                                [args.tauXY, args.sigmaY, args.tauYZ],
                                [args.tauXZ, args.tauYZ, args.sigmaZ]])
        # print(stressMatrix)

        try:
            eigenVals = np.linalg.eigvals(stressMatrix)
        except np.linalg.LinAlgError as err:
            print("Mohr Circle 3D Calculation failer")
            print(str(err))
            return None
        
        sortedEigens = np.sort(eigenVals)

        args.sigmaI = sortedEigens[2]
        args.sigmaII = sortedEigens[1]
        args.sigmaIII = sortedEigens[0]

        # Calculate Center of Each Circle
        args.C1 = (args.sigmaI + args.sigmaII) / 2
        args.C2 = (args.sigmaI + args.sigmaIII) / 2
        args.C3 = (args.sigmaII + args.sigmaIII) / 2

        # Calculate Radius's
        args.R1 = (args.sigmaI - args.sigmaII) / 2
        args.R2 = (args.sigmaI - args.sigmaIII) / 2
        args.R3 = (args.sigmaII - args.sigmaIII) / 2

        # Save Max Shear Stress's
        args.maxTau1 = args.R1
        args.maxTau2 = args.R2
        args.maxTau3 = args.R3

        # Calculate Circle Values
        args.thetaVals = np.linspace(0, 2*np.pi, self.nsteps)

        args.circle1X = args.C1 + args.R1 * np.cos(args.thetaVals)
        args.circle1Y = args.R1 * np.sin(args.thetaVals)

        args.circle2X = args.C2 + args.R2 * np.cos(args.thetaVals)
        args.circle2Y = args.R2 * np.sin(args.thetaVals)

        args.circle3X = args.C3 + args.R3 * np.cos(args.thetaVals)
        args.circle3Y = args.R3 * np.sin(args.thetaVals)



        # Calculate the Von Misses Stress
        # Source https://numbas.mathcentre.ac.uk/question/29067/3d-stress-general-case-and-von-mises-calculation/

        # Calculate Trace of matrix
        i1 = (args.sigmaX + args.sigmaY + args.sigmaZ)
        
        # Calculate sum of the sub determinants
        i2 = args.sigmaX * args.sigmaY + args.sigmaY * args.sigmaZ + args.sigmaZ * args.sigmaX - (args.tauXY**2 + args.tauXZ**2 + args.tauYZ**2)

        # The determinant
        i3 = np.linalg.det(stressMatrix)

        # Calculate Hydrostatic Stress
        args.hydrostaticStress = i1 / 3

        # Calculate Von misses
        args.vonMissesStress = math.sqrt(-3 * (i2 - i1**2 / 3))
        

        return args



    def plotMohrCircle3D(self, vals):
        vals=MohrCircle3DValues

        fig, ax = plt.subplots(1,1)

        ax.set_facecolor("#C4C4C4")
        ax.grid()
        ax.grid(b=True, which='major', color='black', linewidth=1)
        ax.grid(b=True, which='minor', color='black', linewidth=0.1)
        ax.get_yaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
        ax.get_xaxis().set_minor_locator(mpl.ticker.AutoMinorLocator())
        ax.plot(vals.circle1X, vals.circle1Y, self.plotLineWidth, color='red')
        ax.plot(vals.circle2X, vals.circle2Y, self.plotLineWidth, color='blue')
        ax.plot(vals.circle3X, vals.circle3Y, self.plotLineWidth, color='green')
        ax.scatter(vals.sigmaI, 0, s=self.scatterPlotPointSize, color='yellow', label="SigmaI")
        ax.scatter(vals.sigmaII, 0, s=self.scatterPlotPointSize, color='black', label="SigmaII")
        ax.scatter(vals.sigmaIII, 0, s=self.scatterPlotPointSize, color='brown', label="SigmaIII")
        ax.scatter(vals.C1, vals.maxTau1, s=self.scatterPlotPointSize, color="red", marker="*", label="Max TauI")
        ax.scatter(vals.C2, vals.maxTau2, s=self.scatterPlotPointSize, color="blue", marker="*", label="Max TauII")
        ax.scatter(vals.C3, vals.maxTau3, s=self.scatterPlotPointSize, color="green", marker="*", label="Max TauIII")
        ax.plot([vals.sigmaIII, vals.sigmaI], [0, 0], self.plotLineWidth, color="black", linewidth=2)
        ax.legend(loc='upper right', prop={'size':9})
        ax.set_xlabel("Normal Stress")
        ax.set_ylabel("Shear Stress")
        ax.set_xlim(vals.C2 - vals.R2*1.3, vals.C2 + vals.R2*1.3)
        ax.set_ylim(-vals.R2*1.3, vals.R2*1.3)
        
        plt.show()





