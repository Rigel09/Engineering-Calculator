import math
import numpy as np


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
    def getGeocentric2TopoHorizon(latitude: float, localSideRealTime: float) -> np.array:
        lat = latitude
        lst = localSideRealTime
        
        row1 = [math.sin(lat)*math.cos(lst),  math.sin(lat)*math.sin(lst), -math.cos(lat)]
        row2 = [-math.sin(lst), math.cos(lst), 0]
        row3 = [math.cos(lat)*math.cos(lst), math.cos(lat)*math.sin(lst), math.sin(lat)]

        return np.array([row1, row2, row3])


    @staticmethod
    def getTopoHorizon2Geocentric(latitude: float, localSideRealTime: float) -> np.array:
        return np.transpose(CoordinateTransforms.getGeocentric2TopoHorizon(latitude, localSideRealTime))

    @staticmethod
    def calculateRhoVectorSEZ(rho: float, el: float, az: float) -> np.array:
        '''Calculate the RHO Vector in TopoHorizon Frame, Angle must be in radians'''
        rhoS = -rho*math.cos(el)*math.cos(az)
        rhoE = rho*math.cos(el)*math.sin(az)
        rhoZ = rho*math.sin(el)
        return np.array([rhoS, rhoE, rhoZ])

    @staticmethod
    def calculateRhoDotVectorSEZ(rho: float, rhoDot: float, el: float, az: float, elDot: float, azDot: float) -> np.array:
        '''Calculate the RHO DOT Vector in TopoHorizon Frame, Angle must be in radians'''
        rhoDotS = -rhoDot*math.cos(el)*math.cos(az) + rho*math.sin(el)*elDot*math.cos(az) + rho*math.cos(el)*math.sin(az)*azDot
        rhoDotE = rhoDot*math.cos(el)*math.sin(az) - rho*math.sin(el)*elDot*math.sin(az) + rho*math.cos(el)*math.cos(az)*azDot
        rhoDotZ = rhoDot*math.sin(el) + rho*math.cos(el)*elDot
        return np.array([rhoDotS, rhoDotE, rhoDotZ])


    @staticmethod
    def calculateV2(velocity: np.array, delta: float) -> np.array:
        row1 = [math.cos(delta), math.sin(delta), 0]
        row2 = [math.sin(delta), math.cos(delta), 0]
        row3 = [0, 0, 1]
        transform = np.array([row1, row2,row3])
        return np.matmul(transform, velocity)