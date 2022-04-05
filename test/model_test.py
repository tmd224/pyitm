import pytest
from pyitm.itm import ITMAreadBLoss, InputError

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
DIST_KM_ALT = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140,
               150, 200, 250, 300, 350, 400, 450, 500]


def test_areamode_1():
    # Model Results
    RESULTS = {
        10.0: {'FS': 104.5, 0.1: 136.1, 0.5: 145.7, 0.9: 155.3, 0.95: 158.1},
        20.0: {'FS': 110.5, 0.1: 149.3, 0.5: 158.4, 0.9: 167.4, 0.95: 169.9},
        30.0: {'FS': 114.0, 0.1: 156.5, 0.5: 165.1, 0.9: 173.7, 0.95: 176.1},
        40.0: {'FS': 116.5, 0.1: 162.6, 0.5: 170.8, 0.9: 179.0, 0.95: 181.3},
        50.0: {'FS': 118.5, 0.1: 168.0, 0.5: 175.9, 0.9: 183.8, 0.95: 186.1},
        60.0: {'FS': 120.1, 0.1: 172.8, 0.5: 180.6, 0.9: 188.3, 0.95: 190.5},
        70.0: {'FS': 121.4, 0.1: 177.4, 0.5: 185.0, 0.9: 192.7, 0.95: 194.8},
        80.0: {'FS': 122.6, 0.1: 181.7, 0.5: 189.3, 0.9: 196.9, 0.95: 199.0},
        90.0: {'FS': 123.6, 0.1: 185.9, 0.5: 193.4, 0.9: 201.0, 0.95: 203.1},
        100.0: {'FS': 124.5, 0.1: 190.0, 0.5: 197.4, 0.9: 204.9, 0.95: 207.0},
        125.0: {'FS': 126.4, 0.1: 197.4, 0.5: 204.8, 0.9: 212.1, 0.95: 214.2},
        150.0: {'FS': 128.0, 0.1: 200.0, 0.5: 207.2, 0.9: 214.5, 0.95: 216.5},
        175.0: {'FS': 129.4, 0.1: 202.5, 0.5: 209.6, 0.9: 216.8, 0.95: 218.8},
        200.0: {'FS': 130.5, 0.1: 205.0, 0.5: 212.1, 0.9: 219.1, 0.95: 221.1},
        225.0: {'FS': 131.5, 0.1: 207.6, 0.5: 214.6, 0.9: 221.5, 0.95: 223.4},
        250.0: {'FS': 132.5, 0.1: 210.2, 0.5: 217.1, 0.9: 223.9, 0.95: 225.9},
        275.0: {'FS': 133.3, 0.1: 212.8, 0.5: 219.6, 0.9: 226.4, 0.95: 228.3},
        300.0: {'FS': 134.0, 0.1: 215.2, 0.5: 222.0, 0.9: 228.7, 0.95: 230.6},
        325.0: {'FS': 134.7, 0.1: 217.6, 0.5: 224.3, 0.9: 231.1, 0.95: 232.9},
        350.0: {'FS': 135.4, 0.1: 219.9, 0.5: 226.6, 0.9: 233.3, 0.95: 235.2},
        375.0: {'FS': 136.0, 0.1: 222.1, 0.5: 228.8, 0.9: 235.5, 0.95: 237.3},
        400.0: {'FS': 136.5, 0.1: 224.3, 0.5: 230.9, 0.9: 237.6, 0.95: 239.5},
    }
    CONF = [0.10, 0.50, 0.90, 0.95]
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

    for d in DIST_KM:
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
def test_areamode_2():
    # Model Results
    RESULTS = {
        10.0: {'FS': 80.4, 0.1: 110.2, 0.5: 120.1, 0.9: 130.1, 0.95: 132.9},
        20.0: {'FS': 86.4, 0.1: 125.3, 0.5: 134.9, 0.9: 144.5, 0.95: 147.2},
        30.0: {'FS': 90.0, 0.1: 131.3, 0.5: 140.6, 0.9: 149.8, 0.95: 152.5},
        40.0: {'FS': 92.5, 0.1: 136.1, 0.5: 145.1, 0.9: 154.1, 0.95: 156.7},
        50.0: {'FS': 94.4, 0.1: 140.4, 0.5: 149.1, 0.9: 157.9, 0.95: 160.4},
        60.0: {'FS': 96.0, 0.1: 144.2, 0.5: 152.7, 0.9: 161.2, 0.95: 163.7},
        70.0: {'FS': 97.3, 0.1: 147.7, 0.5: 156.0, 0.9: 164.4, 0.95: 166.7},
        80.0: {'FS': 98.5, 0.1: 151.0, 0.5: 159.2, 0.9: 167.3, 0.95: 169.6},
        90.0: {'FS': 99.5, 0.1: 154.1, 0.5: 162.1, 0.9: 170.2, 0.95: 172.4},
        100.0: {'FS': 100.4, 0.1: 157.1, 0.5: 165.0, 0.9: 172.9, 0.95: 175.1},
        125.0: {'FS': 102.3, 0.1: 164.0, 0.5: 171.6, 0.9: 179.2, 0.95: 181.4},
        150.0: {'FS': 103.9, 0.1: 170.3, 0.5: 177.8, 0.9: 185.2, 0.95: 187.3},
        175.0: {'FS': 105.3, 0.1: 176.3, 0.5: 183.6, 0.9: 190.9, 0.95: 193.0},
        200.0: {'FS': 106.4, 0.1: 182.1, 0.5: 189.3, 0.9: 196.4, 0.95: 198.4},
        225.0: {'FS': 107.5, 0.1: 187.8, 0.5: 194.9, 0.9: 202.0, 0.95: 204.0},
        250.0: {'FS': 108.4, 0.1: 193.7, 0.5: 200.7, 0.9: 207.7, 0.95: 209.6},
        275.0: {'FS': 109.2, 0.1: 199.7, 0.5: 206.6, 0.9: 213.5, 0.95: 215.4},
        300.0: {'FS': 110.0, 0.1: 205.8, 0.5: 212.6, 0.9: 219.4, 0.95: 221.4},
        325.0: {'FS': 110.6, 0.1: 211.9, 0.5: 218.7, 0.9: 225.4, 0.95: 227.3},
        350.0: {'FS': 111.3, 0.1: 218.0, 0.5: 224.7, 0.9: 231.4, 0.95: 233.3},
        375.0: {'FS': 111.9, 0.1: 220.3, 0.5: 227.0, 0.9: 233.7, 0.95: 235.5},
        400.0: {'FS': 112.5, 0.1: 222.5, 0.5: 229.1, 0.9: 235.7, 0.95: 237.6},
    }
    CONF = [0.10, 0.50, 0.90, 0.95]
    ModVar = 2
    deltaH = 200.0
    tht_m = 10.0
    rht_m = 1.0
    TSiteCriteria = 1
    RSiteCriteria = 0
    frq_mhz = 25.0
    radio_climate = 5
    pol = 1
    pctTime = 0.7
    pctLoc = 0.5

    for d in DIST_KM:
        for c in CONF:
            dbloss = ITMAreadBLoss(ModVar, deltaH, tht_m, rht_m, d,
                                   TSiteCriteria, RSiteCriteria, EPS, SGM, EN0,
                                   frq_mhz, radio_climate, pol, pctTime, pctLoc,
                                   c)
            assert round(dbloss, 1) == RESULTS[d][c]


