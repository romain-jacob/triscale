![TriScale_logo](assets/img/triscale_logo.svg)

## A Framework Supporting Replicable Performance Evaluations in Networking

---
<!-- [![paper](https://img.shields.io/badge/_-Paper-blue?logo=adobeacrobatreader)](https://doi.org/10.5281/zenodo.3464273)&nbsp;&nbsp; -->
[![paper](https://img.shields.io/badge/_-Paper-blue?logo=adobeacrobatreader)](https://escholarship.org/uc/item/63n4s9w2)&nbsp;&nbsp;
[![code](https://img.shields.io/badge/_-Code-blue?logo=github)](https://github.com/romain-jacob/triscale)&nbsp;&nbsp;
[![tutorial](https://img.shields.io/badge/-Tutorial-blue?logo=airplayvideo)](https://github.com/romain-jacob/triscale/blob/master/tutorial/README.md)&nbsp;&nbsp;
[![group](https://img.shields.io/badge/-Discussion-blue?logo=theconversation)](https://github.com/romain-jacob/triscale/discussions)
<!--![docs](https://img.shields.io/badge/-Documentation-orange?logo=googlesheets)-->

---

<!--
> Following a live tutorial session? Here are the links you're looking for

|Hands-on ||
|:---|:---|
|Part 1 |  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/romain-jacob/triscale/master?filepath=live_exp-sizing.ipynb)  |
|Part 2 |  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/romain-jacob/triscale/master?filepath=live_data-analysis.ipynb)  |
|Notebook Basics |  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/romain-jacob/triscale/master?filepath=tutorial_notebook-basics.ipynb)  |

> **Tell us about your experience!**  
> If you followed one of our tutorials on _TriScale_, we would love to hear what you thought about it!  
> 🙏 &nbsp;&nbsp; Please fill out this short survey (5min max)   
> 
> 👉&nbsp;&nbsp;&nbsp;&nbsp;[![TriScale_survey](https://img.shields.io/badge/feedback-tutorial-brightgreen)](https://docs.google.com/forms/d/e/1FAIpQLScYvkl8D_F6RhVL9qvAoXud6BCWNHiMk00WulEN44JM0tAFhg/viewform?usp=sf_link)

--- 
-->

When designing their performance evaluations, networking researchers often encounter questions such as:

- How long should a run be?
- How many runs to perform?
- How to account for the variability across multiple runs?
- What statistical methods should be used to analyze the data?

Despite the best intentions, researchers often answer these questions differently, thus impairing the replicability of evaluations and the confidence in the results.

Improving the standards of replicability has recently gained traction overall, as well as within the networking community. As an important piece of the puzzle, we developed a systematic methodology that streamlines the design and analysis of performance evaluations, and we have implemented this methodology into a framework called _TriScale_.

<!-- blank line -->
<!--figure class="video_container" style="margin-inline-start: 0px; margin-inline-end: 0px;">
  <iframe width="500" height="340" src="https://www.youtube.com/embed/TVCbTMk64mo" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</figure>
<!-- blank line -->

### Reproduce our study

All data, code and information required to reproduce our study are openly available [on GitHub](https://github.com/romain-jacob/triscale). 

> We use Jupyter notebooks as wrappers for all our analyses. You can reproduce the paper results by running the notebooks locally or directly in your web-browser, thanks to the amazing service provided by [MyBinder.org](https://mybinder.org/)!

See the [`README.md` file on GitHub](https://github.com/romain-jacob/triscale/blob/master/README.md) for detailed instructions.

### Presentations

For more resources, check out the _TriScale_'s [tutorial page](https://github.com/romain-jacob/triscale/blob/master/tutorial/README.md).

> [Research replicability in embedded learning](https://youtu.be/UYv_e1lt16Y)  
ESWEEK Education, Virtual (October 2021)  
[![video](https://img.shields.io/badge/-Video-blue?logo=youtube)](https://youtu.be/UYv_e1lt16Y)&nbsp;&nbsp;
[![slides](https://img.shields.io/badge/-Slides-blue?logo=airplayvideo)](https://mfr.de-1.osf.io/render?url=https://osf.io/s2amu/?direct%26mode=render%26action=download%26mode=render)


> [Tutorial: Supporting Replicable Networking Experiments with TriScale](https://youtu.be/KVA0MZszI-4)  
ACM SIGCOMM 2021, Virtual (August 2021)   
[![slides](https://img.shields.io/badge/-Slides-blue?logo=airplayvideo)](https://osf.io/9cvnd/)&nbsp;&nbsp;
[![video](https://img.shields.io/badge/-Video-blue?logo=youtube)](https://youtu.be/KVA0MZszI-4)

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

### How to cite _TriScale_

```bibtex
@proceedings{jacob2021triscale,
  title         = {Designing Replicable Networking Experiments with TriScale},
  author        = {Jacob, Romain and Zimmerling, Marco and Boano, Carlo Alberto and Vanbever, Laurent and Thiele, Lothar},
  year          = 2021,
  doi           = {10.5281/zenodo.5211642},
  year          = {2021},
  month         = nov,
  journal       = {JSys},
  volume        = {1},
  number        = {1},
  issn          = {2770-5501},
  url           = {https://escholarship.org/uc/item/63n4s9w2},
  urldate       = {2021-11-15},
  area          = {Networking},
  artifacts_url = {https://github.com/romain-jacob/triscale},
  langid        = {english},
  review_url    = {https://openreview.net/forum?id=c1LNi8CTPy6},
}
```

|People||
|---|---|
|[Romain Jacob](https://romainjacob.net)|[![orcid](https://zenodo.org/static/img/orcid.png)](https://orcid.org/0000-0002-2218-5750) &nbsp; ![lead](https://img.shields.io/badge/_-lead-blue)|
|[Marco Zimmerling](https://wwwpub.zih.tu-dresden.de/~mzimmerl/)|[![orcid](https://zenodo.org/static/img/orcid.png)](https://orcid.org/0000-0003-1450-2506)|
|[Carlo Alberto Boano](http://www.carloalbertoboano.com/)|[![orcid](https://zenodo.org/static/img/orcid.png)](https://orcid.org/0000-0001-7647-3734)|
|[Laurent Vanbever](https://vanbever.eu/)|[![orcid](https://zenodo.org/static/img/orcid.png)](https://orcid.org/0000-0003-1455-4381)|
|[Lothar Thiele](https://people.ee.ethz.ch/~thiele/)|[![orcid](https://zenodo.org/static/img/orcid.png)](https://orcid.org/0000-0001-6139-868X)|

[Contact us](https://groups.google.com/g/triscale)

