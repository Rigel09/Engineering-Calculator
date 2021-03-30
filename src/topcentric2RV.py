import math
import numpy as np
from UniversalTOF import UniversalTimeOfFlight
from VectorCoesConverter import Vector2CoesConverter as v2cc
from VectorCoesConverter import OrbitType
from GaussTOF import GaussVelocityVecSolver
from KeplerTOF import KeplerTimeOfFlight as ktof
from CoordinateTransforms import CoordinateTransforms as ct


if __name__ == "__main__":
    print() # Get blank space in command line
    # Double check your units!
    rho = 3
    rhoDot = 0.4
    az = math.radians(30)     # Input degrees
    azDot = 0                 # rad / TU
    el = math.radians(10)     # Input degrees
    elDot = 0.1                  # Radian / TU
    timeGST = 0              # Hours
    localGST = 18           # Hours
    radarStationLongitude = math.radians(-106.6)  # Degrees  (+ East)
    radarStationLatitude = math.radians(32.5)
    radiusPlanet = 1   # Radius of planet the station is at in TU
    planetOmega = 7.292e-5 * 3600  # Rotation rate of planet in rad / hour
    planetOmegaConical = 0.0588    # Rotation rate of planet in rad / TU

    # Calculate the rho vectors in terms of SEZ
    rhoSEZ = ct.calculateRhoVectorSEZ(rho, el, az)
    rhoDotSEZ = ct.calculateRhoDotVectorSEZ(rho, rhoDot, el, az, elDot, azDot)

    # Calculate the radius vector in SEZ accounting for radius of planet
    rSEZ = rhoSEZ + np.array([0, 0, radiusPlanet])

    # Find theta for coord transform
    theta = timeGST + radarStationLongitude + planetOmega * localGST

    # Transformation matrix
    matrixD = ct.getTopoHorizon2Geocentric(radarStationLatitude, theta)

    # Radius Vector in geocentric frame
    rIJK = np.matmul(matrixD, rSEZ)

    # Velocity vecotrs in geocentric frame
    rhoDotIJK = np.matmul(matrixD, rhoDotSEZ)
    vIJK = rhoDotIJK + np.cross(np.array([0, 0, planetOmegaConical]), rIJK)

    # Show the output of each stage of calculation for documentation purposes
    print("RHO SEZ: {}".format(rhoSEZ))
    print("RSEZ: {}".format(rSEZ))
    print("rhoDotSEZ: {}".format(rhoDotSEZ))
    print()
    print("Theta: {}".format(theta))
    print()
    print("D Matrix")
    print(matrixD)
    print()
    print("R IJK: {}".format(rIJK))
    print("V IJK: {}".format(vIJK))
    print()
    v2cc(rIJK, vIJK).printOrbitElements()
    v2cc(rIJK, vIJK).printOrbitElementVectors()