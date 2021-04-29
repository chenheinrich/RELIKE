===================
RELIKE 
===================
:RELIKE: Reionization Effective Likelihood from CMB 
:Author: Chen Heinrich
:Homepage: https://github.com/chenheinrich/RELIKE

If you use this code, please cite `Heinrich & Hu 2021`.


Description and installation
=============================

The Reionization Effective Likelihood (RELIKE) is a fast and accurate likelihood code that 
compresses CMB large-scale E-mode polarization likelihoods for the purpose of 
constraining models of the global ionization history (currently supporting Planck 2018).

For a standard non-editable installation use::

    pip install relike [--user]

The --user is optional and only required if you don't have write permission to your main python installation.
To install from source, clone from github using::

    git clone https://github.com/chenheinrich/RELIKE

Then in the project source root directory use::

    python setup.py install [--user]

If you want to modify the source code, you can install in the editable mode::

    pip install -e . [--user]

