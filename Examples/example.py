from MohrCirclePropogator import MohrCirclePropogator as mcp
from MohrCirclePropogator import MohrCircle3DValues as mc3dVals

if __name__ == "__main__":
    myCircle = mcp(30, 20, 66, 10)
    myCircle.calculateMohrCircleValues()
    myCircle.plotMohrCircle2D()

    vals = mc3dVals
    vals.sigmaX = 30
    vals.sigmaY = 40
    vals.sigmaZ = 50
    vals.tauXY = 40
    vals.tauXZ = 40
    vals.tauYZ = 40

    myCircle.calculateMohrCircle3D(vals)
    myCircle.plotMohrCircle3D(vals)