<h1>Welcome to the SHaDiE Documentation</h1>

## Introduction

`shadie` (Simulating Haploid-Diploid Evolution) is a Python API wrapper for the forward-in-time evolutionary simulation software, SLiM3. `shadie` simulates non-neutral mutations in SLiM, then uses `pyslim` to overlay neutral mutations using coalescent. 

`shadie` also provides a user-friendly Python API framework for using SLiM3. This is meant to make SLiM a little more approachable for users with prior Python knowledge, however it does not incorporate all the functionality of SLiM and it is hightly encouraged for users to familiarize themselves with the SLiMgui and the SliM Manual. 

Finally, `shadie` was first developed with the intention of modelling realistic plant lifecycles in SLiM.

## Use

`shadie` works best in [Jupyter Notebooks](https://jupyter.org/). There are plans to develop a command line tool, however `shadie` relies heavily on visualizations to aid users in designing their SLiM model and analyzing the output of their simulations. For this reason a Python API is recommended, especially for new users. 

### SLiM

[SLiM](https://messerlab.org/slim/) is powerful evolutionary simulation framework developed by the Messer Lab. They provide fanastic documentation and resources on their website. 

### pyslim

[`pyslim`](https://pyslim.readthedocs.io/en/latest/index.html) is a package that modifies `tskit` tree sequence files outpu by SLiM. `shadie` utilizes `pyslim` to overlay neutral muations with `msprime`. This method uses coalescent and is therefore *much* faster than SLiM. 

### Dependencies

**General**
* subprocess
* numpy
* pandas

**Plotting:**
* toyplot: for static plots
* altair: for interactive plots
* IPython: for displaying plots in Jupyter Notebooks