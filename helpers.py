"""
Helper functions used by the TriScale modules
These functions are not part of TriScale API
(ie, not meant to be called by the user)
"""

import math

import numpy as np
import pandas as pd
import scipy
import scipy.stats

def theilslopes_normalized(y,x,confidence,y_bounds=[],x_bounds=[], tolerance_value=[], max_pairs=10000):
    """
    Extend stats.theilslopes
    -> https://docs.scipy.org/doc/scipy-0.17.1/reference/generated/scipy.stats.theilslopes.html

    First normalize x and y to [-1;+1].
    """

    ## Parse the inputs
    mask = np.isnan(y)
    x = x[~mask]
    y = y[~mask]
    assert x.shape[0] == y.shape[0], "x and y must be the same shape."

    ## Set the normalization bounds
    if not y_bounds:
#         print('No bounds provided for y: series normalized based on min-max values.')
        y_min = y.min()
        y_max = y.max()
    else:
        # Verify that bounds contain min/max
        # TODO
        y_min = y_bounds[0]
        y_max = y_bounds[1]
    if not x_bounds:
#         print('No bounds provided for x: series normalized based on min-max values.')
        x_min = x.min()
        x_max = x.max()
    else:
        # Verify that bounds contain min/max
        # TODO
        x_min = x_bounds[0]
        x_max = x_bounds[1]

    ## Randomly subsample x and y if they grow too big
    if (len(x)**2 - len(x)) > max_pairs:
        max_samples = int(np.floor(np.sqrt(max_pairs)))
        rand_index = np.random.choice(len(x), max_samples, replace=False)
        x = x[rand_index]
        y = y[rand_index]

    ## Regression on original series
    reg_orig = scipy.stats.theilslopes(y, x, confidence)
    reg_orig = scipy.stats.theilslopes(y, x, confidence)

    ## Normalization to [-1,+1]
    # x
    x_scale = x_max-x_min
    x = 2*x - (x_min + x_max)
    x = x/x_scale
    # y
    y_scale = y_max-y_min
    y = 2*y - (y_min + y_max)
    y = y/y_scale

    ## Regression on normalized series
    reg_norm = scipy.stats.theilslopes(y, x, confidence)

    # Compute the normalized trend coordinates
    coord_trend_norm = np.array([
        reg_norm[1] - reg_norm[0],  # med_min
        reg_norm[1] + reg_norm[0],  # med_max
        reg_norm[1] - reg_norm[2],  # lo_min
        reg_norm[1] + reg_norm[2],  # lo_max
        reg_norm[1] - reg_norm[3],  # up_min
        reg_norm[1] + reg_norm[3]]) # up_max
    # Revert y normalization to get coordinates in the original scale
    coord_trend_orig = (coord_trend_norm * y_scale + y_min + y_max )/2

    if tolerance_value:
        coord_tol_norm = np.array([
        reg_norm[1] + tolerance_value,  # lo_min
        reg_norm[1] - tolerance_value,  # lo_max
        reg_norm[1] - tolerance_value,  # up_min
        reg_norm[1] + tolerance_value]) # up_max
        coord_tol_orig = (coord_tol_norm   * y_scale + y_min + y_max )/2
    else:
        coord_tol_orig = np.array()

    return np.array((reg_orig,reg_norm)), np.array(coord_trend_orig) , np.array(coord_tol_orig)

def acorr(x):
    if type(x) != np.ndarray:
        x = np.array(x)
    x = x - x.mean()
    autocorr = np.correlate(x, x, mode='full')
    autocorr = autocorr[x.size-1:]
    if not np.isnan(autocorr.max()) and autocorr.max() != 0:
        autocorr /= autocorr.max()

    return autocorr

def independence_test(x):

    corr = acorr(x)
    test = abs(corr[1:]) < (1.96/np.sqrt(len(x)))

    if test.all():
        return True
    else:
        return False



