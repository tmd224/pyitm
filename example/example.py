import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
                             inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from pyitm.itm import ITMAreadBLoss


if __name__ == "__main__":

    CONF = 0.90
    ModVar = 2
    deltaH = 200.0
    tht_m = 10.0
    rht_m = 1.0
    TSiteCriteria = 1
    RSiteCriteria = 0
    radio_climate = 5
    pol = 2
    pctTime = 0.7
    pctLoc = 0.5
    dist_km = 10.0
    frq_mhz = 100.0
    EPS = 15.0
    SGM = 0.005
    EN0 = 301.0

    dbloss = ITMAreadBLoss(ModVar, deltaH, tht_m, rht_m,
                           dist_km, TSiteCriteria, RSiteCriteria, EPS, SGM,
                           EN0, frq_mhz, radio_climate, pol, pctTime, pctLoc,
                           CONF)

    print("dbloss: {}dB".format(round(dbloss,2)))
