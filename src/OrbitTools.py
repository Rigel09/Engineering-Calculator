from os import stat
import numpy as np
import matplotlib.pyplot as plt
import math

from numpy.core.records import array

from .planetary_data import planetaryData as plDat


class InvalidParams(Exception):
    ''' Excpetion thrown for invalid orbit parameters'''
    pass

class ResultCheck(Exception):
    ''' Exception thrown for an invalid calculated orbit parameter'''
    pass

class OrbitPropogationError(Exception):
    '''General orbit propogation error'''
    pass



def plot_n_orbits(rs: list, labels: list, colors: str, body: plDat.base =plDat.Earth, showPlot: bool =True, savePlot: bool =False, title: str="orbit"):
    if rs is None or body is None:
        print("Error No data to plot")
        return

    if len(rs) == 0:
        print("Error no data to plot!")
        return

    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111, projection='3d')

    for r, l, c in zip(rs, labels, colors):
        ax.plot(r[:,0], r[:,1], r[:,2], color=c)
        ax.plot([r[0,0]], [r[0,1]], [r[0,2]], color=c, marker='o', label=l)

    r_plot = body.radius

    _u, _v = np.mgrid[0:2*np.pi:40j, 0:np.pi:30j]
    _x = r_plot * np.cos(_u) * np.sin(_v)
    _y = r_plot * np.sin(_u) * np.sin(_v)
    _z = r_plot * np.cos(_v)
    ax.plot_surface(_x, _y, _z, cmap=body.colormap)

    l = r_plot * 2.0
    x, y, z = [[0,0,0], [0,0,0], [0,0,0]]
    u, v, w = [[l,0,0], [0,l,0], [0,0,l]]
    ax.quiver(x,y,z,u,v,w,color='k')

    max_val = np.max(np.abs(rs)/2)


    ax.set_xlim([-max_val, max_val])
    ax.set_ylim([-max_val, max_val])
    ax.set_zlim([-max_val, max_val])
    ax.set_xlabel("X (km)")
    ax.set_ylabel("Y (km)")
    ax.set_zlabel("Z (km)")

    plt.legend()
    
    if showPlot:
        plt.show()

    if savePlot:
        plt.savefig(title + ".png", dpi=300)



def coes2RvecVvec(annomoly: float, eccentricity: float, inclination: float, trueAnomoly: float, argOfPerig: float, raan: float, deg: bool = False, mu: float = plDat.Earth.mu) -> list:
    ''' Converts Classical orbital elements to standard position and velocity vectors'''

    if deg:
        annomoly = math.radians(annomoly)
        eccentricity = math.radians(eccentricity)
        inclination = math.radians(inclination)
        trueAnomoly = math.radians(trueAnomoly)
        argOfPerig = math.radians(argOfPerig)
        raan = math.radians(raan)
    
    eccentricAnomoly = calculateEccentricAnomoly(trueAnomoly, eccentricity, "tae")

    normR = annomoly * (1-eccentricity**2) / (1 + eccentricity*math.cos(trueAnomoly))


    # Calculate R and V vectors
    perifR = normR * np.array([math.cos(trueAnomoly), math.sin(trueAnomoly), 0])
    perifV = math.sqrt(mu * annomoly) / normR * np.array([-math.sin(eccentricAnomoly), math.cos(eccentricAnomoly) * math.sqrt(1 - eccentricity**2) , 0])

    # rotation matrix from perifocal to ECI
    perif2Eci = np.transpose(CoordinateTransforms.getInertial2PerifocalTransform(raan, argOfPerig, inclination))

    # Calculate r and v vectors in inertial frame
    r = np.array(np.dot(perif2Eci, perifR))
    v = np.dot(perif2Eci, perifV)

    return list(r), list(v)



def calculateEccentricAnomoly(me: float, e: float, method: str = "Newton", tolerance: float = 1e-8) -> float:
    ''' Returns eccentric anomoly, if function fails returns None'''
    if method == "Newton":
        e0, e1 = 0

        if me < np.pi/2: e0 = me + e/2
        else: e0 = me - e

        for n in range(200):
            ratio = (e0 - e*np.sin(e0) - me) / (1 - e*np.cos(e0))

            if abs(ratio) < tolerance:
                if n == 0: return e0
                else: return e1

            else:
                e1 = e0 - ratio
                e0 = 1

        print("{} did not converge in calculating eccentric anomaly".format(method))
        return None

    elif method == 'tae':
        return 2 * math.atan(math.sqrt((1 - e) / (1+e)) * math.tan(me / 2))
    
    else:
        print("{} method not supported".format(method))
        return None




