import mykmeanssp as kmeans
import math
import numpy as np
import pandas as pd
import sys

class Point:
    def __init__(self, data, index) -> None:
        self.data = data
        self.index = index

    def __str__(self) -> str:
        return self.data.__str__()
    
    def __eq__(self, __value: object) -> bool:
        for i in range(len(self.data)):
            if self.data[i] != __value.data[i]:
                return False
        return True

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
    
    def match_cluster(self, list_of_clusters):
        min_distance = self.distance(list_of_clusters[0].centroid)
        nearest_cluster = list_of_clusters[0]
        for cur_cluster in list_of_clusters:
            distance = self.distance(cur_cluster.centroid)
            if distance < min_distance:
                min_distance = distance
                nearest_cluster = cur_cluster
        return nearest_cluster
    
class Cluster:
    def __init__(self, centroid) -> None:
        self.centroid = centroid
        self.points = []

    def __str__(self) -> str:
        return self.centroid.__str__()

    def add_point(self, point):
        self.points.append(point)

    def clear(self):
        self.points.clear()

    def update_centroid(self):
        mean = [0] * len(self.centroid.data)
        for i in range(len(self.centroid.data)):
            print(mean[i])
            for p in self.points:
                mean[i] += p.data[i]
            print(mean[i])
            mean[i] /= len(self.points)
            print(mean[i])
        new_centroid = Point(mean, self.centroid.index)
        converged = new_centroid.distance(self.centroid) < eps
        self.centroid = new_centroid
        return converged
    
def choose_centroid(points, centroids, is_uniform=False):
    # point_matrix = np.array([p.data for p in points])
    # rng = np.random.default_rng(0)
    if (is_uniform):
        return np.random.choice(points)
    center_dist = [p.nearest_center_distance(centroids) for p in points]
    dsum = sum(center_dist)
    prob = [d / dsum for d in center_dist]
    return np.random.choice(points, p=prob)
    
def kmeans_pp(points, k):
    np.random.seed(0)
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

def read_files(file1, file2):
    df1 = pd.read_csv(file1, header=None)
    df2 = pd.read_csv(file2, header=None)
    merged_df = pd.merge(df1, df2, on=0)
    sorted_df = merged_df.sort_values(0)
    #print(sorted_df.head(5))
    return [Point(series.to_list()[1:], series.get(0)) for index, series in sorted_df.iterrows()]

def k_error():
    print("Invalid number of clusters!")
    sys.exit()


def iter_error():
    print("Invalid maximum iteration!")
    sys.exit()


def both_errors():
    print("Invalid number of clusters!")
    print("Invalid maximum iteration!")
    sys.exit()

points = read_files(sys.argv[-2], sys.argv[-1])
args_len = len(sys.argv)
if args_len < 5:
    k_error()
# if args_len > 4:
# need to ask what to return
if args_len == 5:
    if not sys.argv[1].isdigit() or int(sys.argv[1]) <= 1 or int(sys.argv[1]) >= len(points):
        k_error()
else:  # args_len == 4
    if (not sys.argv[1].isdigit()) and (not sys.argv[2].isdigit()):
        both_errors()
    # there might be only one that isn't a number
    if not sys.argv[1].isdigit() and (int(sys.argv[2]) <= 1 or int(sys.argv[2]) >= 1000):
        both_errors()
    if not sys.argv[2].isdigit() and (int(sys.argv[1]) <= 1 or int(sys.argv[1]) >= len(points)):
        both_errors()

k = int(sys.argv[1])
iter = 300 if args_len == 5 else int(sys.argv[2])

if (k <= 1 or k >= len(points)) and (iter <= 1 or iter >= 1000):
    both_errors()
if k <= 1 or k >= len(points):
    k_error()
if iter <= 1 or iter >= 1000:
    iter_error()
eps = int(sys.argv[-3])
centroids = kmeans_pp(points, k)
indicies = [("%d" % cent.index) for cent in centroids]
print(*indicies, sep=',')
arr_centroids = [p.data for p in centroids]
datapoints = [p.data for p in points]
centroids = kmeans.fit(datapoints, arr_centroids, iter, eps)
for cent in centroids:
    data = [float("%.4f" % i) for i in cent]
    print(*data, sep=",")