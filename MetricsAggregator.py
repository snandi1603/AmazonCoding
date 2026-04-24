from collections import defaultdict
import statistics
import heapq
import math
class Stats:
    def __init__(self, min, max, avg, count):
        self.min = min
        self.max = max
        self.avg = avg
        self.count = count
class MetricsAggregator:
    def __init__(self):
        self.hmap = defaultdict(list)
    def binsearch(self, name, target, lower_bound):
        #lower bound: Looking for the leftmost index which is strictly >= target
        #upper bound: Looking for the leftmost index which is strictly > target
        lo = 0
        hi = len(self.hmap[name])
        while lo<hi:
            mid = (lo+hi)//2
            if lower_bound:
                if self.hmap[name][mid][0]>=target:
                    hi = mid
                else:
                    lo = mid+1
            else:
                if self.hmap[name][mid][0]>target:
                    hi = mid
                else:
                    lo = mid+1
        return lo
    def record(self, metric_name, value, timestamp):
        self.hmap[metric_name].append((timestamp, value))
    def getStats(self, name, start, end):
        lo = self.binsearch(name, start, True)
        hi = self.binsearch(name, end, False)
        arr = [a[1] for a in self.hmap[name][lo:hi]]
        if arr is None or len(arr)==0:
            return None
        return Stats(min(arr), max(arr), sum(arr)/len(arr), len(arr))
    def getTopN(self, n, startTime, endTime):
        max_heap = []
        for name, _ in self.hmap.items():
            lo = self.binsearch(name, startTime, True)
            hi = self.binsearch(name, endTime, False)
            arr = [a[1] for a in self.hmap[name][lo:hi]]
            if arr:
                avg = sum(arr)/len(arr)
                heapq.heappush(max_heap, (-avg, name))
        res = []
        while n and max_heap:
            _, s = heapq.heappop(max_heap)
            res.append(s)
            n-=1
        return res
    def getAnomaly(self, metricName, windowSize, threshold):
        i = 0
        j = 0 #windowSize
        res = []
        def find_anal(i, j):
            mean = sum(x[1] for x in self.hmap[metricName][i:j])/len(self.hmap[metricName][i:j])
            std = sum((x[1]-mean)**2 for x in self.hmap[metricName][i:j])/len(self.hmap[metricName][i:j])
            std = math.sqrt(std)
            x = self.hmap[metricName][i:j][-1]
            if abs(mean-x[1]) > threshold*std:
                res.append(x[0])
        for j in range(windowSize-1, len(self.hmap[metricName])):
            find_anal(j-windowSize+1,j+1)
        return res
def check(name, got, expected):
    if isinstance(expected, float):
        ok = abs(got - expected) < 1e-6
    elif isinstance(got, Stats) and isinstance(expected, Stats):
        ok = (got.min == expected.min and got.max == expected.max and
              abs(got.avg - expected.avg) < 1e-6 and got.count == expected.count)
    else:
        ok = got == expected
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        print(f"       got      {got}")
        print(f"       expected {expected}")

# T1: Spec example
agg = MetricsAggregator()
agg.record("cpu", 80, 100); agg.record("cpu", 90, 200); agg.record("cpu", 70, 300)
agg.record("mem", 60, 100)
check("T1a getStats cpu",          agg.getStats("cpu", 100, 300), Stats(70, 90, 80.0, 3))
check("T1b getTopN",               agg.getTopN(1, 100, 300), ["cpu"])
check("T1c anomaly detects 70",    agg.getAnomaly("cpu", 3, 1.0), [300])
check("T1d no anomaly threshold=2",agg.getAnomaly("cpu", 3, 2.0), [])

# T2: getStats boundary inclusion
agg = MetricsAggregator()
agg.record("x", 10, 100); agg.record("x", 20, 200); agg.record("x", 30, 300)
check("T2a start boundary", agg.getStats("x", 100, 100), Stats(10, 10, 10.0, 1))
check("T2b end boundary",   agg.getStats("x", 300, 300), Stats(30, 30, 30.0, 1))
check("T2c full range",     agg.getStats("x", 100, 300), Stats(10, 30, 20.0, 3))
check("T2d partial range",  agg.getStats("x", 150, 300), Stats(20, 30, 25.0, 2))

