import numpy as np
import matplotlib.pyplot as plt
import math

from .planetary_data import planetaryData as plDat
from .planetary_data import BasePlanet


class InvalidParams(Exception):
    ''' Excpetion thrown for invalid orbit parameters'''
    pass

class ResultCheck(Exception):
    ''' Exception thrown for an invalid calculated orbit parameter'''
    pass

class OrbitPropogationError(Exception):
    '''General orbit propogation error'''
    pass



def plot_n_orbits(rs: list, labels: list, colors: str, body: BasePlanet = plDat.getPlanetData("Earth"), showPlot: bool =True, savePlot: bool =False, title: str="orbit"):
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
