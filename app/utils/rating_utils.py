from collections import namedtuple


def calculate_rating(actual_points: float, bill_sum: float, old_rating: namedtuple, new_rating: namedtuple) -> tuple:
    rating_points: float = float(round(actual_points)) + (new_rating.bill * new_rating[0])
    rating_avg: float = rating_points/float(bill_sum)
    return rating_points, rating_avg
