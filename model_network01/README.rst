===============
model_network01
===============

This example demonstrates the implementation of the spread of infectivity on a
network. Each simulation has a default network of 625 nodes (25-by-25 grid)
that has 1 of 4 preset levels of network infectivity. Simulations are
implemented as multi-core (four cores per simulation) to demonstrate logging
and transmisssion between nodes hosted on different cores (note that cores may
or may not be co-located on a common machine.)

An outbreak is initialized by a constant importation pressure of infected
individuals. There is no age structure, vital dynamics, or waning. All
simulations run for 1000 time steps of until total infectivity falls to zero.

Infected individuals are introduced in one node only (lower-left on the grid).
Inter-node populations are not well mixed; the network infectivity feature
implements a gravity-type expression for contagion transmission. All nodes have
equal populations and the coefficient on the distance exponent in the gravity
expression is fixed. Each simulation is assigned 1 of 4 coefficients in the
gravity expression.
