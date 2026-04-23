import heapq
class ListNode:
    def __init__(self, key=None, val=None, next=None, prev=None):
        self.key = key
        self.val = val
        self.access_count = 0
        self.next = next
        self.prev = prev
class AnalyticsLRUCache:
    def __init__(self, capacity):
        self.dll_head = ListNode()
        self.dll_tail = ListNode()
        self.dll_head.next = self.dll_tail
        self.dll_tail.prev = self.dll_head
        self.capacity = capacity
        self.hmap = {}
        self.hits = 0
        self.miss = 0
        self.evict = 0
    def remove(self, node):
        next = node.next
        prev = node.prev
        next.prev = prev
        prev.next = next
        node.next = None
        node.prev = None
        return node
    def insert_head(self, node):
        next = self.dll_head.next
        node.prev = self.dll_head
        node.next = next
        next.prev = node
        self.dll_head.next = node
    def get(self, key):
        if key not in self.hmap:
            self.miss += 1
            return -1
        node = self.hmap[key]
        self.remove(node)
        val = node.val
        node.access_count += 1
        self.insert_head(node)
        self.hits += 1
        return val
    def put(self, key, val):
        if key in self.hmap:
            node = self.hmap[key]
            node.val = val
            self.remove(node)
            self.insert_head(node)
            return
        while len(self.hmap)>=self.capacity:
            node = self.remove(self.dll_tail.prev)
            del self.hmap[node.key]
            self.evict+=1
        node = ListNode(key, val)
        self.insert_head(node)
        self.hmap[key] = node
        return
    def getHitRate(self):
        if self.hits+self.miss:
            return self.hits/(self.hits+self.miss)
        return 0.0
    def getEvictionCount(self):
        return self.evict
    def getMostFrequentlyAccessed(self, n):
        ret = []
        ptr = self.dll_head.next
        while ptr != self.dll_tail:
            ret.append((ptr.access_count, ptr.key))
            ptr = ptr.next
        ret.sort(key = lambda p: -p[0])
        res = [a[1] for a in ret]
        return res[:n]


def check(name, got, expected):
    if isinstance(expected, float):
        ok = abs(got - expected) < 1e-9
    else:
        ok = got == expected
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        print(f"       got      {got}")
        print(f"       expected {expected}")

# T1: Spec example
c = AnalyticsLRUCache(2)
c.put(1, 10); c.put(2, 20)
check("T1a get hit",          c.get(1), 10)
c.put(3, 30)
check("T1b evicted key gone", c.get(2), -1)
check("T1c hit rate 0.5",     c.getHitRate(), 0.5)
check("T1d eviction count 1", c.getEvictionCount(), 1)
check("T1e most accessed",    c.getMostFrequentlyAccessed(1), [1])

# T2: All misses
c = AnalyticsLRUCache(2)
c.get(1); c.get(2); c.get(3)
check("T2 all misses hit rate", c.getHitRate(), 0.0)

# T3: All hits
c = AnalyticsLRUCache(2)
c.put(1, 10); c.put(2, 20)
c.get(1); c.get(2); c.get(1)
check("T3 all hits hit rate", c.getHitRate(), 1.0)

# T4: No gets → no division by zero
c = AnalyticsLRUCache(2)
c.put(1, 10)
check("T4 no gets hit rate", c.getHitRate(), 0.0)

# T5: LRU eviction order
c = AnalyticsLRUCache(3)
c.put(1,1); c.put(2,2); c.put(3,3)
c.get(1)        # LRU order: 2,3,1
c.put(4,4)      # evicts 2
check("T5a key 2 evicted",  c.get(2), -1)
check("T5b key 1 survives", c.get(1), 1)
check("T5c eviction count", c.getEvictionCount(), 1)

# T6: Update existing key doesn't evict
c = AnalyticsLRUCache(2)
c.put(1, 10); c.put(2, 20)
c.put(1, 99)
check("T6a no eviction on update", c.getEvictionCount(), 0)
check("T6b updated value",         c.get(1), 99)

# T7: Multiple evictions
c = AnalyticsLRUCache(2)
c.put(1,1); c.put(2,2)
c.put(3,3); c.put(4,4); c.put(5,5)
check("T7 3 evictions", c.getEvictionCount(), 3)

# T8: getMostFrequentlyAccessed ordering
c = AnalyticsLRUCache(5)
c.put(1,1); c.put(2,2); c.put(3,3)
c.get(1); c.get(1); c.get(1)   # 3 hits
c.get(2); c.get(2)             # 2 hits
c.get(3)                       # 1 hit
check("T8a top 1", c.getMostFrequentlyAccessed(1), [1])
check("T8b top 2", c.getMostFrequentlyAccessed(2), [1, 2])
check("T8c top 3", c.getMostFrequentlyAccessed(3), [1, 2, 3])

# T9: n > number of keys
c = AnalyticsLRUCache(3)
c.put(1,1); c.put(2,2)
c.get(1); c.get(2)
check("T9 n > keys returns all", len(c.getMostFrequentlyAccessed(10)), 2)

# T10: Miss doesn't count toward frequency
c = AnalyticsLRUCache(2)
c.get(99)   # miss
c.put(1,1); c.get(1)
check("T10 miss not in top", c.getMostFrequentlyAccessed(1), [1])

# T11: Mixed hit rate
c = AnalyticsLRUCache(3)
c.put(1,1); c.put(2,2); c.put(3,3)
c.get(1); c.get(2)    # 2 hits
c.get(99); c.get(98)  # 2 misses
check("T11 mixed hit rate 0.5", c.getHitRate(), 0.5)

# T12: Capacity 1
c = AnalyticsLRUCache(1)
c.put(1,10)
check("T12a get 1",      c.get(1), 10)
c.put(2,20)
check("T12b key 1 gone", c.get(1), -1)
check("T12c key 2 ok",   c.get(2), 20)
check("T12d 1 eviction", c.getEvictionCount(), 1)

# T13: put refreshes recency
c = AnalyticsLRUCache(2)
c.put(1,1); c.put(2,2)
c.put(1, 100)   # refresh key 1 → key 2 is now LRU
c.put(3,3)      # evicts key 2
check("T13a key 2 evicted", c.get(2), -1)
check("T13b key 1 updated", c.get(1), 100)