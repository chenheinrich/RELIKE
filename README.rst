==========================================
RELIKE: Reionization Effective Likelihood
==========================================
:RELIKE: Reionization Effective Likelihood
:Homepage: https://github.com/chenheinrich/RELIKE

=============================

.. raw:: html

    <a href="https://github.com/chenheinrich/RELIKE/"><img src="https://img.shields.io/badge/GitHub-chenheinrich%2FRELIKE-blue" height="20px"></a>
    <a href="https://arxiv.org/abs/2104.13998/"><img src="https://img.shields.io/badge/arxiv-2104.13998-red" height="20px"></a>
    <a href="https://github.com/chenheinrich/RELIKE/blob/master/LICENSE.txt"><img src="https://img.shields.io/badge/LICENSE-GPLv3-blue" height="20px"></a>


Description
=============================

RELIKE (Reionization Effective Likelihood) is a fast and accurate likelihood code that compresses the final Planck 2018 likelihoods for the purpose of constraining models of the global ionization history.

- Using the **python package** :code:`relike`, you can obtain the likelihood of any model of ionization history *xe(z)* in the range *6 < z < zmax*. 

- The RELIKE code works by projecting the model onto the principal components (PC) of ionization history in the CMB data for its PC amplitudes *mj*'s, which are used to quickly **return the effective likelihood of the model**; you may also use it to evaluate the likelihood at multiple points and plot the parameter posteriors. 

- To run an MCMC chain, you can either **use the** :code:`relike` **python package from inside of a sampler** (e.g. Cobaya or Cosmosis), or use our release of :code:`CosmoMC-RELIKE` which has an implementation of the relike code in fortran (both in KDE and Gaussian modes) used to produce published results. 

- Note that there are two modes of effective likelihoods, both are sufficiently accurate: 
    - the kernel density estimate (KDE) mode, which is slightly more accurate;
    - the Gaussian approximation mode which is faster and also accurate. The python :code:`relike` contains the Gaussian mode only, while :code:`CosmoMC-RELIKE` has both. 
    
If you use this code, please cite `Heinrich & Hu 2021 <https://arxiv.org/abs/2104.13998>`_.

Installation
=============================

- First, clone all submodules ::

      git clone --recurse-submodules https://github.com/chenheinrich/RELIKE.git
      cd RELIKE 

- If you don't want :code:`CosmoMC-RELIKE` for now, just remove :code:`--recurse-submodules` flag and if you change your mind later, use ::
      
      git submodule update --init --recursive

- To stay updated on submodules, use ::
 
      git submodule update --remote --merge
      


Installing :code:`relike`: The Python Likelihood Package
*********************************************************   

**NEW: You can now install the latest stable release using** ::

      pip install relike 

(Note that we only support python3, so use pip3 and python3 if that's not your default python version.)
Then skip to "Running :code:`relike`".
  
**To install from source**:

- Install requirements
  
  It is recommended to create a virtual environment with python 3.8. See for example https://virtualenvwrapper.readthedocs.io/en/latest/ for getting setup with python virtual envs.

  Activate the virtual environment;

  :code:`pip3 install -r requirements.txt` (add :code:`-user` when working on a cluster if you don't have a virual environment activated)
      
- Install :code:`relike` ::

      pip3 install .

- For editable install ::
  
      pip3 install -e .


Running :code:`relike`
******************

- To run tests ::

        pytest tests

- To play with :code:`relike` using Jupyter notebooks ::

        jupyter notebook examples/example.ipynb

- To run example script (same as in the demo Jupyter notebook)::

      python3 examples/example.py

  This will run two examples: 
  1) print the relative chi-squared of an example tanh model relative to the Planck 2018 best-fit tanh model; 
  2) calculate and plot the optical depth posterior in the tanh model using relike.


Installing :code:`CosmoMC-RELIKE`: MCMC Sampler + RELIKE in Fortran 
***********************************************************************

:code:`CosmoMC-RELIKE` uses the generic sampler of :code:`CosmoMC` to sample the fortran implementation of the RELIKE likelihood. 

You may need to update all submodules recursively like this ::

      git submodule update --init --recursive 
  
      cd CosmoMC-RELIKE
  
See further installation instructions at `COSMOMC-RELIKE <ps://github.com/chenheinrich/CosmoMC-RELIKE>`_ .

Algorithm details
==================

Please see the latest paper `Heinrich & Hu 2021 <https://arxiv.org/abs/2104.13998>`_ for more details.


Branches
=============================

The master branch contains latest changes to the main release version.

The develop branch contains the latest less-stable features in development.




