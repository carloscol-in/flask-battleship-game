"""Utilities functions."""

# Libraries
import string
import random


def id_generator(size=4, chars=string.ascii_letters + string.digits):
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))