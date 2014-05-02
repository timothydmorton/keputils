#!/bin/bash

wget 'http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=cumulative&select=*' -O kois_cumulative.csv
wget 'http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=keplerstellar&select=*' -O keplerstellar.csv

