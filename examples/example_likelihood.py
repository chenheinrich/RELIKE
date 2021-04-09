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
    tanh_model = relike.TanhModel() #tanh model with dz = 0.015(1+z)

    # Get PC amplitudes and log-likelihood for a tanh model with dz = 0.015(1+z)
    zre = 8.27789306640625 #TODO need to update to 10.0
    xe_func = tanh_model.get_xe_func(zre=zre, no_helium=True)
    mjs = pc.get_mjs(xe_func)
    loglike = gauss_like.get_loglike(mjs)

    # Get PC amplitudes and log-likelihood for the Planck 2018 best-fit tanh model
    zre_bf = 8.1 #TODO need to update to actual number
    xe_func_bf = tanh_model.get_xe_func(zre=zre_bf, no_helium=True)
    mjs_bf = pc.get_mjs(xe_func_bf)
    loglike_bf = gauss_like.get_loglike(mjs_bf)

    print('Tanh model at zre = {}: '.format(zre))
    print('    PC amplitudes mjs = {}'.format(mjs))
    print('    log-likehood = {}\n'.format(loglike))

    # Plot xe: exact vs PC projection
    pc.plot_xe(mjs, xe_func=xe_func, plot_name='./plots/plot_xe.pdf')
    # Plot cumulative tau exact vs PC projection 
    pc.plot_tau_cumulative(mjs, plot_name='./plots/plot_tau_cumulative.pdf')

    # Get chi2 relative to Planck best-fit
    loglike_bf = gauss_like.get_loglike(mjs_bf)
    delta_chi_squared = -2.0 * (loglike - loglike_bf)
    print('Chi-squared relative to the best-fit '+
        'Planck 2018 tanh model is = {}\n'.format(delta_chi_squared))

    # Print total tau: exact vs from PC projection
    use_fiducial_cosmology = True
    tau_pc = pc.get_tau(mjs, use_fiducial_cosmology) #TODO to be polished
    tau_exact = .059997 #TODO need to update for a zre = 10.0
    print('tau exact vs PC: {} vs {}\n'.format(tau_exact, tau_pc)) 

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
        './plots/plot_tau_posterior_tanh.pdf')
    plot_zre_posterior_tanh(zre_values, likelihood, \
        './plots/plot_zre_posterior_tanh.pdf')

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

    ax.plot(data[:,0], data[:,1], label = 'Exact')

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


def main():
    example_likelihood_single_model()
    example_posterior()
    
if __name__ == '__main__':
    main()