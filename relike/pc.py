import numpy as np
import os
from scipy import integrate
from scipy import interpolate

from .data_loader import DataLoader
from . import constants
from .second_helium import SecondHelium

class PC():

    def __init__(self, dataset='pl18_zmax30'):

        self.dataset = dataset
        self._data_loader = DataLoader(self.dataset)

        self.data = PCData(self.dataset)
        self.tau = PCTau(self.dataset)
        self.proj = PCProj(self.dataset)

    def get_mjs(self, xe_func):
        return self.proj.get_mjs(xe_func)

    def get_tau(self, mjs, **kwargs):
        return self.tau.get_tau(mjs, **kwargs)

    def plot_pc(self, *args, **kwargs):
        return self.data.plot_pc(*args, **kwargs)

    def plot_xe(self, mjs, **kwargs):
        return self.data.plot_xe(mjs, **kwargs)

    def plot_tau_cumulative(self, mjs, plot_name='./plot_cumulative_tau.pdf'):

        """Saves a plot of tau(>z) given input mjs.
        """
        
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()

        zmin =  0
        zmax = self.data.zmax+5
        #zarray = np.linspace(zmin, zmax, nz_test)

        assert mjs.size == self.data.npc, (mjs.size, self.data.npc)
        
        (zarray, tau_cum) = self.tau.get_tau_cumulative(mjs, use_fiducial_cosmology=True)
        label_tau_from_mjs = 'm = [' + ', '.join(['%.2f'%m for m in mjs]) + ']'
        ax.plot(zarray, tau_cum, '-', lw=1,\
            label=label_tau_from_mjs)
        
        ax.legend()

        ax.axvline(x=self.data.zmin, color='k', lw=1)
        ax.axvline(x=self.data.zmax, color='k', lw=1)
        ax.axvline(x=self.data.z[0], color='k', lw=1)
        ax.axvline(x=self.data.z[-1], color='k', lw=1)

        ax.set_xlabel(r'$z$')
        ax.set_ylabel(r'$\tau(z, z_{\mathrm{max}})$')
        ax.set_xlim([zmin, zmax])

        plt.savefig(plot_name)
        print('Saved plot: {}\n'.format(plot_name))

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

        self.xe_helium_second = SecondHelium().xe

        self.xe_mjs_func = [self._get_func_xe_mjs(j) for j in range(self.npc)]
        self.xe_fid_func = self._get_func_xe_fid()
    
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
        xe_fid_func_no_helium = interpolate.interp1d(values[:,0], values[:,1], kind='linear') 
        
        def xe_fid_func(z):
            xe = xe_fid_func_no_helium(z) + self.xe_helium_second(z)
            return xe

        return xe_fid_func

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

    def plot_pc(self, nz_test=1000, plot_file_name=None):
        """
        Plot the first few PC functions and the fiducial xe(z).
        
        Args:
            nz_test (optional): An integer, for the number of redshift points 
                used for the plot.
            plot_file_name (optional): A string for the file path of the plot
                to save; no plot is saved if plot_file_name=None. 
        """
        
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
        ax.legend()

        ax.axvline(x=self.zmin, color='k', lw=1)
        ax.axvline(x=self.zmax, color='k', lw=1)
        ax.axvline(x=self.z[0], color='k', lw=1)
        ax.axvline(x=self.z[-1], color='k', lw=1)

        ax.set_xlabel(r'$z$')
        ax.set_ylabel(r'$x_e(z)$')
        ax.set_xlim([zmin, zmax])

        if plot_file_name is not None:
            plt.savefig(plot_file_name)
            print('Saved plot: {}\n'.format(plot_file_name))

    def plot_xe(self, mjs, plot_name='plot_xe.pdf', \
            xe_file_name=None, label_xe_from_file=None, \
            xe_func=None, label_xe_from_func=None, \
            nz_test=1000):

        """Saves a plot of xe(z) given input mjs.
        - If xe_file_name is specified, it also plots xe(z) from the file
         which should be in the form of two columns: z and xe(z). 
        - If xe_func is specified, it also plots xe(z) between 0 and zmax+5, 
          where zmax is the PC zmax. 
        """
        
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()

        zmin =  0
        zmax = self.zmax+5
        zarray = np.linspace(zmin, zmax, nz_test)

        assert mjs.size == self.npc, (mjs.size, self.npc)
        
        xe = self.xe_fid_func(zarray) + \
            np.sum(np.array([mjs[j] * self.xe_mjs_func[j](zarray) for j in range(self.npc)]), axis=0)
        label_xe_from_mjs = 'm = [' + ', '.join(['%.2f'%m for m in mjs]) + ']'
        ax.plot(zarray, xe, '-', lw=1,\
            label=label_xe_from_mjs)

        if xe_func is not None:
            if label_xe_from_func is None:
                label_xe_from_func = r'$x_e(z)$ from function'
            ax.plot(zarray, xe_func(zarray), '-', lw=1,\
                label=label_xe_from_func)

        if xe_file_name is not None:
            print('Plotting from input file: {}'.format(xe_file_name))
            xe2 = np.genfromtxt(xe_file_name)
            if label_xe_from_file is None:
                label_xe_from_file = r'$x_e(z)$ from file'
            ax.plot(xe2[:,0], xe2[:,1], '--', lw=1,\
                label=label_xe_from_file)
        
        ax.legend()

        ax.axvline(x=self.zmin, color='k', lw=1)
        ax.axvline(x=self.zmax, color='k', lw=1)
        ax.axvline(x=self.z[0], color='k', lw=1)
        ax.axvline(x=self.z[-1], color='k', lw=1)

        ax.set_xlabel(r'$z$')
        ax.set_ylabel(r'$x_e(z)$')
        ax.set_xlim([zmin, zmax])

        plt.savefig(plot_name)
        print('Saved plot: {}\n'.format(plot_name))


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

