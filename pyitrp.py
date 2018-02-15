import numpy as np

def test():

    x = np.arange(-5, 5.01, 0.1)
    y = np.copy(x)
    xx, yy = np.meshgrid(x, y)
    
    import matplotlib.pyplot as plt
    plt.figure()
    plt.imshow(ITRPCoef.evaluate(xx, yy, 0))
    plt.colorbar()
    plt.show()

class ITRPCoef(object):
    """ Container for coeficients describing spatial and temporal variations of the 
    Sea Ice Thickness Climatology """

    # Time & Space Variables (Table 2 of publication)

    # 1st order terms
    T = -0.079  # 0.007 1.000
    Y = -1.767  # 0.038 1.000
    COS = -0.233  # 0.032 1.000
    SIN = 0.296  # 0.024 1.000

    # 2nd order terms
    X2 = -0.329  # 0.017 1.000
    Y2 = 0.674  # 0.037 1.000
    COS2 = 0.162  # 0.028 0.953
    SIN2 = -0.226  # 0.021 1.000
    XSIN = -0.199  # 0.019 1.000

    # 3rd order terms
    X2Y = 0.398  # 0.024 1.000
    XY2 = 0.253  # 0.040 0.991
    XT2 = -0.002  # 0.000 1.000
    COS3 = 0.140  # 0.030 0.582
    SIN3 = 0.015  # 0.025 0.000

    def __init__(self):
        pass

    @classmethod
    def evaluate(cls, x, y, t):
        """ compute ITRP evaluation of given coordinate(s) x, y and fractional year t 
        XXX: This still needs to be confirmed to be the correct interpretation of equation 2
        """

        # Convert time input for sin/cos
        tdeg = 2.0 * np.pi * t

        # Conpute the terms of different order
        t0 = 0.0
        t1 = cls.Y*y + cls.COS*np.cos(tdeg) + cls.SIN*np.sin(tdeg) + cls.T*t
        t2 = cls.X2*x**2. + cls.Y2*y**2. + cls.COS2*np.cos(tdeg)**2. + cls.SIN2*np.sin(tdeg)**2. + cls.XSIN*x*np.sin(tdeg)
        t3 = cls.X2Y*x**2.*y + cls.XY2*x*y**2. + cls.XT2*x*t**2 + cls.COS3*np.cos(tdeg)**3. + cls.SIN3*np.sin(tdeg)**3. 

        return t0+t1+t2+t3


class ITRPClimatology(object):
    """ 
    
    Notes: 
    x, y is based on a Cartesian grid in units of 1000 km
    t: time coordinate in years relative to 2000
    COS = cos(2 * pi * yearfraction)
    SIN = sin(2 * pi * yearfraction)
    """

    coef = ITRPCoef()

    def __init__(self):
        pass


if __name__ == '__main__':
    test()