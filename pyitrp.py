import numpy as np
from pyproj import Proj

def test():

    x = np.arange(-2.5, 2.501, 0.02)
    y = np.copy(x)
    xx, yy = np.meshgrid(x, y)
    lons, lats = ITRPProj.geo_inverse(xx, yy)
    climsit = ITRPCoef.evaluate(xx, yy, 2.75)
    
    import matplotlib.pyplot as plt
    from mpl_toolkits.basemap import Basemap

    plt.figure(figsize=(5, 4), dpi=300)
    map = Basemap(epsg=ITRPProj.epsg, resolution="i", 
                  height=2.*np.amax(x)*1.e6, width=2.*np.amax(y)*1.e6)
    map.drawmapboundary(fill_color='0.2')
    map.fillcontinents(color='0.75', lake_color='0.75', zorder=200)
    map.drawcoastlines(linewidth=0.5, zorder=200)
    im = map.imshow(climsit, vmin=0, vmax=5, cmap=plt.get_cmap("plasma"))
    map.contour(lons, lats, climsit, linewidths=0.5, latlon=True, levels=np.arange(0, 6), colors="white")
    plt.colorbar(im)
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


class ITRPProj(object):
    """ Definition of the default ITRP projection and conversion between lat/lon and projection 
    coordinates. The projection is defined as the NSIDC SSMI North grid.

    Sources: 
        https://epsg.io/3411
        https://nsidc.org/data/atlas/epsg_3411.html
    """
    
    # Projection parameters
    epsg = 3411
    proj4 = "+proj=stere +lat_0=90 +lon_0=-45 +lat_ts=70 +a=6378273 +rf=298.2794111 +units=m"
    
    def __init__(self):
        pass

    @classmethod
    def geo_inverse(cls, x, y, unit="itrp"):
        scaling = 1.e6
        if unit == "m":
            scaling = 1.0
        proj = Proj(cls.proj4)
        return proj(x*scaling, y*scaling, inverse=True)


if __name__ == '__main__':
    test()