# EMOD-Generic

Uses Eradication executable from branch InstituteforDiseaseModeling/DtkTrunk/Generic-Ongoing

Contents:

  exe_GenericOngoing  - Contains the executable, schema file, and reporters
                        (if any). Including these files here is not best
                        practice (could auto-download) but having a local
                        copy eliminates some VPN issues.

  remote_covariance01 - Experiment on COMPS exercising the covariance feature.
  
  Environment notes:
    Requires idmtools[idm] and emodpy

    ********************************
    Helpful speed-up (see InstituteforDiseaseModeling/idmtools/issues/1395)

    DIRNAME\idmtools\Lib\site-packages\idmtools\entities\templated_simulation.py
      (line 184)
        + sim.task.common_assets = self.base_simulation.task.common_assets

    DIRNAME\idmtools\Lib\site-packages\idmtools\entities\itask.py
      (line 224)
        - if k not in ['_task_log']:
        + if k not in ['_task_log','common_assets']:

    ********************************
