from collections import defaultdict

import numpy as np
from scipy.spatial.distance import pdist, euclidean

from app.models import Booking

metrics = {"euclidean": euclidean}



def evaluate_assignment(bookings, metric):
    depts = group_bookings_by_department(bookings)
    curr_sum = 0.0
    for dept, bks in depts.items():
        coords = np.array([(b.seat.x, b.seat.y) for b in bks])
        curr_sum += pdist(coords, metric).sum()
    return curr_sum

def group_bookings_by_department(bookings: list[Booking]):
    depts = defaultdict(list)
    for booking in bookings:
        depts[booking.owner.department].append(booking)
    return depts

