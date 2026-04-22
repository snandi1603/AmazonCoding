class Server:
    def __init__(self, server_id, level):
        self.server_id = server_id
        self.level = level

class SecurityGrouper:
    def __init__(self):
        self.servers = []
        self.serversset = set()
    def addServer(self, server_id, security_level):
        if server_id in self.serversset:
            print(f"Duplicate Adding {server_id}")
            return
        self.serversset.add(server_id)
        self.servers.append(Server(server_id, security_level))
    def group(self, k):
        base = len(self.servers)//k
        extra = len(self.servers)%k
        self.servers.sort(key=lambda s: s.level)
        ret_server_list = []
        var = 0
        idx = 0
        for i in range(k):
            size = base + 1 if i<extra else base
            ret_server_list.append([a.server_id for a in  self.servers[idx:idx+size]])
            sec_list = [l.level for l in self.servers[idx:idx+size]]
            var += max(sec_list)-min(sec_list)
            idx += size
        return ret_server_list, var

def run_test(name, sg, k, expected_variance, expected_group_count=None, check_membership=None):
    groups, variance = sg.group(k)
    ok_var = (variance == expected_variance)
    ok_cnt = (expected_group_count is None or len(groups) == expected_group_count)
    ok_mem = True
    if check_membership:
        all_servers = set(s for g in groups for s in g)
        ok_mem = (all_servers == set(check_membership))
    status = "PASS" if (ok_var and ok_cnt and ok_mem) else "FAIL"
    print(f"[{status}] {name}")
    if status == "FAIL":
        print(f"       variance: got {variance}, expected {expected_variance}")
        print(f"       groups:   {groups}")

# Test 1: Spec example (6 servers, k=2) → total variance = 5
sg = SecurityGrouper()
for sid, lvl in [("S1",1),("S4",2),("S2",3),("S3",5),("S6",6),("S5",8)]:
    sg.addServer(sid, lvl)
run_test("Spec example k=2", sg, 2, 5, 2, ["S1","S2","S3","S4","S5","S6"])

# Test 2: k=1 → single group, variance = max-min of all levels
sg = SecurityGrouper()
for sid, lvl in [("A",10),("B",1),("C",7)]: sg.addServer(sid, lvl)
run_test("k=1 single group", sg, 1, 9, 1, ["A","B","C"])

# Test 3: k=n → each server alone, variance = 0
sg = SecurityGrouper()
for sid, lvl in [("X",3),("Y",8),("Z",1)]: sg.addServer(sid, lvl)
run_test("k=n each alone", sg, 3, 0, 3, ["X","Y","Z"])

# Test 4: Unequal groups (n=5, k=3 → sizes 2,2,1)
sg = SecurityGrouper()
for sid, lvl in [("A",1),("B",2),("C",3),("D",4),("E",5)]:
    sg.addServer(sid, lvl)
run_test("n=5 k=3 unequal groups", sg, 3, 2, 3, ["A","B","C","D","E"])

# Test 5: All same security level → variance = 0
sg = SecurityGrouper()
for sid, lvl in [("P",5),("Q",5),("R",5),("S",5)]: sg.addServer(sid, lvl)
run_test("All same level k=2", sg, 2, 0, 2, ["P","Q","R","S"])

# Test 6: Already sorted input
sg = SecurityGrouper()
for sid, lvl in [("A",1),("B",3),("C",6),("D",10)]: sg.addServer(sid, lvl)
run_test("Already sorted k=2", sg, 2, 6, 2, ["A","B","C","D"])

# Test 7: Reverse sorted input (should give same result)
sg = SecurityGrouper()
for sid, lvl in [("D",10),("C",6),("B",3),("A",1)]: sg.addServer(sid, lvl)
run_test("Reverse sorted k=2", sg, 2, 6, 2, ["A","B","C","D"])

# Test 8: n=7, k=3 → sizes (3,2,2)
sg = SecurityGrouper()
for sid, lvl in [("S1",2),("S2",4),("S3",6),("S4",8),("S5",10),("S6",12),("S7",14)]:
    sg.addServer(sid, lvl)
run_test("n=7 k=3 sizes(3,2,2)", sg, 3, 8, 3, [f"S{i}" for i in range(1,8)])

# Test 9: Large variance spread, k=3
sg = SecurityGrouper()
for sid, lvl in [("A",1),("B",100),("C",200),("D",201),("E",202),("F",300)]:
    sg.addServer(sid, lvl)
run_test("Large spread k=3", sg, 3, 198, 3, ["A","B","C","D","E","F"])

# Test 10: Single server, k=1
sg = SecurityGrouper()
sg.addServer("ONLY", 42)
run_test("Single server k=1", sg, 1, 0, 1, ["ONLY"])

# Test 11: Two servers, k=1 vs k=2
sg = SecurityGrouper()
sg.addServer("X", 10); sg.addServer("Y", 20)
run_test("Two servers k=1", sg, 1, 10, 1, ["X","Y"])

sg = SecurityGrouper()
sg.addServer("X", 10); sg.addServer("Y", 20)
run_test("Two servers k=2", sg, 2, 0, 2, ["X","Y"])

# Test 12: Duplicate levels across groups
sg = SecurityGrouper()
for sid, lvl in [("A",3),("B",3),("C",7),("D",7)]: sg.addServer(sid, lvl)
run_test("Duplicate levels k=2", sg, 2, 0, 2, ["A","B","C","D"])

# Test 13: n=9, k=4 → sizes (3,2,2,2)
sg = SecurityGrouper()
for i, lvl in enumerate([1,2,4,7,11,16,22,29,37], 1):
    sg.addServer(f"S{i}", lvl)
run_test("n=9 k=4 sizes(3,2,2,2)", sg, 4, 21, 4, [f"S{i}" for i in range(1,10)])
            