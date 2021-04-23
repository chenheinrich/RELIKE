# Reionization Effective Likelihood

The Reionization Effective Likelihood (RELIKE) is a fast and accurate likelihood code that compresses the final Planck 2018 likelihoods for the purpose of constraining models of the global ionization history.

- Using the **python package `relike`**, you can obtain the likelihood of any model of ionization history _xe(z)_ in the range
6 < z < zmax. 

- The `relike` code works by projecting the model onto the principal components (PC) of ionization history in the CMB data for its PC amplitudes _mj_'s, which are used to quickly return the effective likelihood of the model; you may also use it to evaluate the likelihood at multiple points and plot the parameter posteriors (assuming flat prior in the parameter). 

- To run an MCMC chain, you can either use the `relike` python package from inside of a sampler (e.g. Cobaya or Cosmosis), or use our release of **`CosmoMC-relike`** which has an implementation of the relike code in fortran (both in KDE and Gaussian modes) used to produce published results. 

- Note that there are two modes of effective likelihoods: 1) kernel density estimate (KDE) mode, which is slightly more accurate, and 2) the Gaussian approximation mode, which is good enough for most models. The python `relike` contains the Gaussian mode only, while the fortran implementation in `CosmoMC-relike` has both. 

Reference: Heinrich & Hu 2021 (arxiv: _fill in_)

## Release Note

v1.0 (coming soon)
- Added **`relike`**: a standalone python likelihood package.
- Added **`CosmoMC-relike`**: an MCMC implementation using the CosmoMC sampler. 
- Supporting arbitrary xe(z) specified by the user between _6 < z < zmax_, where zmax = 30; assuming fully reionized hydrogen for _z < 6_.
- Planck likelihoods used: plik_lite_TTTEEE + lowl + srollv2.

## Install

- Clone the repository

  `git clone https://github.com/chenheinrich/RELIKE.git`
  
  skip to the `relike` section below to install the standalone python likelihood package.

- If you also want `CosmoMC-relike` (now or later), use

  `git submodule update --init --recursive` 

  See the `CosmoMC-relike` section for how to install this code. 


### Installing `relike`: Python Likelihood Package

This is a standalone python likelihood package, outputting the Planck likelihood for any global ionization history model _xe(z)_. The functional form of _xe(z)_ between 6 < z < zmax is specified by the user (we only support zmax = 30 for now), and fully reionized hydrogen is assumed for _z < 6_ with typical helium ionization history. 

- Install requirements first: 

  (It is recommended to create a virtual environment with python 3.8. See for example https://virtualenvwrapper.readthedocs.io/en/latest/ for getting setup with python virtual envs).

  Activate the virtual environment

  `cd RELIKE`

  `pip install -r requirements.txt` (add `--user` when working on a cluster if you don't have a virual environment activated)

- Install `relike`:

  `pip install .`

  For editable install: 
  
  `pip install -e .`

- To run tests: 

  `pytest tests`

- To play with `relike` using Jupyter notebooks:

  `jupyter notebook examples/example.ipynb `.

- To run example script (same as in the demo Jupyter notebook): 

  `python3 examples/example_likelihood.py`

  This will run two examples: 1) print the relative chi-squared of an example tanh model relative to the Planck 2018 best-fit tanh model; 2) calculate and plot the optical depth posterior in the tanh model using relike.

### Installing `CosmoMC-relike`: MCMC Sampler + relike in Fortran 

CosmoMC-relike uses the generic sampler of CosmoMC to sample the fortran implementation of the `relike` likelihood. 

You may need to update all submodules recursively like this:

  `git submodule update --init --recursive` 
  
  `cd CosmoMC-relike`
  
See further installation instructions at [CosmoMC-relike](https://github.com/chenheinrich/CosmoMC-relike/tree/develop#readme)

  
  
