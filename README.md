![TriScale_logo](triscale_logo.svg)

# A Framework Supporting Replicable Performance Evaluations in Networking

This repository contains an implementation of _TriScale_, a framework supporting reproducible performance evaluations in networking. 

_TriScale_ is described in details in the following paper

> _Designing Replicable Networking Experiments with TriScale_  
Romain Jacob, Marco Zimmerling, Carlo Alberto Boano, Laurent Vanbever, Lothar Thiele   
(under submission), 2021.  
[doi.org/10.5281/zenodo.3464273](https://doi.org/10.5281/zenodo.3464273)

Check out the project webpage for more info:  
http://triscale.ethz.ch/

---

[![paper](https://img.shields.io/badge/_-Paper-blue?logo=adobeacrobatreader)](https://doi.org/10.5281/zenodo.3464273)&nbsp;&nbsp;
[![code](https://img.shields.io/badge/_-Code-blue?logo=github)](https://github.com/romain-jacob/triscale)&nbsp;&nbsp;
[![tutorial](https://img.shields.io/badge/-Tutorial-blue?logo=airplayvideo)](https://github.com/romain-jacob/triscale/blob/master/tutorial/README.md)&nbsp;&nbsp;
[![group](https://img.shields.io/badge/-Discussion-blue?logo=theconversation)](https://github.com/romain-jacob/triscale/discussions)
<!-- [![group](https://img.shields.io/badge/-Discussion-blue?logo=theconversation)](https://groups.google.com/g/triscale) -->
<!--![docs](https://img.shields.io/badge/-Documentation-orange?logo=googlesheets)-->

---

<!-- TOC depthFrom:2 depthTo:3 -->

- [Source code](#source-code)
- [Reproducing the paper](#reproducing-the-paper)
    - [Reproduction alternatives](#reproduction-alternatives)
    - [Case studies](#case-studies)
    - [Scalability Evaluation](#scalability-evaluation)
    - [Plots](#plots)

<!-- /TOC -->

---

## Source code

_TriScale_ source code is split in the following files

- `triscale.py`  
Implements the main functions of _TriScale_ (the public API).
- `helpers.py`  
Additional support functions for running the _TriScale_ analysis.
- `triplots.py`  
Plotting functions used in _TriScale._ All plots are created using [Plotly](https://github.com/plotly/plotly.py).

## Reproducing the paper

This repository contains all the necessary code and information to reproduce the results analysis and plots presented in the [_TriScale_ paper](https://doi.org/10.5281/zenodo.3464273). Jupyter notebooks are used as wrappers for all our data analysis.

> **Note.** If you are not familiar with Jupyter notebooks, you can find some basic information on [_TriScale_'s tutorial page](tutorial/README.md).

### Reproduction alternatives

We provide three options to reproduce the paper results:

1. [Online, using Binder;](#using-mybinderorg)
1. [Online, using `nbviewer`;](#using-nbviewer)
1. [Locally.](#running-locally)

Keep in mind that running the plotting and case study notebooks require to download the experiment raw data (available in a separate [Zenodo repository](https://doi.org/10.5281/zenodo.3451417)); in particular, the congestion-control data zip file is about 2.7 GB large. The required download commands are included in the respective notebooks.

| Recommended alternative||
|:---|:---|
| To quickly try out the API | Binder |
| If not familiar with Python environments | Binder or nbviewer |
| For a quick look | nbviewer |
| With limited Internet connection | nbviewer |
| For a more in-depth trial | locally |

#### Using MyBinder.org

You can run the _TriScale_'s notebooks directly in your web-browser, thanks to the amazing service provided by [MyBinder.org](https://mybinder.org/)!

1. Click this `launch binder` button (it may take a few minutes to load);  
 [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/romain-jacob/triscale/master?filepath=triscale_demo.ipynb)  
2. Open any notebook in the repository (see the notebooks' description below);
2. Explore the different functions, run the example code snippets, modify them, run them again...

> **Note.** You cannot save the state of the notebooks open using Binder; once your session expires, you will not be able to retrieve changes you made, or outputs you computed.  
If you want to do that, you should [run the notebooks locally]().

<details>
<summary> MyBinder.org in a nutshell
</summary>
  <br />
  <p>
    MyBinder.org is a service that fetches a public repository, builds a Docker image with all required dependencies, then runs and serves an image in a cloud platform, making it accessible to anyone with on the web, without requiring any install!
  </p>
  <p>
    Best of all, MyBinder.org is a free and open-source service, managed for scientists by scientists. Check it out, it's really cool!
    <br />
  </p>
</details>

#### Using `nbviewer`

You can simply _visualize_ the notebooks [using `nbviewer`](https://nbviewer.jupyter.org/). 

> **Note.** The code cannot be run, but you can read all descriptions, comments, and see the outputs. Links for visualizing notebooks in `nbviewer`are provided in the descriptions below.

#### Running locally

You can run the notebooks locally by cloning this repository. The list of dependencies is included in the `environment.yml` file. 

If you are using `conda`, simply execute the following commands to get started:

```bash
git clone git@github.com:romain-jacob/triscale.git
cd triscale
conda env create -f environment.yml
conda activate myenv
jupyter notebooks
```

> If you prefer `pip` over `conda`, you will also find a `requirements.txt` file, but this one is not guaranteed to be complete.

### Case studies

The [_TriScale_ paper](https://doi.org/10.5281/zenodo.3464273) includes a set of case studies that illustrate the use and benefits of _TriScale_ for concrete networking performance evaluations.
This repository contains the notebooks that allows to reproduce the analysis of these case studies. The raw data are available in a separate [Zenodo repository](https://doi.org/10.5281/zenodo.3451417), each notebook contains the required `wget` commands.

#### `casestudy_congestion-control.ipynb`

[![nbviewer](https://img.shields.io/badge/render-nbviewer-orange.svg?logo=jupyter) ](https://nbviewer.jupyter.org/github/romain-jacob/triscale/blob/master/casestudy_congestion-control.ipynb)
&nbsp;
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/romain-jacob/triscale/master?filepath=casestudy_congestion-control.ipynb)

This case study presents a comparison between 17 congestion-control schemes. It reproduces some of the analysis performed in the [Pantheon paper](https://pantheon.stanford.edu/), illustrates its limitations, and shows how the approach in _TriScale_ helps to overcome them.

#### `casestudy_glossy.ipynb`

[![nbviewer](https://img.shields.io/badge/render-nbviewer-orange.svg?logo=jupyter) ](https://nbviewer.jupyter.org/github/romain-jacob/triscale/blob/master/casestudy_glossy.ipynb)
&nbsp;
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/romain-jacob/triscale/master?filepath=casestudy_glossy.ipynb)

This case study compares the performance of [Glossy](https://ieeexplore.ieee.org/document/5779066), a low-power wireless communication protocol, for different parameter values, using the [FlockLab testbed](http://flocklab.ethz.ch/) as experiment environment.
In particular, this case study illustrates the importance of network profiling: this example shows how one may reach wrong conclusions (even with high confidence!) when the environmental conditions are not properly assessed.

#### `casestudy_failure-detection.ipynb`

[![nbviewer](https://img.shields.io/badge/render-nbviewer-orange.svg?logo=jupyter) ](https://nbviewer.jupyter.org/github/romain-jacob/triscale/blob/master/casestudy_failure-detection.ipynb)
&nbsp;
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/romain-jacob/triscale/master?filepath=casestudy_failure-detection.ipynb)

This case study revisits the analysis of [Blink](https://www.usenix.org/conference/nsdi19/presentation/holterbach), an algorithm that detects failures and reroutes traffic directly in the data plane. We only perform the data analysis and show how using _TriScale_ allows to generalize the results.


#### `casestudy_video-streaming.ipynb`

[![nbviewer](https://img.shields.io/badge/render-nbviewer-orange.svg?logo=jupyter) ](https://nbviewer.jupyter.org/github/romain-jacob/triscale/blob/master/casestudy_video-streaming.ipynb)
&nbsp;
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/romain-jacob/triscale/master?filepath=casestudy_video-streaming.ipynb)

This case study revisits the analysis of [Pensieve](https://dl.acm.org/doi/10.1145/3098822.3098843), a system that generates adaptive bitrate algorithms for video streaming using reinforcement learning.
We show how _TriScale_ can be used to provide confidence intervals not only on single KPIs, but on entire cumulative distribution functions (CDFs).

### Scalability Evaluation

The scalability evaluation of _TriScale_ can be reproduced by running the `triscale_scalability.ipynb` notebook.

[![nbviewer](https://img.shields.io/badge/render-nbviewer-orange.svg?logo=jupyter) ](https://nbviewer.jupyter.org/github/romain-jacob/triscale/blob/master/triscale_scalability.ipynb)
&nbsp;
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/romain-jacob/triscale/master?filepath=triscale_scalability.ipynb)


> Keep in mind that, for this evaluation, **the results depend on the computing power and load of the machine,** therefore you may obtain results slightly different from those reported in the paper. However, the trends and orders of magnitude should remain similar.

> Running this notebook on Binder is technically possible but not recommended: it includes time measurement of rather heavy computations, which is unlikely to be meaningful (the current load of the servers hosting [MyBinder.org](https://mybinder.org/) is unknown and unpredictable.)

### Plots

All plots presented in the [_TriScale_ paper](https://doi.org/10.5281/zenodo.3464273) have been produced using the `triscale_plots.ipynb` notebook. This same notebook produces larger versions of these plots if you want to have a closer look.

[![nbviewer](https://img.shields.io/badge/render-nbviewer-orange.svg?logo=jupyter) ](https://nbviewer.jupyter.org/github/romain-jacob/triscale/blob/master/triscale_plots.ipynb)
&nbsp;
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/romain-jacob/triscale/master?filepath=triscale_plots.ipynb)

> In order to run this notebook (either in Binder or locally), you will need to download the data from all the case studies. The required download commands are included in the notebook.
