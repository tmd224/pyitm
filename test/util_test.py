import math
from pyitm.util import deg2rad, qerf, fortran_dim, fht, h0f, ahd
from pyitm.itm import ITMVersion


def test_deg2rad():
    assert round(deg2rad(180.0), 10) == round(math.pi, 10)


def test_qerv():
    assert round(qerf(0.5), 5) == 0.30854
    assert round(qerf(-0.5), 5) == 0.69146
    assert round(qerf(11), 5) == 0.0


def test_fortran_dim():
    assert fortran_dim(10, 11) == 0.0


def test_fht():
    assert round(fht(2, 1E-6), 10) == -104.9586471793


def test_h0f():
    assert round(h0f(1, 0), 10) == 16.9899159126
    assert round(h0f(1, 6), 10) == 29.0905781590


def test_ahd():
    assert round(ahd(100E3), 10) == 112.4945611845
    assert round(ahd(50E3), 10) == 103.4497207831


def test_version():
    assert ITMVersion() == 7.0
