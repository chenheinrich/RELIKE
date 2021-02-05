import numpy as np
import os 

from .data_loader import DataLoader

class GaussianLikelihood():

    def __init__(self, dataset='pl18_zmax30'):
        self.dataset = dataset
        self._data_loader = DataLoader(self.dataset)
        self._invcov = self._load_pc_invcov()
        self._npc = self._invcov.shape[0]

    def get_loglike(self, mjs):
        """Returns the log likelihood given PC projection mjs.
        Args:
            mjs: 1d-numpy array of shape (5,) for the first 5 PC amplitudes.
        """

        if mjs.shape != (self._npc,):
            pass
            #TODO raise error 
        chi2 = np.matmul(mjs[np.newaxis,:], np.matmul(self._invcov, mjs[:, np.newaxis]))
        return -0.5 * chi2

    def _load_pc_invcov(self):
        invcov = self._data_loader.load_file('invcov.dat')
        return invcov
