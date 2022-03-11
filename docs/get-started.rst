===========
Get started
===========

Follow the instructions below to

#.  Set up a virtual environment (e.g. conda).

#.  Install requirements via `pip` using the |IDM_s| artifactory::

        pip install -r requirements.txt --index-url=https://packages.idmod.org/api/pypi/pypi-production/simple

#.  Build the environment::

        cd EMOD-Generic/env_Debian11
        python make00_ENV_EMOD.py

#.  Build the executable::

        cd EMOD-Generic/env_Debian11
        python make00_EXE_EMOD.py

#.  Run an experiment::

        cd EMOD_Generic/workflow_covariance01/experiment_covariance01
        python make01_param_dict.py
        python make02_lauch_sims.py
        python make03_pool_brick.py

#.  Generate figures::

        cd EMOD_Generic/workflow_covariance01/figure_attackfrac01
        python make_fig_attackrate.py
