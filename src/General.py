import numpy as np
import math

# File Contains general methods and structures for orbital mechanics


class OrbitalElements:
    satillite   = "UNDEFINED"
    orbitedBody = "UNDEFINED"
    
    # Main Orbital Elements
    semiMajorAxis   = math.nan
    eccentricity    = math.nan
    inclination     = math.nan
    rightAscension  = math.nan
    argOfPerigee    = math.nan
    trueAnomoly     = math.nan

    # Alternate Orbital Elements
    longitudeOfPeriapsis = math.nan
    argOfLatitude        = math.nan
    trueLongitude        = math.nan

    # Vectors
    r                  = np.array([math.nan, math.nan, math.nan])
    v                  = np.array([math.nan, math.nan, math.nan])
    momentumVector     = np.array([math.nan, math.nan, math.nan])
    normalVector       = np.array([math.nan, math.nan, math.nan])
    eccentricityVector = np.array([math.nan, math.nan, math.nan])

    # Magnitudes
    magR        = math.nan
    magV        = math.nan
    magMomentum = math.nan
    magNormal   = math.nan

    # Other Orbit Parameters 
    semiLatusRectum   = math.nan
    meanMotion        = math.nan
    energy            = math.nan
    eccentricAnnomoly = math.nan
    meanAnomaly       = math.nan


    
    
class OrbitType:
    Circular = 0
    Ellipse = 1
    Parabolic = 2
    HyperBolic = 3
    Undefinded = 4


class OrbitChecker(OrbitType):
    def __init__(self, eccentricity: float, energy: float, semimajoraxis: float) -> None:
        self.energy = energy
        self.eccentricity = eccentricity
        self.semimajoraxis = semimajoraxis
        self.thisOrbit = self.Undefinded
        self.checkOrbitType()

    def checkOrbitType(self) -> None:
        if self.eccentricity == 0 and self.energy < 0 and self.semimajoraxis > 0:
            self.thisOrbit = self.Circular
        
        elif self.eccentricity < 1 and self.eccentricity > 0 and self.energy < 0 and self.semimajoraxis > 0:
            self.thisOrbit = self.Ellipse
        
        elif self.eccentricity == 1 and self.energy == 0:
            self.thisOrbit = self.Parabolic
        
        elif self.eccentricity > 1 and self.energy > 0 and self.semimajoraxis < 0:
            self.thisOrbit = self.HyperBolic


    def printOrbitType(self) -> None:
        if self.thisOrbit == OrbitType.Circular:
            print("This orbit is circular")
        
        elif self.thisOrbit == OrbitType.Ellipse:
            print("This orbit is elliptical")
        
        elif self.thisOrbit == OrbitType.HyperBolic:
            print("This orbit is hyperbolic")
        
        elif self.thisOrbit == OrbitType.Parabolic:
            print("This orbit is parabolic")
        
        else:
            print("This orbit is undefined!")
    
    def getOrbitTypeString(self) -> str:
        if self.thisOrbit == OrbitType.Circular:
            return "Circular"
        
        elif self.thisOrbit == OrbitType.Ellipse:
            return "Elliptical"
        
        elif self.thisOrbit == OrbitType.HyperBolic:
            return "Hyperbolic"
        
        elif self.thisOrbit == OrbitType.Parabolic:
            return "Parabolic"
        
        else:
            return "Undefined"
    
    def getOrbitType(self) -> None:
        return self.thisOrbit