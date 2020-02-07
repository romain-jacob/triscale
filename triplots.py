"""
Plotting functions used by the TriScale module
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
pio.templates.default = "none"

from helpers import acorr
import colors

def autocorr_plot(  x,
                    layout=None,
                    out_name=None,
                    show=True,
                    verbose=False):
    """
    Plot the autocorellation function of x.
    If x is a time series, the function assumes that the series is equally
    spaced (as required for simple autocorellation).

    The plot also displays the 95% confidence interval for the sample
    autocorellation coefficient values, that is:
        +/- 1.96*sqrt( len(x) )
    If the sample autocorellation coefficients are within these bounds,
    the series is i.i.d. with 95% probability.
    """

    todo = ''
    todo += '# ---------------------------------------------------------------- \n'
    todo += '# TODO autocorr_plot\n'
    todo += '# ---------------------------------------------------------------- \n'
    todo += '- check the custom layout input\n'
    todo += '- finish the docstring (input/output, support to save the plot)\n'
    todo += '- uniformize the plot colors (use the same as TriScale logo)\n'
    todo += '# ---------------------------------------------------------------- \n'
    if verbose:
        print('%s' % todo)

    ## Initialize the figure
    figure = go.Figure()

    # IID bounds
    bounds = go.Scatter(
        x=[0,len(x),len(x),0],
        y= np.array([1,1,-1,-1])*(1.96)/np.sqrt(len(x)),
        hoverinfo='skip',
        mode='lines',
        fill='toself',
        fillcolor=colors.light_orange,
        line=dict(color=colors.light_orange, width=0),
        showlegend=True,
        name='95% CI on i.i.d. test')
    figure.add_trace(bounds)

    # Autocorellation coefficients
    trace = go.Scatter(
        x=list(range(0,len(x))),
        y=acorr(x),
        mode='markers, lines',
        line={'color':colors.orange},
        marker={'color':colors.orange},
        showlegend=True,
        name='Sample Autocor. Coefficients')
    figure.add_trace(trace)


    # Default Layout
    default_layout = go.Layout(
        title='Autocorrelation',
        xaxis={'title':'Lag'})
    # Custom Layout
    if layout is not None:
        default_layout.update(layout)
    figure.update_layout(default_layout)


    # Output
    if out_name is not None:
        figure.write_image(out_name)

    if show:
        figure.show()
    return figure


def theil_plot(  y,
                 x=None,
                 metric_data=None,
                 convergence_data=None,
                 layout=None,
                 out_name=None,
                 verbose=False):

    todo = ''
    todo += '# ---------------------------------------------------------------- \n'
    todo += '# TODO theil_plot\n'
    todo += '# ---------------------------------------------------------------- \n'
    todo += '- check the custom layout input\n'
    todo += '- write the docstring (input/output, support to save the plot)\n'
    todo += '- uniformize the plot colors (use the same as TriScale logo)\n'
    todo += '- Add the computed metric value (somehow...)\n'
    todo += '# ---------------------------------------------------------------- \n'
    if verbose:
        print('%s' % todo)

    ## Parse the inputs
    if type(y) != np.ndarray:
        y = np.array(y)
    if x is not None and x.size != 0:
        if x.shape[0] != y.shape[0]:
            raise ValueError('x and y must be the same shape.')
    else:
        x = np.arange(y.size)

    if metric_data is None:
        convergence_data_x = np.array(x)
        convergence_data_y = np.array(y)
    else:
        convergence_data_x = np.array(metric_data[0])
        convergence_data_y = np.array(metric_data[1])

    ## Initialize the figure
    figure = go.Figure()

    ## Create the traces to plot
    if len(x) > 1000:
        step = int(len(x)/1000)
        x_subsampled = x[::step]
        y_subsampled = y[::step]
    else:
        x_subsampled = x
        y_subsampled = y

    trace = go.Scatter(
        name='Data',
        x=x_subsampled,
        y=y_subsampled,
        mode='markers',
        marker={'color':colors.blue}
    )
    figure.add_trace(trace)

    if metric_data is not None:
        metric_x = np.array(metric_data[0])
        metric_y = np.array(metric_data[1])
        metric = go.Scatter(
            name='Metric',
            x=metric_x,
            y=metric_y,
            marker={
            'symbol':'circle-open',
            'color':colors.orange},
            mode='markers+lines'
        )
        figure.add_trace(metric)

    if convergence_data is not None:

        # Plot the Theil slope and its bounds
        trend_data = convergence_data[1]

        bounds_slope = go.Scatter(
            name='CI ( Slope )',
            x=[ convergence_data_x.min(), convergence_data_x.max(),
                convergence_data_x.max(), convergence_data_x.min()],
            y=[
                trend_data[2],
                trend_data[3],
                trend_data[5],
                trend_data[4]
            ],
            hoverinfo='skip',
            fill='toself',
            fillcolor=colors.light_orange,
            line=dict(color='rgba(0,0,0,0)')
        )
        figure.add_trace(bounds_slope)

        med_slope = go.Scatter(
            name='Slope',
            x=[convergence_data_x.min(), convergence_data_x.max()],
            y=[trend_data[0],trend_data[1]],
            hoverinfo='skip',
            mode='lines',
            line={'color':colors.darker_orange}
        )
        figure.add_trace(med_slope)

        # Plot tolerance bounds
        tolerance_data = convergence_data[2]
        tol_slope_up = go.Scatter(
            name='Tolerance',
            x=[convergence_data_x.min(), convergence_data_x.max()],
            y=[
                tolerance_data[0],
                tolerance_data[1],
            ],
            hoverinfo='skip',
            line=dict(color='rgba(20,20,20,100)', dash='dash'),
            mode='lines',
            showlegend=False
        )
        figure.add_trace(tol_slope_up)
        tol_slope_lo = go.Scatter(
            name='Tolerance',
            x=[convergence_data_x.min(), convergence_data_x.max()],
            y=[
                tolerance_data[2],
                tolerance_data[3],
            ],
            hoverinfo='skip',
            line=dict(color='rgba(20,20,20,100)', dash='dash'),
            mode='lines',
            showlegend=True
        )
        figure.add_trace(tol_slope_lo)

    ## Layout
    if layout is not None:
        figure.update_layout(go.Layout(layout))

    ## Output
    if out_name is not None:
        figure.write_image(out_name)

    return figure

def ThompsonCI_plot(    data,
                        CI,
                        CI_bound,
                        to_plot,
                        layout=None,
                        out_name=None,
                        verbose=False ):

    todo = ''
    todo += '# ---------------------------------------------------------------- \n'
    todo += '# TODO ThompsonCI_plot \n'
    todo += '# ---------------------------------------------------------------- \n'
    todo += '- write the doctring\n'
    todo += '- check input types\n'
    todo += '- add cumulative mass function\n'
    todo += '- add a text note on the bounds\n'
    todo += '- uniformize the plot colors (use the same as TriScale logo)\n'
    todo += '# ---------------------------------------------------------------- \n'

    if verbose:
        print('%s' % todo)

    # Check inputs
    valid_plots = ['vertical', 'horizontal']
    if to_plot is None:
        return
    if to_plot not in valid_plots:
        raise ValueError("Wrong plot type. Valid types: 'vertical', 'horizontal'")

    # Make sure data is sorted
    sorted_data = np.sort(data)

    # Initialize the CI shape
    interval_shape = {
        'type': 'rect',
        'layer': 'above',
        'xref': 'x',
        'yref': 'paper',
        'x0': 0,
        'y0': 0,
        'x1': 1,
        'y1': 1,
        'fillcolor': colors.light_orange,
        'line': {'width': 0,},
        'layer':'below'
    }


    ## Initialize the figure
    figure = go.Figure()

    ##
    # Horizontal CI plot
    ##
    if to_plot == 'horizontal':

        # Default layout
        default_layout = go.Layout(
            yaxis={'visible':False, 'range':[-1,2]},
            height=250)
        figure.update_layout(default_layout)

        # Serie data
        samples = go.Scatter(
            x=data,
            y=np.ones((len(data),), dtype=int),
            mode='markers',
            marker={'symbol':'circle-open', 'size':8},
            line={'color':'black'},
            name='Data',
                          )
        # CI bounds
        up_bound = go.Scatter(
            x=[sorted_data[CI[1]], sorted_data[CI[1]]],
            y=[-1, 2],
            mode='lines+text',
            # text=sorted_data[CI[1]],
            line={'color':colors.orange, 'width':4},
            hoverinfo='skip',
            name='CI',
            # textposition="top center",
            # textfont={'size':18 },
        )
        lo_bound = go.Scatter(
            x=[sorted_data[CI[0]], sorted_data[CI[0]]],
            y=[-1,2],
            mode='lines+text',
            line={'color':colors.orange, 'width':4},
            hoverinfo='skip',
            name='CI',
        )

        if CI_bound == 'two-sided':
            up_bound.showlegend = False
            figure.add_trace(up_bound)
            figure.add_trace(lo_bound)
            interval_shape['x0'] = sorted_data[CI[0]]
            interval_shape['x1'] = sorted_data[CI[1]]
        if CI_bound == 'lower':
            figure.add_trace(lo_bound)
            interval_shape['x0'] = sorted_data[CI[0]]
            interval_shape['x1'] = max(data)
        if CI_bound == 'upper':
            figure.add_trace(up_bound)
            interval_shape['x0'] = min(data)
            interval_shape['x1'] = sorted_data[CI[1]]

    ##
    # Vertical CI plot
    ##

    if to_plot == 'vertical':

        # Default layout
        default_layout = go.Layout(
            xaxis={'visible':False},
            # height=250
            )
        figure.update_layout(default_layout)

        # Serie data
        samples = go.Scatter(
            x=np.arange(len(data))+1,
            y=data,
            mode='markers',
            marker={'symbol':'circle-open', 'size':8},
            line={'color':'black'},
            name='Data',
                          )
        # CI bounds
        up_bound = go.Scatter(
            x=[0, len(data)+1],
            y=[sorted_data[CI[1]], sorted_data[CI[1]]],
            mode='lines',
            line={'color':colors.orange, 'width':4},
            hoverinfo='skip',
            name='CI',
        )
        lo_bound = go.Scatter(
            x=[0, len(data)+1],
            y=[sorted_data[CI[0]], sorted_data[CI[0]]],
            mode='lines',
            line={'color':colors.orange, 'width':4},
            hoverinfo='skip',
            name='CI',
        )

        interval_shape['xref'] = 'paper'
        interval_shape['yref'] = 'y'
        if CI_bound == 'two-sided':
            up_bound.showlegend = False
            figure.add_trace(up_bound)
            figure.add_trace(lo_bound)
            interval_shape['y0'] = sorted_data[CI[0]]
            interval_shape['y1'] = sorted_data[CI[1]]
        if CI_bound == 'lower':
            figure.add_trace(lo_bound)
            interval_shape['y0'] = sorted_data[CI[0]]
            interval_shape['y1'] = max(data)
        if CI_bound == 'upper':
            figure.add_trace(up_bound)
            interval_shape['y0'] = min(data)
            interval_shape['y1'] = sorted_data[CI[1]]

    ##
    # Customization and output
    ##

    # Custom layout
    if layout is not None:
        figure.update_layout(layout)

    # Output
    figure.add_trace(samples)
    figure.update_layout(shapes=[interval_shape])
    figure.show()
    if out_name is not None:
        figure.write_image(out_name)

    return figure
