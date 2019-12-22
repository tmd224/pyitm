.. pyitm documentation master file, created by
   sphinx-quickstart on Fri Dec 20 16:19:43 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image:: https://travis-ci.org/tmd224/pyitm.svg?branch=master
.. image:: https://img.shields.io/badge/license-MIT-red
.. image:: https://img.shields.io/badge/Python-3.4%2B-blue
.. image:: https://coveralls.io/repos/github/tmd224/pyitm/badge.svg?branch=master
.. image:: https://badge.fury.io/py/pyitm.svg


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


**Original NTIA Disclaimer:**

*The ITM software was developed by NTIA. NTIA does not make any warranty of any kind, express, implied or
statutory, including, without limitation, the implied warranty of merchantability, fitness for a particular purpose,
non-infringement and data accuracy. NTIA does not warrant or make any representations regarding the use of the software
or the results thereof, including but not limited to the correctness, accuracy, reliability or usefulness of the
software or the results. You can use, copy, modify, and redistribute the NTIA-developed software upon your acceptance
of these terms and conditions and upon your express agreement to provide appropriate acknowledgments of NTIA's ownership
of and development of the software by keeping this exact text present in any copied or derivative works. By clicking the
links on this page to download the software, you acknowledge that you have read this disclaimer.*


.. rubric:: Sources

| `[1]` `<https://www.its.bldrdoc.gov/resources/radio-propagation-software/itm/itm.aspx>`_
| `[2]` `<https://www.ntia.doc.gov/report/1982/guide-use-its-irregular-terrain-model-area-prediction-mode>`_
