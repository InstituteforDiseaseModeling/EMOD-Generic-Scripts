=======================
workflow_demographics01
=======================

This example demonstrates the implementation of vital dynamics (births, deaths,
and aging) to reproduce the population pyramid of the United Kingdom over the
period 1950 to 1980. Simulations include no infections or contagion, and have
only one node.

Sweep outcomes are replicates of four model configurations: initialization of
ages at steady-state with steady-state approximation for birth and mortality
rates, initialization of ages at steady-state with time-varying inputs for
birth rate, initialization of ages using historical data with time-varying
inputs for birth rate and steady-state approximation for mortality, and 
initialization of ages using historical data with time-varying inputs for birth
rate and mortality rates adjusted to best fit total population and age pyramid
data.

Calibration outcomes demonstrate the adjustment of three age-structured
mortality multipliers to best fit total population and age pyramid data.
