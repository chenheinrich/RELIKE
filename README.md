# Reionization Effective Likelihood

The Reionization Effective Likelihood (RELIKE) is a fast and accurate likelihood code that compresses the final Planck 2018 likelihoods for the purpose of constraining models of the global ionization history.

1. Using the **python package `relike`**, you can obtain the likelihood of any model of ionization history _xe(z)_ in the range
6 < z < zmax. The code works by projecting the model onto the principal components (PC) of ionization history in the CMB data for its PC amplitudes _mj_'s, which are used to quickly return the effective likelihood of the model; you may also use it to evaluate the likelihood at multiple points and plot the parameter posteriors (assuming flat prior in the parameter). 
- You can also run a MCMC chain by either making use of the `relike` python package from insde of a sampler (e.g. Cobaya or Cosmosis), or use directly the **`CosmoMC-relike`** implementation in fortran that we also include here and have used for producing results in the paper. 
- Note that there are two modes of effective likelihoods: 1) kernel density estimate (KDE) mode, which is slightly more accurate, and 2) the Gaussian approximation mode, which is good enough for most models. The python `relike` contains the Gaussian mode only, while the fortran implementation in `CosmoMC-relike` has both. 

Reference: Heinrich & Hu 2021 (arxiv: _fill in_)

## Release Note

v1.0
- Added **`relike`**: a standalone python likelihood package.
- Added **`CosmoMC-relike`**: a MCMC implementation using CosmoMC sampler. 
- Supporting arbitrary xe(z) specified by the user between _6 < z < zmax_, where zmax = 30; assuming fully reionized hydrogen for _z < 6_.
- Planck likelihoods used: plik_lite_TTTEEE + lowl + srollv2.

## Standalone Python Likelihood: relike

This is a standalone python likelihood package, outputting the Planck likelihood for any global ionization history model _xe(z)_. The functional form of _xe(z)_ between 6 < z < zmax is specified by the user (we only support zmax = 30 for now), and fully reionized hydrogen is assumed for _z < 6_ with typical helium ionization history. 

- To install:

  `pip install .` 

  (Add `--user` when working on a cluster)

  For editable install use: `pip install -e .`

- To run tests: 

  `pytest tests`

- To play with `relike` using Jupyter notebooks:

  `jupyter notebook examples/example.ipynb `.

- To run example script (same as in the demo Jupyter notebook): 

  `python -m examples.example_likelihood`

  This will run two examples: 1) print the relative chi-squared of an example tanh model relative to the Planck 2018 best-fit tanh model; 2) calculate and plot the optical depth posterior in the tanh model using relike.

## CosmoMC: MCMC Sampler + Fortran Implementation

_Installation instructions goes here._

_Instructions for running example goes here._