def test_areamode_3():
    # Model Results
    RESULTS = {
        10.0: {'FS': 92.5, 0.5: 132.8, 0.9: 142.5, 0.1: 123.2},
        20.0: {'FS': 98.5, 0.5: 143.8, 0.9: 153.0, 0.1: 134.6},
        30.0: {'FS': 102.0, 0.5: 150.0, 0.9: 158.8, 0.1: 141.2},
        40.0: {'FS': 104.5, 0.5: 155.1, 0.9: 163.5, 0.1: 146.7},
        50.0: {'FS': 106.4, 0.5: 159.6, 0.9: 167.7, 0.1: 151.4},
        60.0: {'FS': 108.0, 0.5: 163.6, 0.9: 171.4, 0.1: 155.7},
        70.0: {'FS': 109.4, 0.5: 167.3, 0.9: 174.9, 0.1: 159.7},
        80.0: {'FS': 110.5, 0.5: 170.8, 0.9: 178.2, 0.1: 163.3},
        90.0: {'FS': 111.5, 0.5: 174.2, 0.9: 181.6, 0.1: 166.9},
        100.0: {'FS': 112.5, 0.5: 177.6, 0.9: 184.9, 0.1: 170.3},
        110.0: {'FS': 113.3, 0.5: 180.8, 0.9: 188.0, 0.1: 173.7},
        120.0: {'FS': 114.0, 0.5: 184.0, 0.9: 191.1, 0.1: 176.9},
        130.0: {'FS': 114.7, 0.5: 187.2, 0.9: 194.2, 0.1: 180.1},
        140.0: {'FS': 115.4, 0.5: 190.3, 0.9: 197.2, 0.1: 183.3},
        150.0: {'FS': 116.0, 0.5: 193.4, 0.9: 200.3, 0.1: 186.4},
        200.0: {'FS': 118.5, 0.5: 198.9, 0.9: 205.6, 0.1: 192.1},
        250.0: {'FS': 120.4, 0.5: 204.2, 0.9: 210.8, 0.1: 197.6},
        300.0: {'FS': 122.0, 0.5: 209.4, 0.9: 215.9, 0.1: 202.9},
        350.0: {'FS': 123.3, 0.5: 214.3, 0.9: 220.8, 0.1: 207.8},
        400.0: {'FS': 124.5, 0.5: 218.9, 0.9: 225.3, 0.1: 212.4},
        450.0: {'FS': 125.5, 0.5: 223.1, 0.9: 229.5, 0.1: 216.7},
        500.0: {'FS': 126.4, 0.5: 227.1, 0.9: 233.5, 0.1: 220.7},
    }
    CONF = [0.50, 0.90, 0.1]
    ModVar = 3
    deltaH = 90.0
    tht_m = 3.0
    rht_m = 3.0
    TSiteCriteria = 0
    RSiteCriteria = 0
    frq_mhz = 100.0
    radio_climate = 5
    pol = 1
    pctTime = 0.5
    pctLoc = 0.5

    for d in DIST_KM_ALT:
        for c in CONF:
            dbloss = ITMAreadBLoss(ModVar, deltaH, tht_m, rht_m, d,
                                   TSiteCriteria, RSiteCriteria, EPS, SGM, EN0,
                                   frq_mhz, radio_climate, pol, pctTime, pctLoc,
                                   c)
            assert round(dbloss, 1) == RESULTS[d][c]


