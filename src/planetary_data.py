import math

class BasePlanet:
    name = "N/A"
    mass = math.nan
    mu = math.nan
    radius = math.nan
    colormap = "N/A"
    qtColor = (1, 1, 1, 1) # White

class Sun(BasePlanet):
    name = "Sun"
    mass = 1.989e30
    mu = 1.32712e11
    radius = 695700.0
    colormap = "Wistia"
    qtColor = (1, 1, 0, 1)
    DU = 696340     # km
    MU = 1.989e30   # kg
    TU = 57.13      # Days
    


class Mercury(BasePlanet):
    name = "Mercury"
    mass = 0.33e24
    mu = 398600.0
    radius = 2439.5
    colormap = "Blues"
    qtColor = (0, 0, 1, 1)
    DU = 6378.1   # km
    TU = 806.8    # Seconds
    MU = 5.972e24 # kg

class Venus(BasePlanet):
    name = "Venus"
    mass = 4.87e24
    mu = 398600.0
    radius = 6052
    colormap = "Blues"
    qtColor = (0, 0, 1, 1)
    DU = 6378.1   # km
    TU = 806.8    # Seconds
    MU = 5.972e24 # kg


class Earth(BasePlanet):
    name = "Earth"
    mass = 5.972e24
    mu = 398600.0
    radius = 6378
    colormap = "Blues"
    qtColor = (0, 0, 1, 1)
    DU = 6378.1   # km
    TU = 806.8    # Seconds
    MU = 5.972e24 # kg


class Moon(BasePlanet):
    name = "Moon"
    mass = 0.073e24
    mu = 398600.0
    radius = 1737.5
    colormap = "Blues"
    qtColor = (0, 0, 1, 1)
    DU = 6378.1   # km
    TU = 806.8    # Seconds
    MU = 5.972e24 # kg



class Mars(BasePlanet):
    name = "Mars"
    mass = 0.642e24
    mu = 398600.0
    radius = 3396
    colormap = "Blues"
    qtColor = (0, 0, 1, 1)
    DU = 6378.1   # km
    TU = 806.8    # Seconds
    MU = 5.972e24 # kg


class Jupiter(BasePlanet):
    name = "Jupiter"
    mass = 1898e24
    mu = 398600.0
    radius = 71492
    colormap = "Blues"
    qtColor = (0, 0, 1, 1)
    DU = 6378.1   # km
    TU = 806.8    # Seconds
    MU = 5.972e24 # kg


class Saturn(BasePlanet):
    name = "Saturn"
    mass = 568e24
    mu = 398600.0
    radius = 60268
    colormap = "Blues"
    qtColor = (0, 0, 1, 1)
    DU = 6378.1   # km
    TU = 806.8    # Seconds
    MU = 5.972e24 # kg



class Uranus(BasePlanet):
    name = "Uranus"
    mass = 86.8e24
    mu = 398600.0
    radius = 25559
    colormap = "Blues"
    qtColor = (0, 0, 1, 1)
    DU = 6378.1   # km
    TU = 806.8    # Seconds
    MU = 5.972e24 # kg


class Neptune(BasePlanet):
    name = "Neptune"
    mass = 102e24
    mu = 398600.0
    radius = 24764
    colormap = "Blues"
    qtColor = (0, 0, 1, 1)
    DU = 6378.1   # km
    TU = 806.8    # Seconds
    MU = 5.972e24 # kg



class Pluto(BasePlanet):
    name = "Pluto"
    mass = 0.0146e24
    mu = 398600.0
    radius = 1185
    colormap = "Blues"
    qtColor = (0, 0, 1, 1)
    DU = 6378.1   # km
    TU = 806.8    # Seconds
    MU = 5.972e24 # kg

planetDict = {
    "Sun"      : Sun,
    "Mercury"  : Mercury,
    "Venus"    : Venus,
    "Earth"    : Earth,
    "Moon"     : Moon,
    "Mars"     : Mars,
    "Jupiter"  : Jupiter,
    "Saturn"   : Saturn,
    "Uranus"   : Uranus,
    "Neptune"  : Neptune,
    "Pluto"    : Pluto
}

bodyList = ["Sun", 
            "Mercury", 
            "Venus", 
            "Earth", 
            "Moon", 
            "Mars", 
            "Jupiter", 
            "Saturn", 
            "Uranus", 
            "Neptune", 
            "Pluto"]


class planetaryData:
    def __init__(self) -> None:
        

        self.AU = 1.496e8  # km

    @staticmethod
    def getAvailableBodies() -> list: return bodyList

    @staticmethod
    def getPlanetData(planet: str = "Earth") -> BasePlanet: 
        if planet in planetDict:
            return planetDict.get(planet, BasePlanet)
        
        raise KeyError("{} not found in Dictionary.... available planets \n {}".format(planet, planetaryData.getAvailableBodies()))


