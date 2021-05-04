Two Directories. Directory names should not change. Other client-side scripts
will assume the existance of both Assets/dtk and Assets/python.



dtk
   Contains the executable, schema file, and reporters (if any). Including
   these files here is not best practice (could auto-download from Bamboo)
   but having a local copy eliminates some VPN issues.



python
   Contains user-defined python files that are consumed by EMOD server-side.
   Some filenames must remain unchanged: EMOD looks for 'dtk_pre_process.py',
   'dtk_in_process.py', and 'dtk_post_process.py' by name and assumes those
   files contain a function called 'application'. Everything else can be 
   user-defined.

   Note that anything user-defined in this folder can be 'import' without any
   problems. Other server-side packages that don't come built-in (e.g., numpy
   or emod-api) need to ensure that the Assets/site_packages directory is on
   the import path. Good practise is to just do that everywhere just-in-case.



Server-side, each simulation runs the EMOD executable. Almost the first thing
that EMOD does is call the 'application' function in 'dtk_pre_process.py' so
start there for to trace how input files get built.