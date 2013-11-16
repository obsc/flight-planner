from math import pi, cos, sin, tan, radians, acos, asin, atan2, degrees, sinh, cosh

EPS = 1e-6
R = 6371000.

def approx_eq(a, b):
    return abs(a - b) < EPS

'takes angle in degrees and fixes it to conform to latitude '
def fix_lat(angle):
    if angle < -90:
        return angle + 180
    elif angle >90:
        return angle - 180
    else:
        return angle

def fix_lon(angle):
    if angle < -180:
        return angle + 360
    elif angle > 180:
        return angle - 360
    else:
        return angle

def fix_pair(angles):
    lat, lon = angles
    return (fix_lat(lat), fix_lon(lon))


def get_path(start, dest, n):
    """ See wiki: http://en.wikipedia.org/wiki/Great-circle_navigation """
    lat1, lon1 = start
    lat2, lon2 = dest
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

    path = [fix_pair((lat1, lon1))]

    for i in xrange(1,n):
        sigma = sigma01 + (i*d/R)
        phi = degrees(getPhi(sigma))
        lambdu = degrees(getLambda(sigma))
        path.append(fix_pair((phi, lambdu)))

    path.append(fix_pair((lat2, lon2)))

    return path

def to_latlon(northings, eastings, altitude):
    f = 1/298.257223563
    n = f / (2 - f)
    n_0 = 0.0
    k_0 = 0.9996
    e_0 = 500.
    a = 6378.137 #km
    big_a = (a / (1 + n)) * (1 + (n**2 / 4) + (n**4 / 64)) #approximately
    alpha_1 = .5 * n - (2. / 3.) * n**2 + (5. / 16.) * n**3
    alpha_2 = (13./48.) * n**2 - (3./5.) * n**3
    alpha_3 = (61./240.) * n**3
    beta_1 = (1./2.) * n - (2. / 3.) * n**2 + (37./96.) * n**3
    beta_2 = (1./48.) * n**2 + (1. / 15.) * n**3
    beta_3 = (17. /480.) * n**3
    delta_1 = 2. * n - (2./3.) * n**2 - 2* n**3
    delta_2 = (7./3.) * n**2 - (8. / 5.) * n**3 
    delta_3 = (56./15.) * n**3

    psi = (n - n_0) / (k_0 * big_a)
    nu = (e - e_0) / (k_0 * big_a)
    psi_prime = psi - ((beta_1 * sin(2. * 1 * nu) * cosh(2. * 1 * nu)) + 
        (beta_2 * sin(2. * 2 * nu) * cosh(2. * 2 * nu)) + (beta_3 * sin(2. * 3 * nu) * cosh(2. * 3 * nu)))
    nu_prime = nu - ((beta_1 * cos(2. * 1 * psi) * sinh(2. * 1 * nu)) + 
        (beta_2 * cos(2. * 2 * psi) * sinh(2. * 2 * nu)) + (beta_3 * cos(2. * 3 * psi) * sinh(2. * 3 * nu)))
    sigma_prime = 1. - ((2. * 1 * beta_1 * cos(2. * 1 * psi) * cosh(2. * 1 * nu)) +
        (2. * 2 * beta_2 * cos(2. * 2 * psi) * cosh(2. * 2 * nu)) + (2. * 3 * beta_3 * cos(2. * 3 * psi) * cosh(2. * 3 * nu)))
    tau_prime = ((2. * 1 * beta_1 * sin(2. * 1 * psi) * sinh(2. * 1 * nu)) +
        (2. * 2 * beta_2 * sin(2. * 2 * psi) * sinh(2. * 2 * nu)) + (2. * 3 * beta_3 * sin(2. * 3 * psi) * sinh(2. * 3 * nu)))
    chi = asin (sin(psi_prime)/cosh(nu_prime)) 
    phi = chi + (delta_1 * sin(2. * 1 * chi)) + (delta_2 * sin(2. * 2 * chi)) + (delta_3 * sin(2. * 3 * chi))
    lambda_0 = 0
    lambdu = 0 
    k =  0
    gamma = 0
    return None
