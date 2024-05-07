




#Basic algorithm assigning seats to groups based off of their x coordinate (left to right)
def assign_seats(capacities, seat_list):
    seats_sorted = [s.id for s in sorted(seat_list, key=lambda s: s.x)]
    groups = []
    for i,j in enumerate(capacities):
        groups.extend([i for _ in range(j)])
    return list(zip(groups, seats_sorted))