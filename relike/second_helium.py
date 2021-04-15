import numpy as np

from . import constants 

class SecondHelium():

    def __init__(self):  

        self.helium_fullreion_redshiftstart = 5.0
        self.helium_fullreion_redshift = 3.5
        self.helium_fullreion_deltaredshift = 0.5

        self.yhe = constants.yhe
        self.mass_ratio_He_H = constants.mass_ratio_He_H
        self.fHe = self.yhe/(self.mass_ratio_He_H * (1.0 - self.yhe))

    def xe(self, z):
        """Second ionization of helium used in the fiducial model
        for PCs following default from CAMB. """
        xod = (1.0+self.helium_fullreion_redshift - (1.0+z))\
            /self.helium_fullreion_deltaredshift
        xe_helium_second = self.fHe * (1.0 + np.tanh(xod))/2.0
        return xe_helium_second