class PCTau():

    def __init__(self, dataset='pl18_zmax30'):

        self._dataset = dataset
        self._data_loader = DataLoader(self._dataset)

        (self._taufid, self._taumj) = self._load_taufid_and_taumj()

        (self._zarray_cum, self._taufid_cum, self._taumj_cum) = \
            self._load_zarray_and_taufid_and_taumj_cum()

        self._cosmo_fid = self._load_cosmo_fid()

        self._tau_prefactor_fid = self._get_tau_prefactor_fid()

        #print('Fiducial cosmology '+
        #    '(used for tau estimation with PC): {}\n'.format(self._cosmo_fid))

    def _load_taufid_and_taumj(self):
        taumj = self._data_loader.load_file('taumj.dat') 
        taufid = self._data_loader.load_file('taufid.dat') #xe_helium included
        return (taufid, taumj)

    def _load_zarray_and_taufid_and_taumj_cum(self):
        """Returns 1d numpy array for zarray and taufid cumulative, and 
        2d numpy array of shape (nz, npc) for taumj cumulative."""

        taumj_cum = self._data_loader.load_file('taumj_cumulative.dat') 
        taufid_cum = self._data_loader.load_file('taufid_cumulative.dat') #xe_helium included
    
        self._check_zarray_are_same(taufid_cum[:,0], taumj_cum[:,0])
        zarray = taufid_cum[:,0]

        return (zarray, taufid_cum[:, 1], taumj_cum[:, 1:])

    def _check_zarray_are_same(self, z1, z2):
        assert np.allclose(z1, z2)

    def _load_cosmo_fid(self):
        cosmo_fid = self._data_loader.load_yaml('fiducial_cosmology.yaml')
        return cosmo_fid
    
    def _get_tau_prefactor_fid(self):
        tau_prefactor_fid = self._get_tau_prefactor(\
            self._cosmo_fid['omegabh2'],
            self._cosmo_fid['omegamh2'], 
            self._cosmo_fid['yheused']
            )
        return tau_prefactor_fid

    def get_tau(self, mjs, use_fiducial_cosmology=True, omegabh2=None, omegamh2=None, yheused=None):
        """Returns optical depth estimated using PC projection.
        Args:
            mjs: A 1d numpy array of size npc.
            use_fiducial_cosmology (optional): A boolean for whether you 
                want to use the fiducial cosmology or a different set of 
                cosmological parameters, ONLY for the purpose of rescaling 
                tau for a different cosmology; BE CAREFUL that the loglike
                code does not support cosmologies inconsistent with 
                Planck 2018). When use_fiducial_cosmology = False, you also
                need to specify omegabh2, omegamh2 and yheused all at the 
                same time, and the returned tau will be scaled accordingly. 
            omegabh2 (optional): A float or a numpy array for baryon density;
                used when use_fiducial_cosmology = False.
            omegamh2 (optional): A float or a numpy array for matter density;
                used when use_fiducial_cosmology = False.
            yheused (optional): A float or a numpy array for helium fraction;
                used when use_fiducial_cosmology = False.
        """

        tau = self._taufid + np.dot(self._taumj, mjs)
        
        if use_fiducial_cosmology is False:
            if (omegabh2 is None) or (omegamh2 is None) or (yheused is None): 
                raise Exception 
                #TODO add custom error message to ask to set parameters 
                # to see cosmo.yaml for fiducial cosmology.
            tau *= self._get_tau_rescale(omegabh2, omegamh2, yheused)
        
        return tau

    def get_tau_cumulative(self, mjs, use_fiducial_cosmology, omegabh2=None, omegamh2=None, yheused=None):
        """Returns cumulative optical depth tau(>z) estimated using PC projection.
        Args:
            mjs: A 1d numpy array of size npc.
            use_fiducial_cosmology (optional): A boolean for whether you 
                want to use the fiducial cosmology or a different set of 
                cosmological parameters, ONLY for the purpose of rescaling 
                tau for a different cosmology; BE CAREFUL that the loglike
                code does not support cosmologies inconsistent with 
                Planck 2018). When use_fiducial_cosmology = False, you also
                need to specify omegabh2, omegamh2 and yheused all at the 
                same time, and the returned tau will be scaled accordingly. 
            omegabh2 (optional): A float or a numpy array for baryon density;
                used when use_fiducial_cosmology = False.
            omegamh2 (optional): A float or a numpy array for matter density;
                used when use_fiducial_cosmology = False.
            yheused (optional): A float or a numpy array for helium fraction;
                used when use_fiducial_cosmology = False.
        """
        npc = self._taumj_cum.shape[1] #TODO centralize this

        # (npc, nz)
        tau_cum = self._taufid_cum + \
            np.sum(np.array([mjs[j] * self._taumj_cum[:,j] for j in range(npc)]), axis=0)
        
        if use_fiducial_cosmology is False:
            if (omegabh2 is None) or (omegamh2 is None) or (yheused is None): 
                raise Exception 
                #TODO add custom error message to ask to set parameters 
                # to see cosmo.yaml for fiducial cosmology.
            tau_cum *= self._get_tau_rescale(omegabh2, omegamh2, yheused)
        
        return (self._zarray_cum, tau_cum)

    def _get_tau_rescale(self, omegabh2, omegamh2, yheused): 
        """Returns a scalar for the rescaling of tau due to different cosmo parameters."""
        tau_prefactor = self._get_tau_prefactor(omegabh2, omegamh2, yheused)
        rescale = tau_prefactor/self._tau_prefactor_fid
        return rescale

    @staticmethod
    def _get_tau_prefactor(omegabh2, omegamh2, yheused):
        """Returns prefactor for tau given cosmological parameters."""
        tau_prefactor = omegabh2 / np.sqrt(omegamh2) * (1.0-yheused)
        return tau_prefactor

    