def test_freq_exception():
    """"
    Test invalid frequency
    """
    CONF = 0.90
    ModVar = 2
    deltaH = 200.0
    tht_m = 10.0
    rht_m = 1.0
    TSiteCriteria = 1
    RSiteCriteria = 0
    radio_climate = 5
    pol = 1
    pctTime = 0.7
    pctLoc = 0.5
    dist_km = 10.0
    frq_mhz = 10.0

    pytest.raises(InputError, ITMAreadBLoss,ModVar, deltaH, tht_m, rht_m,
                  dist_km, TSiteCriteria, RSiteCriteria, EPS, SGM, EN0,
                  frq_mhz, radio_climate, pol, pctTime, pctLoc,
                  CONF)

    frq_mhz = 21000.0
    pytest.raises(InputError, ITMAreadBLoss,ModVar, deltaH, tht_m, rht_m,
                  dist_km, TSiteCriteria, RSiteCriteria, EPS, SGM, EN0,
                  frq_mhz, radio_climate, pol, pctTime, pctLoc,
                  CONF)


def test_dist_exception():
    """
    Test invalid distance
    """
    CONF = 0.90
    ModVar = 2
    deltaH = 200.0
    tht_m = 10.0
    rht_m = 1.0
    TSiteCriteria = 1
    RSiteCriteria = 0
    radio_climate = 5
    pol = 1
    pctTime = 0.7
    pctLoc = 0.5
    dist_km = 0.5
    frq_mhz = 100.0

    pytest.raises(InputError, ITMAreadBLoss,ModVar, deltaH, tht_m, rht_m,
                  dist_km, TSiteCriteria, RSiteCriteria, EPS, SGM, EN0,
                  frq_mhz, radio_climate, pol, pctTime, pctLoc,
                  CONF)

    dist_km = 2001.0
    pytest.raises(InputError, ITMAreadBLoss,ModVar, deltaH, tht_m, rht_m,
                  dist_km, TSiteCriteria, RSiteCriteria, EPS, SGM, EN0,
                  frq_mhz, radio_climate, pol, pctTime, pctLoc,
                  CONF)

