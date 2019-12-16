from pyitm.itm import ITMAreadBLoss

"""
This test module validates the model against the examples listed in Appendix A
of the NTIA 82-100 Report.
"""
# CONSTANTS
EPS = 15.0
SGM = 0.005
EN0 = 301.0
DIST_KM = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 125, 150, 175, 200, 225,
           250, 275, 300, 325, 350, 375, 400]

def test_areamode_1():
    # Model Results
    RESULTS = {
        10: {0.1: 136.1, 0.5: 145.7, 0.9: 155.3, 0.95: 158.1},
    }
    CONF = [0.10, 0.50, 0.90, 0.95]
    DIST = [10]
    ModVar = 2
    deltaH = 200.0
    tht_m = 10.0
    rht_m = 1.0
    TSiteCriteria = 1
    RSiteCriteria = 0
    frq_mhz = 400.0
    radio_climate = 5
    pol = 1
    pctTime = 0.7
    pctLoc = 0.5
    # pctConf = 0.9

    #dist_km = 10.0
    for d in DIST:
        for c in CONF:
            dbloss = ITMAreadBLoss(ModVar, deltaH, tht_m, rht_m, d,
                                   TSiteCriteria, RSiteCriteria, EPS, SGM, EN0,
                                   frq_mhz, radio_climate, pol, pctTime, pctLoc,
                                   c)
            assert round(dbloss, 1) == RESULTS[d][c]

"""
def test_areamode_2():
    ModVar = 2
    deltaH = 200.0
    tht_m = 10.0
    rht_m = 1.0
    dist_km = 10.0
    TSiteCriteria = 1
    RSiteCriteria = 0
    eps_dielect = 15.0
    sgm_conductivity = 0.005
    eno_ns_surfref = 301.0
    frq_mhz = 25.0
    radio_climate = 5
    pol = 1
    pctTime = 0.7
    pctLoc = 0.5
    pctConf = 0.9

    dist_km = 10.0
    dbloss = ITMAreadBLoss(ModVar, deltaH, tht_m, rht_m, dist_km,
                           TSiteCriteria, RSiteCriteria, eps_dielect,
                           sgm_conductivity, eno_ns_surfref, frq_mhz,
                           radio_climate, pol, pctTime, pctLoc, pctConf)
    assert round(dbloss, 1) == 130.1
"""