#### python
Contains user-defined python files that are consumed by EMOD server-side.
Some filenames must remain unchanged: EMOD looks for 'dtk_pre_process.py',
'dtk_in_process.py', and 'dtk_post_process.py' by name and assumes those
files contain a function called 'application'. Everything else can be
user-defined.



Server-side, each simulation runs the EMOD executable. Almost the first thing
that EMOD does is call the 'application' function in 'dtk_pre_process.py' so
start there for to trace how input files get built.