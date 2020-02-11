![TriScale_logo](triscale_logo.svg)

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/TriScale-Anon/triscale/master)

This repository contains an implementation of _TriScale_ a framework supporting reproducible performance evaluations in networking. _TriScale_ is described in details in the following paper
> _TriScale: A Framework Supporting Reproducible Performance Evaluations Networking_  
Anonymous (under submission), 2020.  
[doi.org/10.5281/zenodo.3464273](https://doi.org/10.5281/zenodo.3464273)

## Live Demo
You can run a live demo of _TriScale_ directly in your web-browser  
(thanks to the amazing service provided by [MyBinder.org](https://mybinder.org/) ! )
1. Click the `launch binder` button (it may take a few minutes to load)
2. Open the `triscale_demo.ipynb` Jupyter notebook
3. Explore the different functions, run the example code snippets, modify them, run them again...

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/TriScale-Anon/triscale/master)

If you are not familiar with Jupyter, you can find many online tutorials to get you started (eg [the official Jupyter tutorial](https://jupyter-notebook.readthedocs.io/en/stable/notebook.html)).

## Source Code
_TriScale_ source code is splitted in the following files
- `triscale.py`  
Implements the main functions of _TriScale_ (the public API).
- `helpers.py`  
Additional support functions for running the _TriScale_ analysis.
- `triplots.py`  
Plotting functions used in _TriScale._ All plots are created using [Plotly](https://github.com/plotly/plotly.py).
