# ######################################################################
# Copyright (c) 2014, Brookhaven Science Associates, Brookhaven        #
# National Laboratory. All rights reserved.                            #
#                                                                      #
# Redistribution and use in source and binary forms, with or without   #
# modification, are permitted provided that the following conditions   #
# are met:                                                             #
#                                                                      #
# * Redistributions of source code must retain the above copyright     #
#   notice, this list of conditions and the following disclaimer.      #
#                                                                      #
# * Redistributions in binary form must reproduce the above copyright  #
#   notice this list of conditions and the following disclaimer in     #
#   the documentation and/or other materials provided with the         #
#   distribution.                                                      #
#                                                                      #
# * Neither the name of the Brookhaven Science Associates, Brookhaven  #
#   National Laboratory nor the names of its contributors may be used  #
#   to endorse or promote products derived from this software without  #
#   specific prior written permission.                                 #
#                                                                      #
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS  #
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT    #
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS    #
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE       #
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,           #
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES   #
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR   #
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)   #
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,  #
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OTHERWISE) ARISING   #
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE   #
# POSSIBILITY OF SUCH DAMAGE.                                          #
########################################################################
from __future__ import (absolute_import, division, print_function,
                        )

import numpy as np
import six
from numpy.testing import (assert_array_equal, assert_array_almost_equal,
                           assert_almost_equal)

from skxray.testing.decorators import known_fail_if
from vttools.to_wrap.fitting import (gaussian_model, lorentzian_model,
                                     lorentzian2_model, quadratic_model,
                                     fit_engine, fit_engine_list, expression_model)
from nose.tools import (assert_equal, assert_true, raises)


@known_fail_if(True)
def test_fit_quad_to_peak():
    assert(False)


def test_gauss_fit():
    x = np.arange(-1, 1, 0.01)
    amplitude = 1
    center = 0
    sigma = 1
    true_val = [amplitude, center, sigma]
    y = amplitude / np.sqrt(2 * np.pi) / sigma * np.exp(-(x - center)**2 / 2 / sigma**2)

    g = gaussian_model('',
                       1, 'fixed', [0, 1],
                       0.1, 'free', [0, 0.5],
                       0.5, 'free', [0, 1])

    result, yfit = fit_engine(g, x, y)

    out = result.values
    fitted_val = (out['amplitude'], out['center'], out['sigma'])
    assert_array_almost_equal(true_val, fitted_val)


def test_lorentzian_fit():
    x = np.arange(-1, 1, 0.01)
    amplitude = 1
    center = 0
    sigma = 1
    true_val = [amplitude, center, sigma]

    y = (amplitude/(1 + ((x - center) / sigma)**2)) / (np.pi * sigma)

    m = lorentzian_model('',
                         0.8, 'free', [0, 1],
                         0.1, 'free', [0, 0.5],
                         0.8, 'bounded', [0, 2])

    result, yfit = fit_engine(m, x, y)
    out = result.values

    fitted_val = (out['amplitude'], out['center'], out['sigma'])
    assert_array_almost_equal(true_val, fitted_val)


@raises(ValueError)
def test_lorentzian2_fit():
    x = np.arange(-1, 1, 0.01)
    area = 1
    center = 0
    sigma = 1
    true_val = [area, center, sigma]

    y = (area/(1 + ((x - center) / sigma)**2)**2) / (np.pi * sigma)

    m = lorentzian2_model('',
                          0.8, 'wrong', [0, 1],
                          0.1, 'free', [0, 0.5],
                          0.5, 'free', [0, 1])

    result, yfit = fit_engine(m, x, y)
    out = result.values

    fitted_val = (out['area'], out['center'], out['sigma'])
    assert_array_almost_equal(true_val, fitted_val)


def test_quadratic_fit():
    x = np.arange(-1, 1, .01)
    a = 1
    b = 2
    c = 3

    true_val = [a, b, c]

    y = a * x*x + b * x + c

    m = quadratic_model('',
                        a, 'free', [-1, 1],
                        b, 'free', [-1, 1],
                        c, 'free', [-1, 1])

    result, yfit = fit_engine(m, x, y)
    out = result.values
    fitted_val = (out['a'], out['b'], out['c'])
    assert_array_almost_equal(true_val, fitted_val)


def test_fit_engine_list():
    a = 1
    b = 2
    c = 3
    m = quadratic_model('',
                        a, 'free', [-1, 1],
                        b, 'free', [-1, 1],
                        c, 'free', [-1, 1])
    x = np.arange(-1, 1, 0.01)
    y = x**2 + 1

    datav = [(x, y), (x, y+2)]
    out = fit_engine_list(m, datav)
    assert_equal(len(out), 2)


def test_expression_model():

    inputv = 'exp(-a*x)'

    x = np.arange(-1, 1, 0.01)
    y = np.exp(-x)

    mod = expression_model(inputv)
    out = mod.fit(y, x=x, a=0.1)
    assert_equal(1, out.values['a'])