def theil_convergence_test(x, y, y_bounds, confidence, tolerance, verbose=False):

    reg_all, coord_trend, coord_tol = theilslopes_normalized(
        y,
        x,
        confidence/100,
        y_bounds=y_bounds,
        tolerance_value=tolerance
    )

    # Keep only the regression on the normalized data
    reg = reg_all[1,:]

    # Output the result of the convergence test
    # The average link quality is considered stationary if
    # - The condidence interval on the trend includes 0
    # - The condidence interval on the trend is included in [+/-stationary_threshold]
    if tolerance < 0:
        tolerance = -tolerance

    output_log = ''
    has_converged=True

    # if reg[2] > 0 or reg[3] < 0:
    #     output_log += ('/!\\ Non-stationary /!\\\n')
    #     output_log += ('The '+str(confidence)+'% CI on the link quality trend does not include 0.\n')
    #     output_log += (str(confidence)+'% CI(scaled): \t['+str(reg[2])+' , '+str(reg[3])+']\n')
    #     has_converged=False

    if reg[2] < -tolerance or reg[3] > tolerance:
        output_log += ('/!\\ Non-stationary /!\\\n')
        output_log += ('The '+str(confidence)+'% CI on the link quality trend exceeds the tolerance.\n')
        output_log += (str(confidence)+'% CI(scaled): \t['+str(reg[2])+' , '+str(reg[3])+']\n')
        output_log += ('Tolerance: \t\t[-'+str(tolerance)+' , '+str(tolerance)+']\n')
        has_converged=False

    if has_converged:
        output_log += ('Environment appears to be stationary!\n')
        output_log += ('The '+str(confidence)+'% CI on the link quality trend meets all criteria.\n')
        output_log += (str(confidence)+'% CI (scaled): \t['+str(reg[2])+' , '+str(reg[3])+']\n')
        output_log += ('Tolerance: \t\t[-'+str(tolerance)+' , '+str(tolerance)+']\n')

    if verbose:
        print(output_log)

    return (has_converged, coord_trend, coord_tol)

def convergence_test(x, y, y_bounds, confidence, tolerance, verbose=False):

    if isinstance(x, pd.DatetimeIndex):
        x_reg = x.astype(np.int64) // 10**9
    else:
        x_reg = x

    ##
    # Perform the linear regression using Theil-Sen estimator
    ##
    results = theil_convergence_test(x_reg,
                                     y,
                                     y_bounds,
                                     confidence,
                                     tolerance/100,
                                     verbose=verbose)

    return results

def min_number_samples(percentile,confidence,robustness=0):

    ##
    # Checking the inputs
    ##

    if confidence >= 100 or confidence <= 0:
        raise ValueError("Invalid confidence: "+repr(confidence)+". Provide a real number strictly between 0 and 100.")
    if percentile >= 100 or percentile <= 0:
        raise ValueError("Invalid percentile: "+repr(percentile)+". Provide a real number strictly between 0 and 100.")
    if not isinstance(robustness, int):
        raise ValueError("Invalid robustness: "+repr(robustness)+". Provide a positive integer.")
    if robustness < 0:
        raise ValueError("Invalid robustness: "+repr(robustness)+". Provide a positive integer.")

    ##
    # Single-sided interval
    ##

    N_single = math.ceil(math.log(1-confidence/100)/math.log(1-percentile/100))

    if robustness:

        # Make sure the first N is large enough
        N_single = max(N_single, 2*(robustness+1))

        # Increse N until the desired confidence is reached
        while True:
            # compute P( x_(1+r) <= Pp )
            bd = scipy.stats.binom(N_single,percentile/100)
            prob = 1-np.cumsum([bd.pmf(k) for k in range(robustness+1)])[-1]
            # test
            if prob >= (confidence/100):
                break
            else:
                N_single += 1

    ##
    # Double-sided interval
    ##

    # only relevant for the median - other percentiles are better estimated with single-sided intervals
    if percentile==50:

        N_double = math.ceil(1 - (math.log(1-confidence/100)/math.log(2)))

        if robustness:

            # Make sure the first N is large enough
            N_double = max(N_double, 2*(robustness+1))

            # Increse N until the desired confidence is reached
            while True:
                # compute P( x_(1+r) <= M <= x_(N-r) )
                bd = scipy.stats.binom(N_double,percentile/100)
                prob = 1-np.cumsum([2*bd.pmf(k) for k in range(robustness+1)])[-1]
                # test
                if prob >= (confidence/100):
                    break
                else:
                    N_double += 1

    else:
        # Double-sided interval is irrelevant -> same as single-sided
        N_double = N_single

    return N_single, N_double



