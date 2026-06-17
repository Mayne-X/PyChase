"""Renamed variables/functions — Type-2. Same structure, different names."""

def find_max_price(prices):
    most_expensive = 0
    for p in prices:
        if p > most_expensive:
            most_expensive = p
    return most_expensive


def find_min_age(ages):
    youngest = 999
    for a in ages:
        if a < youngest:
            youngest = a
    return youngest
