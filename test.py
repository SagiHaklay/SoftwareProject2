import mykmeanssp as kmeans


def read_from_file(fname):
    list_of_points = []
    f = open(fname, "r")
    for line in f:
        current_line = line.split(",")
        current_line = [float(x) for x in current_line]
        list_of_points.append(current_line)
    return list_of_points
datapoints = read_from_file('tests/input_1.txt')
centroids = datapoints[:3]
centroids = kmeans.fit(datapoints, centroids, 600, 0.001)
for cent in centroids:
    data = [float("%.4f" % i) for i in cent]
    print(*data, sep=",")