def test_antenna_height_exception():
    """
    Test invalid distance
    """
    CONF = 0.90
    ModVar = 2
    deltaH = 200.0
    TSiteCriteria = 1
    RSiteCriteria = 0
    radio_climate = 5
    pol = 1
    pctTime = 0.7
    pctLoc = 0.5
    dist_km = 10.0
    frq_mhz = 100.0

    tht_m = 0.25
    rht_m = 1.0
    pytest.raises(InputError, ITMAreadBLoss,ModVar, deltaH, tht_m, rht_m,
                  dist_km, TSiteCriteria, RSiteCriteria, EPS, SGM, EN0,
                  frq_mhz, radio_climate, pol, pctTime, pctLoc,
                  CONF)

    tht_m = 3001.0
    rht_m = 1.0
    pytest.raises(InputError, ITMAreadBLoss,ModVar, deltaH, tht_m, rht_m,
                  dist_km, TSiteCriteria, RSiteCriteria, EPS, SGM, EN0,
                  frq_mhz, radio_climate, pol, pctTime, pctLoc,
                  CONF)

    tht_m = 1.0
    rht_m = 0.25
    pytest.raises(InputError, ITMAreadBLoss,ModVar, deltaH, tht_m, rht_m,
                  dist_km, TSiteCriteria, RSiteCriteria, EPS, SGM, EN0,
                  frq_mhz, radio_climate, pol, pctTime, pctLoc,
                  CONF)

    tht_m = 1.0
    rht_m = 3001.0
    pytest.raises(InputError, ITMAreadBLoss,ModVar, deltaH, tht_m, rht_m,
                  dist_km, TSiteCriteria, RSiteCriteria, EPS, SGM, EN0,
                  frq_mhz, radio_climate, pol, pctTime, pctLoc,
                  CONF)


def test_polarization_exception():
    """
    Test invalid polarization
    """
    CONF = 0.90
    ModVar = 2
    deltaH = 200.0
    tht_m = 10.0
    rht_m = 1.0
    TSiteCriteria = 1
    RSiteCriteria = 0
    radio_climate = 5
    pctTime = 0.7
    pctLoc = 0.5
    dist_km = 0.5
    frq_mhz = 100.0

    pol = 2
    pytest.raises(InputError, ITMAreadBLoss,ModVar, deltaH, tht_m, rht_m,
                  dist_km, TSiteCriteria, RSiteCriteria, EPS, SGM, EN0,
                  frq_mhz, radio_climate, pol, pctTime, pctLoc,
                  CONF)


def test_surface_refractivity_exception():
    """
    Test invalid surface refractivity
    """
    CONF = 0.90
    ModVar = 2
    deltaH = 200.0
    tht_m = 10.0
    rht_m = 1.0
    TSiteCriteria = 1
    RSiteCriteria = 0
    radio_climate = 5
    pol = 1
    pctTime = 0.7
    pctLoc = 0.5
    dist_km = 0.5
    frq_mhz = 100.0

    EN0_NS = 249
    pytest.raises(InputError, ITMAreadBLoss,ModVar, deltaH, tht_m, rht_m,
                  dist_km, TSiteCriteria, RSiteCriteria, EPS, SGM, EN0_NS,
                  frq_mhz, radio_climate, pol, pctTime, pctLoc,
                  CONF)

    EN0_NS = 401
    pytest.raises(InputError, ITMAreadBLoss,ModVar, deltaH, tht_m, rht_m,
                  dist_km, TSiteCriteria, RSiteCriteria, EPS, SGM, EN0_NS,
                  frq_mhz, radio_climate, pol, pctTime, pctLoc,
                  CONF)


def test_climate_exception():
    """
    Test invalid climate
    """
    CONF = 0.90
    ModVar = 2
    deltaH = 200.0
    tht_m = 10.0
    rht_m = 1.0
    TSiteCriteria = 1
    RSiteCriteria = 0
    pctTime = 0.7
    pctLoc = 0.5
    dist_km = 0.5
    frq_mhz = 100.0
    pol = 1

    radio_climate = 8
    pytest.raises(InputError, ITMAreadBLoss,ModVar, deltaH, tht_m, rht_m,
                  dist_km, TSiteCriteria, RSiteCriteria, EPS, SGM, EN0,
                  frq_mhz, radio_climate, pol, pctTime, pctLoc,
                  CONF)


def test_site_criteria_exception():
    """
    Test invalid site criteria
    """
    CONF = 0.90
    ModVar = 2
    deltaH = 200.0
    tht_m = 10.0
    rht_m = 1.0
    pctTime = 0.7
    pctLoc = 0.5
    dist_km = 0.5
    frq_mhz = 100.0
    pol = 1
    radio_climate = 8

    TSiteCriteria = 3
    RSiteCriteria = 0
    pytest.raises(InputError, ITMAreadBLoss,ModVar, deltaH, tht_m, rht_m,
                  dist_km, TSiteCriteria, RSiteCriteria, EPS, SGM, EN0,
                  frq_mhz, radio_climate, pol, pctTime, pctLoc,
                  CONF)

    TSiteCriteria = 1
    RSiteCriteria = 3
    pytest.raises(InputError, ITMAreadBLoss,ModVar, deltaH, tht_m, rht_m,
                  dist_km, TSiteCriteria, RSiteCriteria, EPS, SGM, EN0,
                  frq_mhz, radio_climate, pol, pctTime, pctLoc,
                  CONF)

