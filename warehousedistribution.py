class LogData:
    def __init__(self, start_idx=None, numParts=None):
        self.start_idx = start_idx
        self.numParts = numParts
        self.parts = set()
    def addPart(self, part_num):
        if len(self.parts) >= self.numParts:
            return False
        self.parts.add(part_num)
        return True
    def getNumParts(self):
        return len(self.parts)
        
class WarehouseAllocator:
    def __init__(self, capacity=0):
        self.capacity = capacity
        self.free_idx = 0
        self.hmap = {}
    def getFreeIdx(self, length=0):
        if self.free_idx+length > self.capacity:
            return None
        freeIdx = self.free_idx
        self.free_idx+=length
        return freeIdx
    def addLog(self, logId=None, numParts=0):
        if not logId or not numParts:
            return False
        if logId in self.hmap:
            return False
        start_idx = self.getFreeIdx(length=numParts)
        if start_idx is not None:
            self.hmap[logId] = LogData(start_idx=start_idx, numParts=numParts)
            return True
        return False
    def storePart(self, logId=None, part_num=None):
        if logId not in self.hmap:
            return False
        return self.hmap[logId].addPart(part_num)
    def canFulfillOrder(self, logId=None, partsNeeded=0):
        if logId not in self.hmap:
            return False
        return partsNeeded<=self.hmap[logId].getNumParts()
    def getStorageReport(self):
        ret = {}
        for k,v in self.hmap.items():
            num_parts = v.getNumParts()
            if num_parts:
                ret[k] = num_parts
        return ret


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
    wa = WarehouseAllocator(capacity=10)
    wa.addLog("LOG1", numParts=5)
    wa.addLog("LOG2", numParts=3)
    wa.storePart("LOG1", 1)
    wa.storePart("LOG1", 2)
    wa.storePart("LOG2", 1)
    check("canFulfillOrder LOG1 2 → True",  wa.canFulfillOrder("LOG1", 2), True)
    check("canFulfillOrder LOG1 3 → False", wa.canFulfillOrder("LOG1", 3), False)
    check("getStorageReport", wa.getStorageReport(), {"LOG1": 2, "LOG2": 1})

def test_duplicate_store():
    print("\n[2] Duplicate storePart is no-op")
    wa = WarehouseAllocator(capacity=10)
    wa.addLog("A", 3)
    wa.storePart("A", 1)
    wa.storePart("A", 1)
    wa.storePart("A", 1)
    check("stored count is 1 not 3", wa.getStorageReport(), {"A": 1})

def test_fulfill_no_parts_stored():
    print("\n[3] canFulfillOrder no parts stored")
    wa = WarehouseAllocator(capacity=10)
    wa.addLog("A", 5)
    check("no parts stored → False", wa.canFulfillOrder("A", 1), False)

def test_fulfill_unknown_log():
    print("\n[4] canFulfillOrder unknown log")
    wa = WarehouseAllocator(capacity=10)
    check("unknown log → False", wa.canFulfillOrder("GHOST", 1), False)

def test_report_excludes_empty_logs():
    print("\n[5] getStorageReport excludes logs with 0 stored parts")
    wa = WarehouseAllocator(capacity=10)
    wa.addLog("A", 3)
    wa.addLog("B", 3)
    wa.storePart("A", 1)
    check("only A in report", wa.getStorageReport(), {"A": 1})

def test_report_empty():
    print("\n[6] getStorageReport all empty")
    wa = WarehouseAllocator(capacity=10)
    wa.addLog("A", 3)
    check("empty report → {}", wa.getStorageReport(), {})

def test_capacity_overflow():
    print("\n[7] addLog exceeds capacity")
    wa = WarehouseAllocator(capacity=5)
    wa.addLog("A", 3)
    result = wa.addLog("B", 5)
    check("addLog B fails → False", result, False)
    check("B not in report", wa.getStorageReport(), {})

def test_exact_capacity():
    print("\n[8] addLog fills exactly to capacity")
    wa = WarehouseAllocator(capacity=6)
    wa.addLog("A", 3)
    result = wa.addLog("B", 3)
    check("addLog B succeeds", result, True)
    wa.storePart("B", 1)
    check("B stored successfully", wa.getStorageReport(), {"B": 1})

def test_store_unregistered_log():
    print("\n[9] storePart on unregistered log")
    wa = WarehouseAllocator(capacity=10)
    result = wa.storePart("GHOST", 1)
    check("storePart unregistered → False", result, False)
    check("report still empty", wa.getStorageReport(), {})

def test_duplicate_addLog():
    print("\n[10] Duplicate addLog is no-op")
    wa = WarehouseAllocator(capacity=10)
    wa.addLog("A", 3)
    result = wa.addLog("A", 3)
    check("second addLog returns False", result, False)
    wa.storePart("A", 1)
    check("only 3 slots allocated not 6", wa.getStorageReport(), {"A": 1})

def test_fulfill_exact():
    print("\n[11] canFulfillOrder exact parts match")
    wa = WarehouseAllocator(capacity=10)
    wa.addLog("A", 3)
    wa.storePart("A", 1)
    wa.storePart("A", 2)
    wa.storePart("A", 3)
    check("exactly 3 stored, need 3 → True", wa.canFulfillOrder("A", 3), True)
    check("need 4 → False", wa.canFulfillOrder("A", 4), False)

def test_multiple_logs():
    print("\n[12] Multiple logs full flow")
    wa = WarehouseAllocator(capacity=20)
    wa.addLog("X", 4)
    wa.addLog("Y", 4)
    wa.addLog("Z", 4)
    wa.storePart("X", 1); wa.storePart("X", 2)
    wa.storePart("Y", 1)
    wa.storePart("Z", 1); wa.storePart("Z", 2); wa.storePart("Z", 3)
    check("X: 2 parts", wa.canFulfillOrder("X", 2), True)
    check("Y: 1 part",  wa.canFulfillOrder("Y", 1), True)
    check("Z: 3 parts", wa.canFulfillOrder("Z", 3), True)
    check("Z: 4 → False", wa.canFulfillOrder("Z", 4), False)
    check("full report", wa.getStorageReport(), {"X": 2, "Y": 1, "Z": 3})

def test_single_slot():
    print("\n[13] Single slot capacity")
    wa = WarehouseAllocator(capacity=1)
    wa.addLog("A", 1)
    result = wa.addLog("B", 1)
    check("B fails, no space", result, False)
    wa.storePart("A", 1)
    check("A stored", wa.getStorageReport(), {"A": 1})

tests = [
    test_spec_example, test_duplicate_store,
    test_fulfill_no_parts_stored, test_fulfill_unknown_log,
    test_report_excludes_empty_logs, test_report_empty,
    test_capacity_overflow, test_exact_capacity,
    test_store_unregistered_log, test_duplicate_addLog,
    test_fulfill_exact, test_multiple_logs, test_single_slot,
]

print(f"Running {len(tests)} test groups...\n")
for t in tests:
    t()
print("\nDone.")
        