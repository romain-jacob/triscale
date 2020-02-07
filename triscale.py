"""
triscale module

Public API
    network_profiling
    experiment_sizing
    analysis_metric
    analysis_kpi
    analysis_variability
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from helpers import convergence_test, ThompsonCI, independence_test, min_number_samples, repeatability_test
from triplots import theil_plot, autocorr_plot, ThompsonCI_plot

# ----------------------------------------------------------------------------------------------------------------------------
# NETWORK PROFILING
# ----------------------------------------------------------------------------------------------------------------------------

def network_profiling(  link_quality_data,
                        link_quality_bounds,
                        link_quality_name=None,
                        print_output=False,
                        verbose=False):
    """
    Perform the network profiling as suggested by TriScale [1].

    The function looks for seasonal components in the link quality data.
    The input data must be an equally spaced time series. The function aims
    to identify seosanality with periodicity of at least twice the period
    of the input data (i.e., if the data period is one hour, the minimal
    seasonal component that may be detected is a two-hour correlation).

    This function first performs TriScale's convergence test on the link quality
    data (using 95% confidence level and 1% tolerance). The time series and
    its Theil-Sen [3] linear regression are plotted.

    If the convergence test is passed, the function continues with TriScale's
    independence test, which verify whether the network link quality data
    appears i.i.d.
    If both tests are passed, it indicates that there is no significant
    seasonal component in the data.
    Overwise, the pics in the autocorellation plot identify the seasonal
    components in the link quality data.

    Parameters
    ----------
    link_quality_data : pandas DataFrame
        Contains link quality data from the network where the experiment is
        expected to be performed.
        - Must contain a `link_quality` column.
        - Must contain a `data_time` column or having a DatetimeIndex.
    link_quality_bounds : list-like of len 2.
        Expected extremal values for the link quality data,
        used for the convergence test.
    link_quality_name : string, optional
        Label for the plots axis.
        Default : None
    print_output : True/False, optional
        When True, produces and displays a textual summary of the network
        profiling analysis.
        Default : False
    verbose : True/False, optional
        When true, print non-functional and intermediary outputs.
        Default : False

    Returns
    -------
    figure : plotly graphical object
        The function produces and display the autocorellation plot of the
        link quality data. The figure is returned to the user (e.g., to modify
        the default layout).

    Notes
    -----
    - Computing autocorrelation of a time series requires equally spaced values.
    Missing values must be interpolated based on existing data to compute the
    autocorrelation coefficients.
    In this function, missing values are replaced by the median of all
    collected values.
    - The autocolleration plot shows the the 95th confidence interval for the
    autocorrelation coefficient values such that the data appears i.i.d.
    This confidence interval is computed as +/-1.95*sqrt(N),
    where N is the number of samples [2].
    - A textual output of network profiling analysis is triggered by the
    `print_output` parameter. The current implementation is minimal (it only
    says whether the link quality data appears to be i.i.d.).

    References
    ----------
    .. [1] Anonymous, "TriScale: A Framework Supporting Reproducible Networking
        Evaluations", Submitted to NSDI, 2020,
        https://doi.org/10.5281/zenodo.3464273
    .. [2] Peter J. Brockwell, Richard A. Davis, and Stephen E. Fienberg.
        "Time Series: Theory and Methods: Theory and Methods." Springer Science
        & Business Media, 1991.
    .. [3] Henri Theil. A Rank-Invariant Method of Linear and Polynomial
        Regression Analysis. In Baldev Raj and Johan Koerts, editors,
        Henri Theil’s Contributions to Economics and Econometrics: Econometric
        Theory and Methodology, Advanced Studies in Theoretical and Applied
        Econometrics, pages 345–381. Springer Netherlands, Dordrecht, 1992.
    """

    todo = ''
    todo += '# ---------------------------------------------------------------- \n'
    todo += '# TODO network_profiling \n'
    todo += '# ---------------------------------------------------------------- \n'
    todo += '- verbose display (clearly) advising people what they should do\n'
    todo += 'i.e., how long should be the time span of an experiment\n'
    todo += '- input check\n'
    todo += '- handle the intermediary outputs\n'
    todo += '- check and format the final output: stationary + independence\n'
    todo += '# ---------------------------------------------------------------- \n'

    if verbose:
        print('%s' % todo)

    convergence = { 'expected': True,
                    'confidence': 95,  # in %
                    'tolerance': 1,    # in %
                    }

    # network_name = 'FlockLab - DPP-cc430'
    profiling_output = ''
    profiling_output += '# ---------------------------------------------------------------- \n'
    profiling_output += '# TriScale report - Network profiling\n'
    profiling_output += '# ---------------------------------------------------------------- \n'
    # profiling_output += '\nNetwork \t%s\n' % (network_name)


    ##
    # Checking the inputs
    ##

    ##
    # Data must be a dataframe with (at least) two columns
    # - link_quality
    # - date_time (can also be the index)
    if 'link_quality' not in link_quality_data.columns:
        raise ValueError("""Wrong input. The 'data' DataFrame must contain a
                            'link_quality' column.""")

    if ('date_time' not in link_quality_data.columns) and (
        not isinstance(link_quality_data.index, pd.DatetimeIndex)):
        raise ValueError("""Wrong input.
                            The 'data' DataFrame must contain a 'date_time'
                            column or have DatetimeIndex type.""")

    # Parse dates
    if 'date_time' in link_quality_data.columns:
        link_quality_data['date_time'] = pd.to_datetime(
                                            link_quality_data['date_time'],
                                            utc=True)
        link_quality_data.set_index('date_time')
    # Make sure the DataFrame is sorted
    link_quality_data.sort_index(inplace=True)

    profiling_output += '\nProfiling time span\n'
    profiling_output += 'from \t\t%s\n' % link_quality_data.index[0]
    profiling_output += 'to \t\t%s\n' % link_quality_data.index[-1]
    profiling_output += '\nProfiling granularity\n'
    profiling_output += '\t\t%s\n' % (  link_quality_data.index[1]
                                        - link_quality_data.index[0] )
    profiling_output += '\n# ---------------------------------------------------------------- \n'

    ##
    # Convergence test
    ##

    # Compute the trend of link quality data
    results = convergence_test( link_quality_data.index,
                                link_quality_data.link_quality.values,
                                link_quality_bounds,
                                convergence['confidence'],
                                convergence['tolerance'])

    # Plot the time series and its trend
    default_layout={'xaxis' : {'title':None},
                    'yaxis' : {'title':link_quality_name}}
    datetime = np.array(link_quality_data.index, dtype=object)
    fig_theil = theil_plot( link_quality_data.link_quality.values,
                            x=datetime,
                            convergence_data=results,
                            layout=default_layout)

    ##
    # Stationarity test
    ##

    # Replace missing samples with the series median
    # -> We need continuous data for autocorrelation
    data = link_quality_data.link_quality.values
    data[np.isnan(data)] = np.nanmedian(data)

    stationary = independence_test(data)
    if stationary:
        profiling_output += '\nNetwork link quality appears I.I.D.'
        profiling_output += '(95%% confidence)\n'
    else:
        profiling_output += '\nNetwork link quality does NOT appears I.D.D. !\n\n'
        # profiling_output += '\nNetwork link quality does NOT appears I.D.D. !\nSearching for a suitable time interval...\n\n'

    # Plot the autocorrelation
    fig_autocorr = autocorr_plot(data, show=False)

#     # Search for a suitable test window
#     window_size = 1
#     while not stationary:
#         window_size += 1
#         data_subsampled = [np.nanmean(np.array(data[i:i+window_size])) for i in np.arange(0, len(data), window_size)]
#         stationary = independence_test(data_subsampled)
#         profiling_output += 'Window size: %g\tStationary: %i\n' % (window_size, stationary)
# #         plot_autocorr(data_subsampled)
#
#     # Compute the corresponding time span
#     time_span = link_quality_data.index[window_size] - link_quality_data.index[0]
#
#     profiling_output += '\n\nWith a confidence of 95%\n'
#     profiling_output += 'network link quality appears stationary over a \n'
#     profiling_output += 'time span of'
#     profiling_output += '\t%s\n' % (time_span)
#     profiling_output += '\n# ---------------------------------------------------------------- \n'

    if print_output:
        print(profiling_output)

    return fig_theil, fig_autocorr

# ----------------------------------------------------------------------------------------------------------------------------
# EXPERIMENT SIZING
# ----------------------------------------------------------------------------------------------------------------------------

def experiment_sizing(percentile,
                      confidence,
                      robustness=0,
                      CI_class='one-sided',
                      verbose=False):
    """
    Experiment sizing as suggested by TriScale [1].

    The function returns the minimal number of data samples required to
    computes a one-sided and a two-sided CI for `percentile`,
    with `confidence` confidence level and with `robustness` data samples
    excluded.

    Computation based on [2].

    Parameters
    ----------
    percentile : float
        Percentile to estimate, must be between 0 and 100
    confidence : float
        Confidence level of the estimation, must be between 0 and 100
    robustness : positive integer, optional
        Number to samples to exclude from the estimation
    CI_class : 'one-sided' or 'two-sided', optional
        The class of confidence interval: one- or two-sided.
        Used only for textual output, displayed when `verbose` is True.
        Default : 'one-sided'
    verbose : True/False, optional
        When true, print non-functional and intermediary outputs.
        Default : False

    Returns
    -------
    N_one : integer
        Minimal number of samples for a one-sided CI for `percentile`,
        with `confidence` confidence level, and with `robustness` data samples
        excluded.
    N_two : integer
        Minimal number of samples for a two-sided CI for `percentile`,
        with `confidence` confidence level, and with `robustness` data samples
        excluded.

    References
    ----------
    .. [1] Anonymous, "TriScale: A Framework Supporting Reproducible Networking
        Evaluations", Submitted to NSDI, 2020,
        https://doi.org/10.5281/zenodo.3464273
    .. [2] William R. Thompson, "On Confidence Ranges for the Median and Other
        Expectation Distributions for Populations of Unknown Distribution Form",
        The Annals of Mathematical Statistics, 7(3):122–128, 1936.

    """

    # todo = ''
    # todo += '# ---------------------------------------------------------------- \n'
    # todo += '# TODO experiment_design\n'
    # todo += '# ---------------------------------------------------------------- \n'
    # todo += '# ---------------------------------------------------------------- \n'
    # if verbose:
    #     print('%s' % todo)

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
    if not (CI_class == 'one-sided' or CI_class == 'two-sided'):
        raise ValueError("""Invalid CI_class: %s
                            Valid 'CI_class' values: 'one-sided' or 'two-sided'
                            """ % (repr(CI_class)) )

    # Work with lower-percentiles
    if percentile > 50:
        wk_perc = 100-percentile
    else:
        wk_perc = percentile

    # Compute the minimal number
    # necessary to estimate the given percentile ant the given confidence
    # (possibly with a given number of data sample to omit = robustness)
    N_one, N_two = min_number_samples(wk_perc,confidence,robustness)
    if verbose:
        out = ''
        if CI_class == 'one-sided':
            out += ('A one-sided bound of the \t%i-th percentile\n'
                    % (percentile))
        else:
            out += ('A two-sided bound of the \t%i-th percentile\n'
                    % (percentile))
        out += ('with a confidence level of\t%i %% \n'
                % (confidence))

        if CI_class == 'one-sided':
            out += 'requires a minimum of \t\t%i samples\n' % (N_one)
        else:
            out += 'requires a minimum of \t\t%i samples\n' % (N_two)

        if robustness != 0:
            out += 'with the worst \t\t\t%i run(s) excluded\n' % (robustness)

        print(out)

    return N_one, N_two


# ----------------------------------------------------------------------------------------------------------------------------
# ANALYSIS_METRIC
# ----------------------------------------------------------------------------------------------------------------------------

def analysis_metric(    data,
                        metric,
                        convergence=None,
                        plot=False,
                        plot_out_name=None,
                        showplot=True,
                        custom_layout=None,
                        verbose=False):
    """
    Computation of metrics as suggested by TriScale [1].

    Parameters
    ----------
    data : string or pandas DataFrame
        The input data is a two-dimentional series used for the computation of
        the metric: one control variate (x), one independent variate (y).
        - When a string is passed, `data` is expected to be a name of a csv file
        (comma separated) with `x` data in the first column and `y` data in the
        second column.
        - When a pandas DataFrame is passed, `data` must contain (at least)
        columns named `x` and `y`.
    metric : dictionary
        TriScale metric dictionary.
        - "measure" key is compulsory. The corresponding value is a float
        between 0 and 100 and correspond to the percentile used as performance
        measure for that metric.
        Optional keys:
            - "bounds" : list-like of len 2.
            Expected extremal values for the measure, used for the convergence test.
            - "name"/"units" : strings, for plot layout only
    convergence : dictionary or None
        TriScale convergence dictionary
        - "expected" : True/False
        Triggers the computation of TriScale convergence test when set to True.
        - "confidence" : float, optional
        Confidence level for TriScale convergence test.
        Float between 0 and 100, default to 95.
        - "tolerance" : float, optional
        Tolerance for TriScale convergence test.
        Float between 0 and 100, default to 1.
    plot : True/False, optional
        When true, generate a plot of the input data and convergence data
        (if any).
        Default : False
    plot_out_name : string or None, optional
        When a string, triggers saving of the plot under `plot_out_name` as
        file name (if `plot` is True)
        Default : None
    showplot : True/False, optional
        When true, display the generated plot (if `plot` is True).
        Default : True
    custom_layout : dictionary or None, optional
        Plotly layout dictionary to edit the default layout of the
        generated plot.
        Default : None
    verbose : True/False, optional
        When true, print non-functional and intermediary outputs.
        Default : False

    Returns
    -------
    convergence test result : True/False
        The outcome of the convergence test, when
        `convergence["expected"] == True`
        Always True otherwise.
    measure :
        The computed metric measure, interpolated to `nearest`.
    figure : plotly graphical object or None
        The generated plot when `plot == True`

    References
    ----------
    .. [1] Anonymous, "TriScale: A Framework Supporting Reproducible Networking
        Evaluations", Submitted to NSDI, 2020,
        https://doi.org/10.5281/zenodo.3464273

    """

    todo = ''
    todo += '# ---------------------------------------------------------------- \n'
    todo += '# TODO analysis_preprocessing \n'
    todo += '# ---------------------------------------------------------------- \n'
    todo += '\n'
    # todo += '- modif convergence_test() to output a dictionary\n'
    todo += '- check for crazy values in the input dictionaries\n'
    todo += '# ---------------------------------------------------------------- \n'
    if verbose:
        print('%s' % todo)

    ##
    # Checking the inputs
    ##

    # Parse data
    if isinstance(data, str):
        try:
            df = pd.read_csv(data, delimiter=',', names=['x', 'y'], header=0)
        except FileNotFoundError:
            if verbose:
                print(repr(data) + " not found")
            return False, np.nan, None
    elif isinstance(data, pd.DataFrame):
        try:
            df = data[['x', 'y']]
        except KeyError:
            raise ValueError("Input DataFrame must contain columns names 'x' and 'y'.")
    else:
        raise ValueError("Wrong input type. Expect a string or a DataFrame, got "+repr(data)+".")


    # Verify that the csv file is not empty (at least some 'y' data is in there)
    df.dropna(inplace=True)
    if len(df.index) < 20:
        if verbose:
            print("Input file has only %d data points (min 20 required) (%s)"
                        % ( len(df.index), data_file ))
        return False, np.nan, None


    # Metric
    if 'bounds' not in metric:
        metric['bounds'] = [df.y.min(), df.y.max()]

    if 'name' not in metric:
        metric['name'] = None
        metric_label = ''
    else:
        metric_label = metric['name']
        if 'unit' in metric:
            metric_label += ' [' + metric['unit'] + ']'

    # Convergence
    if convergence is not None and convergence['expected'] == True:

        # Convergence test should run
        run_convergence_test = True

        # Check the confidence and tolerance values
        if 'confidence' not in convergence:
            # Default to 95% confidence
            convergence['confidence'] = 95
        if 'tolerance' not in convergence:
            # Default to 1% tolerance
            convergence['tolerance'] = 1
    else:
        run_convergence_test = False

    ##
    # Convergence test
    ##
    if run_convergence_test:

        # Compute the metric series
        samples_x  = df.x.values
        samples_y  = df.y.values
        metric_y = []
        metric_x = []

        if len(samples_y) > 200:
            nb_chuncks = 200
        else:
            nb_chuncks = len(samples_y)

        # for chuncks in range(int(nb_chuncks/2),nb_chuncks+1):
        for chuncks in range(0,int(nb_chuncks/2)):
            chunck_x   = chuncks*2+1
            chunck_len = int((int(nb_chuncks/2+chuncks)*len(samples_y)/nb_chuncks))
            metric_y.append(np.percentile(  samples_y[:chunck_len],
                                            metric['measure'],
                                            interpolation='midpoint' ))
            metric_x.append(samples_x[int(chunck_x*len(samples_y)/nb_chuncks)])
            # print(chunck_x, metric_x)

        # Convergence test
        results = convergence_test(np.array(metric_x),
                                   np.array(metric_y),
                                   metric['bounds'],
                                   convergence['confidence'],
                                   convergence['tolerance'],
                                   verbose=verbose)

        if results[0]:
            has_converged = True
        else:
            has_converged = False

        # Produce the output string
        if verbose:
            if has_converged:
                flag_convergence1 = '[ PASSING ]'
                flag_convergence2 = ''
                preprocessing_warning = '\n'
            else:
                flag_convergence1 = '[ FAILED ]'
                flag_convergence2 = 'NOT '
                preprocessing_warning = '\n[ WARNING ] These data should not be used to estimate \nthe long-term performance of the system under test!\n'

            preprocessing_output = ''
            preprocessing_output += '%s\n' % flag_convergence1
            preprocessing_output += 'With a confidence level of \t%g%%\n' % (convergence['confidence'])
            preprocessing_output += 'given a tolerance of \t\t%g%%\n' % (convergence['tolerance'])
            preprocessing_output += 'Run has %sconverged.\n' % flag_convergence2
            preprocessing_output += '%s' % preprocessing_warning

            print(preprocessing_output)
    else:
        results = None

    ##
    # Plot
    ##
    if plot:
        default_layout={'title' : ('%s' % metric_label),
                        'xaxis' : {'title':None},
                        'yaxis' : {'title':metric_label}}
        if custom_layout is not None:
            default_layout.update(custom_layout)
        figure = theil_plot(    samples_y,
                                x=samples_x,
                                metric_data=[metric_x, metric_y],
                                convergence_data=results,
                                layout=default_layout,
                                out_name=plot_out_name)
        if showplot:
            figure.show()
    else:
        figure = None

    ##
    # Return the run's measure
    ##

    if run_convergence_test:
        # Test failed
        if not has_converged:
            return False, np.nan, figure
        # Test passed
        else:
            return True, np.percentile(metric_y, 50 , interpolation='nearest'), figure
    else:
        return True, np.percentile(df.y.values, metric['measure'] , interpolation='nearest'), figure



# ----------------------------------------------------------------------------------------------------------------------------
# ANALYSIS_KPI
# ----------------------------------------------------------------------------------------------------------------------------

def analysis_kpi(data,
                 KPI,
                 to_plot=None,
                 plot_out_name=None,
                 custom_layout=None,
                 verbose=False):
    """
    Computation of KPIs as suggested by TriScale [1].

    Parameters
    ----------
    data : 1-d np.array or list
        The metric data for a series of run.
    KPI : dictionary
        TriScale KPI dictionary.
        Compulsory keys:
            - "percentile" : float
            Percentile to estimate, float between 0 and 100
            - "confidence" : float
            Confidence level for the percentile estimation,
            float between 50 and 100
            - "bounds" : list-like of len 2.
            Expected extremal values for the measure,
            used for the stationarity test.
        Optional keys:
            - "name"/"units" : strings, for plot layout only
            - "bound" : 'upper' or 'lower'
            Set whether the KPI is an upper- or lower-bound of the percentile.
            Inferred based on the percentile value:
                * 'lower' if `percentile < 50`
                * 'upper' if `percentile > 50`
            Must be defined by the user of `percentile == 50`
    to_plot : list of strings or None (default), optional
        List of plots to produce. Valid plot names are
        'autocorr', 'horizontal', 'vertical'
    plot_out_name : string or None, optional
        File name to save the 'horizontal' or 'vertical' plot.
        Default : None
    custom_layout : dictionary or None, optional
        Plotly layout dictionary to edit the default layout of the
        generated plot.
        Default : None
    verbose : True/False, optional
        When true, print non-functional and intermediary outputs.
        Default : False

    Returns
    -------
    independence test result : True/False
        The outcome of the independence test
    KPI_out : float or NaN
        NaN if there are not enough data points to compute the KPI,
        computed KPI value otherwise.

    References
    ----------
    .. [1] Anonymous, "TriScale: A Framework Supporting Reproducible Networking
        Evaluations", Submitted to NSDI, 2020,
        https://doi.org/10.5281/zenodo.3464273

    """

    todo = ''
    todo += '# ---------------------------------------------------------------- \n'
    todo += '# TODO analysis_kpi \n'
    todo += '# ---------------------------------------------------------------- \n'
    todo += '# ---------------------------------------------------------------- \n'
    if verbose:
        print('%s' % todo)


    ##
    # Input checks
    ##

    # Force one-sided CI for the KPI
    if 'class' in KPI:
        if KPI['class'] != 'one-sided':
            KPI['class'] = 'one-sided'
            raise ValueError("TriScale KPIs can only have 'class' 'one-sided'.")
    else:
        KPI['class'] = 'one-sided'

    if 'bound' not in KPI:
        if KPI['percentile'] > 50:
            KPI['bound'] = 'upper'
        elif KPI['percentile'] < 50:
            KPI['bound'] = 'lower'
        else:
            if KPI['percentile'] == 50:
                raise ValueError("If the median is used as percentile, \n"
                             "\t\tspecify the desired 'bound': 'lower' of 'upper'")

    # For now, we assume the inputs are correct...
    output_log = ''
    sorted_data = np.sort(data)

    ##
    # Independence test
    ##
    if len(data) < 2:
        weak_stationary = False
    else:

        weak_stationary, trend, tol = convergence_test(np.arange(len(data)),
                                           np.array(data),
                                           KPI['bounds'],
                                           50,
                                           10)
    stationary = independence_test(data)
    stationary = (stationary and weak_stationary)

    if stationary:
        output_log += ('Data appears i.i.d. (95%% confidence)\n')
    else:
        # Check whether the data points have all the same value
        # -> This leads the stationarity test to fail
        # -> TriScale considers this as valid, but raises a warning.
        if sorted_data[0] == sorted_data[-1]:
            stationary = True
            output_log += ('All data points are the same. Considered stationary.\n')
            output_log += ('(but maybe you want to double-check that the data is really constant...)\n')
        else:
            output_log += ('Data appears NOT I.D.D. !\n')
            output_log += ('Analysis continues but results are not trustworthy...')

    if verbose:
        print(output_log)

    ##
    # Compute the KPI
    ##
    KPI_bounds = ThompsonCI(len(data),
                           KPI['percentile'],
                           KPI['confidence'],
                           KPI['class'],
                           verbose)
    ##
    # Plots
    ##
    if to_plot is not None:
        if 'autocorr' in to_plot:
            autocorr_plot( data )

        layout = go.Layout(
            title=KPI['name'],
            width=500)
        if custom_layout is not None:
            layout.update(custom_layout)
        if not np.isnan(KPI_bounds[0]):
            if 'horizontal' in to_plot:
                ThompsonCI_plot( data, KPI_bounds, KPI['bound'], 'horizontal', layout, out_name=plot_out_name)
            if 'vertical' in to_plot:
                ThompsonCI_plot( data, KPI_bounds, KPI['bound'], 'vertical', layout, out_name=plot_out_name)

    ##
    # outputs
    ##
    if KPI_bounds == [np.nan, np.nan]:
        return stationary, np.nan

    if KPI['bound'] == 'upper':
        KPI_out = sorted_data[KPI_bounds[1]]
    else:
        KPI_out = sorted_data[KPI_bounds[0]]

    return stationary, KPI_out

# ----------------------------------------------------------------------------------------------------------------------------
# ANALYSIS_VARIABILITY
# ----------------------------------------------------------------------------------------------------------------------------

def analysis_variability(data,
                         score,
                         to_plot=None,
                         plot_out_name=None,
                         custom_layout=None,
                         verbose=False):
    """
    Computation of variability scores as suggested by TriScale [1].

    Parameters
    ----------
    data : 1-d np.array or list
        The metric data for a series of run.
    score : dictionary
        TriScale score dictionary.
        Compulsory keys:
            - "percentile" : float
            Percentile to estimate, float between 0 and 100
            - "confidence" : float
            Confidence level for the percentile estimation,
            float between 50 and 100
            - "bounds" : list-like of len 2.
            Expected extremal values for the measure,
            used for the stationarity test.
        Optional keys:
            - "name"/"units" : strings, for plot layout only
    to_plot : list of strings or None (default), optional
        List of plots to produce. Valid plot names are
        'autocorr', 'horizontal', 'vertical'
    plot_out_name : string or None, optional
        File name to save the 'horizontal' or 'vertical' plot.
        Default : None
    custom_layout : dictionary or None, optional
        Plotly layout dictionary to edit the default layout of the
        generated plot.
        Default : None
    verbose : True/False, optional
        When true, print non-functional and intermediary outputs.
        Default : False

    Returns
    -------
    independence test result : True/False
        The outcome of the independence test
    score lower-bound : float
        Lower-bound of the CI defining the variability score
    score upper-bound : float
        Upper-bound of the CI defining the variability score
    score : float
        Variability score (absolute)
    relative score : float
        Variability score (relative) : score / mean(upper-bound, lower-bound)

    References
    ----------
    .. [1] Anonymous, "TriScale: A Framework Supporting Reproducible Networking
        Evaluations", Submitted to NSDI, 2020,
        https://doi.org/10.5281/zenodo.3464273

    """

    todo = ''
    todo += '# ---------------------------------------------------------------- \n'
    todo += '# TODO analysis_repeatability \n'
    todo += '# ---------------------------------------------------------------- \n'
    todo += '# ---------------------------------------------------------------- \n'
    if verbose:
        print('%s' % todo)

    ##
    # Independence test
    ##
    if len(data) < 2:
        weak_stationary = False
    else:

        weak_stationary, trend, tol = convergence_test(np.arange(len(data)),
                                           np.array(data),
                                           score['bounds'],
                                           50,
                                           10)
    stationary = independence_test(data)
    stationary = (stationary and weak_stationary)

    output_log = ''
    if stationary:
        output_log += ('Data appears i.i.d. (95%% confidence)\n')
    else:
        # Check whether the data points have all the same value
        # -> This leads the stationarity test to fail
        # -> TriScale considers this as valid, but raises a warning.
        if data[0] == data[-1]:
            stationary = True
            output_log += ('All data points are the same. Considered stationary.\n')
            output_log += ('(but maybe you want to double-check that the data is really constant...)\n')
        else:
            output_log += ('Data appears NOT I.D.D. !\n')
            output_log += ('Analysis continues but results are not trustworthy...')

    if verbose:
        print(output_log)

    ##
    # Compute the repeatability bounds
    ##
    variability_bound = ThompsonCI(len(data),
                                   score['percentile'],
                                   score['confidence'],
                                   'two-sided',
                                   verbose)

    ##
    # Plots
    ##
    if to_plot is not None:

        if 'autocorr' in to_plot:
            autocorr_plot( data )

        layout = go.Layout(
            title='Variability Score'
        )
        if custom_layout is not None:
            layout.update(custom_layout)
        if not np.isnan(variability_bound[0]):
            if 'horizontal' in to_plot:
                ThompsonCI_plot( data, variability_bound, 'two-sided', 'horizontal', layout, out_name=plot_out_name)
            if 'vertical' in to_plot:
                ThompsonCI_plot( data, variability_bound, 'two-sided', 'vertical', layout, out_name=plot_out_name)


    ##
    # Compute the score
    ##
    data.sort()
    if variability_bound[0] is not np.nan:
        variability_bound_values = [ data[variability_bound[k]] for k in [0,1] ]
        variability_score = data[variability_bound[1]] - data[variability_bound[0]]
    else:
        variability_score = np.nan
        variability_bound_values = [np.nan, np.nan, np.nan]

    relative_score = variability_score / ((variability_bound_values[0] + variability_bound_values[1])/2)

    return stationary, variability_bound_values[0], variability_bound_values[1], variability_score, relative_score



# ----------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------



# Below are undocumented and (possibly) non-functional TriScale functions



# ----------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------


def analysis_report(data, meta_data, output_file_name=None):
    '''
    Prepare and output the TriScale performance report based on the profided data, which may be
    - a list (of list) of file names, which contain the raw data
    - a list (of list) of values, which are the metric values for each run and series
    - a list of values, which are the KPI for each series
    '''

    todo = ''
    todo += '# ---------------------------------------------------------------- \n'
    todo += '# TODO analysis_report \n'
    todo += '# ---------------------------------------------------------------- \n'
    todo += '- finish the doctring\n'
    todo += '- check input files\n'
    todo += '# ---------------------------------------------------------------- \n'

    if verbose:
        print('%s' % todo)

    ##
    # Input checks
    ##

    # format of meta_data? probably a dictionary...
    metric = {'name': 'Throuput',
          'unit': 'MBit/s',
          'measure': 95,
          'bounds': [0,120]}
    convergence = {'expected': True,
                   'confidence': 95,  # in %
                   'tolerance': 1,    # in %
                  }
    KPI = {'percentile': 50,
           'confidence': 75,
           'class': 'one-sided',
           'side': 'lower'}
    confidence_repeatability = 75


    # for now we write the case with list of csv files name

    ##
    # Preprocessing
    ##
    metric_all = []
    for series in data:
        metric_series = []
        for run in series:
            converged, metric_run = analysis_preprocessing(run,
                                                     metric,
                                                     plot=False,
                                                     convergence=convergence,
                                                     verbose=False)
            if converged is True:
                metric_series.append(metric_run)
            else:
                metric_series.append(np.nan)

        metric_all.append(metric_series)



    # artificial data for debugging
    metric_series = np.array([10,9,10,10,8,12,65,12,10])
    metric_all = [metric_series+0.1,
                  metric_series+0.3,
                  metric_series+0.07,
                  metric_series-0.2,
                  metric_series+0.13,
                  metric_series-0.34]

#     print(metric_all)

    ##
    # Performance evaluation
    ##
    KPI_series = []
    for series in metric_all:
        stationary, KPI_bounds = analysis_kpi(series, KPI, verbose=False)
        if stationary is True:
            series.sort()
            if KPI['side'] == 'lower':
                KPI_series.append(series[KPI_bounds[1]])
            else:
                KPI_series.append(series[KPI_bounds[0]])
        else:
            KPI_series.append(np.nan)

    ##
    # Repeatability
    ##
    to_plot = None
    stationary, repeatability_mean_value, repeatability_bounds, repeatability_score = analysis_repeatability(KPI_series, confidence_repeatability, verbose=False, to_plot=to_plot)


    ##
    # Produce the performance report
    ##

    # these info should be in the meta_data
    # get inspiration from Pantheon json file
    protocol_name = 'BBR'
    network_name = 'PantheonXYZ'
    metric_label = 'Throughput'
    KPI_label = '95% CI on 85th percentile'
    metric_desc = 'description to fetch from some dictionary sdfsdfsdf  sdfsdf sdfsdfs sdfsdfsdfsdfsdf  sdfsdf sdfsdfs sdfsdfsdfsdfsdf  sdfsdf sdfsdfs sdfsdfsdfsdfsdf  sdfsdf sdfsdfs sdfsdfsdfsdfsdf  sdfsdf sdfsdfs sdfsdfsdfsdfsdf  sdfsdf sdfsdfs sdfsdfsdfsdfsdf  sdfsdf sdfsdfs sdfsdfsdfsdfsdf  sdfsdf sdfsdfs sdfsdf'

    serie_ids = range(len(data))
    serie_labels = []
    for ids in serie_ids:
        serie_labels.append('Serie '+str(ids))

    if KPI['side'] == 'lower':
        direction = 'less or equal to'
    else:
        direction = 'greater or equal to'

    analysis_output = ''
    analysis_output += '# ---------------------------------------------------------------- \n'
    analysis_output += '# TriScale Performance Report \n'
    analysis_output += '# ---------------------------------------------------------------- \n'
    analysis_output += 'Protocol \t%s\n' % (protocol_name)
    analysis_output += 'Network \t%s\n' % (network_name)
    analysis_output += 'Metric \t\t%s\n' % (metric_label)
    analysis_output += 'defined as \t%s\n' % (metric_desc)
    analysis_output += 'KPI\t\t%s\n' % (KPI_label)
    analysis_output += '# ---------------------------------------------------------------- \n'
    analysis_output += '\n'
    analysis_output += 'For the different series, with a confidence level of %g%%,\n' % KPI['confidence']
    analysis_output += 'the %g-th percentile of the %s metric \n' % (
       KPI['percentile'],
       metric_label)

    analysis_output += 'in a run of %s is %s\n' % (
       protocol_name,
       direction)
    analysis_output += '\n'

    analysis_output += '%s :\t%f\t%s\n' % (
        serie_labels[0],
        KPI_series[0],
        metric['unit'])
    for serie_cnt in range(1,len(data)):
        analysis_output += '%s :\t%f\n' % (
            serie_labels[serie_cnt],
            KPI_series[serie_cnt])

    analysis_output += '\n'

#     if repeatable:
#         flag_repeatability = ''
#     else:
#         flag_repeatability = 'NOT '

#     analysis_output += 'Given a tolerance of %g%%, these results are %s%g%%-repeatable.\n' %             (tolerance_repeatability,
#              flag_repeatability,
#              confidence_repeatability)

    analysis_output += '# ---------------------------------------------------------------- \n'
    analysis_output += '\n'

    if stationary:
        analysis_output += 'With a confidence level of %g%%, \n' % KPI['confidence']
        analysis_output += ('the evaluation of %s %s on %s results in\n'
                            % (protocol_name,
                               metric_label,
                               network_name))
        analysis_output += ('Value :\t\t    %f \t%s \n'
                            % (repeatability_mean_value, metric['unit']) )
        analysis_output += ('Rep. Score :\t+/- %f \n'
                            % (repeatability_score) )

#         analysis_output += 'the repeatability score is\n'
#         analysis_output += ('Rep. Score :\t+/- %f \t%s \n'
#                             % (repeatability_score, metric['unit']) )
#         analysis_output += ('Rep. Score :\t+/- %f \t%s \n'
#                             % (repeatability_bounds[1], metric['unit']) )
    else:
        analysis_output += 'to be handled\n'
    analysis_output += '\n'
    analysis_output += '# ----------------------------------------------------------------'

#     if print_output:
    print(analysis_output)

    return


def analysis(data,
                 percentile,
                 confidence_percentile,
                 bound_side=None,
                 confidence_repeatability=None,
                 tolerance_repeatability=None,
                 data_label=None,
                 serie_labels=None,
                 print_output=True):
    '''
    Perform the analysis of (a series of) data, as suggested by TriScale.

    The analysis comprises of multiple steps:
    - The stationarity of each data series is assessed using autocorralation.
    - A confidence interval for the specified percentile and confidence level is computed, for each data series.
    - The repeatability of the data series is tested.
    - A confidence interval for the specified percentile and confidence level is computed, for entire data set.


    Parameters
    ----------
    data : list of list, or list of 1d-np.array
    percentile: float
        Must be strictly between 0 and 100.
    bound_side: string. [Optional]
        'lower' or 'upper'
        Whether we search an upper- or lower-bound of 'percentile'.
        If None, value is picked based on 'percentile', i.e.,
         - 'lower' for percentile < 50
         - 'upper' for percentile >= 50
    confidence_percentile: float
        Confidence level for estimating the given percentile.
        Must be strictly between 0 and 100.
        -> TODO: single/double sided comment for the median?
    confidence_repeatability: float or None. [Optional]
        Confidence level for the repeatability test.
        Must be strictly between 0 and 100.
        If None, repeatability test is not performed.
    tolerance_repeatability: float or None. [Optional]
        Must be strictly between 0 and 100.
        Tolerance for the repeatability test.
        If None, repeatability test is not performed.
    data_label: string, or None. [Optional]
        Label for the analysed data.
    series_label: list of strings, or None. [Optional]
        Label for the individual data series.


    Returns
    -------

    To be added

    Notes
    -----

    To be completed.

    The implementation of `theilslopes` follows [1]_. The intercept is
    not defined in [1]_, and here it is defined as ``median(y) -
    medslope*median(x)``, which is given in [3]_. Other definitions of
    the intercept exist in the literature. A confidence interval for
    the intercept is not given as this question is not addressed in
    [1]_.

    References
    ----------
    .. [1] P.K. Sen, "Estimates of the regression coefficient based on Kendall's tau",
           J. Am. Stat. Assoc., Vol. 63, pp. 1379-1389, 1968.
    .. [2] H. Theil, "A rank-invariant method of linear and polynomial
           regression analysis I, II and III",  Nederl. Akad. Wetensch., Proc.
           53:, pp. 386-392, pp. 521-525, pp. 1397-1412, 1950.
    .. [3] W.L. Conover, "Practical nonparametric statistics", 2nd ed.,
           John Wiley and Sons, New York, pp. 493.

    Examples
    --------

    Relevant?

    >>> from scipy import stats
    >>> import matplotlib.pyplot as plt

    >>> x = np.linspace(-5, 5, num=150)
    >>> y = x + np.random.normal(size=x.size)
    >>> y[11:15] += 10  # add outliers
    >>> y[-5:] -= 7

    Compute the slope, intercept and 90% confidence interval.  For comparison,
    also compute the least-squares fit with `linregress`:

    >>> res = stats.theilslopes(y, x, 0.90)
    >>> lsq_res = stats.linregress(x, y)

    Plot the results. The Theil-Sen regression line is shown in red, with the
    dashed red lines illustrating the confidence interval of the slope (note
    that the dashed red lines are not the confidence interval of the regression
    as the confidence interval of the intercept is not included). The green
    line shows the least-squares fit for comparison.

    >>> fig = plt.figure()
    >>> ax = fig.add_subplot(111)
    >>> ax.plot(x, y, 'b.')
    >>> ax.plot(x, res[1] + res[0] * x, 'r-')
    >>> ax.plot(x, res[1] + res[2] * x, 'r--')
    >>> ax.plot(x, res[1] + res[3] * x, 'r--')
    >>> ax.plot(x, lsq_res[1] + lsq_res[0] * x, 'g-')
    >>> plt.show()
    '''


    todo = ''
    todo += '# ---------------------------------------------------------------- \n'
    todo += '# TODO \n'
    todo += '# ---------------------------------------------------------------- \n'
    todo += '- handle the intermediary outputs\n'
    todo += '- finish the doctring\n'
    todo += '- polish the plot (in particular, the subplot with all data series)\n'
    todo += '- write output to file\n'
    todo += '- iterate through the list of inputs to see if we have all we need\n'
    todo += '- include autocorellation plots? \n'
    todo += '# ---------------------------------------------------------------- \n'
    print('%s' % todo)


    ##
    # Input checks
    ##

    # For now, we assume the inputs are correct...

    serie_ids = range(len(data))
    serie_labels = []
    for ids in serie_ids:
        serie_labels.append('Serie '+str(ids))

    ##
    # Stationarity test
    ##
    serie_cnt = 0
    for series in data:

        # test
        stationary = independence_test(series)
        # plot autocorrelation
#         plot_autocorr(data)
        # output
        if stationary:
            print(('%s : Data appears i.i.d. (95%% confidence)')
                  % serie_labels[serie_cnt])
        else:
            print(('%s : Data appears NOT I.D.D. !\nAnalysis continues but results are not trustworthy...')
                  % serie_labels[serie_cnt])
        #increment
        serie_cnt += 1

    ##
    # Compute and plot the confidence interval of each series
    ##
#     CI_bounds = ci( data, percentile, confidence_percentile, plot=False, bound_side=bound_side)
#     print(CI_bounds)

    ##
    # Repeatability test
    ##

    # TODO: Correct for multiple k!

#     if confidence_repeatability and tolerance_repeatability:
    # - take the CI bounds are new data series
    # - compute the two-sided CI on the median, with the given confidence_repeatability
    # - test the width of that CI agains the tolerance_repeatability value
#         repeatable = repeatability_test( CI_bounds, confidence_repeatability, tolerance_repeatability )

    ##
    # Compute CI for the entire data set and plot
    ##
#     data_all = [item for sublist in data for item in sublist]
#     print(data_all)
#     CI_bounds_final = ci( [data_all], percentile, confidence_percentile, plot=True, bound_side=bound_side )

    ##
    # Produce the outputs
    ##
    repeatable=True
    protocol_name = 'BBR'
    network_name = 'PantheonXYZ'
    metric_label = 'Throughput'
    metric_desc = 'description to fetch from some dictionary sdfsdfsdf  sdfsdf sdfsdfs sdfsdfsdfsdfsdf  sdfsdf sdfsdfs sdfsdfsdfsdfsdf  sdfsdf sdfsdfs sdfsdfsdfsdfsdf  sdfsdf sdfsdfs sdfsdfsdfsdfsdf  sdfsdf sdfsdfs sdfsdfsdfsdfsdf  sdfsdf sdfsdfs sdfsdfsdfsdfsdf  sdfsdf sdfsdfs sdfsdfsdfsdfsdf  sdfsdf sdfsdfs sdfsdf'
    if bound_side == 'lower':
        direction = 'less or equal to'
    else:
        direction = 'greater or equal to'

    analysis_output = ''
    analysis_output += '# ---------------------------------------------------------------- \n'
    analysis_output += '# Etalon report \n'
    analysis_output += '# ---------------------------------------------------------------- \n'
    analysis_output += 'Protocol \t%s\n' % (protocol_name)
    analysis_output += 'Network \t%s\n' % (network_name)
    analysis_output += 'Metric \t\t%s\n' % (metric_label)
    analysis_output += 'defined as \t%s\n' % (metric_desc)
    analysis_output += '# ---------------------------------------------------------------- \n\n'
    analysis_output += 'For the different series, with a confidence level of %g%%,\n' % confidence_percentile
    analysis_output += 'the %g-th percentile of the %s in a run of %s is %s\n\n' % (percentile,
       metric_label,
       protocol_name,
       direction
       )
    for serie_cnt in range(len(data)):
        analysis_output += '%s :\t%f\n' % (serie_labels[serie_cnt], 0)

    if confidence_repeatability and tolerance_repeatability:
        analysis_output += '\n'
        if repeatable:
            flag_repeatability = ''
        else:
            flag_repeatability = 'NOT '

        analysis_output += 'Given a tolerance of %g%%, these results are %s%g%%-repeatable.\n' %             (tolerance_repeatability,
             flag_repeatability,
             confidence_repeatability)

    analysis_output += '# ---------------------------------------------------------------- \n\n'


    analysis_output += ('Considering all collected data, with a confidence level of %g%%,\n'
                        % confidence_percentile)
    analysis_output += ('the %g-th percentile of the %s distribution for %s on network %s is %s %f\n\n'
                        % (percentile,
                           metric_label,
                           protocol_name,
                           network_name,
                           direction,
                           0))
    analysis_output += '# ----------------------------------------------------------------'

    if print_output:
        print(analysis_output)

    return CI_bounds_final[0]