# T3: getStats empty range
agg = MetricsAggregator()
agg.record("x", 10, 100)
check("T3a no points in range", agg.getStats("x", 200, 300), None)
check("T3b before all data",    agg.getStats("x", 0, 50),    None)

# T4: Same timestamp multiple records
agg = MetricsAggregator()
agg.record("x", 10, 100); agg.record("x", 20, 100); agg.record("x", 30, 100)
check("T4 same timestamp", agg.getStats("x", 100, 100), Stats(10, 30, 20.0, 3))

# T5: Single data point
agg = MetricsAggregator()
agg.record("x", 42, 100)
check("T5 single point", agg.getStats("x", 100, 100), Stats(42, 42, 42.0, 1))

# T6: getTopN ranking
agg = MetricsAggregator()
for ts in [100, 200, 300]:
    agg.record("cpu", 90, ts); agg.record("mem", 50, ts); agg.record("disk", 70, ts)
check("T6a top 1", agg.getTopN(1, 100, 300), ["cpu"])
check("T6b top 2", agg.getTopN(2, 100, 300), ["cpu", "disk"])
check("T6c top 3", agg.getTopN(3, 100, 300), ["cpu", "disk", "mem"])

# T7: getTopN respects time range
agg = MetricsAggregator()
agg.record("cpu", 100, 100); agg.record("cpu", 10, 200)
agg.record("mem", 50, 100);  agg.record("mem", 50, 200)
check("T7 topN time range", agg.getTopN(1, 200, 200), ["mem"])

# T8: getTopN n > number of metrics
agg = MetricsAggregator()
agg.record("a", 10, 100); agg.record("b", 20, 100)
check("T8 n > metrics", len(agg.getTopN(10, 100, 100)), 2)

# T9: getTopN excludes metrics with no data in range
agg = MetricsAggregator()
agg.record("cpu", 80, 100); agg.record("mem", 60, 500)
check("T9 exclude out-of-range metric", agg.getTopN(2, 100, 200), ["cpu"])

# T10: getAnomaly spike detected
agg = MetricsAggregator()
for v, ts in [(10,100),(10,200),(10,300),(10,400),(100,500)]:
    agg.record("cpu", v, ts)
check("T10 spike at 500", 500 in agg.getAnomaly("cpu", 5, 1.0), True)

# T11: getAnomaly no anomaly
agg = MetricsAggregator()
for v, ts in [(10,100),(11,200),(10,300),(11,400),(10,500)]:
    agg.record("cpu", v, ts)
check("T11 no anomaly", agg.getAnomaly("cpu", 3, 2.0), [])

# T12: getAnomaly mid-series spike
agg = MetricsAggregator()
for v, ts in [(10,100),(10,200),(50,300),(10,400),(10,500)]:
    agg.record("x", v, ts)
result = agg.getAnomaly("x", 3, 1.0)
check("T12a spike at 300",       300 in result, True)
check("T12b no false positives", 100 not in result and 500 not in result, True)

# T13: getAnomaly windowSize=1 never anomalous (std=0)
agg = MetricsAggregator()
for v, ts in [(10,100),(999,200),(10,300)]: agg.record("x", v, ts)
check("T13 windowSize=1 no anomaly", agg.getAnomaly("x", 1, 1.0), [])

# T14: Multiple metrics independent
agg = MetricsAggregator()
agg.record("a", 10, 100); agg.record("a", 20, 200)
agg.record("b", 50, 100); agg.record("b", 60, 200)
check("T14a stats a", agg.getStats("a", 100, 200), Stats(10, 20, 15.0, 2))
check("T14b stats b", agg.getStats("b", 100, 200), Stats(50, 60, 55.0, 2))

# T15: getStats count and avg in subrange
agg = MetricsAggregator()
for v, ts in [(1,100),(2,200),(3,300),(4,400),(5,500)]: agg.record("x", v, ts)
check("T15a count in range", agg.getStats("x", 200, 400).count, 3)
check("T15b avg in range",   agg.getStats("x", 200, 400).avg,   3.0)
            