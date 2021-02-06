import numpy as np
import os
from scipy import integrate
from scipy import interpolate

from .data_loader import DataLoader
from . import constants
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
        
        self.nz = self.pc.shape[0]
        self.npc = self.pc.shape[1]

        self.dz = self.z[2] - self.z[1]
        self.zmin = self.z[0] - self.dz
        self.zmax = self.z[-1] + self.dz

        self.xef = 0.15
        self.xe_lowz = self._get_xe_lowz()

        self.xe_mjs_func = [self._get_func_xe_mjs(j) for j in range(5)]
        self.xe_fid_func = self._get_func_xe_fid()
        self.xe_fid_func2 = np.vectorize(self.xe_fid_func_single_input)
    
    def _load_z_and_pc(self):
        data = self._data_loader.load_file('pc.dat') # TODO make sure to flip sign ahead of time
        z = data[:,0]
        pc = data[:,1:]
        return (z, pc)

    def _get_func_xe_mjs(self, j):
        """Returns a function that interpolates the jth PC, j = 0, 1, ..."""
        before = np.array([[0.0, 0.0], [self.zmin, 0.0]])
        after = np.array([[self.zmax, 0.0], [self.zmax+10, 0.0]])
        values = np.transpose(np.array([self.z, self.pc[:,j]]))
        values = np.vstack((before, values))
        values = np.vstack((values, after))
        return interpolate.interp1d(values[:,0], values[:,1], kind='linear')

    def _get_func_xe_fid(self):
        """Returns a function that interpolates the fiducial xe(z)."""
        values = np.array([\
                [0,          self.xe_lowz],\
                [self.zmin,  self.xe_lowz], \
                [self.z[0],  self.xef], \
                [self.z[-1], self.xef], \
                [self.zmax,  0.0], \
                [self.zmax+10,  0.0]\
            ])
        return interpolate.interp1d(values[:,0], values[:,1], kind='linear')

    def xe_fid_func_single_input(self, z):
        """Returns a function that interpolates the fiducial xe(z)."""
        
        if (z < self.zmin):
            xe_fiducial = self.xe_lowz
        elif (z > self.zmax):
            xe_fiducial = 0.
        else:
            if (z < self.z[0]):
                xe_fiducial = (z-self.zmin) * (self.xef-self.xe_lowz) / self.dz + self.xe_lowz
            elif (z > self.z[-1]):
                xe_fiducial = \
                    (z-self.z[-1]) * (0.-self.xef) / (self.dz) + self.xef
            else:
                xe_fiducial = self.xef

        return xe_fiducial
    
    def _get_xe_lowz(self): 
        yhe = constants.yhe
        mass_ratio_He_H = constants.mass_ratio_He_H
        xe_lowz = 1. + self._get_fhe(yhe, mass_ratio_He_H)
        return xe_lowz

    @staticmethod
    def _get_fhe(yhe, mass_ratio_He_H):
        fhe = yhe/(mass_ratio_He_H*(1 - yhe)) 
        return fhe

    def plot_xe(self, nz_test=1000):

        """Saves a plot of the PC and fiducial xe(z) functions as a check for interpolation."""
        
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()

        zmin = 0
        zmax = self.zmax+5
        zarray = np.linspace(zmin, zmax, nz_test)

        for j in range(self.npc):
            label_pc = r'$S_j(z), j=1..%s$'%self.npc if j==0 else '__nolegend__'
            ax.plot(zarray, self.xe_mjs_func[j](zarray), color='dodgerblue', lw=1,\
                label=label_pc)

        ax.plot(zarray, self.xe_fid_func(zarray), '-', color='tab:orange', lw=1,\
            label=r'$x_e^{\mathrm{fid}}(z)$')
        #ax.plot(zarray, self.xe_fid_func2(zarray), '--', lw=1)
        ax.legend()

        ax.axvline(x=self.zmin, color='k', lw=1)
        ax.axvline(x=self.zmax, color='k', lw=1)
        ax.axvline(x=self.z[0], color='k', lw=1)
        ax.axvline(x=self.z[-1], color='k', lw=1)

        ax.set_xlabel(r'$z$')
        ax.set_ylabel(r'$x_e(z)$')
        ax.set_xlim([zmin, zmax])

        fname = './plot_xe.pdf'
        plt.savefig(fname)
        print('Saved plot: {}'.format(fname))

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

    def get_mjs(self, xe_func, n_simpson=1000):
        """Returns 1d numpy array of shape (npc,1) for pc amplitudes.
        Arg:
            xe_func: a function for the global ionization history xe(z),
                taking redshift z as input argument, valued on z = [6, 30].
            n_simpson (optional): an integer for the number of z intervals
                to use for the integration with Simpson rule (if an odd 
                number is given, we add one automatically to make it even). 
        """

        npc = self.pc_data.npc

        if (n_simpson%2 == 1): 
            n_simpson= n_simpson+1

        zarray = np.linspace(self.pc_data.zmin, self.pc_data.zmax, n_simpson+1)
        xe_fid_array = self.pc_data.xe_fid_func(zarray) 

        xe_array = xe_func(zarray)

        mjs = np.zeros(npc)
        for j in range(npc):
            xe_mj_array = self.pc_data.xe_mjs_func[j](zarray)
            integrand = xe_mj_array * (xe_array - xe_fid_array)
            mjs[j] = integrate.simpson(integrand, zarray)
        mjs = mjs/(self.pc_data.zmax - self.pc_data.zmin) 

        return mjs

