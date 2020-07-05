from utils.haversine_distance import haversine_distance

class Point:
    def __init__(self, lon, lat):
        self.lon = lon
        self.lat = lat

    def closest_point(self, points):
        distance = -1
        closest_point = None

        for point in points:
            new_dist = haversine_distance(self.lon, self.lat, point.lon, point.lat)

            if distance == -1 or new_dist < distance:
                distance = new_dist
                closest_point = point

        return closest_point
