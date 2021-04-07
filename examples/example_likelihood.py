from profiler import profiler
import numpy as np
import matplotlib.pyplot as plt
import os

import relike

def example_profiling(xe_func=None):
    
    pc = relike.PC()
    if xe_func is None:
        tanh_model = relike.TanhModel()
        xe_func = tanh_model.get_xe_func(zre=7.1, no_helium=True)

    @profiler
    def get_mjs(func):
        [pc.get_mjs(func) for i in range(1000)]

    get_mjs(xe_func)  

def example_plot_pc():
    pc = relike.PC()
    pc.plot_pc()

def example_likelihood_single_model():

    pc = relike.PC()
    gauss_like = relike.GaussianLikelihood()
    tanh_model = relike.TanhModel()

    xe_func = tanh_model.get_xe_func(zre=8.27789306640625, no_helium=True)
    xe_func_bf = tanh_model.get_xe_func(zre=7.1, no_helium=True)
    mjs = pc.get_mjs(xe_func)

    mjs_bf = pc.get_mjs(xe_func_bf)

    loglike = gauss_like.get_loglike(mjs)
    loglike_bf = gauss_like.get_loglike(mjs_bf)

    print('mjs = {}\n'.format(mjs))
    print('loglike = {}\n'.format(loglike))

    pc.data.plot_xe(mjs, xe_func=xe_func)

    likelihood_ratio = np.exp(loglike-loglike_bf)
    print('likelihood ratio to best-fit Planck 2018 tanh model is: \
        {}'.format(likelihood_ratio))

    chi2 = 2.0 * (loglike-loglike_bf)
    print('chi2 between this model and the best-fit Planck 2018 tanh model is: \
        {}\n'.format(chi2))

    use_fiducial_cosmology = True
    tau = pc.get_tau(mjs, use_fiducial_cosmology) #TODO to be polished
    tau_real = .059997

    print('PC estimated tau = {}'.format(tau)) 
    print('real tau = {}\n'.format(tau_real))

def main():
    example_likelihood_single_model()
    example_posterior()
    

def example_posterior(): #Plot out tanh posterior (evaluated w/ Gaussian likelihood at points)
    
    zre_values = np.linspace(6.1, 10.5, 101)
    pc = relike.PC()
    use_fiducial_cosmology = True
    gauss_like = relike.GaussianLikelihood()

    tau_values = np.zeros_like(zre_values)
    likelihood = np.zeros_like(zre_values)
    for i, zre in enumerate(zre_values):
        tanh_model = relike.TanhModel()
        xe_func = tanh_model.get_xe_func(zre=zre, no_helium=True)
        mjs = pc.get_mjs(xe_func)
        #TODO do we want use_fiducial_cosmology=True instead?
        use_fiducial_cosmology = True
        tau_values[i] = pc.get_tau(mjs, use_fiducial_cosmology)
        likelihood[i] = np.exp(gauss_like.get_loglike(mjs))

    plot_tau_posterior_tanh(tau_values, likelihood, \
        './plots/plot_tau_posterior_tanh.png')
    plot_zre_posterior_tanh(zre_values, likelihood, \
        './plots/plot_zre_posterior_tanh.png')

def plot_tau_posterior_tanh(tau_values, likelihood, plot_file_name):
    """Assuming flat prior in tau"""
    fig, ax = plt.subplots()
    ax.plot(tau_values, likelihood/np.max(likelihood), label = 'RELIKE')
    ax.set_xlabel(r'$\tau_{\rm tanh}$')
    ax.set_ylabel(r'$P(\tau_{\rm tanh})$')
    ax.set_xlim([tau_values[0], tau_values[-1]])

    example_dir = os.path.dirname(os.path.realpath(__file__))
    fn = 'tau_posterior_pl18_tanh_pliklite_srollv2_dz_auto.dat'
    fn = os.path.join(example_dir, 'data/', fn)
    data = np.genfromtxt(fn)

    fn2 = 'tau_posterior_pl18_tanh_mcmc_gaussian_likelihood_dz_auto.dat'
    fn2 = os.path.join(example_dir, 'data/', fn2)
    data2 = np.genfromtxt(fn2)

    fn3 = 'tau_posterior_pl18_tanh_mcmc_kde_dz_auto.dat'
    fn3 = os.path.join(example_dir, 'data/', fn3)
    data3 = np.genfromtxt(fn3)

    ax.plot(data[:,0], data[:,1], label = 'Exact')
    #ax.plot(data2[:,0], data2[:,1], '--', label = 'Gaussian')
    #ax.plot(data3[:,0], data3[:,1], ':', label = 'KDE')

    ax.legend()

    plt.savefig(plot_file_name)
    print('Saved plot: {}'.format(plot_file_name))

def plot_zre_posterior_tanh(zre_values, likelihood, plot_file_name):
    """Assuming flat prior in zre"""
    fig, ax = plt.subplots()
    plt.plot(zre_values, likelihood)
    ax.set_xlabel(r'$z_{\rm re}$')
    ax.set_ylabel(r'$P(z_{\rm re})$')
    ax.set_xlim([zre_values[0], zre_values[-1]])

    plt.savefig(plot_file_name)
    print('Saved plot: {}'.format(plot_file_name))

        



    

if __name__ == '__main__':
    main()