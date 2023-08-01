===============
model_rubella01
===============

Simulations that produce Figure 5 in the manuscript "Examination of scenarios
introducing rubella vaccine in the Democratic Republic of the Congo." These
simulations are used to demonstrate the potential for increased congenital
rubella syndrome (CRS) after vaccine introduction.

See https://doi.org/10.1016/j.jvacx.2021.100127

Extensions the cited work to examine the impact of non-steady-state
demographics; vital dynamics and fertility from WPP data. Applies agent weights
during simulation so that outputs are corectly scaled to total population.

Important features include:
- Maternally derived immunity.
- Optional steady-state population pyramid.
- Very low rates of exogeneous importation.
- Posterior distribution of R0 values used as input.
