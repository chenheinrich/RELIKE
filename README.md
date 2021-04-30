# RELIKE: Reionization Effective Likelihood

RELIKE (Reionization Effective Likelihood) is a fast and accurate likelihood code that compresses the final Planck 2018 likelihoods for the purpose of constraining models of the global ionization history.

- Using the **python package `relike`**, you can obtain the likelihood of any model of ionization history _xe(z)_ in the range 6 < z < zmax. 

- The `relike` code works by projecting the model onto the principal components (PC) of ionization history in the CMB data for its PC amplitudes _mj_'s, which are used to quickly **return the effective likelihood of the model**; you may also use it to evaluate the likelihood at multiple points and plot the parameter posteriors. 

- To run an MCMC chain, you can either **use the `relike` python package from inside of a sampler** (e.g. Cobaya or Cosmosis), or use our release of **`CosmoMC-RELIKE`** which has an implementation of the relike code in fortran (both in KDE and Gaussian modes) used to produce published results. 

- Note that there are two modes of effective likelihoods, both are sufficiently accurate: 
    - the kernel density estimate (KDE) mode, which is slightly more accurate;
    - the Gaussian approximation mode which is faster and also accurate. The python `relike` contains the Gaussian mode only, while `CosmoMC-RELIKE` has both. 

- The master branch contains latest changes to the main release version. The develop branch contains the latest less-stable features in development.

If you use this code, please cite Heinrich & Hu 2021 (https://arxiv.org/abs/2104.13998).

## Release Note

v0.0.1 
- Added **`RELIKE`**: a standalone python likelihood package (supporting **only python3**).
- Added **`CosmoMC-RELIKE`**: an MCMC implementation using the CosmoMC sampler. 
- Supporting arbitrary xe(z) specified by the user between _6 < z < 30_; assuming fully reionized hydrogen and singly ionized helium at _z < 6_.
- Planck likelihoods used: `plik_lite_TTTEEE + lowl + Sroll2`.

## Getting Started

- First, clone all submodules:

  `git clone --recurse-submodules https://github.com/chenheinrich/RELIKE.git`

- If you don't want `CosmoMC-RELIKE` for now, just `git clone` and if you change your mind later, use

  `git submodule update --init --recursive`
  
- To stay updated, use `git submodule update --remote --merge` beside `git pull`.


### Installing `relike`: Python Likelihood Package

**NEW: You can now install with a simple `pip install relike`**. Note that we only support python3, so use pip3 and python3 if that's not your default python version. **Once done, you can skip to "run tests" after `cd RELIKE`**. 

- Install requirements first: 

  (It is recommended to create a virtual environment with python 3.8. See for example https://virtualenvwrapper.readthedocs.io/en/latest/ for getting setup with python virtual envs).

  Activate the virtual environment

  `cd RELIKE`

  `pip3 install -r requirements.txt` (add `--user` when working on a cluster if you don't have a virual environment activated)

- Install `relike`:

  `pip3 install .`

  For editable install: 
  
  `pip3 install -e .`

- To run tests: 

  `pytest tests`

- To play with `relike` using Jupyter notebooks:

  `jupyter notebook examples/example.ipynb `.

- To run example script (same as in the demo Jupyter notebook): 

  `python3 examples/example.py`

  This will run two examples: 1) print the relative chi-squared of an example tanh model relative to the Planck 2018 best-fit tanh model; 2) calculate and plot the optical depth posterior in the tanh model using relike.

### Installing `CosmoMC-RELIKE`: MCMC Sampler + RELIKE in Fortran 

CosmoMC-RELIKE uses the generic sampler of CosmoMC to sample the fortran implementation of the RELIKE likelihood. 

You may need to update all submodules recursively like this:

  `git submodule update --init --recursive` 
  
  `cd CosmoMC-RELIKE`
  
See further installation instructions at [CosmoMC-RELIKE](https://github.com/chenheinrich/CosmoMC-RELIKE)


  
  
