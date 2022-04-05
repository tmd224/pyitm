
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

System Parameters
-----------------------
Frequency
^^^^^^^^^^^
The model is valid for frequencies between 20MHz and 20GHz.  Frequency parameter is expressed in units of MHz.

Distance
^^^^^^^^^^^
The model is valid for distances between 1km and 2000km.  The distance parameter is expressed in km and represents 
the `great circle distance <https://en.wikipedia.org/wiki/Great-circle_distance>`_ between the transmit and received antenna.

Antenna Heights (rht_m, tht_m)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The antenna heigh parameters are expressed in m and represent the center of the radiation above the ground.
The model is valid for antenna heights in the range 0.5-3000m.

Polarization
^^^^^^^^^^^^^^^
The model assumes the antenna polarization is the same for both of the receive and transmit antennas.
The polarization argument must be one of the following values:

====================== ==============
**Polarization**         **Value**  
---------------------- --------------
Horizontal              0
Vertical                1
====================== ==============

Environmental Parameters
----------------------------
Terrain Irregularity Parameter (deltaH)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This parameter is used to characterize the random irregularities in the height of the terrain between the transmit and receive antenna 
should represent the interdecile range of the terrain elevations (top and bottom 10% of values removed).  Suggested values for classes of terrain topography are listed below.

====================== ==============
**Terrain**              **deltaH**  
---------------------- --------------
Flat (or smooth water)  0
Plains                  30
Hills                   90
Mountains               200
Rugged mountains        500
====================== ==============

Average terrain should use a value of 90.

Electrical Ground Constants (EPS, SGM)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Suggested values for the relative permittivity and conductivity of earth are presribed below.

================= ========================= ===================
**Condition**     **Relative Permittivity**  **Conductivity**
----------------- ------------------------- -------------------
Average ground       15                      0.005
Poor ground          4                       0.001
Good ground          25                      0.020
Fresh water          81                      0.010
Sea water            81                      5.0
================= ========================= ===================

For most purposes, use the constants for average ground.

Surface Refractivity and Climate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The surface refractivity represents the normal value of refractivity near the ground (surface) and is measured in N-units (parts per million).
The model also uses a qualitative radio_climate argument to characterize the atmosphere and its variability in time.  The model recognizes specific 
enumerated climate categories and the associated surface refractivity is given in the table below.

=========================================== ================================== =====================
**Climate**                                   **Surface Refractivity (Ns)**      **radio_climate**
------------------------------------------- ---------------------------------- ---------------------
Equatorial (Congo)                              360                                 1
Continental Subtropical (Sudan)                 320                                 2
Maritime Subtropical (West Coast of Africa)     370                                 3
Desert (Sahara)                                 280                                 4
Continental Temperate                           301                                 5
Maritime Temperate, over land                   320                                 6
Maritime Temperate, over sea                    350                                 7
=========================================== ================================== =====================

The Surface refractivity value must be in the range 250-400.

Deployment Parameters
------------------------
Siting Criteria
^^^^^^^^^^^^^^^^^^^^^^^^^
The Siting Criteria is a qualitative assessment used for the *RSiteCriteria* and *TSiteCriteria* model arguments to describe the quality of antenna deployment.
The three valid enumerations for siting criteria are listed in the table below.

====================== ==============
**Siting Criteria**     **Value**  
---------------------- --------------
Random                     0
Careful                    1
Very Careful               2
====================== ==============

When most of the terminals are sited on high ground with some effort to locate them where signals appear strong, we say the siting is *very careful*.  When terminals are located at 
elevated sites but no attempt has been made to specifically select hilltops or other advantaged points where signals are strong, we would classify it as a *careful* site.  If there is an
equal chance that the terminal siting could be good or poor, we classify it as *random*.


Statistical Parameters
----------------------------
Time, Location, and confidence
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
There are 3 model arguments that are used to characterize the parameter reliability of the system.  Each of these arguments are expressed as floating point values in the 
range 0.01-0.99 and represent the reliability or confidence interval percentage.

- **time**: Percentage of time the system is expected to operate.  Note that this should represent long-term availability and not short term fluctuations in service due to fading.
- **Location**: Percentage of locations in which the receiver is expected to operate
- **Confidence**: Confidence level of the returned channel attenuation values.

Model variability
^^^^^^^^^^^^^^^^^^^^^^^^^
This is a brief explanation of the statistical parameters used in the model.  For a more complete discussion on the topic, refer to the ITU documentation referenced at the bottom of the page.
The model variability argument can take on 1 of 4 enumerated values which dictate how the underlying statistical parameters of the model are treated.  The model considers the 1st order statistics
to be related to *Time*, *Location*, and *Situation* reliability.  The confidence intervals are related to these individual (or combined) reliability parameters.

- **[0] Single Message Mode**: This mode combines all 3 kinds of variability into a one-dimensional random variable.  The *time* and *location* reliability percentage arguments are not used in this mode.  The system is only characterized by the confidence level argument.  For example, a system operating in this mode can be described as *"There is a 95% probability that the channel attenuation is 87.4dB"*.
- **[1] Individual Mode**: This mode combines *situation* and *location* variability into a single variable and treats *time* variability seperately.  The *location* argument is ignored.  Here, the *Time reliability* argument means time availability and the confidence measures the combined situation/location variability.  In this mode, you could say something like *"For at least 70% of the time, there is a 90% probability that the channel attenuation is 50.7dB"*.
- **[2] Mobile Mode**: This mode combines *location* and *time* variability since for a mobile node location is a function of time.  The *location* argument is ignored.  Reliability means Time/location variability and the confidence measures situation variability.  In this mode, you could say *"For at least 80% of the time there is a probability that 95% of like situations will have a channel loss of 100.9dB"*.
- **[3] Broadcast Mode**:  All 3 kinds of variability are treated seperately.  In this mode, you could say *"In 90% of like situation there will be at least 70% of the locations where the attenuation will not exceed 32.6dB for at least 95% of the time"*.


.. rubric:: Sources

| `[1]` `<https://www.ntia.doc.gov/report/1982/guide-use-its-irregular-terrain-model-area-prediction-mode>`_

