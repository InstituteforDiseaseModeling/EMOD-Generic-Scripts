================
workflow_covid01
================

Demonstration simulations for SARS-CoV-2 transmission. The model strcuture was
used to examine the impact of Supplementary Immunization Activities (SIA)s for
non Covid-19 diseases on SARS-CoV-2 tranmsssion.

Important features include:

- Multi-node network used to represent an urban center with peri-urban and
  rural locations.
- Population migration between the nodes.
- Health care workers (HCW) and non-HWC moving between locations.
- Personal protective equipment (PPE) for HWC.
- Age-dependent susceptibility.
- Self-quarantine behavior.
- Age-structured contact matricies.
- Overdispersion of the infection rate.

This model does not inlclude:

- SARS-CoV-2 variants of concern.
- Waning immunity, re-infection, or secondary vaccine failure.
- Vital dynamics (births, deaths, or aging).