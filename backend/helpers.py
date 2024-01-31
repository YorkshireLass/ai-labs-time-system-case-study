"""
Helpers for backend_main module.
"""


def generate_next(xn=0, yn=0, zn=0, sigma=1, rho=1, beta=1, delta_t=1):
    """
    Generator to calculate next coordinate values.

    Args:
        xn (float)      : Last known x coordinate
        yn (float)      : Last known y coordinate
        zn (float)      : Last known z coordinate

        sigma (float)   : User parameter
        rho (float)     : User parameter
        beta (float)    : User parameter

        delta_t (int)   : User time delta input

    Yields:
        generate_next (tuple) : Tuple of values of coordinates (n,x,y,z) for step n+1.
        >> print([generate_next(x, y, z, sigma, rho, beta, delta_t)])
        [(0,0,0),]
    """
    # formatting values for step n

    # calculating x, y and z for step n+1
    x = xn + ( zn * sigma * (yn - xn) ) * delta_t
    y = yn + ( xn * (rho - zn) - zn * yn ) * delta_t
    z = zn + ( xn * yn - beta * zn ) * delta_t

    # produce x,y,z coordinates
    yield (x, y, z)