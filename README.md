# Effective Reionization Likelihood

The Effective Reionization Likelihood (ERLike) is a fast and accurate likelihood code that compresses the final Planck 2018 likelihoods for the purpose of constraining reionization models.

- You can constrain any model of the global ionization history _xe(z)_ in the range
6 < z < zmax; this is done by projecting the model onto principal components (PC) of ionization history in the CMB data. 
- You can quickly evaluate the likelihood of a single model and plot parameter posteriors (see **Standalone Python Likelihood: erlike**). 
- You can also run a MCMC chain, which typically converges a few hundred times faster than directly sampling the Planck likelihoods. 
- We offer CosmoMC implementations in fortran; one can easily install the python standalone code using Cobaya in python. 

Reference: <...>

## Release Note

v1.0
- Added **erlike**: a standalone python likelihood package.
- Added **CosmoMC**: a MCMC implementation using CosmoMC sampler. 
- Supporting arbitrary xe(z) specified by the user between _6 < z < zmax_, where zmax = 30; assuming fully reionized hydrogen for _z < 6_.
- Planck likelihoods used: plik_lite_TTTEEE + lowl + srollv2.

## Standalone Python Likelihood: erlike

This is a standalone python likelihood package, outputting the Planck likelihood for any global ionization history model _xe(z)_. The functional form of _xe(z)_ between 6 < z < zmax is specified by the user (we only support zmax = 30 for now), and fully reionized hydrogen is assumed for _z < 6_ with typical helium ionization history. 

To run an example: 
`python -m examples.example_likelihood`

This will print the likelihood of an example model relative to the Planck 2018 best-fit tanh model and to plot the posterior of the reionization parameter in an example model.

## CosmoMC: MCMC Sampler + Fortran Implementation

_Installation instructions goes here._

_Instructions for running example goes here._