# TODO:
# + polish the return data format
# + add a "verbose" parameter for printing
def ThompsonCI( n_samples, percentile, confidence, CI_class=None, verbose=False):
    '''This function computes the confidence interval for the given percentile
    of the data array, with the given confidence level.
    '''


    todo = ''
    todo += '# ---------------------------------------------------------------- \n'
    todo += '# TODO ThompsonCI \n'
    todo += '# ---------------------------------------------------------------- \n'
    todo += '- write the doctring\n'
    todo += '- check input types\n'
    todo += '- clean-up\n'
    todo += '# ---------------------------------------------------------------- \n'
    if verbose:
        print('%s' % todo)

    ##
    # Checking the inputs
    ##

    if confidence >= 100 or confidence <= 0:
        raise ValueError("Invalid confidence: "+repr(confidence)+". Provide a real number strictly between 0 and 100.")
    if percentile >= 100 or percentile <= 0:
        raise ValueError("Invalid percentile: "+repr(percentile)+". Provide a real number strictly between 0 and 100.")

    # Handling the CI_class parameter
    if not (CI_class == 'one-sided' or CI_class == 'two-sided' or CI_class is None):
        raise ValueError("Invalid CI_class: "+repr(CI_class)+". Valid 'CI_class' values: 'one-sided' or 'two-sided'")
    if percentile == 50 and CI_class is None:
        raise ValueError("CI_class parameter is required for computing a confidence interval for the median. Valid 'CI_class' values: 'one-sided' or 'two-sided'")

    # Always work with lower percentiles and compute a lower-bound (single-sided confidence interval)
    if percentile > 50:
        p_high = percentile
        p_low = 100 - percentile
    else:
        p_low  = percentile
        p_high = 100 - percentile

    Nmax = int(n_samples/2)
    firstel = range(Nmax)
    lastel = [n_samples-1-k for k in firstel]

    # compute all probabilities from the binomiale distribution for the percentile of interest
    bd=scipy.stats.binom(n_samples,p_low/100)
    ppm = [np.maximum(1-x,0.0) for x in np.cumsum([bd.pmf(k) for k in firstel])]

    if percentile == 50 and CI_class == 'two-sided':
        ppm = [np.maximum(1-x,0.0) for x in np.cumsum([2*bd.pmf(k) for k in firstel])]
    else:
        ppm = [np.maximum(1-x,0.0) for x in np.cumsum([bd.pmf(k) for k in firstel])]


    # check the probabilities against the confidence level desired
    CI = None
    output_log = ''
    for k in reversed(range(Nmax)):
        if ppm[k]>=confidence/100:
            CI = [ firstel[k], lastel[k] ]
#                 CI = [ firstel[k]+1, lastel[k]+1, serie[firstel[k]], serie[lastel[k]] ]

            if verbose:
                output_log += ('With %g data samples\n') %  n_samples

                if percentile == 50 and CI_class == 'two-sided':
                    output_log += ('( x[%g], x[%g] ) is a %.0f%%-confidence interval for the median') % (
                        CI[0], CI[1], confidence )
                    output_log += (' (two-sided).')

                if percentile == 50 and CI_class == 'one-sided':
                    output_log += ('x[%g] and x[%g] are the lower- and upper- bounds ') % ( CI[0], CI[1] )
                    output_log += ('of %.0f%%-confidence intervals for the median') % ( confidence )
                    output_log += (' (one-sided).')

                if percentile != 50:
                    output_log += ('x[%g] and x[%g] are the lower- and upper- bounds ') % ( CI[0], CI[1] )
                    output_log += ('of %.0f%%-confidence intervals for P_%.0f and P_%.0f') % ( confidence, p_low, p_high )
                    output_log += (' (one-sided).')

            break

    if CI is None:
        CI = [ np.nan, np.nan ]
        output_log += ('%g is not enough data samples to estimate a %.0f%% confidence interval for '
                       % ( n_samples, confidence ))
        if percentile != 50:
            output_log += ('P_%.0f and P_%.0f.') % ( p_low, p_high )
        else:
            output_log += 'the median'
            if CI_class == 'two-sided':
                output_log += (' (two-sided).')
            else:
                output_log += (' (one-sided).')

    if verbose:
        print(output_log)

    return CI


def repeatability_test( data,
                        confidence_repeatability=95,
                        tolerance_repeatability=None):

        # Make sure data is sorted
        data.sort()

        # get the index ranges
        N = len(data)
        Nmax = int(N/2)
        firstel = range(Nmax)
        lastel = [N-1-k for k in firstel]

        # compute all probabilities from the binomiale distribution for the median
        bd=scipy.stats.binom(N,0.5)
        ppm = [np.maximum(1-x,0.0) for x in np.cumsum([2*bd.pmf(k) for k in firstel])]

        # check the probabilities against the confidence level desired
        serie_bound = None
        for k in reversed(range(Nmax)):
            if ppm[k]>=confidence_repeatability/100:
                serie_bound = [ firstel[k]+1, lastel[k]+1, data[firstel[k]], data[lastel[k]] ]
                break
        if serie_bound is None:
            print('You do not have enough data to report a %.0f%s confidence interval. Repeatability cannot be assessed with that level of confidence.' % (confidence_repeatability,'%'))
            return

        # compute the CI error and compare against the tolerance
        CI_mean = ( data[lastel[k]] + data[firstel[k]] ) / 2
        error = (data[lastel[k]] - data[firstel[k]])/(2*CI_mean)

        if tolerance_repeatability is None:
            return error

        if error < tolerance_repeatability/100:
#             print('repeatable')
            return True
        else:
#             print('not repeatable')
            return False