class CoordinateTransforms:
    validFrames = ["Inertial -> Perifocal", "Perifocal -> Inertial", "Perifocal -> Geocentric", "Geocentric -> Perifocal", 
                "Topocentric-Horizon -> Geocentric", "Geocentric -> Topocentric-Horizon"]

    @staticmethod
    def getInertial2PerifocalTransform(raan: float, aop: float, inclination: float) -> np.array:
        i = inclination
        row0 = [-math.sin(raan)*math.cos(i)*math.sin(aop) + math.cos(raan)*math.cos(aop), 
                math.cos(raan)*math.cos(i)*math.sin(aop) + math.sin(raan)*math.cos(aop), 
                math.sin(i)*math.sin(aop)]

        row1 = [-math.sin(raan)*math.cos(i)*math.cos(aop) - math.cos(raan)*math.sin(aop), 
                math.cos(raan)*math.cos(i)*math.cos(aop) - math.sin(raan)*math.sin(aop), 
                math.sin(i)*math.cos(aop)]

        row2 = [math.sin(raan)*math.sin(i), -math.cos(raan)*math.sin(i), math.cos(i)]

        return np.array([row0, row1, row2])

    
    @staticmethod
    def getPerifocal2InertialTransform(raan: float, aop: float, inclination: float) -> np.array:
        return np.transpose(CoordinateTransforms.getInertial2PerifocalTransform(raan, aop, inclination))


    @staticmethod
    def getPerifcoal2GeocentricTransform(raan: float, argOfPerig: float, inclination: float) -> np.array:
        i = inclination
        aop = argOfPerig

        row1 = [math.cos(raan)*math.cos(aop) - math.sin(raan)*math.sin(aop)*math.cos(i),
                -math.cos(raan)*math.sin(aop) - math.sin(raan)*math.cos(aop)*math.cos(i),
                math.sin(raan)*math.sin(i)]

        row2 = [math.sin(raan)*math.cos(aop) + math.cos(raan)*math.sin(aop)*math.cos(i),
                -math.sin(raan)*math.sin(aop) + math.cos(raan)*math.cos(aop)*math.cos(i),
                -math.cos(raan)*math.cos(i)]

        row3 = [math.sin(aop)*math.sin(i), math.cos(aop)*math.sin(i), math.cos(i)]

        return np.array([row1, row2, row3])


    @staticmethod
    def getGeocentric2PerifocalTransform(raan: float, argOfPerig: float, inclination: float) -> np.array:
        return np.transpose(CoordinateTransforms.getPerifcoal2GeocentricTransform(raan, argOfPerig, inclination))

    
    @staticmethod
    def getTopoHorizon2Geocentric(latitude: float, localSideRealTime: float) -> np.array:
        lat = latitude
        lst = localSideRealTime
        
        row1 = [math.sin(lat)*math.cos(lst),  math.sin(lat)*math.sin(lst), -math.cos(lat)]
        row2 = [-math.sin(lst), math.cos(lst), 0]
        row3 = [math.cos(lat)*math.cos(lst), math.cos(lat)*math.sin(lst), math.sin(lat)]

        return np.array([row1, row2, row3])


    @staticmethod
    def getGeocentric2TopoHorizon(latitude: float, localSideRealTime: float) -> np.array:
        return np.transpose(CoordinateTransforms.getTopoHorizon2Geocentric(latitude, localSideRealTime))


        

            



