import math


def deg2rad(d):
    return d * math.pi / 180.0


def curve(c1, c2, x1, x2, x3, de):
    r = (c1 + c2 / (1.0 + math.pow((de - x2) / x3, 2.0))) * math.pow(de / x1, 2.0) \
        / (1.0 + math.pow(de / x1, 2.0))
    return r


def abq_alos(r):
    return (r.real * r.real) + (r.imag * r.imag)


def qerf(z):
    b1 = 0.319381530
    b2 = -0.356563782
    b3 = 1.781477937
    b4 = -1.821255987
    b5 = 1.330274429
    rp = 4.317008
    rrt2pi = 0.398942280
    x = z
    t = abs(x)
    if t >= 10.0:
        qerfv = 0.0
    else:
        t = rp / (t + rp)
        qerfv = math.exp(-0.5 * x * x) * rrt2pi * ((((b5 * t + b4) * t + b3) * t + b2) * t + b1) * t

    if x < 0.0:
        qerfv = 1.0 - qerfv

    return qerfv


def fortran_dim(x, y):
    # result is x-y if x is greater than y; otherwise result is 0.0
    if x > y:
        return x - y
    else:
        return 0.0


def aknfe(v2):
    if v2 < 5.76:
        a = 6.02 + 9.11 * math.sqrt(v2) - 1.27 * v2
    else:
        a = 12.953 + 4.343 * math.log(v2)
    return a


def qerfi(q):
    c0 = 2.515516698
    c1 = 0.802853
    c2 = 0.010328
    d1 = 1.432788
    d2 = 0.189269
    d3 = 0.001308
    x = 0.5 - q
    t = max(0.5 - abs(x), 0.000001)
    t = math.sqrt(-2.0 * math.log(t))
    v = t - ((c2 * t + c1) * t + c0) / (((d3 * t + d2) * t + d1) * t + 1.0)
    if x < 0.0:
        v = -v

    return v


def fht(x, pk):
    if x < 200.0:
        w = -math.log(pk)
        if pk < 1e-5 or x * math.pow(w, 3.0) > 5495.0:
            fhtv = -117.0
            if x > 1.0:
                fhtv = 17.372 * math.log(x) + fhtv
        else:
            fhtv = 2.5e-5 * x * x / pk - 8.686 * w - 15.0

    else:
        fhtv = 0.05751 * x - 4.343 * math.log(x)
        if x < 2000.0:
            w = 0.0134 * x * math.exp(-0.005 * x)
            fhtv = (1.0 - w) * fhtv + w * (17.372 * math.log(x) - 117.0)

    return fhtv


def h0f(r, et):
    a = (25.0, 80.0, 177.0, 395.0, 705.0)
    b = (24.0, 45.0, 68.0, 80.0, 105.0)
    it = int(et)
    if it <= 0:
        it = 1
        q = 0.0
    elif it >= 5:
        it = 5
        q = 0.0
    else:
        q = et - it

    x = math.pow(1.0 / r, 2.0)
    h0fv = 4.343 * math.log((a[it - 1] * x + b[it - 1]) * x + 1.0)
    if q != 0.0:
        h0fv = (1.0 - q) * h0fv + q * 4.343 * math.log((a[it] * x + b[it]) * x + 1.0)

    return h0fv


def ahd(td):
    a = (133.4, 104.6, 71.8)
    b = (0.332e-3, 0.212e-3, 0.157e-3)
    c = (-4.343, -1.086, 2.171)
    if td <= 10E3:
        i = 0
    elif 10E3 < td <= 70E3:
        i = 1
    else:
        i = 2

    return a[i] + b[i] * td + c[i] * math.log(td)
