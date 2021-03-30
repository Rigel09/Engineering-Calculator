import math
import numpy as np
from .VectorCoesConverter import Vector2CoesConverter, OrbitType


class UniversalTimeOfFlight(Vector2CoesConverter):
    def __init__(self, r: list, v: list, tof: float, initialGuess: float = 0, mu: float = 1, verbose: bool = False) -> None:
        self.r = np.array(r)
        self.v = np.array(v)
        self.tof = tof
        self.initialGuess = initialGuess
        self.mu = mu
        super().__init__(self.r, self.v, degrees=False, mu=self.mu)
        self.converganceTol = 1e-7
        self.verbose = verbose
        self.rdotv = np.dot(self.r, self.v)
        self.sqrtA = 0
        self.sqrtMuA = 0

        if self.thisOrbit == self.Circular or self.thisOrbit == self.Ellipse:
            self.sqrtA = math.sqrt(self.semiMajorAxis)
            self.sqrtMuA = math.sqrt(self.mu * self.semiMajorAxis)

    def calculateZ(self, x: float) -> float:
        if self.thisOrbit == self.Parabolic:
            return 0
        else:
            return (x**2 / self.semiMajorAxis)

    
    def calculateS(self, x: float) -> float:
        z = self.calculateZ(x)
        s = 0
        
        if abs(z) < 0.001:
            s = 1/6

        elif z > 0:
            sqrtz = math.sqrt(z)
            s = (sqrtz - math.sin(sqrtz)) / math.sqrt(z**3)
        
        elif z < 0:
            sqrtz = math.sqrt(-z)
            s = (math.sinh(sqrtz) - sqrtz) / math.sqrt(abs(z)**3)
        
        return s

    
    def calculateC(self, x: float) -> float:
        z = self.calculateZ(x)
        c = 0
        
        if abs(z) < 0.001:
            c = 0.5

        
        elif z > 0:
            sqrtz = math.sqrt(z)
            c = (1 - math.cos(sqrtz)) / z
        
        elif z < 0:
            sqrtz = math.sqrt(-z)
            c = (1 - math.cosh(sqrtz)) / z
        
        return c




    def calculateT(self, x: float) -> float:
        if self.thisOrbit == self.Circular or self.thisOrbit == OrbitType.Ellipse:
            time = self.semiMajorAxis * (x - self.sqrtA * math.sin(x/self.sqrtA)) + \
                    self.rdotv / math.sqrt(self.mu) * self.semiMajorAxis * (1 - math.cos(x/self.sqrtA)) + \
                    self.magR * self.sqrtA * math.sin(x/self.sqrtA)
        
        else:
            s = self.calculateS(x)
            c = self.calculateC(x)
            z = self.calculateZ(x)
            time = (x**3 * s + self.rdotv / math.sqrt(self.mu) * x**2 * c + self.magR * x * (1 - z * s)) / math.sqrt(self.mu)

        return time

    
    def calcdtdx(self, x: float) -> float:
        if self.thisOrbit == self.Circular or self.thisOrbit == OrbitType.Ellipse:
            dtdx = (self.semiMajorAxis + self.semiMajorAxis * (self.rdotv / math.sqrt(self.mu * self.semiMajorAxis) * \
                math.sin(x/self.sqrtA) + (self.magR / self.semiMajorAxis - 1) * math.cos(x/self.sqrtA))) / math.sqrt(self.mu)
        else:
            s = self.calculateS(x)
            c = self.calculateC(x)
            z = self.calculateZ(x)
            dtdx = x**2 * c + self.rdotv / math.sqrt(self.mu) * x * (1 - z * s) + self.magR * (1 - z * c)

        return dtdx


    def findX(self) -> float:
        deltaTOF = 100

        if self.thisOrbit == self.Circular or self.thisOrbit == self.Ellipse and self.initialGuess == 0:
            self.initialGuess = math.sqrt(self.mu) * self.tof / self.semiMajorAxis

        x = self.initialGuess
        
        if self.verbose:
            print("{}{:=<45}{}".format("|", "", "|"))
            print("{}{:^15}{:^15}{:^15}{}".format("|", "Xn", "\u0394tn", "dt/dx", "|"))
            print("{}{:=<45}{}".format("|", "", "|"))

        while abs(deltaTOF) > self.converganceTol:
            t = self.calculateT(x)
            deltaTOF = self.tof - t
            dtdx = self.calcdtdx(x)

            if self.verbose:
                print("{}{:^15}{:^15}{:^15}{:^15}{}".format("|", round(x, 4), round(deltaTOF, 4), round(dtdx, 4), round(t, 4), "|"))

            x = x + deltaTOF / dtdx
        
        if self.verbose:
            print("{}{:=<45}{}".format("|", "", "|"))

        return x

    def calculateF(self, x: float) -> float:
        if self.thisOrbit == self.Circular or self.thisOrbit == OrbitType.Ellipse:
            return (1 - self.semiMajorAxis / self.magR * (1 - math.cos(x / self.sqrtA)))
        else:
            c = self.calculateC(x)
            return 1 - x**2 / self.magR * c
    
    def calculateFDot(self, x: float, magR2: float) -> float:
        if self.thisOrbit == self.Circular or self.thisOrbit == OrbitType.Ellipse:
            return (-math.sqrt(self.mu * self.semiMajorAxis) * math.sin(x / self.sqrtA) / (magR2 * self.magR))
        else:
            z = self.calculateZ(x)
            s = self.calculateS(x)
            return (math.sqrt(self.mu) * x / (self.magR * magR2) * (z * s - 1))
    
    def calculateG(self, x: float) -> float:
        if self.thisOrbit == self.Circular or self.thisOrbit == OrbitType.Ellipse:
            return (self.semiMajorAxis**2 / self.sqrtMuA * (np.dot(self.r, self.v) / self.sqrtMuA * (1 - math.cos(x / self.sqrtA)) + \
                self.magR / self.semiMajorAxis * math.sin(x / self.sqrtA)))
        else:
            s = self.calculateS(x)
            return (self.tof - x**3 / math.sqrt(self.mu) * s)
    
    def calculateGDot(self, x: float, magR2: float) -> float:
        if self.thisOrbit == self.Circular or self.thisOrbit == OrbitType.Ellipse:
            return (1 - self.semiMajorAxis / magR2 + self.semiMajorAxis / magR2 * math.cos(x / self.sqrtA))
        else:
            c = self.calculateC(x)
            return (1 - x**2 / magR2 * c)

    def checkFG(self, f: float, fDot: float, g: float, gDot: float) -> bool:
        return (((f * gDot - fDot * g) - 1) < 0.01)
    
    def calculateR2V2(self) -> tuple:
        x = self.findX()

        f = self.calculateF(x)
        g = self.calculateG(x)
        r2 = f * self.r + g * self.v
        magR2 = self.getMagnitude(r2)
        gDot = self.calculateGDot(x, magR2)
        fDot = self.calculateFDot(x, magR2)
        v2 = fDot * self.r + gDot * self.v

        if (self.checkFG(f, fDot, g, gDot)):
            return (r2, v2)
        else:
            print("FG Check failed in Universal Time Of Flight Calculation")
            print("f: {}   fDot: {}".format(f, fDot))
            print("g: {}   gDot: {}".format(g, gDot))
            print("Result: {}".format((f * gDot - fDot * g)))
            return (None, None)