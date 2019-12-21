
User Guide
============

Interaction with the model is accomplished by invoking the ``ITMAreadBLoss()`` function with the appropriate
arguments.  Refer to the :doc:`API </api>` for a description of the arguments.

Here is a simple example:

.. code-block:: python

   from pyitm.itm import ITMAreadBLoss

   # define arguments
   EPS = 15.0
   SGM = 0.005
   EN0 = 301.0
   ModVar = 2
   deltaH = 90.0
   tht_m = 10.0
   rht_m = 1.0
   TSiteCriteria = 1
   RSiteCriteria = 0
   radio_climate = 5
   pol = 1
   pctTime = 0.7
   pctLoc = 0.5
   pctConf = 0.90
   dist_km = 10.0
   frq_mhz = 100.0


   dbloss = ITMAreadBLoss(ModVar, deltaH, tht_m, rht_m, dist_km,
                          TSiteCriteria, RSiteCriteria, EPS, SGM, EN0,
                          frq_mhz, radio_climate, pol, pctTime, pctLoc, pctConf)

   print("dbloss: {}dB".format(round(dbloss, 2)))

