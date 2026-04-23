from collections import deque
class UnregisteredUserError(Exception):
    pass
class UserRl:
    def __init__(self, name, maxRequests, windowSeconds):
        self.maxRequests = maxRequests
        self.windowSeconds = windowSeconds
        self.name = name
        self.rl = deque()
    def recordRequest(self, timestamp):
        while self.rl and (timestamp - self.rl[0] >= self.windowSeconds):
            self.rl.popleft()
        if len(self.rl) >= self.maxRequests:
            return False
        self.rl.append(timestamp)
        return True
    def reset(self):
        self.rl = deque()
    def getRemainingRequests(self, currentTime):
        while self.rl and (currentTime - self.rl[0] >= self.windowSeconds):
            self.rl.popleft()
        return self.maxRequests-len(self.rl)
class RateLimiter:
    def __init__(self):
        self.per_client_ratelimiter = {}
    def registerUser(self, client_name, maxRequests, windowSeconds):
        self.per_client_ratelimiter[client_name] = UserRl(client_name, maxRequests, windowSeconds)
    def recordRequest(self, client_name, timestamp):
        if client_name not in self.per_client_ratelimiter:
            raise UnregisteredUserError(f"User {client_name} is not registered")
        return self.per_client_ratelimiter[client_name].recordRequest(timestamp)
    def getRemainingRequests(self, client_name, currentTime):
        if client_name not in self.per_client_ratelimiter:
            raise UnregisteredUserError(f"User {client_name} is not registered")
        return self.per_client_ratelimiter[client_name].getRemainingRequests(currentTime)
    def resetUser(self, client_name):
        if client_name not in self.per_client_ratelimiter:
            raise UnregisteredUserError(f"User {client_name} is not registered")
        self.per_client_ratelimiter[client_name].reset()
        
        
        
def check(name, got, expected):
    status = "PASS" if got == expected else "FAIL"
    print(f"[{status}] {name}")
    if status == "FAIL":
        print(f"       got {got}, expected {expected}")

def check_raises(name, fn):
    try:
        fn()
        print(f"[FAIL] {name} — expected UnregisteredUserError, got nothing")
    except UnregisteredUserError:
        print(f"[PASS] {name}")
    except Exception as e:
        print(f"[FAIL] {name} — wrong exception: {e}")

# ── Test 1: Basic allow up to limit ──────────────────────────────────────────
rl = RateLimiter()
rl.registerUser("alice", maxRequests=3, windowSeconds=60)
check("T1a allow 1st", rl.recordRequest("alice", 100), True)
check("T1b allow 2nd", rl.recordRequest("alice", 110), True)
check("T1c allow 3rd", rl.recordRequest("alice", 120), True)
check("T1d deny 4th",  rl.recordRequest("alice", 130), False)

# ── Test 2: Sliding window boundary ──────────────────────────────────────────
rl = RateLimiter()
rl.registerUser("bob", maxRequests=2, windowSeconds=60)
rl.recordRequest("bob", 100)
rl.recordRequest("bob", 110)
check("T2a deny before slide",   rl.recordRequest("bob", 150), False)
check("T2b allow at t=160",      rl.recordRequest("bob", 160), True)   # 160-100=60 → expired
check("T2c deny at t=161",       rl.recordRequest("bob", 161), False)  # queue=[110,160] full

# ── Test 3: getRemainingRequests ──────────────────────────────────────────────
rl = RateLimiter()
rl.registerUser("carol", maxRequests=3, windowSeconds=60)
rl.recordRequest("carol", 100)
rl.recordRequest("carol", 110)
check("T3a remaining=1 mid-window",       rl.getRemainingRequests("carol", 120), 1)
check("T3b remaining=2 after t=100 gone", rl.getRemainingRequests("carol", 161), 2)  # 161-100=61
check("T3c remaining=3 fully expired",    rl.getRemainingRequests("carol", 171), 3)  # 171-110=61

# ── Test 4: resetUser clears history ─────────────────────────────────────────
rl = RateLimiter()
rl.registerUser("dave", maxRequests=2, windowSeconds=60)
rl.recordRequest("dave", 100)
rl.recordRequest("dave", 110)
check("T4a denied before reset",  rl.recordRequest("dave", 120), False)
rl.resetUser("dave")
check("T4b allowed after reset",  rl.recordRequest("dave", 120), True)
check("T4c remaining=1 after reset+1 request", rl.getRemainingRequests("dave", 120), 1)

# ── Test 5: Exact boundary expires ───────────────────────────────────────────
rl = RateLimiter()
rl.registerUser("eve", maxRequests=1, windowSeconds=60)
rl.recordRequest("eve", 100)
check("T5a t=159 still in window", rl.recordRequest("eve", 159), False)
rl.resetUser("eve")
rl.recordRequest("eve", 100)
check("T5b t=160 exactly expired", rl.recordRequest("eve", 160), True)  # 160-100=60 ≥ 60

# ── Test 6: Same timestamp counts individually ────────────────────────────────
rl = RateLimiter()
rl.registerUser("frank", maxRequests=3, windowSeconds=60)
check("T6a same ts 1", rl.recordRequest("frank", 100), True)
check("T6b same ts 2", rl.recordRequest("frank", 100), True)
check("T6c same ts 3", rl.recordRequest("frank", 100), True)
check("T6d same ts 4 denied", rl.recordRequest("frank", 100), False)

# ── Test 7: Unregistered user raises error ────────────────────────────────────
rl = RateLimiter()
check_raises("T7a recordRequest unregistered",  lambda: rl.recordRequest("ghost", 100))
check_raises("T7b getRemaining unregistered",   lambda: rl.getRemainingRequests("ghost", 100))
check_raises("T7c resetUser unregistered",      lambda: rl.resetUser("ghost"))

# ── Test 8: Multiple users are independent ────────────────────────────────────
rl = RateLimiter()
rl.registerUser("u1", maxRequests=2, windowSeconds=60)
rl.registerUser("u2", maxRequests=5, windowSeconds=60)
rl.recordRequest("u1", 100)
rl.recordRequest("u1", 110)
check("T8a u1 denied",       rl.recordRequest("u1", 120), False)
check("T8b u2 unaffected",   rl.recordRequest("u2", 120), True)
check("T8c u2 remaining=4",  rl.getRemainingRequests("u2", 120), 4)

# ── Test 9: maxRequests=1 strict ─────────────────────────────────────────────
rl = RateLimiter()
rl.registerUser("strict", maxRequests=1, windowSeconds=30)
check("T9a first allowed",    rl.recordRequest("strict", 200), True)
check("T9b second denied",    rl.recordRequest("strict", 210), False)
check("T9c remaining=0",      rl.getRemainingRequests("strict", 215), 0)
check("T9d allowed at t=230", rl.recordRequest("strict", 230), True)  # 230-200=30 expired

# ── Test 10: Window rolls continuously ───────────────────────────────────────
rl = RateLimiter()
rl.registerUser("g", maxRequests=3, windowSeconds=10)
rl.recordRequest("g", 0)
rl.recordRequest("g", 1)
rl.recordRequest("g", 2)
check("T10a denied at t=5",   rl.recordRequest("g", 5),  False)
check("T10b allowed at t=10", rl.recordRequest("g", 10), True)   # t=0 expires
check("T10c allowed at t=11", rl.recordRequest("g", 11), True)   # t=1 expires
check("T10d allowed at t=12", rl.recordRequest("g", 12), True)   # t=2 expires
check("T10e denied at t=13",  rl.recordRequest("g", 13), False)  # queue=[10,11,12] full