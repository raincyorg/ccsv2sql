# ccsv2sql
<!--[![Build Status](https://travis-ci.org/stpettersens/csql2mongo.svg?branch=master)](https://travis-ci.org/stpettersens/csql2mongo) 
[![Build status](https://ci.appveyor.com/api/projects/status/github/stpettersens/csql2mongo?branch=master&svg=true)](https://ci.appveyor.com/project/stpettersens/csql2mongo)-->

Utility to convert a CSV file to a SQL dump.

Usage: `ccsv2sql-f data.csv -o data.sql`

Tested with:
* Python 2.7.9, PyPy 2.5.1 and IronPython 2.7.5 (works).
* Jython 2.5.3 (use Jython tweaked version): 
* `jython ccsv2sql.jy.py -f data.csv -o data.sql`
