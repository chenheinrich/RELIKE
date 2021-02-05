import numpy as np
import os

from .data_loader import DataLoader

class PC():

    def __init__(self, dataset='pl18_zmax30'):

        self.dataset = dataset
        self._data_loader = DataLoader(self.dataset)

        self.data = PCData(self.dataset)
        self.tau = PCTau(self.dataset)
        self.proj = PCProj(self.dataset)

    def get_mjs(self, xe_func):
        return self.proj.get_mjs(xe_func)

    def get_tau(self, mjs):
        return self.tau.get_tau(mjs)

class PCData():

    def __init__(self, dataset='pl18_zmax30'):

        self.dataset = dataset
        self._data_loader = DataLoader(self.dataset)

        (self.z, self.pc) = self._load_z_and_pc()
        self.npc = self.pc.shape[1]
        
    def _load_z_and_pc(self):
        data = self._data_loader.load_file('pc.dat') # TODO make sure to flip sign ahead of time
        z = data[:,0]
        pc = data[:,1:]
        return (z, pc)

class PCTau():

    def __init__(self, dataset='pl18_zmax30'):

        self._dataset = dataset
        self._data_loader = DataLoader(self._dataset)

        (self._taufid, self._taumj) = self._load_taufid_and_taumj()

    def _load_taufid_and_taumj(self):
        taumj = self._data_loader.load_file('taumj.dat') # TODO make sure to flip sign ahead of time
        taufid = self._data_loader.load_file('taufid.dat') 
        return (taufid, taumj)
    
    def get_tau(self, mjs):
        """Returns optical depth estimated using PC decomposition and cosmo parameters.
        Args:
            cosmo: ... <to fill>
        """
        tau = self._taufid + np.dot(self._taumj, mjs)
        rescale = self._get_tau_rescale()
        tau *= rescale
        return tau

    def _get_tau_rescale(self): #TODO add cosmo parameter scaling here
        return 1

class PCProj():   

    def __init__(self, dataset='pl18_zmax30'):

        self.pc_data = PCData(dataset)

    def get_mjs(self, xe_func):
        """Returns 1d numpy array of shape (npc,1) for pc amplitudes.
        Arg:
            xe_func: a function for the global ionization history xe(z),
                taking redshift z as input argument, valued on z = [6, 30].
        """
        return np.ones(5)
        #TODO fill here 
        #TODO test results

