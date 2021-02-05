# TODO write these examples

# Example 1:

import numpy as np

import erlike as erl

pc = erl.PC()
gauss_like = erl.GaussianLikelihood()

mjs = pc.get_mjs(erl.xe_tanh_pl18)
mjs_bf = pc.get_mjs(erl.xe_tanh_pl18_best_fit)

loglike = gauss_like.get_loglike(mjs)
loglike_bf = gauss_like.get_loglike(mjs_bf)

likelihood_ratio = np.exp(loglike-loglike_bf)
print('likelihood ratio to best-fit Planck 2018 tanh model is: \
    {}'.format(likelihood_ratio))

tau = pc.get_tau(mjs)
print('PC estimated tau = {}'.format(tau))

# Example 2:

# Plot out tanh posterior (evaluated w/ Gaussian likelihood at points)

# specify zre, make xe(z); get tau value by integrating (might wanna work on integration to be fast)

# plot Gaussian likelihood at these points for the posterior