class Vector2CoesConverter():
    '''
        Class converts the R & V vectors into classical orbital elements
        User has option of having elements in degrees or radians
    '''
    def __init__(self, r: list, v: list, degrees: bool = True, mu:float = 1) -> None:
        self.degrees = degrees
        self.mu = mu
        self.rVec = np.array(r)                 # Position Vector
        self.vVec = np.array(v)                 # Velocity Vector
        self.hVec = np.array([0.0, 0.0, 0.0])   # Momentum Vector
        self.nVec = np.array([0.0, 0.0, 0.0])   # N Vector
        self.eVec = np.array([0.0, 0.0, 0.0])   # E Vector
        self.magR = 0                           
        self.magV = 0
        self.magH = 0
        self.magN = 0
        self.magE = 0
        self.inclination = 0.0
        self.argOfPerig = 0.0   # Argument of Perigee
        self.raan = 0.0         # Right Ascension of Ascending Node
        self.trueAnomaly = 0.0
        self.eccentricity = 0.0
        self.anomaly = 0.0
        self.p = 0          # Semi-Latus Rectum
        self.a = 0          # Semi-Major Axis

        self.magR = self.getMagnitude(self.rVec)
        self.magV = self.getMagnitude(self.vVec)
        self.__calculateEvector__()
        self.__calculateHvector__()
        self.__calculateNvector__()
        self.__calculateInclination__()
        self.__calculateArgOfPerig__()
        self.__calculateRaan__()
        self.__calculateTrueAnomaly__()
        self.__calculateEccentricty__()
        self.__calculatePA__()

    def getSemiLatusRectum(self)-> float: return self.p
    def getSemiMajorAxis(self)  -> float: return self.a
    def getInclination(self)    -> float: return self.inclination
    def getArgOfPerig(self)     -> float: return self.argOfPerig
    def getRaan(self)           -> float: return self.raan
    def getTrueAnomaly(self)    -> float: return self.trueAnomaly
    def getEccentricity(self)   -> float: return self.eccentricity
    def getAnomaly(self)        -> float: return self.anomaly
    def getMagH(self)           -> float: return self.magH
    def getMagN(self)           -> float: return self.magN
    def getMagE(self)           -> float: return self.magE
    def getMagR(self)           -> float: return self.magR
    def getMagV(self)           -> float: return self.magV
    def getRVector(self)        -> np.array: return self.rVec
    def getVvector(self)        -> np.array: return self.vVec
    def getHvector(self)        -> np.array: return self.hVec
    def getEvector(self)        -> np.array: return self.eVec
    def getNvector(self)        -> np.array: return self.nVec


    def getMagnitude(self, vec: np.array) -> float:
        i2 = vec[0]**2
        j2 = vec[1]**2
        k2 = vec[2]**2
        return math.sqrt(i2 + j2 + k2)


    def __calculateNvector__(self) -> None:
        k = np.array([0,0,1])
        self.nVec = np.cross(k, self.hVec)
        self.magN = self.getMagnitude(self.nVec)


    def __calculateHvector__(self) -> None:
        self.hVec = np.cross(self.rVec, self.vVec)
        self.magH = self.getMagnitude(self.hVec)


    def __calculateEvector__(self) -> None:
        self.eVec = 1/self.mu  * ((self.magV**2 - self.mu/self.magR)*self.rVec - (np.dot(self.rVec, self.vVec)*self.vVec))
        self.magE = self.getMagnitude(self.eVec)

    
    def __calculatePA__(self) -> None:
        self.p = self.magH**2 / self.mu
        self.a = self.p / (1 - self.magE**2)


    def __calculateInclination__(self) -> None:
        self.inclination = math.acos(self.hVec[2] / self.magH)
        if self.degrees: self.inclination = math.degrees(self.inclination)


    def __calculateEccentricty__(self) -> None:
        self.eccentricity = self.magE


    def __calculateTrueAnomaly__(self) -> None:
        self.trueAnomaly = math.acos(np.dot(self.eVec, self.rVec) / (self.magE*self.magR))

        if (np.dot(self.rVec, self.vVec) > 0 and self.trueAnomaly > 180):
            raise ResultCheck("True anomoly invalid")

        if self.degrees: self.trueAnomaly = math.degrees(self.trueAnomaly)


    def __calculateRaan__(self) -> None:
        self.raan = math.acos(self.nVec[0] / self.magN)
        if self.degrees: self.raan = math.degrees(self.raan)


    def __calculateArgOfPerig__(self) -> None:
        self.argOfPerig = math.acos(np.dot(self.nVec, self.eVec) / (self.magN * self.magE))
        if self.degrees: self.argOfPerig = math.degrees(self.argOfPerig)

        if self.eVec[2] > 0 and self.degrees:
            self.argOfPerig = 360 - self.argOfPerig

        elif self.eVec[2] > 0 and not self.degrees:
            self.argOfPerig = 2*math.pi - self.argOfPerig