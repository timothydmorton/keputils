#!/bin/bash

mkdir -p ~/.keputils

wget 'http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=cumulative&select=*' -O ~/.keputils/kois_cumulative.csv
wget 'http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=keplerstellar&select=*' -O ~/.keputils/keplerstellar.csv

