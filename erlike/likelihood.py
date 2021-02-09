import numpy as np
import os 

from .data_loader import DataLoader

class GaussianLikelihood():

    def __init__(self, dataset='pl18_zmax30'):
        self.dataset = dataset
        self._data_loader = DataLoader(self.dataset)
        self._invcov = self._load_pc_invcov()
        self._npc = self._invcov.shape[0]
        self._mjs_mean = self._load_pc_mean()

    def get_loglike(self, mjs):
        """Returns the log likelihood given PC projection mjs.
        Args:
            mjs: 1d-numpy array of shape (5,) for the first 5 PC amplitudes.
        """

        if mjs.shape != (self._npc,):
            pass
            #TODO raise error 
        #chi2 = np.matmul(mjs[np.newaxis,:], np.matmul(self._invcov, mjs[:, np.newaxis]))

        dmjs = mjs - self._mjs_mean
        chi2 = np.matmul(dmjs, np.matmul(self._invcov, np.transpose(dmjs)))
        return -0.5 * chi2

    def _load_pc_invcov(self):
        return self._data_loader.load_file('invcov.dat')

    def _load_pc_mean(self):
        return self._data_loader.load_file('mean.dat')

