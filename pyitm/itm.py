import math
import cmath
from pyitm.util import curve, abq_alos, fortran_dim, aknfe, qerfi, fht, h0f, \
    ahd


# CONSTANTS
THIRD = 1.0/3.0
ITMVERSION = 7.0


class PropType:
    """
    Class to model the prop_type struct

    Attributes:
        aref (float): reference attenuation.  This is calculated in lrprop
        dist (float): Distance between terminals
        hg (list): Heights of the antennas above the ground [Tx, Rx]
        wn (float): Wave number of the radio frequency
        dh (float): Terrain irregularity parameter
        ens (float): Surface Refractivity
        gme (float): Effective curvature of the earth
        zgndreal (float): Surface transfer impedance (real)
        zgndimag (float): Surface transfer impedance (imag)
        he (list): Effect antenna heights [Tx, Rx]
        dl (list): Horizon distances [Tx, Rx]
        the (list): Horizon elevation angles [Tx, Rx]
        kwx (int): Error marker code
        mdp (int): Mode of the propagation model
    """
    def __init__(self):
        self.aref = float()
        self.dist = float()
        self.hg = [float(), float()]
        self.wn = float()
        self.dh = float()
        self.ens = float()
        self.gme = float()
        self.zgndreal = float()
        self.zgndimag = float()
        self.he = [float(), float()]
        self.dl = [float(), float()]
        self.the = [float(), float()]
        self.kwx = 0
        self.mdp = 0


class PropvType:
    """
    Class to model propv_type struct

    Attributes:
        sgc (float): Standard deviation of the confidence
        lvar (int): Level to which coefficients in AVAR must be defined
        mdvar (int): Mode of variability
        klim (int): Climate code
    """
    def __init__(self):
        self.sgc = float()
        self.lvar = int()
        self.mdvar = int()
        self.klim = int()


class PropaType:
    """
    Class to model the propa_type struct.
    Note that this object is used for internal calculations only

    Attributes:
        dlsa (float):
        dx (float):
        ael (float):
        ak1 (float):
        ak2 (float):
        aed (float):
        emd (float):
        aes (float):
        ems (float)
        dls (list):
        dla (float):
        tha (float):
    """
    def __init__(self):
        self.dlsa = float()
        self.dx = float()
        self.ael = float()
        self.ak1 = float()
        self.ak2 = float()
        self.aed = float()
        self.emd = float()
        self.aes = float()
        self.ems = float()
        self.dls = [float(), float()]
        self.dla = float()
        self.tha = float()


