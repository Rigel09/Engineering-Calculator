import math
import numpy as np

from src.General import OrbitChecker, OrbitType, OrbitalElements
from src.CoordinateTransforms import CoordinateTransforms as ct



class CoesToStateVectors(OrbitalElements, OrbitChecker):
    def __init__(self, orbitalElements: OrbitalElements, mu: float = 1, inDegrees: bool = True) -> None:

        # Define needed params
        self.semiMajorAxis = orbitalElements.semiMajorAxis
        self.eccentricity = orbitalElements.eccentricity
        self.trueAnomoly = orbitalElements.trueAnomoly
        self.energy = orbitalElements.energy
        self.inclination = orbitalElements.inclination
        self.rightAscension = orbitalElements.rightAscension
        self.argOfPerigee = orbitalElements.argOfPerigee
        self.semiLatusRectum = orbitalElements.semiLatusRectum
        self.inDegrees = inDegrees
        self.mu = mu


        super().__init__(self.eccentricity, self.energy, self.semiMajorAxis)

        if self.thisOrbit == OrbitType.Circular:
            raise RuntimeError("Circular Orbit Detected Cannot convert Orbital Elements to State Vectors")

        if math.isnan(self.inclination):
            raise RuntimeError("Inclination is NAN")

        if math.isnan(self.argOfPerigee):
            raise RuntimeError("Argument of Perigee is NAN")

        if math.isnan(self.rightAscension):
            raise RuntimeError("RAAN is NAN")

        if self.inDegrees: 
            self.trueAnomoly = math.radians(self.trueAnomoly)
            self.rightAscension = math.radians(self.rightAscension)
            self.inclination = math.radians(self.inclination)
            self.argOfPerigee = math.radians(self.argOfPerigee)



    
    def __calculateR(self) -> float:
        return self.semiMajorAxis * (1 - self.eccentricity**2) / (1 + self.eccentricity * math.cos(self.trueAnomoly))

    def __calculateRPQW(self, r: float) -> np.array:
        rpqw = np.array([0.0, 0.0, 0.0])
        rpqw[0] = r * math.cos(self.trueAnomoly)
        rpqw[1] = r * math.sin(self.trueAnomoly)
        return rpqw

    def __calculateVPQW(self) -> np.array:
        vpqw = np.array([0.0, 0.0, 0.0])

        vpqw[0] = math.sqrt(self.mu / self.semiLatusRectum) * (-1) * math.sin(self.trueAnomoly)
        vpqw[1] = math.sqrt(self.mu / self.semiLatusRectum) * (self.eccentricity + math.cos(self.trueAnomoly))

        return vpqw

    def getRandV(self) -> tuple:
        rVec = np.array([0.0, 0.0, 0.0])
        vVec = np.array([0.0, 0.0, 0.0])

        transform = ct.getPerifcoal2GeocentricTransform(self.rightAscension, self.argOfPerigee, self.inclination)

        radius = self.__calculateR()
        rpqw = self.__calculateRPQW(radius)
        vpqw = self.__calculateVPQW()

        rVec = np.matmul(transform, rpqw)
        vVec = np.matmul(transform, vpqw)

        return rVec, vVec 