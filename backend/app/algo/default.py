from scipy.spatial.distance import pdist, euclidean

import app.algo.k_furthest as k_furthest
import app.algo.simple as simple

algorithms = {"k_furthest": k_furthest.assign_seats,
              "simple": simple.assign_seats}