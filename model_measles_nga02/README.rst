===================
model_measles_nga02
===================

Simulations of measles transmission in Nigeria. The model is structured so that
each state is implemented separately. Age-structured mortality from UN WPP
reports for national estimates have been used for all states; crude birth rates
are initialized using values from the 2013 Nigeria DHS and scaled in time using
relative trends from the UN WPP.

Important features include:

- Multi-node network used to represent regions of Nigeria at the adm02 scale.
- Network infectivity contagion transfer between nodes.
- Annual seasonality in measles infectivity.
- Spatially varying rates of routine immunization.
- Pre-specified calendar of supplemental immunization activities (SIAs).
- Maternally derived immunity.
- Maximum simulation duration based on elapsed time.
- Weighted agents to represent multiple individuals per agent.
- Age-based immunity initialization to approximate endemic transmission.
- Infectivity reservoir to represent persistent exogeneous importation.
- Event based notification of vaccine doses delivered by routine immunization.
- Future SIA vaccines as non-contagious infections for labeling and tracking.
