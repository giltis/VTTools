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
"""
This is the model for 3D tomography reconstruction
"""

import sys
import numpy as np
import tomopy
import logging


def load_data(file_name, slices_start, slices_end, data_center):
    """Read data from HDF5 file

    Parameters
    ----------
    file_name : str
        filename of input HDF5 file

    slices_start : int
        starting index of image stacks (3D)

    slices_end : int
        ending index of image stacks (3D)

    data_center : float
        center of projections

    Returns
    ----------
    d : array_like
        stores the XTomoDataset object with input dataset loaded
    """

    # Xtomo reader reads data from HDF5 file
    data, white, dark, theta = tomopy.xtomo_reader(file_name,
                                                   slices_start=slices_start,
                                                   slices_end=slices_end)

    # Create Xtomo dataset object
    d = tomopy.xtomo_dataset(log='debug')
    d.dataset(data, white, dark, theta)

    d.center = data_center

    return d

def normalize(dataset):
    """Normalize input dataset

    Parameters
    ----------
    dataset : array_like
        raw input dataset

    Returns
    ----------
    dataset : array_like
        normalized input dataset
    """

    dataset.normalize()

    return dataset

def correct_drift(dataset):
    """Drift correction

    Parameters
    ----------
    dataset : array_like
        input dataset without drift correction

    Returns
    ----------
    dataset : array_like
        input dataset with drift correction
    """

    dataset.correct_drift()

    return dataset

def phase_retrieval(dataset):
    """Phase retrieval

    Parameters
    ----------
    dataset : array_like
        input dataset

    Returns
    ----------
    dataset : array_like
        input dataset after phase retrieval
    """

    dataset.phase_retrieval()

    return dataset

def optimize_center(dataset, center_init=None):
    """Find center of projections

    Parameters
    ----------
    dataset : array_like
        input dataset without drift correction

    center_init : float, optional
        initial value of center

    Returns
    ----------
    dataset : array_like
        object with attribute "center" updated
    """
    dataset.optimize_center()

    return dataset

def gridrec(dataset):
    """GridRec reconstruction

    Parameters
    ----------
    dataset : array_like
        input dataset

    Returns
    ----------
    dataset : array_like
        dataset with attribute "data_recon" computed
    """

    dataset.gridrec()

    return dataset

def sirt(dataset, iters=1):
    """SIRT reconstruction

    Parameters
    ----------
    dataset : array_like
        input dataset

    iters : int, optional
        number of iterations

    Returns
    ----------
    dataset : array_like
        dataset with attribute "data_recon" computed
    """

    dataset.sirt(iters=iters)

    return dataset

def art(dataset, iters=1):
    """Art reconstruction

    Parameters
    ----------
    dataset : array_like
        input dataset

    iters : int, optional
        the number of iterations

    Returns
    ----------
    dataset : array_like
        dataset with attribute "data_recon" computed
    """

    dataset.art()

    return dataset

def save_data(dataset, file_name, axis=0):
    """Write reconstructed data to stack of tif files

    Parameters
    ----------
    dataset : array_like
        input dataset

    file_name : str
        name of output file

    axis : int, optional
        the axis to read along the images
    """

    # Write to stack of TIFFs.
    tomopy.xtomo_writer(dataset.data_recon, file_name, axis=axis)

########

def _generate_xtomo_object(data=None, white=None, dark=None, theta=None, center=None, recon=None, log_mode='info'):
    """Generate xtomo_dataset object internally to enable passing only ndarrays

    Parameters
    ----------
    data : np.ndarray
        sample data

    white : np.ndarray
        white background of the sample

    dark : np.ndarray
        dark background of the sample

    theta : np.ndarray
        the angle array of projections

    center : float
        the center of the projections

    recon : np.ndarray
        the reconstructed data

    log_mode : string
        the logging mode: debug, info, error, warn, and warning

    Returns
    ----------
    dataset : array_like
        the Xtomo_dataset object used internally by other functions
    """

    # create xtomo_dataset object and initialize it
    d = tomopy.xtomo_dataset(log=log_mode)

    if data is not None:
        d.data = data

    if white is not None:
        d.data_white = white

    if dark is not None:
        d.data_dark = dark

    if theta is not None:
        d.theta = theta

    if center is not None:
        d.center = center

    if recon is not None:
        d.recon_data = recon

    return d


