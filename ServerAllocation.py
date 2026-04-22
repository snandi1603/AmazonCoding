import heapq
class Server:
    def __init__(self, server_id=None, class_id=None, cost=0):
        self.server_id = server_id
        self.class_id = class_id
        self.cost = cost
        self.allocated = False
    def getCost(self, time):
        return self.cost*time
    def allocate(self):
        self.allocated = True
    def deallocate(self):
        self.allocated = False

class ServerPool:
    def __init__(self):
        self.tier_free_map = {}
        self.server_map = {}
    def addServer(self, server_id, tier, cost):
        server = Server(server_id, tier, cost)
        if tier not in self.tier_free_map:
            self.tier_free_map[tier] = []
        heapq.heappush(self.tier_free_map[tier], (cost, server_id, server))
    def allocate(self, tier):
        if tier not in self.tier_free_map:
            raise ValueError(f"No idle {tier} servers available")
        if len(self.tier_free_map[tier])==0:
            raise ValueError(f"No idle {tier} servers available")
        _, server_id, server = heapq.heappop(self.tier_free_map[tier])
        self.server_map[server_id] = server
        server.allocate()
        return server_id
    def idleCount(self, tier):
        if tier not in self.tier_free_map:
            return 0
        if len(self.tier_free_map[tier])==0:
            return 0
        return len(self.tier_free_map[tier])
    def getCost(self, server_id, time):
        if server_id not in self.server_map:
            return 0.0
        server = self.server_map[server_id]
        return server.getCost(time)
    def release(self, server_id):
        if server_id not in self.server_map:
            return
        server = self.server_map[server_id]
        server.deallocate()
        tier = server.class_id
        cost = server.cost
        heapq.heappush(self.tier_free_map[tier], (cost, server_id, server))
        del self.server_map[server_id]

# ── Test runner ───────────────────────────────────────────────────────────────

def check(name, actual, expected):
    if isinstance(expected, float):
        ok = abs(actual - expected) < 1e-9
    else:
        ok = actual == expected
    if ok:
        print(f"  PASS  {name}")
    else:
        print(f"  FAIL  {name}")
        print(f"         expected : {expected}")
        print(f"         actual   : {actual}")

def check_raises(name, fn, exc_type):
    try:
        fn()
        print(f"  FAIL  {name} (no exception raised)")
    except exc_type:
        print(f"  PASS  {name}")
    except Exception as e:
        print(f"  FAIL  {name} (wrong exception: {e})")

def test_spec_example():
    print("[1] Spec example")
    pool = ServerPool()
    pool.addServer("i-001", "small", 0.05)
    pool.addServer("i-002", "small", 0.03)
    pool.addServer("i-003", "large", 0.20)
    check("allocate small → cheapest i-002", pool.allocate("small"), "i-002")
    check("idleCount small → 1", pool.idleCount("small"), 1)
    check("getCost i-002 10hrs → 0.30", pool.getCost("i-002", 10), 0.30)
    pool.release("i-002")
    check("idleCount small → 2 after release", pool.idleCount("small"), 2)

def test_allocate_cheapest():
    print("\n[2] Always allocates cheapest")
    pool = ServerPool()
    pool.addServer("A", "medium", 1.00)
    pool.addServer("B", "medium", 0.50)
    pool.addServer("C", "medium", 0.75)
    check("first allocate → B", pool.allocate("medium"), "B")
    check("second allocate → C", pool.allocate("medium"), "C")
    check("third allocate → A", pool.allocate("medium"), "A")

def test_allocate_empty_raises():
    print("\n[3] Allocate from empty pool raises ValueError")
    pool = ServerPool()
    check_raises("empty pool raises", lambda: pool.allocate("small"), ValueError)

def test_allocate_wrong_type_raises():
    print("\n[4] Allocate unavailable type raises ValueError")
    pool = ServerPool()
    pool.addServer("i-001", "large", 0.20)
    check_raises("no small servers raises", lambda: pool.allocate("small"), ValueError)

def test_release_returns_to_pool():
    print("\n[5] Release returns server to idle pool")
    pool = ServerPool()
    pool.addServer("i-001", "small", 0.05)
    pool.allocate("small")
    check("idle after alloc → 0", pool.idleCount("small"), 0)
    pool.release("i-001")
    check("idle after release → 1", pool.idleCount("small"), 1)
    check("can re-allocate", pool.allocate("small"), "i-001")

