from itertools import combinations_with_replacement
from math import comb

from armstrong_nums import c_engine

ENGINES = ('python', 'c')
# Keeps requests to a few seconds; the C engine works with 64-bit integers.
MAX_END_RANGE = {'python': 10 ** 15, 'c': 2 ** 64 - 1}


def _is_armstrong_number(number, powers):
    num_str = str(number)
    return sum(powers[digit] for digit in num_str) == number


def _armstrong_numbers_with_digits(digits, low, high):
    """Armstrong numbers with exactly `digits` digits inside [low, high]."""
    powers = {str(d): d ** digits for d in range(10)}

    # Few candidates: checking each number directly is cheaper.
    if high - low + 1 <= comb(digits + 9, 9):
        return [num for num in range(low, high + 1) if _is_armstrong_number(num, powers)]

    # The digit sum doesn't depend on digit order, so try every digit multiset once
    # (e.g. 153, 135, 315... are all the multiset {1, 3, 5}) and check if the sum
    # is made of exactly those digits.
    found = []
    for combo in combinations_with_replacement('0123456789', digits):
        total = sum(powers[digit] for digit in combo)
        if low <= total <= high:
            total_str = str(total)
            if len(total_str) == digits and ''.join(sorted(total_str)) == ''.join(combo):
                found.append(total)
    return sorted(found)


def find_armstrong_numbers_python(start, end):
    armstrong_numbers = []
    for digits in range(len(str(start)), len(str(end)) + 1):
        low = max(start, 10 ** (digits - 1) if digits > 1 else 0)
        high = min(end, 10 ** digits - 1)
        armstrong_numbers.extend(_armstrong_numbers_with_digits(digits, low, high))
    return armstrong_numbers


def find_armstrong_numbers(start, end, engine='python'):
    if engine == 'c':
        return c_engine.find_armstrong_numbers(start, end)
    return find_armstrong_numbers_python(start, end)
