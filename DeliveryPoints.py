import math
from collections import defaultdict
class Point:
    def __init__(self, point_id="", x=0, y=0):
        self.point_id = point_id
        self.x = x
        self.y = y
    def distance(self, x, y):
        return math.sqrt((x-self.x)*(x-self.x) + (y-self.y)*(y-self.y))

class Zone:
    def __init__(self, zone_id=None, points=None):
        self.zone_id = zone_id
        self.points = points if points is not None else []
        self.centroid = None
    
    def addPoint(self, point = None):
        self.points.append(point)
        self.centroid = Point(point_id = "centroid", x=sum([p.x for p in self.points])//len(self.points), y=sum([p.y for p in self.points])//len(self.points))
    
    def getPointsStr(self):
        sp = [p for p in self.points]
        sp.sort(key = lambda y: y.distance(self.centroid.x, self.centroid.y))
        return [a.point_id for a in sp]

    def getPoints(self):
        sp = [p for p in self.points]
        sp.sort(key = lambda y: y.distance(self.centroid.x, self.centroid.y))
        return sp
    
    def nearestPoint(self, p):
        min_dist = float("inf")
        nearest_point = None
        for pc in self.points:
            d = pc.distance(p.x, p.y)
            if min_dist > d:
                min_dist = d
                nearest_point = pc.point_id
        return (nearest_point, min_dist)

class DeliveryNetwork:
    def __init__(self):
        self.hmap = {}
    def addPoint(self, point_id, x, y, zone_id):
        if zone_id not in self.hmap:
            self.hmap[zone_id] = Zone(zone_id=zone_id)
        self.hmap[zone_id].addPoint(Point(point_id, x, y))
    def getZonePoints(self, zone_id):
        if zone_id in self.hmap:
            return self.hmap[zone_id].getPointsStr()
        return []
    def nearestPoint(self, x, y):
        pin = Point("target", x, y)
        nearest_point = None
        min_dist = float("inf")
        for _, v in self.hmap.items():
            np, md = v.nearestPoint(pin)
            if min_dist>md:
                min_dist = md
                nearest_point = np
        return nearest_point
    def mergeZones(self, zone_id1, zone_id2, zone_id3):
        if zone_id1 not in self.hmap or zone_id2 not in self.hmap:
            return False
        zone1 = self.hmap[zone_id1]
        zone2 = self.hmap[zone_id2]
        zone3 = Zone(zone_id=zone_id3)
        for p in zone1.getPoints()+zone2.getPoints():
            zone3.addPoint(p)
        self.hmap[zone_id3] = zone3
        del self.hmap[zone_id1]
        del self.hmap[zone_id2]


# ── Test runner ───────────────────────────────────────────────────────────────

def check(name, actual, expected):
    if actual == expected:
        print(f"  PASS  {name}")
    else:
        print(f"  FAIL  {name}")
        print(f"         expected : {expected}")
        print(f"         actual   : {actual}")

def test_spec_example():
    print("[1] Spec example")
    net = DeliveryNetwork()
    net.addPoint("P1", 0, 0, "Z1")
    net.addPoint("P2", 1, 1, "Z1")
    net.addPoint("P3", 5, 5, "Z2")
    result = net.getZonePoints("Z1")
    check("Z1 has P1 and P2", set(result), {"P1", "P2"})
    check("nearestPoint(4,4) → P3", net.nearestPoint(4, 4), "P3")
    check("nearestPoint(0,0) → P1", net.nearestPoint(0, 0), "P1")

def test_single_point_zone():
    print("\n[2] Single point zone")
    net = DeliveryNetwork()
    net.addPoint("A", 3, 4, "Z1")
    check("getZonePoints Z1", net.getZonePoints("Z1"), ["A"])
    check("nearestPoint(0,0) → A", net.nearestPoint(0, 0), "A")

def test_zone_points_sorted_by_centroid_distance():
    print("\n[3] Zone points sorted by centroid distance")
    net = DeliveryNetwork()
    net.addPoint("Far",  4, 4, "Z1")
    net.addPoint("Mid",  3, 2, "Z1")
    net.addPoint("Near", 2, 2, "Z1")
    result = net.getZonePoints("Z1")
    check("closest to centroid is first", result[0], "Mid")
    check("farthest from centroid is last", result[-1], "Far")

def test_empty_zone():
    print("\n[4] Empty zone")
    net = DeliveryNetwork()
    check("getZonePoints empty zone → []", net.getZonePoints("Z99"), [])

def test_nearest_point_exact_match():
    print("\n[5] nearestPoint exact coordinate match")
    net = DeliveryNetwork()
    net.addPoint("P1", 1, 1, "Z1")
    net.addPoint("P2", 5, 5, "Z1")
    check("exact match P1", net.nearestPoint(1, 1), "P1")
    check("exact match P2", net.nearestPoint(5, 5), "P2")

def test_nearest_point_tiebreak():
    print("\n[6] nearestPoint equidistant points")
    net = DeliveryNetwork()
    net.addPoint("P1", -1, 0, "Z1")
    net.addPoint("P2",  1, 0, "Z1")
    result = net.nearestPoint(0, 0)
    check("one of the equidistant points returned", result in {"P1", "P2"}, True)

def test_nearest_across_zones():
    print("\n[7] nearestPoint searches across all zones")
    net = DeliveryNetwork()
    net.addPoint("A", 0, 0, "Z1")
    net.addPoint("B", 10, 10, "Z2")
    net.addPoint("C", 5, 5, "Z3")
    check("nearest to (4,4) is C", net.nearestPoint(4, 4), "C")
    check("nearest to (9,9) is B", net.nearestPoint(9, 9), "B")
    check("nearest to (1,1) is A", net.nearestPoint(1, 1), "A")

def test_merge_zones_basic():
    print("\n[8] mergeZones basic")
    net = DeliveryNetwork()
    net.addPoint("P1", 0, 0, "Z1")
    net.addPoint("P2", 1, 1, "Z1")
    net.addPoint("P3", 5, 5, "Z2")
    net.mergeZones("Z1", "Z2", "Z3")
    result = net.getZonePoints("Z3")
    check("merged zone has all 3 points", set(result), {"P1", "P2", "P3"})
    check("Z1 no longer exists", net.getZonePoints("Z1"), [])
    check("Z2 no longer exists", net.getZonePoints("Z2"), [])

def test_merge_zones_centroid_updates():
    print("\n[9] mergeZones centroid recalculates")
    net = DeliveryNetwork()
    net.addPoint("A", 0, 0, "Z1")
    net.addPoint("B", 4, 0, "Z2")
    net.mergeZones("Z1", "Z2", "ZM")
    result = net.getZonePoints("ZM")
    check("merged zone has A and B", set(result), {"A", "B"})

def test_nearest_empty_network():
    print("\n[10] nearestPoint on empty network")
    net = DeliveryNetwork()
    check("empty network → None", net.nearestPoint(0, 0), None)

def test_add_multiple_zones():
    print("\n[11] Multiple zones independent")
    net = DeliveryNetwork()
    net.addPoint("A", 0, 0, "Z1")
    net.addPoint("B", 1, 0, "Z1")
    net.addPoint("C", 10, 0, "Z2")
    net.addPoint("D", 11, 0, "Z2")
    check("Z1 points", set(net.getZonePoints("Z1")), {"A", "B"})
    check("Z2 points", set(net.getZonePoints("Z2")), {"C", "D"})

def test_merge_then_nearest():
    print("\n[12] nearestPoint after merge")
    net = DeliveryNetwork()
    net.addPoint("P1", 0, 0, "Z1")
    net.addPoint("P2", 10, 10, "Z2")
    net.mergeZones("Z1", "Z2", "ZM")
    check("nearest to (1,1) still P1", net.nearestPoint(1, 1), "P1")
    check("nearest to (9,9) still P2", net.nearestPoint(9, 9), "P2")

def test_negative_coordinates():
    print("\n[13] Negative coordinates")
    net = DeliveryNetwork()
    net.addPoint("P1", -5, -5, "Z1")
    net.addPoint("P2",  5,  5, "Z1")
    check("nearest to (-4,-4) is P1", net.nearestPoint(-4, -4), "P1")
    check("nearest to (4,4) is P2",   net.nearestPoint(4, 4),   "P2")

def test_large_coordinates():
    print("\n[14] Large coordinates")
    net = DeliveryNetwork()
    net.addPoint("Far",  1000, 1000, "Z1")
    net.addPoint("Near", 1,    1,    "Z1")
    check("nearest to (0,0) is Near", net.nearestPoint(0, 0), "Near")

tests = [
    test_spec_example, test_single_point_zone,
    test_zone_points_sorted_by_centroid_distance, test_empty_zone,
    test_nearest_point_exact_match, test_nearest_point_tiebreak,
    test_nearest_across_zones, test_merge_zones_basic,
    test_merge_zones_centroid_updates, test_nearest_empty_network,
    test_add_multiple_zones, test_merge_then_nearest,
    test_negative_coordinates, test_large_coordinates,
]

print(f"Running {len(tests)} test groups...\n")
for t in tests:
    t()
print("\nDone.")