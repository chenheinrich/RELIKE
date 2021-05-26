import numpy as np
import matplotlib.pyplot as plt
import os

import relike

def example_plot_pc():
    print('Example 3: Plot PCs and the fiducial xe function used for PCs.\n')
    pc = relike.PC()
    pc.plot_pc(plot_file_name='plot_pc.pdf')

def example_likelihood_single_model():

    print('Example 1: likelihood ratio of a single model against tanh best-fit\n')

    pc = relike.PC()
    gauss_like = relike.GaussianLikelihood()
    tanh_model = relike.TanhModel() #tanh model with dz = 0.015(1+z)

    # Get PC amplitudes and log-likelihood for a tanh model (normalized to Planck best-fit)
    zre = 10.0 
    xe_func = tanh_model.get_xe_func(zre=zre)
    mjs = pc.get_mjs(xe_func)
    loglike = gauss_like.get_loglike(mjs)

    print('\tTanh model at zre = {}: '.format(zre))
    print('\t    PC amplitudes mjs = {}'.format(mjs))
    print('\t    log-likehood = {}\n'.format(loglike))

    # Get likelihood ratio and chi2 (equiavlent) relative to Planck best-fit
    likelihood_ratio = np.exp(loglike)
    delta_chi_squared = -2.0 * (loglike)
    print('\tLikelihood ratio relative to the best-fit Planck 2018 tanh model is: {} (>1 is better)'.format(likelihood_ratio))
    print('\tChi-squared relative to the best-fit ' +
        'Planck 2018 tanh model is: {} (negative is better) \n'.format(delta_chi_squared))

    # Plot xe: exact vs PC projection
    pc.plot_xe(mjs, xe_func=xe_func, plot_name='./plot_xe.pdf')
    
    # Get total optical depth tau using PCs
    tau_pc = pc.get_tau(mjs)
    tau_exact = 0.07816

    fmt = '%1.5f'
    print('\tComparing tau exact vs tau estimated from PCs: {} (exact), {} (PC)\n'\
        .format(tau_exact, fmt%(tau_pc)))

def example_posterior(): 
    
    print('Example 2: Plot posterior for a one-parameter model: tanh model\n')

    zre_values = np.linspace(6.1, 10.5, 101)
    pc = relike.PC()
    gauss_like = relike.GaussianLikelihood()

    tau_values = np.zeros_like(zre_values)
    likelihood = np.zeros_like(zre_values)
    for i, zre in enumerate(zre_values):
        tanh_model = relike.TanhModel()
        xe_func = tanh_model.get_xe_func(zre=zre)
        mjs = pc.get_mjs(xe_func)
        tau_values[i] = pc.get_tau(mjs)
        likelihood[i] = np.exp(gauss_like.get_loglike(mjs))

    plot_tau_posterior_tanh(tau_values, likelihood, \
        'plot_tau_posterior_tanh.pdf')

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
    print('Saved plot: {}\n'.format(plot_file_name))

def main():
    example_likelihood_single_model()
    example_posterior()
    example_plot_pc()
    
    
if __name__ == '__main__':
    main()