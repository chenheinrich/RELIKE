import numpy as np

from . import constants 
from .second_helium import SecondHelium

class TanhModel():

    def __init__(self):
        self._setup()

    def _setup(self):

        self.reion_zexp = 1.5

        self.yhe = constants.yhe
        self.mass_ratio_He_H = constants.mass_ratio_He_H
        self.fHe = self.yhe/(self.mass_ratio_He_H * (1.0 - self.yhe))

        self.xe_helium_second = SecondHelium().xe

        self.xstart = 0.0 # TODO might wanna do something with this

    def get_xe_func(self, zre):
        def xe_func(z, zre=zre):
            return (self.xe_hydrogen(z, zre) + self.xe_helium_second(z))
        return xe_func

    def xe_hydrogen(self, z, zre):
        """Hydrogen + singly ionized helium"""

        (WindowVarDelta, WindowVarMid) = self._get_yvar(zre) 
        xod = (WindowVarMid - (1.0+z)**self.reion_zexp)/WindowVarDelta
        xe_hydrogen = ((1.0+self.fHe) - self.xstart)*(np.tanh(xod)+1.0)/2.0 + self.xstart

        return xe_hydrogen

    def _get_yvar(self, zre):
        
        reion_delta_redshift = 0.015 * (1.0+zre)
        WindowVarDelta = self.reion_zexp*(1.0+zre)**(self.reion_zexp-1.0)\
            *reion_delta_redshift
        WindowVarMid = (1.0+zre)**self.reion_zexp
        
        return (WindowVarDelta, WindowVarMid)