def test_release_noop_on_idle():
    print("\n[6] Release of non-allocated server is no-op")
    pool = ServerPool()
    pool.addServer("i-001", "small", 0.05)
    pool.release("i-001")
    check("idle count unchanged", pool.idleCount("small"), 1)

def test_release_unknown_noop():
    print("\n[7] Release of unknown instanceId is no-op")
    pool = ServerPool()
    pool.release("ghost")
    check("pool still empty", pool.idleCount("small"), 0)

def test_getcost_allocated():
    print("\n[8] getCost for allocated server")
    pool = ServerPool()
    pool.addServer("i-001", "large", 0.20)
    pool.allocate("large")
    check("getCost 5hrs → 1.00", pool.getCost("i-001", 5), 1.00)
    check("getCost 0hrs → 0.00", pool.getCost("i-001", 0), 0.00)

def test_getcost_not_allocated():
    print("\n[9] getCost for idle/unknown server")
    pool = ServerPool()
    pool.addServer("i-001", "small", 0.05)
    check("getCost idle → 0.0", pool.getCost("i-001", 10), 0.0)
    check("getCost unknown → 0.0", pool.getCost("ghost", 10), 0.0)

def test_cost_preserved_after_release():
    print("\n[10] Cost computed at allocation time")
    pool = ServerPool()
    pool.addServer("i-001", "small", 0.05)
    pool.allocate("small")
    check("getCost before release", pool.getCost("i-001", 10), 0.50)
    pool.release("i-001")
    check("getCost after release → 0.0", pool.getCost("i-001", 10), 0.0)

def test_reallocate_after_release():
    print("\n[11] Re-allocate picks cheapest again")
    pool = ServerPool()
    pool.addServer("i-001", "small", 0.10)
    pool.addServer("i-002", "small", 0.05)
    pool.allocate("small")
    pool.release("i-002")
    check("re-allocate picks i-002", pool.allocate("small"), "i-002")

def test_idle_count_multiple_types():
    print("\n[12] idleCount per type independent")
    pool = ServerPool()
    pool.addServer("s1", "small",  0.05)
    pool.addServer("s2", "small",  0.06)
    pool.addServer("m1", "medium", 0.10)
    pool.addServer("l1", "large",  0.20)
    check("small → 2",  pool.idleCount("small"),  2)
    check("medium → 1", pool.idleCount("medium"), 1)
    check("large → 1",  pool.idleCount("large"),  1)
    check("xlarge → 0", pool.idleCount("xlarge"), 0)

def test_same_cost_tiebreak():
    print("\n[13] Same cost — any valid server")
    pool = ServerPool()
    pool.addServer("A", "small", 0.05)
    pool.addServer("B", "small", 0.05)
    result = pool.allocate("small")
    check("A or B allocated", result in {"A", "B"}, True)
    check("idle → 1", pool.idleCount("small"), 1)

def test_large_hourly_cost():
    print("\n[14] Large hourly cost precision")
    pool = ServerPool()
    pool.addServer("i-001", "xlarge", 9.999)
    pool.allocate("xlarge")
    check("getCost 100hrs", pool.getCost("i-001", 100), 999.9)

def test_allocate_all_then_release_all():
    print("\n[15] Allocate all then release all")
    pool = ServerPool()
    for i in range(5):
        pool.addServer(f"i-{i:03}", "small", 0.01 * (i+1))
    ids = [pool.allocate("small") for _ in range(5)]
    check("idle → 0", pool.idleCount("small"), 0)
    check_raises("raises when empty", lambda: pool.allocate("small"), ValueError)
    for i in ids:
        pool.release(i)
    check("idle → 5 after release", pool.idleCount("small"), 5)

tests = [
    test_spec_example, test_allocate_cheapest,
    test_allocate_empty_raises, test_allocate_wrong_type_raises,
    test_release_returns_to_pool, test_release_noop_on_idle,
    test_release_unknown_noop, test_getcost_allocated,
    test_getcost_not_allocated, test_cost_preserved_after_release,
    test_reallocate_after_release, test_idle_count_multiple_types,
    test_same_cost_tiebreak, test_large_hourly_cost,
    test_allocate_all_then_release_all,
]

print(f"Running {len(tests)} test groups...\n")
for t in tests:
    t()
print("\nDone.")
        