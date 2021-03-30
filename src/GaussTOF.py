import math
import numpy as np
from src.VectorCoesConverter import Vector2CoesConverter




class GaussVelocityVecSolver():
    def __init__(self, r1: list, r2: list, tof: float, mu: float = 1, transferType: str = "Short", verbose: bool = False) -> None:
        self.r1 = np.array(r1)
        self.r2 = np.array(r2)
        self.mu = mu
        self.magR1 = Vector2CoesConverter.getMagnitude(self.r1)
        self.magR2 = Vector2CoesConverter.getMagnitude(self.r2)
        self.constA = 0
        self.theta = 0
        self.tof = tof
        self.transferType = transferType
        self.tolerance = 1e-7
        self.verbose = verbose  # Include extra print statemnets of iterations
        self.__checkTransferType__()
        self.__calculateTheta__()
        self.__calculateA__()
        

    def __calculateTheta__(self):
        self.theta = math.acos(np.dot(self.r1, self.r2) / (self.magR1 * self.magR2))

        if self.transferType == "Long":
            self.theta = 2 * math.pi - self.theta

        
    def __calculateA__(self):
        self.constA = math.sqrt(self.magR1 * self.magR2) * math.sin(self.theta) / \
            math.sqrt(1 - math.cos(self.theta))
    
    def __checkTransferType__(self) -> None:
        if self.transferType != "Short" and self.transferType != "Long":
            raise ValueError("Incorrect Transfer Type! Valid Types {} & {}".format("Short", "Long"))

    
    def __calculateS__(self, z: float) -> float:
        s = 0
        
        if abs(z) < 0.001:
            fact = 3
            s = 0
            for ii in range(200):
                s += z**ii / math.factorial(fact)
                fact += 2
        
        elif z > 0:
            sqrtz = math.sqrt(z)
            s = (sqrtz - math.sin(sqrtz)) / math.sqrt(z**3)
        
        elif z < 0:
            sqrtz = math.sqrt(-z)
            s = (math.sinh(sqrtz) - sqrtz) / math.sqrt(abs(z)**3)
        
        return s

    
    def __calculateC__(self, z: float) -> float:
        c = 0
        
        if abs(z) < 0.001:
            fact = 2
            c = 0
            for ii in range(200):
                c += z**ii / math.factorial(fact)
                fact += 2
        
        elif z > 0:
            sqrtz = math.sqrt(z)
            c = (1 - math.cos(sqrtz)) / z
        
        elif z < 0:
            sqrtz = math.sqrt(-z)
            c = (1 - math.cosh(sqrtz)) / z
        
        return c

    def __calculateY__(self, z: float, s: float, c: float) -> float:
        return (self.magR1 + self.magR2 - self.constA * (1 - z * s) / math.sqrt(c))
    
    def __calculateTOF__(self, x: float, s: float, y: float) -> float:
        return (x**3 * s + self.constA * math.sqrt(y)) / math.sqrt(self.mu)

    def __calculateX__(self, c: float, y: float) -> float:
        return math.sqrt(y / c)

    def __calculateDSDZ__(self, c: float, s: float, z: float) -> float:
        return (c - 3 * s) / ( 2 * z)

    def __calculateDCDZ__(self, c: float, s: float, z: float) -> float:
        return (1 - z * s - 2 * c) / ( 2 * z)

    def __calculateDTDZ__(self, x: float, y: float, z: float, s: float, c: float) -> float:
        dsdz = self.__calculateDSDZ__(c, s, z)
        dcdz = self.__calculateDCDZ__(c, s, z)
        return (x**3 * (dsdz - (3 * s * dcdz) / (2 * c)) + self.constA / 8 * \
                (3 * s * math.sqrt(y) / c + self.constA / x))

    def __calculateF__(self, y: float) -> float:
        return (1 - y / self.magR1)

    def __calculateFDot__(self, s: float, x: float, z: float) -> float:
        return (-math.sqrt(self.mu) * x * (1 - z * s) / (self.magR1 * self.magR2))
    
    def __calculateG__(self, y: float) -> float:
        return (self.constA * math.sqrt(y / self.mu))

    def __calculateGDot__(self, y: float) -> float:
        return (1 - y / self.magR2)

    def __calculateV1__(self, f: float, g: float) -> np.array:
        return (self.r2 - f * self.r1) / g

    def __calculateV2__(self, g: float, gdot: float) -> np.array:
        return (gdot * self.r2 - self.r1) / g
    
    def checkFG(self, f: float, fDot: float, g: float, gDot: float) -> bool:
        return (((f * gDot - fDot * g) - 1) < 0.001)

    def calculateV1V2(self) -> None:
        z = 2 * math.pi
        deltaTOF = 100

        if self.verbose:
            print("{}{:=<90}{}".format("|", "", "|"))
            print("{}{:^15}{:^15}{:^15}{:^15}{:^15}{:^15}{}".format("|", "z", "y", \
                "x", "t", "dt/dz", "Znew", "|"))
            print("{}{:=<90}{}".format("|", "", "|"))

        while abs(deltaTOF) > self.tolerance:
            c = self.__calculateC__(z)
            s = self.__calculateS__(z)
            y = self.__calculateY__(z, s, c)
            x = self.__calculateX__(c, y)
            time = self.__calculateTOF__(x, s, y)
            deltaTOF = self.tof - time
            dtdz = self.__calculateDTDZ__(x, y, z, s, c)
            znew = z + deltaTOF / dtdz
            if self.verbose:
                print("{}{:^15}{:^15}{:^15}{:^15}{:^15}{:^15}{}".format("|", round(z, 4), round(y, 4), round(x, 4), \
                    round(time, 4), round(dtdz, 4), round(znew, 4), "|"))
            z = znew

        if self.verbose:
            print("{}{:=<90}{}".format("|", "", "|"))
        
        f = self.__calculateF__(y)
        g = self.__calculateG__(y)
        gdot = self.__calculateGDot__(y)
        v1 = self.__calculateV1__(f, g)
        v2 = self.__calculateV2__(g, gdot)

        return v1, v2
