===================
model_rubella_cod02
===================

Extension of model_rubella_cod01 to examine the impact of non-steady-state
demographics; vital dynamics from WPP data as in model_demographics02 for
median estimates.

Adjusts fertility assumptions from model_rubella_cod01 where post-process
birthrates were not necessarily consistent with simulated birthrates. Corrects
error in model_rubella_cod01 where DHS fertility rates were incorrectly
interpreted as per-3-years instead of per-year (3 year average). Outcomes are
equivalent to previous results multiplied by a scale factor.

Applies agent weights during simulation so that outputs are corectly scaled to
total population (contrast model_rubella_cod01 where required required based
on the number of agents used during the simulation).

Implements additional features:
- Adjustable importation rates.
- Time varying routine immunization rates.
