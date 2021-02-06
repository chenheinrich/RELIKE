#TODO add tanh xe(z) function here

import numpy as np

from . import constants 

def xe_tanh_pl18_best_fit(z):
    pass#return xe_tanh(z, zre=7.1) #TODO put in the right zre

def xe_tanh_pl18_single(z, zre=7.0):
    pass#return tanh.xe(z, zre=zre)

xe_tanh_pl18 = np.vectorize(xe_tanh_pl18_single)

class TanhModel():

    def __init__(self):
        self._setup()

    def _setup(self):

        self.reion_zexp = 1.5
        self.reion_delta_redshift = 0.5

        self.helium_fullreion_redshiftstart = 5.0
        self.helium_fullreion_redshift = 3.5
        self.helium_fullreion_deltaredshift = 0.5

        self.yhe = constants.yhe
        self.mass_ratio_He_H = constants.mass_ratio_He_H
        self.fHe = self.yhe/(self.mass_ratio_He_H * (1.0 - self.yhe))

        self.xstart = 0.0 # TODO might wanna do something with this

    def get_xe_func(self, zre):
        def xe_func(z, zre=zre):
            xe = self.xe_hydrogen(z, zre) + self.xe_helium(z)
            #TODO decide what to do with recomb: xe = xe - xe_recomb(z)	
            return xe	
        return xe_func
        #return np.vectorize(xe_func)

    def xe_helium(self, z):
        #TODO any difference when we abort this
        #if z > self.helium_fullreion_redshiftstart:
        #    return 0.0
        #else:
        xod = (1.0+self.helium_fullreion_redshift - (1.0+z))\
            /self.helium_fullreion_deltaredshift
        xe_helium = self.fHe * (1.0 + np.tanh(xod))/2.0
        return xe_helium

    def xe_hydrogen(self, z, zre):

        (WindowVarDelta, WindowVarMid) = self._get_yvar(zre) #TODO change name
        xod = (WindowVarMid - (1.0+z)**self.reion_zexp)/WindowVarDelta
        xe_hydrogen = ((1.0+self.fHe) - self.xstart)*(np.tanh(xod)+1.0)/2.0 + self.xstart

        return xe_hydrogen

    def _get_yvar(self, zre):

        WindowVarDelta = self.reion_zexp*(1.0+zre)**(self.reion_zexp-1.0)\
            *self.reion_delta_redshift
        WindowVarMid = (1.0+zre)**self.reion_zexp
        
        return (WindowVarDelta, WindowVarMid)

        
        #TODO turn into actual test
        #if zre == 10.0:
        #    print('Test: zre, WindowVarDelta, WindowVarMid = ', zre, WindowVarDelta, WindowVarMid) 
        #    print('Expect: 10.0, 0.25795162261908E+01, 0.40684689150538E+02')
        #    assert np.isclose(zre, 10.0)
        #    assert np.isclose(WindowVarDelta, 0.25795162261908E+01)
        #    assert np.isclose(WindowVarMid, 0.40684689150538E+02)
