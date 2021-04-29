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

    def get_loglike(self, mjs, normalize=True):
        """Returns the log likelihood given PC projection mjs.
        Args:
            mjs: 1d-numpy array of shape (5,) for the first 5 PC amplitudes.
        """

        #TODO raise error if mjs.shape != (self._npc,):

        dmjs = mjs - self._mjs_mean
        loglike = -0.5 * np.matmul(dmjs, np.matmul(self._invcov, np.transpose(dmjs)))

        if normalize == True:
            loglike_tanh_best_fit = -0.4581744062705327
            loglike -= loglike_tanh_best_fit 
            
        return loglike

    def _load_pc_invcov(self):
        return self._data_loader.load_file('invcov.dat')

    def _load_pc_mean(self):
        return self._data_loader.load_file('mean.dat')

