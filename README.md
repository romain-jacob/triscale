![TriScale_logo](triscale_logo.svg)

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/romain-jacob/triscale/master) 

---
> Have you followed one of our tutorials on TriScale?  
> We would love to hear what you thought about it!  
>   
> 👇  Please fill out this short survey  🙏   
>   
> [![TriScale_survey](https://img.shields.io/badge/feedback-tutorial-brightgreen)](https://docs.google.com/forms/d/e/1FAIpQLScYvkl8D_F6RhVL9qvAoXud6BCWNHiMk00WulEN44JM0tAFhg/viewform?usp=sf_link)
---

This repository contains an implementation of _TriScale_ a framework supporting reproducible performance evaluations in networking. _TriScale_ is described in details in the following paper
> _TriScale: A Framework Supporting Replicable Performance Evaluations Networking_  
Romain Jacob, Marco Zimmerling, Carlo Alberto Boano, Laurent Vanbever, Lothar Thiele (under submission), 2021.  
[doi.org/10.5281/zenodo.3464273](https://doi.org/10.5281/zenodo.3464273)

- [Tutorial](#Tutorial)
- [Live Demo](#Live-Demo)
- [Source Code](#Source-Code)
- [Reproducing the Paper](#Reproducing-the-Paper)
  - [Case Studies](#Case-Studies)
  - [Plots](#Plots)
  - [Scalability Evaluation](#Scalability-Evaluation)

## Tutorial
You are following a tutorial on TriScale? Here is the link you are looking for 
> Click this `launch binder` button (it may take a few minutes to load)  
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/romain-jacob/triscale/master?filepath=live_exp-sizing.ipynb)  

## Live Demo
You can run a live demo of _TriScale_ directly in your web-browser  
(thanks to the amazing service provided by [MyBinder.org](https://mybinder.org/) ! )
1. Click this `launch binder` button (it may take a few minutes to load)  
 [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/romain-jacob/triscale/master?filepath=triscale_demo.ipynb)  
3. Explore the different functions, run the example code snippets, modify them, run them again...

If you are not familiar with Jupyter, you can find many online tutorials to get you started (eg [the official Jupyter tutorial](https://jupyter-notebook.readthedocs.io/en/stable/notebook.html)).

## Source Code
_TriScale_ source code is splitted in the following files
- `triscale.py`  
Implements the main functions of _TriScale_ (the public API).
- `helpers.py`  
Additional support functions for running the _TriScale_ analysis.
- `triplots.py`  
Plotting functions used in _TriScale._ All plots are created using [Plotly](https://github.com/plotly/plotly.py).

## Reproducing the Paper

This repository contains all the necessary code and information to reproduce the results analysis and plots presented in the [_TriScale_ paper](https://doi.org/10.5281/zenodo.3464273).
Jupyter notebooks are used as wrappers for everything.
You can reproduce the paper results by running the notebooks, either
- locally by cloning the repository (see `requirements.txt` for the list of dependencies)
- online using Binder (same procedure as for the [Live Demo](#Live-Demo))

Keep in mind however that the plotting and case study notebooks require to download the experiment raw data (available in a separate [Zenodo repository](https://doi.org/10.5281/zenodo.3451417)); in particular, the congestion-control data zip file is about 2.7 GB large. The required download commands are included in the respective notebooks.

Alternatively, you can simply visualize the notebooks using [nbviewer](https://nbviewer.jupyter.org/). The code cannot be run, but you can read all descriptions, comments, and outputs. This is **recommended if your internet connection is limited**.
Links for visualizing notebooks in nbviewer are provided below.

### Case Studies

The [_TriScale_ paper](https://doi.org/10.5281/zenodo.3464273) includes a set of case studies that illustrate the use and benefits of _TriScale_ for concrete networking performance evaluations.
This repository contains the notebooks that allows to reproduce the analysis of these case studies. The raw data are available in a separate [Zenodo repository](https://doi.org/10.5281/zenodo.3451417), each notebook contains the required `wget` commands.

#### `casestudy_congestion-control.ipynb`

- [![nbviewer](https://img.shields.io/badge/render-nbviewer-orange.svg) ](https://nbviewer.jupyter.org/github/romain-jacob/triscale/blob/master/casestudy_congestion-control.ipynb)
- [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/romain-jacob/triscale/master?filepath=casestudy_congestion-control.ipynb)

This case study presents a comparison between 17 congestion-control schemes. It reproduces some of the analysis performed in the [Pantheon paper](https://pantheon.stanford.edu/), illustrates its limitations, and shows how the approach in _TriScale_ helps to overcome them.

#### `casestudy_glossy.ipynb`

- [![nbviewer](https://img.shields.io/badge/render-nbviewer-orange.svg) ](https://nbviewer.jupyter.org/github/romain-jacob/triscale/blob/master/casestudy_glossy.ipynb)  
- [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/romain-jacob/triscale/master?filepath=casestudy_glossy.ipynb)

This case study compares the performance of [Glossy](https://ieeexplore.ieee.org/document/5779066), a low-power wireless communication protocol, for different parameter values, using the [FlockLab testbed](http://flocklab.ethz.ch/) as experiment environment.
In particular, this case study illustrates the importance of network profiling: this example shows how one may reach wrong conclusions (even with high confidence!) when the environmental conditions are not properly assessed.

#### `casestudy_failure-detection.ipynb`

- [![nbviewer](https://img.shields.io/badge/render-nbviewer-orange.svg) ](https://nbviewer.jupyter.org/github/romain-jacob/triscale/blob/master/casestudy_failure-detection.ipynb)  
- [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/romain-jacob/triscale/master?filepath=casestudy_failure-detection.ipynb)

This case study revisits the analysis of [Blink](https://www.usenix.org/conference/nsdi19/presentation/holterbach), an algorithm that detects failures and reroutes traffic directly in the data plane. We only perform the data analysis and show how using _TriScale_ allows to generalize the results.


#### `casestudy_video-streaming.ipynb`

- [![nbviewer](https://img.shields.io/badge/render-nbviewer-orange.svg) ](https://nbviewer.jupyter.org/github/romain-jacob/triscale/blob/master/casestudy_video-streaming.ipynb)  
- [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/romain-jacob/triscale/master?filepath=casestudy_video-streaming.ipynb)

This case study revisits the analysis of [Pensieve](https://dl.acm.org/doi/10.1145/3098822.3098843), a system that generates adaptive bitrate algorithms for video streaming using reinforcement learning.
We show how _TriScale_ can be used to provide confidence intervals not only on single KPIs, but on entire cumulative distribution functions (CDFs).

### Plots

All plots presented in the [_TriScale_ paper](https://doi.org/10.5281/zenodo.3464273) have been produced using the `triscale_plots.ipynb` notebook. This same notebook produces larger versions of these plots if you want to have a closer look.

> In order to run this notebook (either in Binder or locally), you will need to download the data from all the case studies. The required download commands are included in the notebook.

- [![nbviewer](https://img.shields.io/badge/render-nbviewer-orange.svg) ](https://nbviewer.jupyter.org/github/romain-jacob/triscale/blob/master/triscale_plots.ipynb)  
- [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/romain-jacob/triscale/master?filepath=triscale_plots.ipynb)

### Scalability Evaluation

The scalability evaluation of _TriScale_ can be reproduced by running the `triscale_scalability.ipynb` notebook.
> Keep in mind that, for this evaluation, **the results depend on the computing power and load of the machine,** therefore you may obtain results slightly different from those reported in the paper. However, the trends and orders of magnitude should remain similar.

> Running this notebook on Binder is technically possible but not recommended: it includes time measurement of rather heavy computations, which is unlikely to be meaningful (the current load of the servers hosting [MyBinder.org](https://mybinder.org/) is unknown and unpredictable.)

- [![nbviewer](https://img.shields.io/badge/render-nbviewer-orange.svg) ](https://nbviewer.jupyter.org/github/romain-jacob/triscale/blob/master/triscale_scalability.ipynb)  
- [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/romain-jacob/triscale/master?filepath=triscale_scalability.ipynb)
