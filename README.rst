==========================================
RELIKE: Reionization Effective Likelihood
==========================================
:RELIKE: Reionization Effective Likelihood
:Homepage: https://github.com/chenheinrich/RELIKE

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

- To run example script (same as in the demo Jupyter notebook)
  
        :code:`python3 examples/example.py`

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

The develop branch is a development branch.

