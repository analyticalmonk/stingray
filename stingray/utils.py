from __future__ import division
import numpy as np
import warnings

# If numba is installed, import jit. Otherwise, define an empty decorator
# with the same name.
try:
    from numba import jit
except:
    def jit(fun):
        return fun


def simon(message, **kwargs):
    """
    The Statistical Interpretation MONitor.

    A warning system designed to always remind the user that Simon
    is watching him/her.

    Parameters
    ---------
    message : string
        The message that is thrown
    kwargs : dict
        The rest of the arguments that are passed to warnings.warn
    """
    warnings.warn("SIMON says: {0}".format(message), **kwargs)


def rebin_data(x, y, dx_new, method='sum'):

    """
    Rebin some data to an arbitrary new data resolution. Either sum
    the data points in the new bins or average them.

    Parameters
    ----------
    x: iterable
        The dependent variable with some resolution dx_old = x[1]-x[0]

    y: interable
        The independent variable to be binned

    dx_new: float
        The new resolution of the dependent variable x

    method: {"sum" | "average" | "mean"}, optional, default "sum"
        The method to be used in binning. Either sum the samples y in
        each new bin of x, or take the arithmetic mean.


    Returns
    -------
    xbin: numpy.ndarray
        The midpoints of the new bins in x

    ybin: numpy.ndarray
        The binned quantity y
    """

    dx_old = x[1] - x[0]

    assert dx_new >= dx_old, "New frequency resolution must be larger than " \
                             "old frequency resolution."

    step_size = dx_new/dx_old

    output = []
    for i in np.arange(0, y.shape[0], step_size):
        total = 0

        prev_frac = int(i+1) - i
        prev_bin = int(i)
        total += prev_frac * y[prev_bin]

        if i + step_size < len(x):
            # Fractional part of next bin:
            next_frac = i+step_size - int(i+step_size)
            next_bin = int(i+step_size)
            total += next_frac * y[next_bin]

        total += sum(y[int(i+1):int(i+step_size)])
        output.append(total)

    output = np.asarray(output)

    if method in ['mean', 'avg', 'average', 'arithmetic mean']:
        ybin = output/np.float(step_size)

    elif method == "sum":
        ybin = output
    else:
        raise Exception("Method for summing or averaging not recognized. "
                        "Please enter either 'sum' or 'mean'.")

    tseg = x[-1]-x[0]+dx_old

    if tseg/dx_new % 1 > 0:
        ybin = ybin[:-1]

    xbin = np.arange(ybin.shape[0])*dx_new + x[0]-dx_old + dx_new

    return xbin, ybin, step_size
