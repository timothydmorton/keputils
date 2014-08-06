keputils
=====

Basic module for interaction with KOI and *Kepler*-stellar tables.


**Installation**

::

   pip install keputils

Installing will also install ``pandas``, ``plotutils``, and ``simpledist`` modules, if not already installed.

The first time you import ``keputils.koiutils``, python will download the current cumulative
KOI table in .csv form from the `NASA Exoplanet Archive <http://exoplanetarchive.ipac.caltech.edu/>`_,
and save it to ``~/.keputils/kois_cumulative.csv``.  Also, the first time importing, it will ingest the .csv
data and re-write it to an HDF5 file, from where it will read the data in the future (faster loading).

Similarly, the first time you import ``keputils.kicutils``, python will download the *Kepler* stellar properties table,
save it to the ``~/.keputils`` directory, and put it into the HDF5 file for future fast loading.


