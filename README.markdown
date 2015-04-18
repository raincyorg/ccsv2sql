# ccsv2sql
[![Build Status](https://travis-ci.org/stpettersens/ccsv2sql.svg?branch=master)](https://travis-ci.org/stpettersens/ccsv2sql) 
[![Build status](https://ci.appveyor.com/api/projects/status/github/stpettersens/ccsv2sql?branch=master&svg=true)](https://ci.appveyor.com/project/stpettersens/ccsv2sql)

Utility to convert a CSV file to a SQL dump.

Usage: `ccsv2sql-f data.csv -o data.sql`

Tested with:
* Python 2.7.9, PyPy 2.5.1 and IronPython 2.7.5 (works).
* Jython 2.5.3 (use Jython tweaked version): 
* `jython ccsv2sql.jy.py -f data.csv -o data.sql`
