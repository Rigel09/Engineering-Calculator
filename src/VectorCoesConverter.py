import math
import numpy as np

from src.General import OrbitChecker, OrbitType, OrbitalElements
    


class Vector2CoesConverter(OrbitChecker, OrbitalElements):
    '''
        Class converts the R & V vectors into classical orbital elements
        User has option of having elements in degrees or radians
        User also has the option of using Canonical units (defualt)
    '''
    def __init__(self, r: list, v: list, degrees: bool = True, mu: float = 1) -> None:
        self.degrees = degrees
        self.mu      = mu
        print("Made it here")

        # Initialize
        self.r                  = np.array(r)
        self.v                  = np.array(v)
        self.magR               = self.getMagnitude(self.r)
        self.magV               = self.getMagnitude(self.v)
        self.eccentricityVector = self.calculateEvector(self.r, self.v, self.mu)
        self.eccentricity       = self.calculateEccentricty(self.eccentricityVector)
        self.energy             = self.calculateEnergy(self.magR, self.magV, self.mu)
        self.momentumVector     = self.calculateHvector(self.r, self.v)
        self.magMomentum        = self.getMagnitude(self.momentumVector)
        

        if self.energy != 0:
            self.semiMajorAxis = self.calculateSemiMajorAxis(self.mu, self.energy)

        super().__init__(self.eccentricity, self.energy, self.semiMajorAxis)


        if self.thisOrbit != OrbitType.Circular:
            self.trueAnomoly = self.calculateTrueAnomaly(self.eccentricityVector, self.r, self.v)
        
        if self.thisOrbit != OrbitType.Parabolic:
            self.semiLatusRectum = self.calculateSemiLatusRectum(self.magMomentum, self.mu)
            self.meanMotion = self.calculateMeanMotion(self.semiMajorAxis, self.mu)

        
        self.normalVector         = self.calculateNvector(self.momentumVector)
        self.magNormal            = self.getMagnitude(self.normalVector)
        self.inclination          = self.calculateInclination(self.momentumVector)
        self.argOfPerigee         = self.calculateArgOfPerig(self.normalVector, self.eccentricityVector)
        self.rightAscension       = self.calculateRaan(self.normalVector)
        self.eccentricAnomoly     = self.calculateEccentricAnomoly(self.eccentricity, self.semiMajorAxis, self.trueAnomoly)
        self.longitudeOfPeriapsis = self.calculateLongPeriapsis(self.rightAscension, self.argOfPerigee)
        self.argOfLatitude        = self.calculateArgOfLat(self.trueAnomoly, self.argOfPerigee)
        self.trueLongitude        = self.calculateTrueLongitude(self.rightAscension, self.argOfPerigee, self.trueAnomoly)
        self.meanAnomaly          = self.calculateMeanAnomaly(self.eccentricAnnomoly, self.eccentricity)
        
        


    def getSemiLatusRectum(self)    -> float: return self.semiLatusRectum
    def getSemiMajorAxis(self)      -> float: return self.semiMajorAxis
    def getInclination(self)        -> float: return self.inclination
    def getArgOfPerig(self)         -> float: return self.argOfPerigee
    def getRaan(self)               -> float: return self.rightAscension
    def getTrueAnomaly(self)        -> float: return self.trueAnomoly
    def getEccentricity(self)       -> float: return self.eccentricity
    def getEccentricAnomaly(self)   -> float: return self.eccentricAnomoly
    def getMeanMotion(self)         -> float: return self.meanMotion
    def getOrbitEnergy(self)        -> float: return self.energy
    def getLongitudePeriapsis(self) -> float: return self.longitudeOfPeriapsis
    def getArgLatitude(self)        -> float: return self.argOfLatitude
    def getTrueLongitude(self)      -> float: return self.trueLongitude
    def getMeanAnomaly(self)        -> float: return self.meanAnomaly
    def getMagH(self)               -> float: return self.magMomentum
    def getMagN(self)               -> float: return self.magNormal
    def getMagE(self)               -> float: return self.eccentricity
    def getMagR(self)               -> float: return self.magR
    def getMagV(self)               -> float: return self.magV
    def getRVector(self)            -> np.array: return self.r
    def getVvector(self)            -> np.array: return self.v
    def getHvector(self)            -> np.array: return self.momentumVector
    def getEvector(self)            -> np.array: return self.eccentricityVector
    def getNvector(self)            -> np.array: return self.normalVector


    def getOrbitalElements(self) -> OrbitalElements:
        oe = OrbitalElements()

        oe.semiLatusRectum      = self.getSemiLatusRectum()
        oe.semiMajorAxis        = self.getSemiMajorAxis()
        oe.inclination          = self.getInclination()
        oe.argOfPerigee         = self.getArgOfPerig()
        oe.rightAscension       = self.getRaan()
        oe.trueAnomoly          = self.getTrueAnomaly()
        oe.eccentricity         = self.getEccentricity()
        oe.eccentricAnnomoly    = self.getEccentricAnomaly()
        oe.meanMotion           = self.getMeanMotion()
        oe.energy               = self.getOrbitEnergy()
        oe.longitudeOfPeriapsis = self.getLongitudePeriapsis()
        oe.argOfLatitude        = self.getArgLatitude()
        oe.trueLongitude        = self.getTrueLongitude()
        oe.magMomentum          = self.getMagH()
        oe.magNormal            = self.getMagN()
        oe.magR                 = self.getMagR()
        oe.magV                 = self.getMagV()
        oe.momentumVector       = self.getHvector()
        oe.eccentricityVector   = self.getEvector()
        oe.normalVector         = self.getNvector()
        oe.meanAnomaly          = self.getMeanAnomaly()

        return oe


    @staticmethod
    def getMagnitude(vec: np.array) -> float:
        i2 = vec[0]**2
        j2 = vec[1]**2
        k2 = vec[2]**2
        return math.sqrt(i2 + j2 + k2)


    @staticmethod
    def calculateNvector(momentumVec: np.array) -> np.array:
        k = np.array([0,0,1])
        return np.cross(k, momentumVec)


    @staticmethod
    def calculateHvector(r:np.array, v: np.array) -> np.array:
        return np.cross(r, v)


    @staticmethod
    def calculateEvector(r: np.array, v: np.array, mu: float) -> np.array:
        magR = Vector2CoesConverter.getMagnitude(r)
        magV = Vector2CoesConverter.getMagnitude(v)
        return 1/mu  * ((magV**2 - mu/magR) * r - (np.dot(r, v) * v))


    @staticmethod
    def calculateSemiLatusRectum(momentumMag: float, mu: float) -> float:
        return momentumMag**2 / mu
    

    @staticmethod
    def calculateSemiMajorAxis(mu: float, energy: float) -> float:
        return (-mu / (2 * energy))


    @staticmethod
    def calculateInclination(momentumVector: np.array, useDegrees: bool = True) -> float:
        magH = Vector2CoesConverter.getMagnitude(momentumVector)
        inclination = math.acos(momentumVector[2] / magH)

        return math.degrees(inclination) if useDegrees else  inclination 


    @staticmethod
    def calculateEccentricty(eccentricityVector: np.array) -> float:
        return Vector2CoesConverter.getMagnitude(eccentricityVector)


    @staticmethod
    def calculateTrueAnomaly(eccentrictyVector: np.array, rVector: np.array, vVector: np.array, useDegrees: bool = True) -> float:
        magR = Vector2CoesConverter.getMagnitude(rVector)
        eccentricity = Vector2CoesConverter.getMagnitude(eccentrictyVector)
        trueAnomaly = math.acos(np.dot(eccentrictyVector, rVector) / (eccentricity* magR))

        if (np.dot(rVector, vVector) > 0 and trueAnomaly > math.pi):
            trueAnomaly = 2 * math.pi - trueAnomaly
        elif (np.dot(rVector, vVector) < 0 and trueAnomaly < math.pi):
            trueAnomaly = 2 * math.pi - trueAnomaly

        return math.degrees(trueAnomaly) if useDegrees else  trueAnomaly 


    @staticmethod
    def calculateRaan(normalVector: np.array, useDegrees: bool = True) -> float:
        magN = Vector2CoesConverter.getMagnitude(normalVector)

        if magN == 0: return math.nan 

        raan = math.acos(normalVector[0] / magN)
        
        if normalVector[1] < 0:
            raan = 2 * math.pi - raan

        return math.degrees(raan) if useDegrees else  raan 


    @staticmethod
    def calculateArgOfPerig(normalVector: np.array, eccentricityVector: np.array, useDegrees: bool = True) -> float:
        magN = Vector2CoesConverter.getMagnitude(normalVector)
        eccentricity = Vector2CoesConverter.getMagnitude(eccentricityVector)

        if magN == 0 or eccentricity == 0: return math.nan 

        argOfPerig = math.acos(np.dot(normalVector, eccentricityVector) / (magN * eccentricity))

        if eccentricityVector[2] < 0:
            argOfPerig = 2*math.pi - argOfPerig

        return math.degrees(argOfPerig) if useDegrees else argOfPerig

    @staticmethod
    def calculateEccentricAnomoly(eccentricity: float, semiMajAxis: float, theta: float, degrees: bool = True) -> float:
        if semiMajAxis > 0.0:
            eccentricAnnomoly = math.acos( (eccentricity + math.cos(theta)) / 
                                            (1 + eccentricity*math.cos(theta)) )
            if theta > math.pi:
                eccentricAnnomoly = 2*math.pi - eccentricAnnomoly
        else:
            eccentricAnnomoly = math.acosh((eccentricity + math.cos(theta)) / (1 + eccentricity * math.cos(theta))) 

        return math.degrees(eccentricAnnomoly) if degrees else eccentricAnnomoly


    @staticmethod
    def calculateMeanMotion(semiMajorAxis: float, mu: float = 1) -> float:
        return math.sqrt(mu / abs(semiMajorAxis)**3)


    @staticmethod
    def calculateEnergy(magnitdeR: float, magnitudeV: float, mu: float) -> float:
        return (magnitudeV**2 / 2 - mu / magnitdeR)


    @staticmethod
    def calculateLongPeriapsis(raan: float, argOfPerig: float) -> float:
        return raan + argOfPerig


    @staticmethod
    def calculateArgOfLat(trueAnomaly: float, argOfPerig: float) -> float:
        return argOfPerig + trueAnomaly


    @staticmethod
    def calculateTrueLongitude(raan: float, argOfPerig: float, trueAnomaly: float) -> float:
        return raan + argOfPerig + trueAnomaly


    @staticmethod
    def calculateMeanAnomaly(eccentricAnomaly: float, eccentricity: float, useDegrees: bool = True) -> float:
        if useDegrees: eccentricAnomaly = math.radians(eccentricAnomaly)

        meanAnomoly = eccentricAnomaly - eccentricity * math.sin(eccentricAnomaly)

        return math.degrees(meanAnomoly) if useDegrees else meanAnomoly

    def printOrbitElements(self) -> None:
        print()
        print("{:=<45}".format(""))
        print("{:^45}".format("Orbit Parameters"))
        print("{:=<45}".format(""))
        print("{:<30}{}".format("Orbit Type", self.getOrbitTypeString()))
        print("{:-<30}{}".format("i Inclination",self.getInclination()))
        print("{:<30}{}".format("\u03B8 True Anomaly", self.getTrueAnomaly()))
        print("{:-<30}{}".format("p Semi-Latus Rectum", self.getSemiLatusRectum()))
        print("{:<30}{}".format("a Semi-Major Axis", self.getSemiMajorAxis()))
        print("{:-<30}{}".format("\u03A9 RAAN",self.getRaan()))
        print("{:<30}{}".format("\u03C9 Argument of Perigee",self.getArgOfPerig()))
        print("{:-<30}{}".format("e Eccentricity", self.getEccentricity()))
        print("{:<30}{}".format("Mean Motion", self.getMeanMotion()))
        print("{:-<30}{}".format("\u03B5 Energy", self.getOrbitEnergy()))
        print("{:<30}{}".format("Eccentric Anomoly", self.getEccentricAnomaly()))
        print("{:-<30}{}".format("\u03A0 Longitude Periapsis", self.getLongitudePeriapsis()))
        print("{:<30}{}".format("True Longitude", self.getTrueLongitude()))
        print("{:-<30}{}".format("Arg of Latitude", self.getArgLatitude()))
        print("{:=<45}".format(""))


    def printOrbitElementVectors(self) -> None:
        print()
        print("{:=<45}".format(""))
        print("{:^45}".format("Orbit Parameter Vectors"))
        print("{:=<45}".format(""))
        print("{:-<30}{}".format("Orbit Type", self.getOrbitTypeString()))
        print("{:<30}{}".format("H Vector", self.getHvector()))
        print("{:-<30}{}".format("E Vector", self.getEvector()))
        print("{:<30}{}".format("N Vector", self.getNvector()))
        print("{:-<30}{}".format("Mag H Vector", self.getMagH()))
        print("{:<30}{}".format("Mag N Vector", self.getMagN()))
        print("{:-<30}{}".format("Mag E Vector", self.getMagE()))
        print("{:<30}{}".format("Mag R Vector", self.getMagR()))
        print("{:-<30}{}".format("Mag V Vector", self.getMagV()))
        print("{:<30}{}".format("R Vector",self.getRVector()))
        print("{:-<30}{}".format("V Vector",self.getVvector()))
        print("{:=<45}".format(""))