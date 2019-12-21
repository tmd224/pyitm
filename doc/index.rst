.. pyitm documentation master file, created by
   sphinx-quickstart on Fri Dec 20 16:19:43 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image:: https://travis-ci.org/tmd224/pyitm.svg?branch=master
.. image:: https://img.shields.io/badge/license-MIT-red
.. image:: https://img.shields.io/badge/Python-3.4%2B-blue
.. image:: https://coveralls.io/repos/github/tmd224/pyitm/badge.svg?branch=master


pyitm: Longley-Rice Irregular Terrain Model
====================================================

.. toctree::
   :maxdepth: 2
   :hidden:

   user-guide
   api


This is a pure python implementation of the NTIA Longley-Rice Irregular Terrain Model.  This model is a port from the
C++ *[1]* model which itself was a port from the original FORTRAN implementation.  *pyitm* only supports the
*area-prediction* mode of the original model and has been validated against the example data sets from NTIA report
82-100 *[2]*.



Installation
-------------------
*pyitm* is available on PyPI and can be installed using pip::

   pip install pyitm


.. rubric:: Sources

| `[1]` `<https://www.its.bldrdoc.gov/resources/radio-propagation-software/itm/itm.aspx>`_
| `[2]` `<https://www.ntia.doc.gov/report/1982/guide-use-its-irregular-terrain-model-area-prediction-mode>`_
