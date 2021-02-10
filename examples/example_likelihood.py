from profiler import profiler

import numpy as np

import erlike as erl

def example_profiling(xe_func=None):
    
    pc = erl.PC()
    if xe_func is None:
        tanh_model = erl.TanhModel()
        xe_func = tanh_model.get_xe_func(zre=7.1, no_helium=True)

    @profiler
    def get_mjs(func):
        [pc.get_mjs(func) for i in range(1000)]

    get_mjs(xe_func)  

def example_plot_pc():
    pc = erl.PC()
    pc.data.plot_pc()

def example_likelihood_single_model():

    pc = erl.PC()
    gauss_like = erl.GaussianLikelihood()
    tanh_model = erl.TanhModel()

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
    pass
    #TODO implement

if __name__ == '__main__':
    main()