=========================
Welcome to |EMOD_Generic|
=========================

|EMOD_Generic| is a collection of Python scripts and utilities created to
streamline user interactions with the generic simtype of |EMOD_s| (current with
the Generic-Ongoing branch), |emod_api|, and |IT_s|. It is similar to |emodpy_generic|
but runs more substantial experiments on |COMPS_l|.

The workflow is a bit different from the one used in |emodpy_generic|. It
still uses |emod_api| for file creation and |IT_s| to talk to |COMPS_s|, but
the file creation is also done on |COMPS_s| (in contrast to |emodpy_generic|,
which does file creation locally and then uploads everything to |COMPS_s|).
This can be helpful if you have bandwidth issues.

Additional information about how to use |IT_s| can be found in the
:doc:`documentation <idmtools:index>`.  Additional information about |EMOD_s| generic
parameters can be found in the :doc:`parameter overview <emod-generic:parameter-overview>`.

:doc:`Click here <idmtools:index>` for a diagram showing how |IT_s| and each of the
related packages are used in an end-to-end workflow using |EMOD_s| as the
disease transmission model.

Contents
========

.. toctree::
   :maxdepth: 3
   :titlesonly:

   get-started
   workflow
   examples

