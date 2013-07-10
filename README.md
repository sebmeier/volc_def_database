volc_def_database
=================

Database of volcano deformation and 
tools to use it.

Dates
-----

Note that dates (startdate and enddate of 
events and studies) are stored as python
date objects from the datetime module.
This means that years have to be positive
and that we can only handle 'An idealized 
naive date, assuming the current Gregorian 
calendar always was, and always will be, in 
effect.' If we need BC, or approximate dates
we should look at the date module from the
datatools package (which is not installed 
by default).