def load_data_new(file_name, slices_start, slices_end, data_center):
    """Read data from HDF5 file

    Parameters
    ----------
    file_name : str
        filename of input HDF5 file

    slices_start : int
        starting index of image stacks (3D)

    slices_end : int
        ending index of image stacks (3D)

    data_center : float
        center of projections

    Returns
    ----------
    data : np.ndarray
        loaded raw input projections of the sample

    white : np.ndarray
        white background

    dark : np.ndarray
        dark background

    theta : np.ndarray
        the angle list of projections

    center : float
        center of projections
    """

    # Xtomo reader reads data from HDF5 file
    data, white, dark, theta = tomopy.xtomo_reader(file_name,
                                                   slices_start=slices_start,
                                                   slices_end=slices_end)

    # Create Xtomo dataset object
    d = tomopy.xtomo_dataset(log='debug')
    # dataset function does additional operations to make sure the loaded data are correct
    d.dataset(data, white, dark, theta)
    d.center = data_center

    # prepare return values
    data = d.data
    white = d.data_white
    dark = d.data_dark
    theta = d.theta
    center = d.center

    return data, white, dark, theta, center

def normalize_new(data, white, dark):
    """Normalize input dataset

    Parameters
    ----------
    data : np.ndarray
        loaded raw input projections of the sample

    white : np.ndarray
        white background

    dark : np.ndarray
        dark background

    Returns
    ----------
    data : np.ndarray
        loaded raw input projections of the sample
    """

    # create xtomo_dataset object and initialize it
    d = _generate_xtomo_object(data, white, dark)

    # normalize the data with multi-threading supported
    data = d.normalize(overwrite=False)

    return data

def correct_drift_new(data, theta, center):
    """Drift correction

    Parameters
    ----------
    data : np.ndarray
        input projections of the sample

    theta : np.ndarray
        the angle list of projections

    center : float
        center of projections

    Returns
    ----------
    data : np.ndarray
        updated projection data
    """

    # create xtomo_dataset object and initialize it
    d = _generate_xtomo_object(data=data, theta=theta, center=center)

    data = d.correct_drift(overwrite=False)

    return data

def phase_retrieval_new(data, theta, center):
    """Phase retrievel

    Parameters
    ----------
    data : np.ndarray
        input projections of the sample

    theta : np.ndarray
        the angle list of projections

    center : float
        center of projections

    Returns
    ----------
    data : np.ndarray
        updated projection data
    """

    # create xtomo_dataset object and initialize it
    d = _generate_xtomo_object(data=data, theta=theta, center=center)

    data = d.phase_retrieval(overwrite=False)

    return data

def optimize_center_new(data, theta, center_init=None):
    """Find the center of projections

    Parameters
    ----------
    data : np.ndarray
        input projections of the sample

    theta : np.ndarray
        the angle list of projections

    center_init : float, optional
        initial center of projections

    Returns
    ----------
    data : np.ndarray
        updated projection data

    center : float
        center of projections
    """

    # create xtomo_dataset object and initialize it
    d = _generate_xtomo_object(data=data, theta=theta)

    center = d.optimize_center(center_init=center_init, overwrite=False)

    return data, center

def gridrec_new(data, theta, center):
    """GridRec reconstruction

    Parameters
    ----------
    data : np.ndarray
        input projections of the sample

    theta : np.ndarray
        the angle list of projections

    center : float
        the center of projections

    Returns
    ----------
    data_recon : np.ndarray
        the reconstructed data by GridRec algorithm
    """

    # create xtomo_dataset object and initialize it
    d = _generate_xtomo_object(data=data, theta=theta, center=center)

    data_recon = d.gridrec(overwrite=False)

    return data_recon

def sirt_new(data, white, dark, theta, center, iters=1):
    """SIRT reconstruction

    Parameters
    ----------
    data : np.ndarray
        input projections of the sample

    white : np.ndarray
        white background

    dark : np.ndarray
        dark background

    theta : np.ndarray
        the angle list of projections

    center : float
        the center of projections

    iters : int, optional
        the number of iterations

    Returns
    ----------
    data_recon : np.ndarray
        the reconstructed data by SIRT algorithm
    """

    # create xtomo_dataset object and initialize it
    d = _generate_xtomo_object(data=data, white=white, dark=dark, theta=theta, center=center)

    data_recon = d.sirt(iters=iters, overwrite=False)

    return data_recon

def art_new(data, white, dark, theta, center, iters=1):
    """ART reconstruction

    Parameters
    ----------
    data : np.ndarray
        input projections of the sample

    white : np.ndarray
        white background

    dark : np.ndarray
        dark background

    theta : np.ndarray
        the angle list of projections

    center : float
        the center of projections

    iters : int, optional
        the number of iterations

    Returns
    ----------
    data_recon : np.ndarray
        the reconstructed data by ART algorithm
    """

    # create xtomo_dataset object and initialize it
    d = _generate_xtomo_object(data=data, white=white, dark=dark, theta=theta, center=center)

    data_recon = d.art(iters=iters, overwrite=False)

    return data_recon

def save_data_new(data_recon, file_name, axis=0):
    """Write reconstructed data to stack of tif files

    Parameters
    ----------
    data_recon : np.ndarray
        output reconstructed data

    file_name : str
        name of output file

    axis : int, optional
        the axis to read along the images
    """

    # Write to stack of TIFFs.
    tomopy.xtomo_writer(data_recon, file_name, axis=axis)

