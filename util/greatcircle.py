from math import pi, cos, sin, tan, radians, acos, asin, atan2, degrees

EPS = 1e-6
R = 6371000.

def approx_eq(a, b):
    return abs(a - b) < EPS

def midpoint(lat1, lat2, lon1, lon2, n):
    """ See wiki: http://en.wikipedia.org/wiki/Great-circle_navigation """
    phi1 = radians(lat1)
    phi2 = radians(lat2)
    lambda1 = radians(lon1)
    lambda2 = radians(lon2)
    lambda12 = lambda2 - lambda1
    if lambda12 > pi:
        lambda12 = lambda12 - 2*pi
    elif lambda12 < -pi:
        lambda12 = lambda12 + 2*pi

    alpha1 = atan2(sin(lambda12), (cos(phi1)*tan(phi2) - sin(phi1)*cos(lambda12)))
    alpha2 = atan2(sin(lambda12), (-cos(phi2)*tan(phi1) + sin(phi2)*cos(lambda12)))

    sigma12 = acos(sin(phi1)*sin(phi2) + cos(phi1)*cos(phi2)*cos(lambda12))

    s12 = R*sigma12
    d = s12/n

    alpha0 = asin(sin(alpha1)*cos(phi1))

    sigma01 = 0 if (approx_eq(phi1, 0) and approx_eq(alpha1, pi / 2)) else atan2(tan(phi1), cos(alpha1))
    sigma02 = sigma01 + sigma12

    lambda01 = atan2(sin(alpha0)*sin(sigma01), cos(sigma01))

    lambda0 = lambda1 - lambda01

    def getPhi(sigma):
        return asin(cos(alpha0)*sin(sigma))
    def getLambda(sigma):
        return atan2(sin(alpha0)*sin(sigma), cos(sigma)) + lambda0

    path = [(lat1, lon1)]

    for i in xrange(1,n):
        sigma = sigma01 + (i*d/R)
        phi = degrees(getPhi(sigma))
        lambdu = degrees(getLambda(sigma))
        path.append((phi, lambdu))

    path.append((lat2, lon2))

    return path