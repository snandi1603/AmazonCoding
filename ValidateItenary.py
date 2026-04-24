class ValidationReport:
    def __init__(self, is_valid, errors):
        self.is_valid = is_valid
        self.errors = errors
def validate_itinerary(segments):
    def rule1(segments):
        st = set()
        for s in segments:
            if s["flight_id"] in st:
                return f"Duplicate flight_id {s["flight_id"]}"
            st.add(s["flight_id"])
        return None
    def rule2(segments):
        for s in segments:
            if s["departure_time"] >= s["arrival_time"]:
                return f"Flight {s["flight_id"]} has departure_time({s["departure_time"]} >= arrival_time({s["arrival_time"]})"
        return None
    def rule3(segments):
        for i in range(len(segments)-1):
            if segments[i]["destination"] != segments[i+1]["origin"]:
                return f"Flight {segments[i]["flight_id"]} and {segments[i+1]["flight_id"]} disconnected"
        return None
    def rule4(segments):
        for i in range(len(segments)-1):
            if segments[i]["arrival_time"] > segments[i+1]["departure_time"]:
                return f"Flight {segments[i]["flight_id"]} and {segments[i+1]["flight_id"]} overlap"
        return None
    def rule5(segments):
        trip_duration = 0
        for s in segments:
            trip_duration += (s["arrival_time"]-s["departure_time"])
        return "Total duration exceeds 48hr" if trip_duration>2880 else None 
    errors = []
    err = rule1(segments)
    if err:
        errors.append(f"Rule 1: {err}")
    err = rule2(segments)
    if err:
        errors.append(f"Rule 2: {err}")
    err = rule3(segments)
    if err:
        errors.append(f"Rule 3: {err}")
    err = rule4(segments)
    if err:
        errors.append(f"Rule 4: {err}")
    err = rule5(segments)
    if err:
        errors.append(f"Rule 5: {err}")
    return ValidationReport(is_valid=len(errors)==0, errors=errors)

def seg(fid, org, dst, dep, arr):
    return {"flight_id": fid, "origin": org, "destination": dst,
            "departure_time": dep, "arrival_time": arr}

def check(name, report, expected_valid, expected_rule_nums=None):
    ok_valid = report.is_valid == expected_valid
    ok_rules = True
    if expected_rule_nums is not None:
        found = set()
        for e in report.errors:
            for r in expected_rule_nums:
                if f"Rule {r}:" in e:
                    found.add(r)
        ok_rules = found == set(expected_rule_nums)
    status = "PASS" if (ok_valid and ok_rules) else "FAIL"
    print(f"[{status}] {name}")
    if status == "FAIL":
        print(f"       is_valid: {report.is_valid}, expected {expected_valid}")
        print(f"       errors:   {report.errors}")

# T1: Spec example — Rule 1 (dup) + Rule 3 (broken chain)
check("T1 spec example", validate_itinerary([
    seg("AA100", "JFK", "LAX", 600,  900),
    seg("AA100", "LAX", "SFO", 950,  1050),
    seg("UA200", "ORD", "SEA", 1100, 1300),
]), False, [1, 3])

# T2: Perfectly valid itinerary
check("T2 all valid", validate_itinerary([
    seg("F1", "JFK", "LAX", 0,   300),
    seg("F2", "LAX", "SFO", 300, 400),
    seg("F3", "SFO", "SEA", 400, 500),
]), True)

# T3: Single segment
check("T3 single segment", validate_itinerary([
    seg("F1", "JFK", "LAX", 100, 400)
]), True)

# T4: Two different duplicate ids — both reported
r = validate_itinerary([
    seg("F1", "JFK", "LAX", 0,   100),
    seg("F1", "LAX", "SFO", 100, 200),
    seg("F2", "SFO", "SEA", 200, 300),
    seg("F2", "SEA", "PDX", 300, 400),
])
check("T4a two dup ids", r, False, [1])
print(f"[{'PASS' if len([e for e in r.errors if 'Rule 1' in e]) == 2 else 'FAIL'}] T4b both dups reported")

# T5: Rule 2 — dep > arr and dep == arr
check("T5a dep > arr",  validate_itinerary([seg("F1","JFK","LAX",500,400)]), False, [2])
check("T5b dep == arr", validate_itinerary([seg("F1","JFK","LAX",400,400)]), False, [2])

# T6: Rule 3 — broken chain
check("T6 disconnected", validate_itinerary([
    seg("F1", "JFK", "LAX", 0,   100),
    seg("F2", "SFO", "SEA", 200, 300),
]), False, [3])

# T7: Rule 4 — overlap and boundary
check("T7a overlap", validate_itinerary([
    seg("F1", "JFK", "LAX", 0,   300),
    seg("F2", "LAX", "SFO", 200, 400),
]), False, [4])
check("T7b same minute OK", validate_itinerary([
    seg("F1", "JFK", "LAX", 0,   300),
    seg("F2", "LAX", "SFO", 300, 400),
]), True)

# T8: Rule 5 — 48h boundary
check("T8a exceeds 48h", validate_itinerary([
    seg("F1", "JFK", "LAX", 0,    1000),
    seg("F2", "LAX", "SFO", 1000, 2881),
]), False, [5])
check("T8b exactly 48h OK", validate_itinerary([
    seg("F1", "JFK", "LAX", 0,    1000),
    seg("F2", "LAX", "SFO", 1000, 2880),
]), True)

# T9: Multiple rules fail at once
check("T9 rules 1+2+3", validate_itinerary([
    seg("F1", "JFK", "LAX", 500, 400),   # Rule 2
    seg("F1", "ORD", "SEA", 600, 700),   # Rule 1 + Rule 3
]), False, [1, 2, 3])

# T10: Rules 3 and 4 together
check("T10 rules 3+4", validate_itinerary([
    seg("F1", "JFK", "LAX", 0,   300),
    seg("F2", "ORD", "SEA", 200, 400),
]), False, [3, 4])

# T11: Empty itinerary
check("T11 empty", validate_itinerary([]), True)
    