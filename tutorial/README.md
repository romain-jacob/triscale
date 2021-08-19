![TriScale_logo](../docs/assets/img/triscale_logo.svg)

# A Framework Supporting Replicable Performance Evaluations in Networking

[![paper](https://img.shields.io/badge/_-Paper-blue?logo=adobeacrobatreader)](https://doi.org/10.5281/zenodo.3464273)&nbsp;&nbsp;
[![code](https://img.shields.io/badge/_-Code-blue?logo=github)](https://github.com/romain-jacob/triscale)&nbsp;&nbsp;
[![tutorial](https://img.shields.io/badge/-Tutorial-blue?logo=airplayvideo)](tutorial.md)&nbsp;&nbsp;
[![group](https://img.shields.io/badge/-Discussion-blue?logo=theconversation)](https://groups.google.com/g/triscale)
<!--![docs](https://img.shields.io/badge/-Documentation-orange?logo=googlesheets)-->

> **Tell us about your experience!**  
> If you followed one of our tutorials on _TriScale_, we would love to hear what you thought about it!  
> 🙏 &nbsp;&nbsp; Please fill out this short survey (5min max)     
> 
> 👉&nbsp;&nbsp;&nbsp;&nbsp;[![TriScale_survey](https://img.shields.io/badge/feedback-tutorial-brightgreen)](https://docs.google.com/forms/d/e/1FAIpQLScYvkl8D_F6RhVL9qvAoXud6BCWNHiMk00WulEN44JM0tAFhg/viewform?usp=sf_link)

# Tutorial

[![CC BY 4.0][cc-by-shield]][cc-by]

This page gathers tutorial materials related to _TriScale._ You will find here:

- Slides and recordings from live tutorial sessions, which are more "lecture-style;"
- Jupyter notebooks that combine documentation with example code snippets as well as some hands-on exercises.

> If you are not familiar with Jupyter notebooks, you can get started with some basics by clicking `launch binder` button below (it may take a few minutes to load). It will take you to a live demo of Jupyter notebooks covering everything you need to know to follow the _TriScale_ tutorials.  
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/romain-jacob/triscale/master?filepath=live_exp-sizing.ipynb)  
> 
> As an alternative, you can find online many tutorials to get you started (eg [the official Jupyter tutorial](https://jupyter-notebook.readthedocs.io/en/stable/notebook.html)).


<!-- TOC -->

- [Hands-on notebooks](#hands-on-notebooks)
    - [Experiment sizing](#experiment-sizing)
    - [Data analysis](#data-analysis)
    - [Seasonal components](#seasonal-components)
- [Slides and recordings](#slides-and-recordings)
- [Reusing this material](#reusing-this-material)

<!-- /TOC -->

---

## Hands-on notebooks

There are two sets of notebooks covering tutorial materials for _TriScale_. One is intended for self-study, one for the live tutorial sessions. They cover the same content, but the second set contains less documentation and discussions (since these happen live!).

We recommend that you run the tutorial notebooks online, using [Binder](mybinder.org), by simply clicking the `launch binder` buttons listed below (it may take a few minutes to load the first time).

Alternatively, you can of course run them locally after cloning this repo and installing the corresponding dependencies (see [instructions](../triscale#running-locally)).

### Experiment sizing

This notebook presents _TriScale_'s experiment_sizing function, which implement a methodology to define the minimal number of runs required to estimate a certain performance objective with a given level of confidence.

|Version||
|:---|:---|
|Live session|  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/romain-jacob/triscale/master?filepath=live_exp-sizing.ipynb)  |
|Self-study|    [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/romain-jacob/triscale/master?filepath=tutorial_exp-sizing.ipynb)  |

### Data analysis

This notebook presents _TriScale_'s data analysis functions, leading to the computation of variability scores, which serve to quantify replicability.

|Version||
|:---|:---|
|Live session|  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/romain-jacob/triscale/master?filepath=live_data-analysis.ipynb)  |
|Self-study|    [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/romain-jacob/triscale/master?filepath=tutorial_data-analysis.ipynb)  |

### Seasonal components

This notebook presents the importance of accounting for seasonal components in the data analysis.

|Version||
|:---|:---|
|Live session|  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/romain-jacob/triscale/master?filepath=live_seasonal-comp)  |
|Self-study|    [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/romain-jacob/triscale/master?filepath=tutorial_seasonal-comp)  |


## Slides and recordings

> [Tutorial: Supporting Replicable Networking Experiments with TriScale](https://youtu.be/f9k7gS-QpWI)  
4th CPS-IoTBench Workshop, Virtual (May 2021)  
[![video](https://img.shields.io/badge/-Video-blue?logo=youtube)](https://youtu.be/f9k7gS-QpWI)

> [IoTBench: Reproducibility challenge in wireless networking research](https://osf.io/m7a6w/)  
5th CROSS Symposium, Virtual (October 2020)  
[![slides](https://img.shields.io/badge/-Slides-blue?logo=airplayvideo)](https://osf.io/m7a6w/)

> [Confidence in experimental evaluations:  
Time to do better than "Believe me, it’s true!"](https://osf.io/aktn7/)  
EWSN Conference, Lyon, France (February 2020)  
[![slides](https://img.shields.io/badge/-Slides-blue?logo=airplayvideo)](https://osf.io/aktn7/)


## Reusing this material

All the tutorial material listed on this page is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by]. You are more than welcome to adapt and/or reuse any of it. If you do so,

- Please give appropriate credit by indicated the source (this repository);
- Please [drop me a line](mailto:jacobr@ethz.ch) about it, I would love to here in which context this was useful for you. 🙂

<!-- [![CC BY 4.0][cc-by-image]][cc-by] -->

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg