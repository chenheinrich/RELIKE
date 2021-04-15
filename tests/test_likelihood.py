#TODO To write
import pytest
import numpy as np

import relike as rel

pc = rel.PC()
gauss_like = rel.GaussianLikelihood()
tanh_model = rel.TanhModel()

def test_get_mjs():
    xe_func = tanh_model.get_xe_func(zre=8.27789306640625)
    mjs = pc.get_mjs(xe_func)
    mjs_exp = np.array([ -0.122551897483178, \
        -3.983205659237149E-003, \
        9.736410659918895E-002, \
        -0.161935661107380, \
        0.164459056800131  
        ])
    assert np.allclose(mjs, mjs_exp)

def test_get_loglike():
    xe_func = tanh_model.get_xe_func(zre=8.27789306640625)
    mjs = pc.get_mjs(xe_func)
    loglike = gauss_like.get_loglike(mjs)
    expected = 0.009721218348963334
    assert np.allclose(loglike, expected)

def test_plotting():
    xe_func = tanh_model.get_xe_func(zre=8.27789306640625)
    fn_xe = './tests/data/xe.dat'
    data = np.genfromtxt(fn_xe)
    zarray = data[:,0]
    xe_expected = data[:,1]
    assert np.allclose(xe_func(zarray), xe_expected)

#TODO 
# def test_tau(xe_func):
#   tau_expected = 0.06

