# TODO write these examples
from profiler import profiler

# Example 1:

import numpy as np

import erlike as erl


def example_1():

    pc = erl.PC()
    gauss_like = erl.GaussianLikelihood()
    tanh_model = erl.TanhModel()

    #TODO put in other example scripts?
    #TODO put in jupyter notebook?
    # Timing
    #@profiler
    #def get_mjs(func):
    #    [pc.get_mjs(func) for i in range(1000)]
    #timing_test = pc.get_mjs(xe_func_1)

    # Plot PC and fiducial xe(z)
    #pc.data.plot_pc()

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
    example_1()
    example_2()

def example_2():
    pass
    #TODO implement
    # Example 2:

    # Plot out tanh posterior (evaluated w/ Gaussian likelihood at points)

    # specify zre, make xe(z); get tau value by integrating (might wanna work on integration to be fast)

    # plot Gaussian likelihood at these points for the posterior

if __name__ == '__main__':
    main()