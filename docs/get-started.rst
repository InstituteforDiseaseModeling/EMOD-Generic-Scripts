===========
Get started
===========

Follow the instructions below to

#.  Set up a virtual python environment (e.g. conda).

#.  Install requirements via `pip` using the |IDM_s| artifactory::

        pip install -r requirements.txt --index-url=https://packages.idmod.org/api/pypi/pypi-production/simple

#.  Run an experiment::

        cd EMOD-Generic-Scripts/model_covariance01/experiment_covariance01
        python make01_param_dict.py
        python make02_lauch_sims.py
        python make03_pool_brick.py

#.  Generate figures::

        cd EMOD-Generic-Scripts/model_covariance01/figure_attackfrac01
        python make_fig_attackrate.py
