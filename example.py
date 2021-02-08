from src.OrbitTools import plot_n_orbits
from src.OrbitPropagator import OrbitParams, OrbitPropogator
from src.planetary_data import planetaryData as plDat
import numpy as np


if __name__ == "__main__":

    orbits = []

    # ISS
    params = OrbitParams
    params.eccentricity = 0.0006189
    params.inclination = 51.6393
    params.trueAnnomoly = 0
    params.raan = 105.6372
    params.argOfPerig = 234.1955
    params.annomoly = plDat.Earth.radius + 414
    params.timeStep = 100
    params.timelength = 10000 * 60
    orb1 = OrbitPropogator(params, useCoes=True)
    orb1.propogateOrbit()
    orbits.append(orb1.getRadiusArray())



    # # GEO
    # params = OrbitParams
    # params.eccentricity = 0
    # params.inclination = 0
    # params.trueAnnomoly = 0
    # params.raan = 0
    # params.argOfPerig = 0
    # params.annomoly = plDat.Earth.radius + 35800
    # params.timeStep = 100
    # params.timelength = 10000 * 60
    # myOrbit = OrbitPropogator(params, useCoes=True)
    # myOrbit.propogateOrbit()
    # orbits.append(myOrbit.getRadiusArray())


    # # Random
    # params = OrbitParams
    # params.eccentricity = 0.3
    # params.inclination = 20
    # params.trueAnnomoly = 0
    # params.raan = 40
    # params.argOfPerig = 15
    # params.annomoly = plDat.Earth.radius + 3000
    # params.timeStep = 100
    # params.timelength = 10000 * 60
    # myOrbit = OrbitPropogator(params, useCoes=True)
    # myOrbit.propogateOrbit()
    # orbits.append(myOrbit.getRadiusArray())

    # plot_n_orbits(orbits, ["0", "1", "2"], ["b", "g", "r"])






    # orbits = []

    # rmag =plDat.Earth.radius + 1000 
    # r0 = [rmag, 0, 0]
    # vmag = np.sqrt(plDat.Earth.mu/rmag) * 1.3
    # v0 = [0, vmag, 0.8]

    # tspan = 10000 * 60

    # dt = 100

    # myOrbit = OrbitPropogator(r0, v0, tspan, dt)
    # myOrbit.propogateOrbit()
    # orbits.append(myOrbit.getRadiusArray())



    # rmag =plDat.Earth.radius + 400
    # r0 = [rmag, 0, 0]
    # vmag = np.sqrt(plDat.Earth.mu/rmag)
    # v0 = [0, vmag, 0]

    # tspan = 10000 * 60

    # dt = 100

    # myOrbit = OrbitPropogator(r0, v0, tspan, dt)
    # myOrbit.propogateOrbit()
    # orbits.append(myOrbit.getRadiusArray())

    # plot_n_orbits(orbits, ["0", "1"], ["b", "g"])