def test_modvar_exception():
    """
    Test invalid modVar
    """
    CONF = 0.90
    ModVar = 5
    deltaH = 200.0
    tht_m = 10.0
    rht_m = 1.0
    pctTime = 0.7
    pctLoc = 0.5
    dist_km = 0.5
    frq_mhz = 100.0
    pol = 1
    radio_climate = 1

    TSiteCriteria = 0
    RSiteCriteria = 0
    pytest.raises(InputError, ITMAreadBLoss,ModVar, deltaH, tht_m, rht_m,
                  dist_km, TSiteCriteria, RSiteCriteria, EPS, SGM, EN0,
                  frq_mhz, radio_climate, pol, pctTime, pctLoc,
                  CONF)


def test_reliability_exception():
    """
    Test invalid reliability parameters
    """
    CONF = 0.90
    ModVar = 2
    deltaH = 200.0
    tht_m = 10.0
    rht_m = 1.0
    dist_km = 0.5
    frq_mhz = 100.0
    pol = 1
    radio_climate = 1
    TSiteCriteria = 0
    RSiteCriteria = 0

    pctTime = 1.1
    pctLoc = 0.5
    pytest.raises(InputError, ITMAreadBLoss,ModVar, deltaH, tht_m, rht_m,
                  dist_km, TSiteCriteria, RSiteCriteria, EPS, SGM, EN0,
                  frq_mhz, radio_climate, pol, pctTime, pctLoc,
                  CONF)     

    pctTime = 0.0
    pctLoc = 0.5
    pytest.raises(InputError, ITMAreadBLoss,ModVar, deltaH, tht_m, rht_m,
                  dist_km, TSiteCriteria, RSiteCriteria, EPS, SGM, EN0,
                  frq_mhz, radio_climate, pol, pctTime, pctLoc,
                  CONF)                               

    pctTime = 0.9
    pctLoc = 1.1
    pytest.raises(InputError, ITMAreadBLoss,ModVar, deltaH, tht_m, rht_m,
                  dist_km, TSiteCriteria, RSiteCriteria, EPS, SGM, EN0,
                  frq_mhz, radio_climate, pol, pctTime, pctLoc,
                  CONF)                      

    pctTime = 0.9
    pctLoc = 0.0
    pytest.raises(InputError, ITMAreadBLoss,ModVar, deltaH, tht_m, rht_m,
                  dist_km, TSiteCriteria, RSiteCriteria, EPS, SGM, EN0,
                  frq_mhz, radio_climate, pol, pctTime, pctLoc,
                  CONF)                     


def test_modvar():
    CONF = 0.90
    deltaH = 200.0
    tht_m = 10.0
    rht_m = 1.0
    TSiteCriteria = 1
    RSiteCriteria = 0
    radio_climate = 5
    pol = 1
    pctTime = 0.7
    pctLoc = 0.5
    dist_km = 10.0
    frq_mhz = 100.0
    EPS = 15.0
    SGM = 0.005
    EN0 = 301.0

    MODVAR = [0, 1, 2, 3]
    RESULT = [142, 142.1, 141.0, 136.2]
    for idx, modvar in enumerate(MODVAR):
        dbloss = ITMAreadBLoss(modvar, deltaH, tht_m, rht_m,
                    dist_km, TSiteCriteria, RSiteCriteria, EPS, SGM, EN0,
                    frq_mhz, radio_climate, pol, pctTime, pctLoc,
                    CONF)
    
        assert round(dbloss, 1) == RESULT[idx]            

def test_climate():
    CONF = 0.90
    modvar = 1
    deltaH = 200.0
    tht_m = 10.0
    rht_m = 1.0
    TSiteCriteria = 1
    RSiteCriteria = 0
    radio_climate = 5
    pol = 1
    pctTime = 0.7
    pctLoc = 0.5
    dist_km = 10.0
    frq_mhz = 100.0
    EPS = 15.0
    SGM = 0.005
    EN0 = 301.0

    CLIMATE = range(1, 8)
    RESULT = [142.1, 142.1, 142.0, 142.2, 142.1, 142.0, 142.0]
    for idx, radio_climate in enumerate(CLIMATE):
        dbloss = ITMAreadBLoss(modvar, deltaH, tht_m, rht_m,
                    dist_km, TSiteCriteria, RSiteCriteria, EPS, SGM, EN0,
                    frq_mhz, radio_climate, pol, pctTime, pctLoc,
                    CONF)
    
        assert round(dbloss, 1) == RESULT[idx]           