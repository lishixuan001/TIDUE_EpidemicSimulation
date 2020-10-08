import random

def if_success(rate):
    return random.choices([True, False], weights=(rate, 1-rate), k=1)

def get_result(death_rate, recov_rate):
    """
    1: Death
    0: Recover
    -1: Unchanged
    """
    return random.choices([1, 0, -1], weights=(death_rate, recov_rate, 1-death_rate-recov_rate), k=1)
