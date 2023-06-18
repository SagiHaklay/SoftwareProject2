import mykmeanssp as kmeans
import math
import numpy as np

class Point:
    def __init__(self, data) -> None:
        self.data = data

    def __str__(self) -> str:
        return self.data.__str__()

    def distance(self, other):
        sum = 0
        for j in range(len(self.data)):
            sum += (self.data[j] - other.data[j]) ** 2
        return math.sqrt(sum)
    
    def nearest_center_distance(self, centroids):
        min_dist = self.distance(centroids[0])
        for center in centroids[1:]:
            curr_dist = self.distance(center)
            min_dist = min(min_dist, curr_dist)
        return min_dist
    
def choose_centroid(points, centroids, is_uniform=False):
    # point_matrix = np.array([p.data for p in points])
    rng = np.random.default_rng(0)
    if (is_uniform):
        return rng.choice(points)
    center_dist = [p.nearest_center_distance(centroids) for p in points]
    dsum = sum(center_dist)
    prob = [d / dsum for d in center_dist]
    return rng.choice(points, p=prob)
    
def kmeans_pp(points, k):
    centroids = []
    non_centroids = points[:]
    new_center = choose_centroid(non_centroids, centroids, True)
    non_centroids.remove(new_center)
    centroids.append(new_center)
    while len(centroids) < k:
        new_center = choose_centroid(non_centroids, centroids)
        non_centroids.remove(new_center)
        centroids.append(new_center)
    return centroids
    
def read_from_file(fname):
    list_of_points = []
    f = open(fname, "r")
    for line in f:
        current_line = line.split(",")
        current_line = [float(x) for x in current_line]
        list_of_points.append(current_line)
    return list_of_points
datapoints = read_from_file('tests/input_1.txt')
centroids = kmeans_pp(datapoints, 3)
centroids = kmeans.fit(datapoints, centroids, 600, 0.001)
for cent in centroids:
    data = [float("%.4f" % i) for i in cent]
    print(*data, sep=",")