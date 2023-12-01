import math

from whyfp.integration import pi_approxs
from whyfp.util import second


def test_pi_approxs():
    pi = second(pi_approxs())
    assert math.isclose(pi, math.pi, abs_tol=1e-5)


def test_easy_integrate():
    pass


def test_integrate():
    pass


def test_within_integrate():
    pass
