import numpy as np

import app.algo.util as util
from app.config import ALGO_METRIC

#Picks farthest point from center of point set
#Outputs a single point and the remaining points that weren't chosen
def startpoint(points, left=np.array([-1,1]), right=np.array([1,-1])):
    a = right-left
    b = left-points
    d = np.abs(np.cross(a, b)/np.linalg.norm(a))
    index = np.argmax(d)
    out = points[index]

    points = np.delete(points, index, axis=0)
    return out, points, index

#Outputs k points that are chosen to be as far from each other as possible
#Output as a list of those points and the remaining points that weren't chosen
def incremental_farthest_search(points, k, ids):
    assert(points.shape[0]>=k)
    remaining_points = points[:]
    remaining_ids = ids
    one, remaining_points, index = startpoint(remaining_points)
    solution_ids = [remaining_ids[index]]
    remaining_ids.pop(index)
    solution_set = [one]
    #Each iteration of for loop picks one point
    for _ in range(k-1):
        distances = [metric(p, solution_set[0]) for p in remaining_points]
        for i, p in enumerate(remaining_points):
            for _, s in enumerate(solution_set):
                distances[i] = min(distances[i], metric(p, s))
        inx = distances.index(max(distances))
        solution_set.append(remaining_points[inx])
        solution_ids.append(remaining_ids[inx])
        remaining_points = np.delete(remaining_points, inx, axis=0)
        remaining_ids.pop(inx)
    return solution_set, solution_ids, remaining_points, remaining_ids

#Distance between two points
metric = util.metrics[ALGO_METRIC]

def k_furthest_points(starters, starter_ids, points, ids, numbers):
    remaining_points = points
    remaining_ids = ids
    number_of_sets = len(numbers)
    number_of_points = sum(numbers)
    sorted_capacities = sorted(numbers, reverse=True)
    max_capacities = [max(numbers) for _ in range(number_of_sets)]
    number_sofar = [1 for _ in range(number_of_sets)]
    available_sets = [i for i in range(number_of_sets)]
    remaining_below = [number_of_sets for _ in range(number_of_sets)]
    final_set = np.zeros((number_of_points, 3))
    final_ids = starter_ids

    for i in range(number_of_sets):
        final_set[i] = [starters[i][0], starters[i][1], i]
    for i in range(sorted_capacities.count(1)):
        max_capacities[i] = 1
    slot = number_of_sets

    while slot < number_of_points:
        to_remove = []
        for l in available_sets:
            if number_sofar[l] == max_capacities[l]:
                to_remove.append(l)
                print(l)
        available_sets = [e for e in available_sets if e not in to_remove]

        distance_best = metric(remaining_points[0], starters[available_sets[0]])
        infopoint = 0
        infoset = available_sets[0]
        for i, p in enumerate(remaining_points):
            for s in available_sets:
                if metric(p, starters[s]) < distance_best:
                    distance_best = metric(p,starters[s])
                    infopoint = i
                    infoset = s
        final_set[slot] = [remaining_points[infopoint][0], remaining_points[infopoint][1], infoset]
        final_ids.append(remaining_ids[infopoint])
        remaining_points = np.delete(remaining_points, infopoint, axis=0)
        number_sofar[infoset] = number_sofar[infoset] + 1
        for k in range(number_of_sets):
            if number_sofar[infoset] == sorted_capacities[k] + 1:
                remaining_below[k] = remaining_below[k] - 1
                if remaining_below[k] == number_of_sets - k:
                    for l in available_sets:
                        if number_sofar[l] <= sorted_capacities[k] and max_capacities[l] >= sorted_capacities[k]:
                            max_capacities[l] = sorted_capacities[k]
        slot += 1
    return final_set, final_ids
    
#Basic algorithm assigning seats to groups based off of their x coordinate (left to right)
def simple_assign(numbers, points):
    assignments = []
    for i in range(len(numbers)):
        assignments.extend([i for _ in range(numbers[i])])
    assignments = np.array([assignments])
    points = points[points[:, 0].argsort()]
    points = np.concatenate((points, assignments.T), axis=1)
    return points

# Inputs a list of group sizes and seats
# Outputs a list of seats with a number attached corresponding to the group 
# (List of pairs (d, sid) where d is the department and sid is the seat_id)
def assign_seats(capacities, seat_list):
    point_list, id_list = convert_from_seats(seat_list)
    starters, starter_ids, remaining_points, remaining_ids = incremental_farthest_search(point_list, len(capacities), id_list)
    seated, final_ids = k_furthest_points(starters, starter_ids, remaining_points, remaining_ids, capacities)
    output = []
    for i in range(sum(capacities)):
        output.append([int(seated[i][2]), final_ids[i]])
    return output

def convert_from_seats(list_of_seats):
    point_list = []
    id_list = []
    for item in list_of_seats:
        point_list.append([item.x, item.y])
        id_list.append(item.id)
    return(np.array(point_list), id_list)
        