from point.point import Point

class NamedPoint(Point):
    def __init__(self, name, lon, lat):
        Point.__init__(self, lon, lat)
        self.name = name
