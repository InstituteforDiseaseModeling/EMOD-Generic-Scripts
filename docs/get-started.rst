===========
Get started
===========

Follow the instructions below to

#.  Set up a virtual environment (e.g. conda).

#.  Install requirements via `pip` using the |IDM_s| artifactory::

        pip install -r requirements.txt --index-url=https://packages.idmod.org/api/pypi/pypi-production/simple

#.  Build the environment::

        cd EMOD-Generic/env_CentOS8
        python make00_container.py

#.  Build the executable::

        cd EMOD-Generic/env_BuildEMOD
        python make00_executable.py

#.  Run an experiment::

        cd EMOD_Generic/workflow_covariance01/experiment_covariance01
        python make01_param_dict.py
        python make02_lauch_sims.py
        python make03_pool_brick.py

#.  Generate figures::

        cd EMOD_Generic/workflow_covariance01/figure_attackfrac01
        make_fig_attackrate01.py
