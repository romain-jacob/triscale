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
        # print('No bounds provided for x: series normalized based on min-max values.')
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
    elif CI_class is None:
        CI_class = 'one-sided'
        print('CI_class non-specified. Computing one-sided CIs.')

    if CI_class == 'one-sided':

        # 1. Compute the lower-bound of P_p

        p_work = percentile
        # compute all probabilities from the binomiale distribution for the percentile of interest
        bd=scipy.stats.binom(n_samples,p_work/100)
        ppm = [np.maximum(1-x,0.0) for x in np.cumsum([bd.pmf(k) for k in range(n_samples)])]

        # search the index defining a lower-bound for p_work
        if ppm[0] < confidence/100:
            LB=np.nan
        else:
            for k in range(n_samples):
                # search for first index reaching below the desired confidence
                if ppm[k] < confidence/100:
                    # lower-bound is the previous index
                    LB = k-1
                    break

        # 2. Compute the lower-bound of P_(1-p)

        p_work = 100 - percentile
        # compute all probabilities from the binomiale distribution for the percentile of interest
        bd=scipy.stats.binom(n_samples,p_work/100)
        ppm = [np.maximum(1-x,0.0) for x in np.cumsum([bd.pmf(k) for k in range(n_samples)])]

        # search the index defining a lower-bound for p_work
        if ppm[0] < confidence/100:
            tmp=np.nan
        else:
            for k in range(n_samples):
                # search for first index reaching below the desired confidence
                if ppm[k] < confidence/100:
                    # lower-bound is the previous index
                    tmp = k-1
                    break

        # 3. Deduce the upper-bound of P_p

        if np.isnan(tmp):
            UB = np.nan
        else:
            UB = ((n_samples-1) - tmp) # /!\ First index is 0 (not 1)

        return LB,UB

    if CI_class == 'two-sided':

        ## Median

        if percentile == 50:
            # compute all probabilities from the binomiale distribution for the percentile of interest
            bd=scipy.stats.binom(n_samples,0.5)
            ppm = [np.maximum(1-x,0.0) for x in np.cumsum([2*bd.pmf(k) for k in range(n_samples)])]

            # search the index defining a lower-bound for the median (two-sided)
            if ppm[0] < confidence/100:
                LB=np.nan
            else:
                for k in range(n_samples):
                    # search for first index reaching below the desired confidence
                    if ppm[k] < confidence/100:
                        # lower-bound is the previous index
                        LB = k-1
                        break

            # deduce the UB
            UB = ((n_samples-1) - LB) # /!\ First index is 0 (not 1)
            return LB,UB

        ## Other percentiles

        if percentile > 50:
            p_high = percentile
            p_low = 100 - percentile
        elif percentile < 50:
            p_low  = percentile
            p_high = 100 - percentile

        # 1. Compute lower-bound on P_low

        p_work = p_low
        # compute all probabilities from the binomiale distribution for the percentile of interest
        bd=scipy.stats.binom(n_samples,p_work/100)
        ppm = [np.maximum(1-x,0.0) for x in np.cumsum([bd.pmf(k) for k in range(n_samples)])]

        # search the index defining a lower-bound for p_work
        if ppm[0] < confidence/100:
            LB=np.nan
        else:
            for k in range(n_samples):
                # search for first index reaching below the desired confidence
                if ppm[k] < confidence/100:
                    # lower-bound is the previous index
                    LB = k-1
                    break

        # 2. Deduce the upper-bound of P_high

        if np.isnan(LB):
            UB = np.nan
        else:
            UB = ((n_samples-1) - LB) # /!\ First index is 0 (not 1)

        return LB,UB

def ThompsonCI_onesided( n_samples, percentile, confidence, CI_side='lower', verbose=False):
    '''This function computes a one-sided confidence interval for the given
    percentile, with the given confidence level.
    Unless CI_side='upper', a lower-bound is computed.
    The index of the sample is returned.
    None is returned if there are not enough samples for the desired CI.
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

    # Confidence and percentile must be between 0 and 100
    if confidence >= 100 or confidence <= 0:
        raise ValueError("Invalid confidence: "+repr(confidence)+". Provide a real number strictly between 0 and 100.")
    if percentile >= 100 or percentile <= 0:
        raise ValueError("Invalid percentile: "+repr(percentile)+". Provide a real number strictly between 0 and 100.")

    # Handling the CI_side
    if not (CI_side == 'lower' or CI_side == 'upper'):
        raise ValueError("Invalid CI_side: "+repr(CI_side)+". Valid 'CI_side' values: 'lower' or 'upper'")

    # Define the working percentile
    if CI_side == 'upper':
        p_work = 100 - percentile
    else:
        p_work = percentile

    # compute all probabilities from the binomiale distribution for the percentile of interest
    bd=scipy.stats.binom(n_samples,p_work/100)
    ppm = [np.maximum(1-x,0.0) for x in np.cumsum([bd.pmf(k) for k in range(n_samples)])]
    # print([bd.pmf(k) for k in range(n_samples+1)])
    # print([(1-bd.cdf(k)) for k in range(n_samples+1)])
    # print(ppm)

    # search the index defining a lower-bound for p_work
    if ppm[0] < confidence/100:
        return np.nan
    else:
        for k in range(n_samples):
            # search for first index reaching below the desired confidence
            if ppm[k] < confidence/100:
                # lower-bound is the previous index
                CI = k-1
                break

    # return the requested CI index
    if CI_side == 'lower':
        return CI
    else:
        return ((n_samples-1) - CI) # First index is 0 (not 1)


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
