from math import degrees
import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.npyio import save
from scipy.integrate import ode

from .planetary_data import planetaryData as plDat
from src.planetary_data import Earth

from .OrbitTools import plot_n_orbits
from src.CoesToState import CoesToStateVectors
from src.General import OrbitalElements




class OrbitPropogator():
    def __init__(self, params: OrbitalElements, timeLength: float, timeStep: float, planet: Earth, useCoes: bool = False) -> None:
        super().__init__()
        self.r0 = params.r
        self.v0 = params.v
        self.timeSpan = timeLength
        self.dt = timeStep
        self.body = planet
        self.rs = None
        self.vs = None
        self.color = params.color
        self.params = params

        if useCoes:
            self.r0, self.v0 = CoesToStateVectors(params, self.body.mu)
        



    def getRadiusArray(self) -> np.array:
        return self.rs

    def getVelocityArray(self) -> np.array:
        return self.vs

    def propogateOrbit(self):
        n_steps = int(np.ceil(self.timeSpan/self.dt))

        ys = np.zeros((n_steps, 6))
        ts = np.zeros((n_steps, 1))

        y0 = self.r0 + self.v0
        ys[0] = np.array(y0)
        step = 1

        solver = ode(self.__diffyQ__)
        solver.set_integrator('lsoda')
        solver.set_initial_value(y0, 0)

        while solver.successful() and step < n_steps:
            solver.integrate(solver.t + self.dt)
            ts[step] = solver.t
            ys[step] = solver.y
            step += 1


        self.rs = ys[:,:3]
        self.vs = ys[:,3:]


    def plot(self, showPlot=True, savePlot=False, title="orbit"):
        if self.rs is None or self.vs is None:
            print("Error No data to plot")
            return

        fig = plt.figure(figsize=(10,10))
        ax = fig.add_subplot(111, projection='3d')


        ax.plot(self.rs[:,0], self.rs[:,1], self.rs[:,2], color='k')
        ax.plot([self.rs[0,0]], [self.rs[0,1]], [self.rs[0,2]], color='k', marker='o')

        r_plot = self.body.radius

        _u, _v = np.mgrid[0:2*np.pi:40j, 0:np.pi:30j]
        _x = r_plot * np.cos(_u) * np.sin(_v)
        _y = r_plot * np.sin(_u) * np.sin(_v)
        _z = r_plot * np.cos(_v)
        ax.plot_surface(_x, _y, _z, cmap=self.body.colormap)

        l = r_plot * 2.0
        x, y, z = [[0,0,0], [0,0,0], [0,0,0]]
        u, v, w = [[l,0,0], [0,l,0], [0,0,l]]
        ax.quiver(x,y,z,u,v,w,color='k')

        max_val = np.max(np.abs(self.rs))


        ax.set_xlim([-max_val, max_val])
        ax.set_ylim([-max_val, max_val])
        ax.set_zlim([-max_val, max_val])
        ax.set_xlabel("X (km)")
        ax.set_ylabel("Y (km)")
        ax.set_zlabel("Z (km)")

        plt.legend(['Trajectory', 'Starting Position'])
        
        if showPlot:
            plt.show()

        if savePlot:
            plt.savefig(title + ".png", dpi=300)


    def __diffyQ__(self, t, y):
        rx,ry,rz,vx,vy,vz=y

        r = np.array([rx,ry,rz])

        norm_r = np.linalg.norm(r)

        ax,ay,az = -r * self.body.mu / norm_r**3

        return [vx,vy,vz,ax,ay,az]





