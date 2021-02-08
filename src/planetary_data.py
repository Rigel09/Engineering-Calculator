class planetaryData:
    bodyList = ["Sun", "Mercury", "Venus", "Earth", "Moon", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]

    AU = 1.496e8  # km

    class base:
        name = None
        mass = None
        mu = None
        radius = None
        colormap = None
        qtColor = None
    
    class Sun:
        name = "Sun"
        mass = 1.989e30
        mu = 1.32712e11
        radius = 695700.0
        colormap = "Wistia"
        qtColor = (1, 1, 0, 1)
        DU = 696340     # km
        MU = 1.989e30   # kg
        TU = 57.13      # Days


    class Mercury:
        name = "Mercury"
        mass = 0.33e24
        mu = 398600.0
        radius = 2439.5
        colormap = "Blues"
        qtColor = (0, 0, 1, 1)
        DU = 6378.1   # km
        TU = 806.8    # Seconds
        MU = 5.972e24 # kg

    class Venus:
        name = "Venus"
        mass = 4.87e24
        mu = 398600.0
        radius = 6052
        colormap = "Blues"
        qtColor = (0, 0, 1, 1)
        DU = 6378.1   # km
        TU = 806.8    # Seconds
        MU = 5.972e24 # kg


    class Earth:
        name = "Earth"
        mass = 5.972e24
        mu = 398600.0
        radius = 6378
        colormap = "Blues"
        qtColor = (0, 0, 1, 1)
        DU = 6378.1   # km
        TU = 806.8    # Seconds
        MU = 5.972e24 # kg


    class Moon:
        name = "Moon"
        mass = 0.073e24
        mu = 398600.0
        radius = 1737.5
        colormap = "Blues"
        qtColor = (0, 0, 1, 1)
        DU = 6378.1   # km
        TU = 806.8    # Seconds
        MU = 5.972e24 # kg


    
    class Mars:
        name = "Mars"
        mass = 0.642e24
        mu = 398600.0
        radius = 3396
        colormap = "Blues"
        qtColor = (0, 0, 1, 1)
        DU = 6378.1   # km
        TU = 806.8    # Seconds
        MU = 5.972e24 # kg


    class Jupiter:
        name = "Jupiter"
        mass = 1898e24
        mu = 398600.0
        radius = 71492
        colormap = "Blues"
        qtColor = (0, 0, 1, 1)
        DU = 6378.1   # km
        TU = 806.8    # Seconds
        MU = 5.972e24 # kg


    class Saturn:
        name = "Saturn"
        mass = 568e24
        mu = 398600.0
        radius = 60268
        colormap = "Blues"
        qtColor = (0, 0, 1, 1)
        DU = 6378.1   # km
        TU = 806.8    # Seconds
        MU = 5.972e24 # kg



    class Uranus:
        name = "Uranus"
        mass = 86.8e24
        mu = 398600.0
        radius = 25559
        colormap = "Blues"
        qtColor = (0, 0, 1, 1)
        DU = 6378.1   # km
        TU = 806.8    # Seconds
        MU = 5.972e24 # kg


    class Neptune:
        name = "Neptune"
        mass = 102e24
        mu = 398600.0
        radius = 24764
        colormap = "Blues"
        qtColor = (0, 0, 1, 1)
        DU = 6378.1   # km
        TU = 806.8    # Seconds
        MU = 5.972e24 # kg



    class Pluto:
        name = "Pluto"
        mass = 0.0146e24
        mu = 398600.0
        radius = 1185
        colormap = "Blues"
        qtColor = (0, 0, 1, 1)
        DU = 6378.1   # km
        TU = 806.8    # Seconds
        MU = 5.972e24 # kg