class InputError(Exception):
    """
    Custom Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


def qlrps(fmhz, zsys, en0, ipol, eps, sgm, prop):
    """
    Function to prepare parameters for area prediction mode.  Prior to calling
    this function one should define HG, DH, WN, ENS, GME, ZGND in Prop object

    Args:
        fmhz (float): Frequency of signal in MHz
        zsys (float): Avg elevation above sea level of the system; if 0,
            en0 will be interpreted as ENS
        en0 (float): Minimum monthly mean surface refractivity reduced to
            sea level; if it is desired to introduce ENS instead,
            then set ZSYS=0.
        ipol (int): Antenna polarization; 0 - horizontal, 1 - vertical
        eps (float): Ground permitivity
        sgm (float): Ground conductance
        prop (PropType): Prop object

    Returns:
        None
    """
    gma = 157E-9
    prop.wn = fmhz / 47.7
    prop.ens = en0
    if zsys != 0.0:
        prop.ens *= math.exp(-zsys / 9460.0)

    prop.gme = gma * (1.0 - 0.04665 * math.exp(prop.ens / 179.3))
    zq = eps + (376.62 * (sgm / prop.wn))*1j
    prop_zgnd = cmath.sqrt(zq - 1.0)
    if ipol != 0.0:
        prop_zgnd = prop_zgnd / zq

    prop.zgndreal = prop_zgnd.real
    prop.zgndimag = prop_zgnd.imag


def qlra(kst, klimx, mdvarx, prop, propv):
    """

    Args:
        kst (list): Siting criterion code for each terminal [Tx, Rx]
        klimx (int): Climate code
        mdvarx (int): Mode of variability
        prop (PropType): prop object
        propv (PropvType): propv object

    Returns:
        None
    """
    for j in range(0, 2):
        if kst[j] <= 0:
            prop.he[j] = prop.hg[j]
        else:
            q = 4.0
            if kst[j] != 1:
                q = 9.0
            if prop.hg[j] < 5.0:
                q *= math.sin(0.3141593 * prop.hg[j])

            prop.he[j] = prop.hg[j] + (1.0 + q) * \
                         math.exp(-min(20.0, 2.0 * prop.hg[j] /
                                       max(1E-3, prop.dh)))

        q = math.sqrt(2.0 * prop.he[j] / prop.gme)
        prop.dl[j] = q * math.exp(-0.07 * math.sqrt(prop.dh /
                                                    max(prop.he[j], 5.0)))
        prop.the[j] = (0.65 * prop.dh * (q / prop.dl[j] - 1.0) - 2.0 *
                       prop.he[j]) / q

    prop.mdp = 1
    propv.lvar = max(propv.lvar, 3)
    if mdvarx >= 0:
        propv.mdvar = mdvarx
        propv.lvar = max(propv.lvar, 4)

    if klimx > 0:
        propv.klim = klimx
        propv.lvar = 5


def lrprop(d, prop, propa):
    """

    Args:
        d (float): Distance between terminals in meters
        prop (PropType): PropType instance
        propa (PropaType): PropaType instance

    Returns:
        None
    """
    prop_zgnd = prop.zgndreal + prop.zgndimag*1j
    # python implementation of C++ static variables
    if not hasattr(lrprop, "wlos"):
        lrprop.wlos = False

    if not hasattr(lrprop, "wscat"):
        lrprop.wscat = False

    if not hasattr(lrprop, "dmin"):
        lrprop.dmin = float()

    if not hasattr(lrprop, "xae"):
        lrprop.xae = float()

    if prop.mdp != 0:
        for j in range(0, 2):
            propa.dls[j] = math.sqrt(2.0 * prop.he[j] / prop.gme)

        propa.dlsa = propa.dls[0] + propa.dls[1]
        propa.dla = prop.dl[0] + prop.dl[1]
        propa.tha = max(prop.the[0] + prop.the[1], -propa.dla * prop.gme)
        lrprop.wlos = False
        lrprop.wscat = False

        if prop.wn < 0.838 or prop.wn > 210.0:
            prop.kwx = max(prop.kwx, 1)

        for j in range(0, 2):
            if prop.hg[j] < 1.0 or prop.hg[j] > 1000.0:
                prop.kwx = max(prop.kwx, 1)

        for j in range(0, 2):
            if abs(prop.the[j]) > 200e-3 or prop.dl[j] < 0.1 * \
                    propa.dls[j] or prop.dl[j] > 3.0 * propa.dls[j]:
                prop.kwx = max(prop.kwx, 3)

        if prop.ens < 250.0 or prop.ens > 400.0 or prop.gme < 75E-9 or \
                prop.gme > 250E-9 or prop_zgnd.real <= abs(prop_zgnd.imag) or \
                prop.wn < 0.419 or prop.wn > 420.0:
            prop.kwx = 4

        for j in range(0, 2):
            if prop.hg[j] < 0.5 or prop.hg[j] > 3000.0:
                prop.kwx = 4

        lrprop.dmin = abs(prop.he[0] - prop.he[1]) / 200E-3
        q = adiff(0.0, prop, propa)
        xae = math.pow(prop.wn * math.pow(prop.gme, 2), -THIRD)
        d3 = max(propa.dlsa, 1.3787 * xae + propa.dla)
        d4 = d3 + 2.7574 * xae
        a3 = adiff(d3, prop, propa)
        a4 = adiff(d4, prop, propa)
        propa.emd = (a4 - a3) / (d4 - d3)
        propa.aed = a3 - propa.emd * d3

    if prop.mdp >= 0:
        prop.mdp = 0
        prop.dist = d

    if prop.dist > 0.0:
        if prop.dist > 1000E3:
            prop.kwx = max(prop.kwx, 1)

        if prop.dist < lrprop.dmin:
            prop.kwx = max(prop.kwx, 3)

        if prop.dist < 1E3 or prop.dist > 2000E3:
            prop.kwx = 4

    if prop.dist < propa.dlsa:
        if not lrprop.wlos:
            q = alos(0.0, prop, propa)
            d2 = propa.dlsa
            a2 = propa.aed + d2 * propa.emd
            d0 = 1.908 * prop.wn * prop.he[0] * prop.he[1]
            if propa.aed >= 0.0:
                d0 = min(d0, 0.5*propa.dla)
                d1 = d0 + 0.25 * (propa.dla - d0)
            else:
                d1 = max(-propa.aed / propa.emd, 0.25 * propa.dla)

            a1 = alos(d1, prop, propa)
            wq = False
            if d0 < d1:
                a0 = alos(d0, prop, propa)
                q = math.log(d2 / d0)
                propa.ak2 = max(0.0, ((d2 - d0) *
                                      (a1.real - a0.real) - (d1 - d0) *
                                      (a2 - a0.real)) / ((d2 - d0) *
                                math.log(d1 / d0) - (d1 - d0) * q))

                wq = propa.aed >= 0.0 or propa.ak2 > 0.0
                if wq:
                    propa.ak1 = (a2 - a0.real - propa.ak2 * q) / (d2 - d0)
                    if propa.ak1 < 0.0:
                        propa.ak1 = 0
                        propa.ak2 = fortran_dim(a2, a0.real) / q
                        if propa.ak2 == 0:
                            propa.ak1 = propa.emd

            if not wq:
                propa.ak1 = fortran_dim(a2, a1.real) / (d2 - d1)
                propa.ak2 = 0.0
                if propa.ak1 == 0.0:
                    propa.ak1 = propa.emd

            propa.ael = a2 - propa.ak1 * d2 - propa.ak2 * math.log(d2)
            lrprop.wlos = True

            if prop.dist > 0.0:
                prop.aref = propa.ael + propa.ak1 * prop.dist + propa.ak2 * \
                            math.log(prop.dist)

    if prop.dist <= 0.0 or prop.dist >= propa.dlsa:
        if not lrprop.wscat:
            q = ascat(0.0, prop, propa)
            d5 = propa.dla + 200E3
            d6 = d5 + 200E3
            a6 = ascat(d6, prop, propa)
            a5 = ascat(d5, prop, propa)
            if a5 < 1000.0:
                propa.ems = (a6 - a5) / 200E3
                propa.dx = max(propa.dlsa,
                               max(propa.dla + 0.3 * lrprop.xae *
                               math.log(47.7 * prop.wn),
                                   (a5 - propa.aed - propa.ems * d5) /
                               (propa.emd - propa.ems)))
                propa.aes = (propa.emd - propa.ems) * propa.dx + propa.aed
            else:
                propa.ems = propa.emd
                propa.aes = propa.aed
                propa.dx = 10.0E6

            lrprop.wscat = True

        if prop.dist > propa.dx:
            prop.aref = propa.aes + propa.ems * prop.dist
        else:
            prop.aref = propa.aed + propa.emd * prop.dist

    prop.aref = max(prop.aref, 0.0)


def alos(d, prop, propa):
    """

    Args:
        d:
        prop:
        propa:

    Returns:
        alosv (float):
    """
    prop_zgnd = prop.zgndreal + prop.zgndimag*1j
    if not hasattr(alos, "wls"):
        # python implementation of C++ static variable
        alos.wls = float()  # initialize static variable

    if d == 0.0:
        alos.wls = 0.021 / (0.021 + prop.wn * prop.dh / max(10E3, propa.dlsa))
        alosv = 0.0
    else:
        q = (1.0 - 0.8 * math.exp(-d / 50E3)) * prop.dh
        s = 0.78 * q * math.exp(-math.pow(q / 16.0, 0.25))
        q = prop.he[0] + prop.he[1]
        sps = q / math.sqrt((d * d) + (q * q))
        r = (sps - prop_zgnd) / (sps + prop_zgnd) * \
            math.exp(-min(10.0, prop.wn * s * sps))
        q = abq_alos(r)
        if q < 0.25 or q < sps:
            r = r * math.sqrt(sps / q)

        alosv = (propa.emd * d) + propa.aed
        q = prop.wn * prop.he[0] * prop.he[1] * 2.0 / d
        if q > 1.57:
            q = 3.14 - 2.4649

        alosv = (-4.343 * cmath.log(abq_alos((math.cos(q) -
                                              (math.sin(q) * 1j)) + r))
                 - alosv) * alos.wls + alosv

    return alosv.real


def adiff(d, prop, propa):
    """

    Args:
        d (float): distance
        prop (PropType):
        propa (PropaType):

    Returns:
        adiffv (float):
    """
    prop_zgnd = prop.zgndreal + prop.zgndimag*1j
    # python implementation of C++ static variables
    if not hasattr(adiff, "wd1"):
        adiff.wd1 = float()

    if not hasattr(adiff, "xd1"):
        adiff.xd1 = float()

    if not hasattr(adiff, "afo"):
        adiff.afo = float()

    if not hasattr(adiff, "qk"):
        adiff.qk = float()

    if not hasattr(adiff, "aht"):
        adiff.aht = float()

    if not hasattr(adiff, "xht"):
        adiff.xht = float()

    if d == 0:
        q = prop.hg[0] * prop.hg[1]
        adiff.qk = prop.he[0] * prop.he[1] - q
        if prop.mdp < 0.0:
            q += 10.0
        adiff.wd1 = math.sqrt(1.0 + adiff.qk / q)
        adiff.xd1 = propa.dla + propa.tha / prop.gme
        q = (1.0 - 0.8 * math.exp(-propa.dlsa / 50E3)) * prop.dh
        q *= 0.78 * math.exp(-math.pow(q / 16.0, 0.25))
        adiff.afo = min(15.0, 2.171 * math.log(1.0 + 4.77E-4 *
                                               prop.hg[0] * prop.hg[1] *
                        prop.wn * q))
        adiff.qk = 1.0 / abs(prop_zgnd)
        adiff.aht = 20.0
        adiff.xht = 0.0
        for j in range(0, 2):
            a = 0.5 * math.pow(prop.dl[j], 2.0) / prop.he[j]
            wa = math.pow(a * prop.wn, THIRD)
            pk = adiff.qk / wa
            q = (1.607 - pk) * 151.0 * wa * prop.dl[j] / a
            adiff.xht += q
            adiff.aht += fht(q, pk)

        adiffv = 0.0

    else:
        th = propa.tha + d * prop.gme
        ds = d - propa.dla
        q = 0.0795775 * prop.wn * ds * math.pow(th, 2.0)
        adiffv = aknfe(q * prop.dl[0] / (ds + prop.dl[0])) + \
                 aknfe(q * prop.dl[1] / (ds + prop.dl[1]))
        a = ds / th
        wa = math.pow(a * prop.wn, THIRD)
        pk = adiff.qk / wa
        q = (1.607 - pk) * 151.0 * wa * th + adiff.xht
        ar = 0.05751 * q - 4.343 * math.log(q) - adiff.aht
        q = (adiff.wd1 + adiff.xd1 / d) * \
            min(((1.0 - 0.8 * math.exp(-d / 50e3)) *
                 prop.dh * prop.wn), 6283.2)
        wd = 25.1 / (25.1 + math.sqrt(q))
        adiffv = ar * wd + (1.0 - wd) * adiffv + adiff.afo

    return adiffv


def ascat(d, prop, propa):
    """

    Args:
        d (float):
        prop (PropType):
        propa (PropaType):

    Returns:
        ascatv (float):
    """
    prop_zgnd = prop.zgndreal + prop.zgndimag*1j
    # python implementation of C++ static variables
    if not hasattr(ascat, "ad"):
        ascat.ad = float()

    if not hasattr(ascat, "rr"):
        ascat.rr = float()

    if not hasattr(ascat, "etq"):
        ascat.etq = float()

    if not hasattr(ascat, "h0s"):
        ascat.h0s = float()

    if d == 0.0:
        ascat.ad = prop.dl[0] - prop.dl[1]
        ascat.rr = prop.he[1] / prop.he[0]
        if ascat.ad < 0.0:
            ascat.ad = -ascat.ad
            ascat.rr = 1.0 / ascat.rr

        ascat.etq = (5.67E-6 * prop.ens - 2.32E-3) * prop.ens + 0.031
        ascat.h0s = -15.0
        ascatv = 0.0

    else:
        if ascat.h0s > 15.0:
            h0 = ascat.h0s
        else:
            th = prop.the[0] + prop.the[1] + d * prop.gme
            r2 = 2.0 * prop.wn * th
            r1 = r2 * prop.he[0]
            r2 *= prop.he[1]
            if r1 < 0.2 and r2 < 0.2:
                return 1001.0       # early return

            ss = (d - ascat.ad) / (d + ascat.ad)
            q = ascat.rr / ss
            ss = max(0.1, ss)
            q = min(max(0.1, q), 10.0)
            z0 = (d - ascat.ad) * (d + ascat.ad) * th * 0.25 / d
            et = (ascat.etq * math.exp(-math.pow(min(1.7, z0 / 8.0E3), 6.0)) +
                  1.0) * z0 / 1.7556e3
            ett = max(et, 1.0)
            h0 = (h0f(r1, ett) + h0f(r2, ett)) * 0.5
            h0 += min(h0, (1.38 - math.log(ett)) * math.log(ss) *
                      math.log(q) * 0.49)
            h0 = fortran_dim(h0, 0.0)
            if et < 1.0:
                h0 = et * h0 + (1.0 - et) * 4.343 * \
                     math.log(math.pow((1.0 + 1.4142 / r1) *
                               (1.0 + 1.4142 / r2), 2.0) *
                              (r1 + r2) / (r1 + r2 + 2.8284))

            if h0 > 15.0 and ascat.h0s >= 0.0:
                h0 = ascat.h0s

        ascat.h0s = h0
        th = propa.tha + d * prop.gme
        ascatv = ahd(th * d) + 4.343 * math.log(47.7 * prop.wn *
                                                math.pow(th, 4.0)) - 0.1 * \
                    (prop.ens - 301.0) * math.exp(-th * d / 40e3) + h0

    return ascatv


def avar(zzt, zzl, zzc, prop, propv):
    """

    Args:
        zzt (float):
        zzl (float):
        zzc (float):
        prop (PropType):
        propv (PropvType):

    Returns:
        avarv (float):
    """
    # python implementation of C++ static variables
    if not hasattr(avar, "kdv"):
        avar.kdv = int()
    if not hasattr(avar, "dexa"):
        avar.dexa = float()
    if not hasattr(avar, "de"):
        avar.de = float()
    if not hasattr(avar, "sgl"):
        avar.sgl = float()
    if not hasattr(avar, "sgtm"):
        avar.sgtm = float()
    if not hasattr(avar, "sgtp"):
        avar.sgtp = float()
    if not hasattr(avar, "sgtd"):
        avar.sgtd = float()
    if not hasattr(avar, "tgtd"):
        avar.tgtd = float()
    if not hasattr(avar, "gm"):
        avar.gm = float()
    if not hasattr(avar, "gp"):
        avar.gp = float()
    if not hasattr(avar, "cv1"):
        avar.cv1 = float()
    if not hasattr(avar, "cv2"):
        avar.cv2 = float()
    if not hasattr(avar, "yv1"):
        avar.yv1 = float()
    if not hasattr(avar, "yv2"):
        avar.yv2 = float()
    if not hasattr(avar, "yv3"):
        avar.yv3 = float()
    if not hasattr(avar, "csm1"):
        avar.csm1 = float()
    if not hasattr(avar, "csm2"):
        avar.csm2 = float()
    if not hasattr(avar, "ysm1"):
        avar.ysm1 = float()
    if not hasattr(avar, "ysm2"):
        avar.ysm2 = float()
    if not hasattr(avar, "ysm3"):
        avar.ysm3 = float()
    if not hasattr(avar, "csp1"):
        avar.csp1 = float()
    if not hasattr(avar, "csp2"):
        avar.csp2 = float()
    if not hasattr(avar, "ysp1"):
        avar.ysp1 = float()
    if not hasattr(avar, "ysp2"):
        avar.ysp2 = float()
    if not hasattr(avar, "ysp3"):
        avar.ysp3 = float()
    if not hasattr(avar, "csd1"):
        avar.csd1 = float()
    if not hasattr(avar, "zd"):
        avar.zd = float()
    if not hasattr(avar, "cfm1"):
        avar.cfm1 = float()
    if not hasattr(avar, "cfm2"):
        avar.cfm2 = float()
    if not hasattr(avar, "cfm3"):
        avar.cfm3 = float()
    if not hasattr(avar, "cfp1"):
        avar.cfp1 = float()
    if not hasattr(avar, "cfp2"):
        avar.cfp2 = float()
    if not hasattr(avar, "cfp3"):
        avar.cfp3 = float()
    if not hasattr(avar, "ws"):
        avar.ws = bool()
    if not hasattr(avar, "w1"):
        avar.w1 = bool()

    bv1 = [-9.67, -0.62, 1.26, -9.21, -0.62, -0.39, 3.15]
    bv2 = [12.7, 9.19, 15.5, 9.05, 9.19, 2.86, 857.9]
    xv1 = [144.9e3, 228.9e3, 262.6e3, 84.1e3, 228.9e3, 141.7e3, 2222.e3]
    xv2 = [190.3e3, 205.2e3, 185.2e3, 101.1e3, 205.2e3, 315.9e3, 164.8e3]
    xv3 = [133.8e3, 143.6e3, 99.8e3, 98.6e3, 143.6e3, 167.4e3, 116.3e3]
    bsm1 = [2.13, 2.66, 6.11, 1.98, 2.68, 6.86, 8.51]
    bsm2 = [159.5, 7.67, 6.65, 13.11, 7.16, 10.38, 169.8]
    xsm1 = [762.2e3, 100.4e3, 138.2e3, 139.1e3, 93.7e3, 187.8e3, 609.8e3]
    xsm2 = [123.6e3, 172.5e3, 242.2e3, 132.7e3, 186.8e3, 169.6e3, 119.9e3]
    xsm3 = [94.5e3, 136.4e3, 178.6e3, 193.5e3, 133.5e3, 108.9e3, 106.6e3]
    bsp1 = [2.11, 6.87, 10.08, 3.68, 4.75, 8.58, 8.43]
    bsp2 = [102.3, 15.53, 9.60, 159.3, 8.12, 13.97, 8.19]
    xsp1 = [636.9e3, 138.7e3, 165.3e3, 464.4e3, 93.2e3, 216.0e3, 136.2e3]
    xsp2 = [134.8e3, 143.7e3, 225.7e3, 93.1e3, 135.9e3, 152.0e3, 188.5e3]
    xsp3 = [95.6e3, 98.6e3, 129.7e3, 94.2e3, 113.4e3, 122.7e3, 122.9e3]
    bsd1 = [1.224, 0.801, 1.380, 1.000, 1.224, 1.518, 1.518]
    bzd1 = [1.282, 2.161, 1.282, 20., 1.282, 1.282, 1.282]
    bfm1 = [1.0, 1.0, 1.0, 1.0, 0.92, 1.0, 1.0]
    bfm2 = [0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0]
    bfm3 = [0.0, 0.0, 0.0, 0.0, 1.77, 0.0, 0.0]
    bfp1 = [1.0, 0.93, 1.0, 0.93, 0.93, 1.0, 1.0]
    bfp2 = [0.0, 0.31, 0.0, 0.19, 0.31, 0.0, 0.0]
    bfp3 = [0.0, 2.00, 0.0, 1.79, 2.00, 0.0, 0.0]

    rt = 7.8
    rl = 24.0
    # modeling as static due to python switch implementation.
    avar.q = float()    # Re-initialize on every call

    avar.temp_klim = propv.klim - 1

    if propv.lvar > 0:
        # python model of a c++ switch statement
        def switch(case):
            def default():
                if propv.klim <= 0 or propv.klim > 7:
                    propv.klim = 5
                    avar.temp_klim = 4
                    prop.kwx = max(prop.kwx, 2)
                avar.cv1 = bv1[avar.temp_klim]
                avar.cv2 = bv2[avar.temp_klim]
                avar.yv1 = xv1[avar.temp_klim]
                avar.yv2 = xv2[avar.temp_klim]
                avar.yv3 = xv3[avar.temp_klim]
                avar.csm1 = bsm1[avar.temp_klim]
                avar.csm2 = bsm2[avar.temp_klim]
                avar.ysm1 = xsm1[avar.temp_klim]
                avar.ysm2 = xsm2[avar.temp_klim]
                avar.ysm3 = xsm3[avar.temp_klim]
                avar.csp1 = bsp1[avar.temp_klim]
                avar.csp2 = bsp2[avar.temp_klim]
                avar.ysp1 = xsp1[avar.temp_klim]
                avar.ysp2 = xsp2[avar.temp_klim]
                avar.ysp3 = xsp3[avar.temp_klim]
                avar.csd1 = bsd1[avar.temp_klim]
                avar.zd = bzd1[avar.temp_klim]
                avar.cfm1 = bfm1[avar.temp_klim]
                avar.cfm2 = bfm2[avar.temp_klim]
                avar.cfm3 = bfm3[avar.temp_klim]
                avar.cfp1 = bfp1[avar.temp_klim]
                avar.cfp2 = bfp2[avar.temp_klim]
                avar.cfp3 = bfp3[avar.temp_klim]
                case4()

            def case4():
                avar.kdv = propv.mdvar
                avar.ws = avar.kdv >= 20
                if avar.ws:
                    avar.kdv -= 20
                avar.w1 = avar.kdv >= 10
                if avar.w1:
                    avar.kdv -= 10
                if avar.kdv < 0 or avar.kdv > 3:
                    avar.kdv = 0
                    prop.kwx = max(prop.kwx, 2)
                case3()

            def case3():
                avar.q = math.log(0.133 * prop.wn)
                avar.gm = avar.cfm1 + avar.cfm2 / \
                          (math.pow(avar.cfm3 * avar.q, 2.0) + 1.0)
                avar.qp = avar.cfp1 + avar.cfp2 / \
                          (math.pow(avar.cfp3 * avar.q, 2.0) + 1.0)
                case2()

            def case2():
                avar.dexa = math.sqrt(18e6 * prop.he[0]) + \
                            math.sqrt(18e6 * prop.he[1]) + \
                            math.pow((575.7e12 / prop.wn), THIRD)
                case1()

            def case1():
                if prop.dist < avar.dexa:
                    avar.de = 130E3 * prop.dist / avar.dexa
                else:
                    avar.de = 130E3 + prop.dist - avar.dexa

            switcher = {1: case1,
                        2: case2,
                        3: case3,
                        4: case4,
                        }

            return switcher.get(case, default)()
        switch(propv.lvar)  # execute the switch statement

        avar.vmd = curve(avar.cv1, avar.cv2, avar.yv1, avar.yv2, avar.yv3,
                         avar.de)
        avar.sgtm = curve(avar.csm1, avar.csm2, avar.ysm1, avar.ysm2,
                          avar.ysm3, avar.de) * avar.gm
        avar.sgtp = curve(avar.csp1, avar.csp2, avar.ysp1, avar.ysp2,
                          avar.ysp3, avar.de) * avar.gp
        avar.sgtd = avar.sgtp * avar.csd1
        avar.tgtd = (avar.sgtp - avar.sgtd) * avar.zd
        if avar.w1:
            avar.sg1 = 0.0
        else:
            avar.q = (1.0 - 0.8 * math.exp(-prop.dist / 50E3)) * \
                     prop.dh * prop.wn
            avar.sgl = 10.0 * avar.q / (avar.q + 13.0)

        if avar.w1:
            avar.vs0 = 0.0
        else:
            avar.vs0 = math.pow(5.0 + 3.0 * math.exp(-avar.de / 100E3), 2.0)

        propv.lvar = 0

    zt = zzt
    zl = zzl
    zc = zzc

    if avar.kdv == 0:
        zt = zc
        zl = zc
    elif avar.kdv == 1:
        zl = zc
    elif avar.kdv == 2:
        zl = zt

    if abs(zt) > 3.1 or abs(zl) > 3.1 or abs(zc) > 3.1:
        prop.kwx = max(prop.kwx, 1)

    if zt < 0.0:
        avar.sgt = avar.sgtm
    elif zt <= avar.zd:
        avar.sgt = avar.sgtp
    else:
        avar.sgt = avar.sgtd + avar.tgtd / zt

    vs = avar.vs0 + math.pow(avar.sgt * zt, 2.0) / (rt + zc * zc) + \
         math.pow(avar.sgl * zl, 2.0) / (rl + zc * zc)

    if avar.kdv == 0:
        yr = 0.0
        propv.sgc = math.sqrt(avar.sgt * avar.sgt + avar.sgl * avar.sgl + vs)

    elif avar.kdv == 1:
        yr = avar.sgt * zt
        propv.sgc = math.sqrt(avar.sg1 * avar.sgl + vs)

    elif avar.kdv == 2:
        yr = math.sqrt(avar.sgt * avar.sgt + avar.sgl * avar.sgl) * zt
        propv.sgc = math.sqrt(vs)

    else:
        yr = avar.sgt * zt + avar.sgl * zl
        propv.sgc = math.sqrt(vs)

    avarv = prop.aref - avar.vmd - yr - propv.sgc * zc
    if avarv < 0.0:
        avarv = avarv * (29.0 - avarv) / (29.0 - 10.0 * avarv)

    return avarv


def area(ModVar, deltaH, tht_m, rht_m, dist_km, TSiteCriteria, RSiteCriteria,
         eps_dielect, sgm_conductivity, eno_ns_surfref, frq_mhz, radio_climate,
         pol, pctTime, pctLoc, pctConf):
    """

    Args:
        ModVar (int): 0 - Single: pctConf is "Time/Situation/Location",
                        pctTime, pctLoc not used
                      1 - Individual: pctTime is "Situation/Location",
                        pctConf is "Confidence", pctLoc not used
                      2 - Mobile: pctTime is "Time/Locations (Reliability)",
                        pctConf is "Confidence", pctLoc not used
                      3 - Broadcast: pctTime is "Time", pctLoc is "Location",
                        pctConf is "Confidence"
        deltaH (float): Terrain irregularity parameter [m].  This is the
            interdecile range of terrain elevation between Tx/Rx sites.  For
            average terrain use 90.  Other recommendations are:
            Flat (or smooth water): 0; Plains: 30; Hills: 90; Mountains:
            200; Rugged Mountains: 500
        tht_m (float): Transmitter antenna height [m].  The height is
            determined by the center of the radiating element above ground.
            [0.5 - 3000]
        rht_m (float): Receiver antenna height [m].  The height is
            determined by the center of the radiating element above ground.
            [0.5 - 3000]
        dist_km (float): Distance between antennas [km]. The model is valid
            for distances in the range 1km - 2000km.
        TSiteCriteria (int): Tx Antenna deployment sitting criteria:
            0 - random, 1 - careful, 2 - very careful
        RSiteCriteria (int): Rx Antenna deployment sitting criteria:
            0 - random, 1 - careful, 2 - very careful
        eps_dielect (float): Relative Permittivity of the earth
        sgm_conductivity (float): Conductivity of the earth
        eno_ns_surfref (float): Surface Refractivity [250 - 400 N-units]
        frq_mhz (float): Carrier frequency [MHz]; The model is valid for
            frequencies in the range 20MHz - 20GHz
        radio_climate (int): 1-Equatorial, 2-Continental Subtropical,
                             3-Maritime Tropical, 4-Desert, 5-Continental
                             Temperate, 6-Maritime Temperate, Over Land,
                             7-Maritime Temperate, Over Sea
        pol (int): Antenna polarization; 0-Horizontal, 1-Vertical.  It is
            assumed that both antenna elements have the same polarization.
        pctTime (float): Time Reliability Percentage [.01 to .99]
        pctLoc (float): Location Reliability Percentage [.01 to .99]
        pctConf (float): Confidence Interval Percentage [.01 to .99]

    Returns:
        dbloss (float): RF Propogation loss [dB]
        errnum (int): 0- No Error.
                      1- Warning: Some parameters are nearly out of range.
                                  Results should be used with caution.
                      2- Note: Default parameters have been substituted for
                        impossible ones.
                      3- Warning: A combination of parameters is out of range.
                                  Results are probably invalid.
    """
    prop = PropType()
    propa = PropaType()
    propv = PropvType()
    kst = list()
    kst.append(int(TSiteCriteria))
    kst.append(int(RSiteCriteria))
    zt = qerfi(pctTime)
    zl = qerfi(pctLoc)
    zc = qerfi(pctConf)
    eps = eps_dielect
    sgm = sgm_conductivity
    eno = eno_ns_surfref
    prop.dh = deltaH
    prop.hg[0] = tht_m
    prop.hg[1] = rht_m
    propv.klim = radio_climate
    prop.ens = eno
    prop.kwx = 0
    ivar = ModVar
    ipol = pol

    # argument checking
    if frq_mhz < 20 or frq_mhz > 20000:
        raise InputError("frq_mhz={}MHz".format(frq_mhz),
                         "ITM model is only valid for frequencies 20MHz - "
                         "20GHz")

    if dist_km < 1.0 or dist_km > 2000:
        raise InputError("dist_km={}km".format(dist_km),
                         "ITM model is only valid for distances 1km - 2000km")

    if tht_m < 0.5 or tht_m > 3000:
        raise InputError("tht_m:{}m".format(tht_m),
                         "ITM model is only valid for antenna heights 0.5m - "
                         "3000m")

    if rht_m < 0.5 or rht_m > 3000:
        raise InputError("rht_m:{}m".format(rht_m),
                         "ITM model is only valid for antenna heights 0.5m - "
                         "3000m")

    if ipol not in [0, 1]:
        raise InputError("ipol={}".format(ipol),
                         "Invalid antenna polarization code {}.  Valid "
                         "codes: [0, 1]")

    if eno_ns_surfref < 250 or eno_ns_surfref > 400:
        raise InputError("eno_ns_surfref={}".format(eno_ns_surfref),
                         "Invalid Surface Refractivity Valid range: ["
                         "250 - 400")

    if radio_climate not in range(1, 8):
        raise InputError("radio_climate={}".format(radio_climate),
                         "Invalid radio climate parameter. "
                         "Valid values: [{}]".format(range(0, 8)))

    if TSiteCriteria not in range(0, 3):
        raise InputError("TSiteCriteria={}".format(TSiteCriteria),
                         "Invalid Tx sitting criterial. Valid values: [{}]"
                         .format(TSiteCriteria, range(0, 4)))

    if RSiteCriteria not in range(0, 3):
        raise InputError("RSiteCriteria={}".format(RSiteCriteria),
                         "Invalid Rx sitting criterial. Valid values: [{}]"
                         .format(RSiteCriteria, range(0, 4)))

    if pctTime < 0.01 or pctTime > 0.99:
        raise InputError("pctTime: {}".format(pctTime),
                         "Invalid pctTime. Valid range: [0.01 - 0.99]")

    if pctLoc < 0.01 or pctLoc > 0.99:
        raise InputError("pctLoc: {}".format(pctLoc),
                         "Invalid pctLoc. Valid range: [0.01 - 0.99]")

    if pctConf < 0.01 or pctConf > 0.99:
        raise InputError("pctConf: {}".format(pctConf),
                         "Invalid pctConf. Valid range: [0.01 - 0.99]")

    qlrps(frq_mhz, 0.0, eno, ipol, eps, sgm, prop)
    # prop.dump()
    qlra(kst, propv.klim, ivar, prop, propv)
    # prop.dump()
    # propv.dump()
    if propv.lvar < 1:
        propv.lvar = 1

    lrprop(dist_km * 1000.0, prop, propa)

    fs = 32.45 + 20.0 * math.log10(frq_mhz) + 20.0 * \
         math.log10(prop.dist / 1000.0)
    xlb = fs + avar(zt, zl, zc, prop, propv)
    dbloss = xlb
    if prop.kwx == 0:
        errnum = 0
    else:
        errnum = prop.kwx

    return dbloss, errnum


def ITMAreadBLoss(ModVar, deltaH, tht_m, rht_m, dist_km, TSiteCriteria,
                  RSiteCriteria, eps_dielect, sgm_conductivity,
                  eno_ns_surfref, frq_mhz, radio_climate,
                  pol, pctTime, pctLoc, pctConf):
    """

    Args:
        ModVar (int): Mode of variability. 0 - [Single] pctConf is
            "Time/Situation/Location", pctTime, pctLoc not used.  1 - [
            Individual] pctTime is "Situation/Location", pctConf is
            "Confidence", pctLoc not used.  2 - [Mobile] pctTime is
            "Time/Locations (Reliability)", pctConf is "Confidence", pctLoc
            not used.  3 - [Broadcast] pctTime is "Time", pctLoc is
            "Location", pctConf is "Confidence".
        deltaH (float): Terrain irregularity parameter [m].  This is the
            interdecile range of terrain elevation between Tx/Rx sites.  For
            average terrain use 90.  Other recommendations are:
            Flat (or smooth water): 0; Plains: 30; Hills: 90; Mountains:
            200; Rugged Mountains: 500.
        tht_m (float): Transmitter antenna height [m].  The height is
            determined by the center of the radiating element above ground.
        rht_m (float): Receiver antenna height [m].  The height is
            determined by the center of the radiating element above ground.
        dist_km (float): Distance between antennas [km]. The model is valid
            for distances in the range 1km - 2000km.
        TSiteCriteria (int): Tx Antenna deployment sitting criteria:
            0 - random, 1 - careful, 2 - very careful
        RSiteCriteria (int): Rx Antenna deployment sitting criteria:
            0 - random, 1 - careful, 2 - very careful
        eps_dielect (float): Relative Permittivity of the earth
        sgm_conductivity (float): Conductivity of the earth
        eno_ns_surfref (float): Surface Refractivity [250 - 400 N-units]
        frq_mhz (float): Carrier frequency [MHz]; The model is valid for
            frequencies in the range 20MHz - 20GHz
        radio_climate (int): 1-Equatorial, 2-Continental Subtropical,
                             3-Maritime Tropical, 4-Desert, 5-Continental
                             Temperate, 6-Maritime Temperate, Over Land,
                             7-Maritime Temperate, Over Sea
        pol (int): Antenna polarization; 0-Horizontal, 1-Vertical.  It is
            assumed that both antenna elements have the same polarization.
        pctTime (float): Time Reliability Percentage [.01 to .99]
        pctLoc (float): Location Reliability Percentage [.01 to .99]
        pctConf (float): Confidence Interval Percentage [.01 to .99]

    Returns:
        dbloss (float): RF propogation loss [dB]
    """
    dbloss, _ = area(ModVar, deltaH, tht_m, rht_m, dist_km, TSiteCriteria,
                     RSiteCriteria, eps_dielect, sgm_conductivity,
                     eno_ns_surfref, frq_mhz, radio_climate,
                     pol, pctTime, pctLoc, pctConf)
    return dbloss


def ITMVersion():
    return ITMVERSION
