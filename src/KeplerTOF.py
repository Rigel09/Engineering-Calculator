import math
from src.VectorCoesConverter import Vector2CoesConverter



class KeplerTimeOfFlight():
    '''
    Brief: Calculates Time of Flight between peripasis and true annomoly

    Inputs:
        theta: True annomoly
        semimajor axis
        eccentricity
        mu
        inputDegrees: True signifies input is in degress (default)
    '''
    def __init__(self, theta1: float, theta2: float, semiMajorAxis: float, eccentricity: float, 
                mu: float = 1, inputDegrees: bool = True) -> None:

        self.theta1 = theta1
        self.theta2 = theta2
        self.semiMajorAxis = semiMajorAxis
        self.eccentricity = eccentricity
        self.mu = mu
        self.inputDegrees = inputDegrees
        self.numTimesPassPeriapsis = 0

        # If the input was in degrees go ahead and convert to radians
        if self.inputDegrees:
            self.theta1 = math.radians(self.theta1)
            self.theta2 = math.radians(self.theta2)

        if self.theta2 < self.theta1:
            self.numTimesPassPeriapsis += 1
        

    def calculateTOF(self) -> float:
        eccentricAnnom1 = Vector2CoesConverter.calculateEccentricAnomoly(self.eccentricity, self.semiMajorAxis, self.theta1, degrees=False)
        eccentricAnnom2 = Vector2CoesConverter.calculateEccentricAnomoly(self.eccentricity, self.semiMajorAxis, self.theta2, degrees=False)
        meanMot = Vector2CoesConverter.calculateMeanMotion(self.semiMajorAxis, self.mu)
        total1 = (eccentricAnnom1 - self.eccentricity * math.sin(eccentricAnnom1))
        total2 = (eccentricAnnom2 - self.eccentricity * math.sin(eccentricAnnom2))
        tof = (2 * self.numTimesPassPeriapsis * math.pi + total2 - total1) / meanMot
        return tof