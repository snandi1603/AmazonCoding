from collections import defaultdict
class Rule:
    def __init__(self, name = None, condition_func=None, discount_func=None):
        self.name = name
        self.condition_func = condition_func
        self.discount_func = discount_func
    def apply_condition(self, data):
        return self.condition_func(data)
    def apply_discount(self, data):
        return self.discount_func(data)
class PricingEngine:
    def __init__(self):
        self.rules = []
    def addRule(self, rule_name, cond_func, disc_func):
        self.rules.append(Rule(rule_name, cond_func, disc_func))
    def applyRules(self, cart):
        res = {}
        for item, price in cart.items():
            effective_price = price
            for rule in self.rules:
                if rule.apply_condition(effective_price):
                    effective_price = rule.apply_discount(effective_price)
            res[item] = effective_price
        return res
    def getRuleReport(self, cart):
        res = []
        rules_dict = defaultdict(list)
        for rule in self.rules:
            for item, effective_price in cart.items():
                if rule.apply_condition(effective_price):
                    effective_price = rule.apply_discount(effective_price)
                    rules_dict[rule.name].append((item, cart[item], effective_price))
                    cart[item] = effective_price
        for rule_name, affected in rules_dict.items():
            res.append({"rule": rule_name, "affected":[{"item":a[0], "before":a[1], "after":a[2]} for a in affected]})
        return res
    
    
def check(name, got, expected):
    if isinstance(expected, dict):
        ok = all(abs(got.get(k, -1) - v) < 1e-9 for k, v in expected.items()) and len(got) == len(expected)
    elif isinstance(expected, float):
        ok = abs(got - expected) < 1e-9
    else:
        ok = got == expected
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        print(f"       got      {got}")
        print(f"       expected {expected}")

# T1: Spec example
e = PricingEngine()
e.addRule("bulk",    lambda p: p > 50,  lambda p: p * 0.90)
e.addRule("loyalty", lambda p: True,    lambda p: p - 2.0)
check("T1 spec example", e.applyRules({"A": 60.0, "B": 30.0, "C": 100.0}),
      {"A": 52.0, "B": 28.0, "C": 88.0})

# T2: No rules → unchanged
e = PricingEngine()
check("T2 no rules", e.applyRules({"X": 10.0, "Y": 20.0}), {"X": 10.0, "Y": 20.0})

# T3: Original cart not mutated
e = PricingEngine()
e.addRule("flat", lambda p: True, lambda p: p * 0.5)
cart = {"A": 100.0}; original = dict(cart)
e.applyRules(cart)
check("T3 original not mutated", cart, original)

# T4: No rule matches any item
e = PricingEngine()
e.addRule("highonly", lambda p: p > 1000, lambda p: p * 0.5)
check("T4 no rule matches", e.applyRules({"A": 10.0, "B": 20.0}), {"A": 10.0, "B": 20.0})

# T5: Cumulative rules (order matters)
e = PricingEngine()
e.addRule("r1", lambda p: True, lambda p: p * 0.9)
e.addRule("r2", lambda p: True, lambda p: p * 0.9)
check("T5 cumulative rules", e.applyRules({"A": 100.0}), {"A": 81.0})

# T6: Rule condition uses post-previous-rule price
e = PricingEngine()
e.addRule("r1", lambda p: True,   lambda p: p * 0.5)
e.addRule("r2", lambda p: p > 40, lambda p: p - 10.0)
# A: 60→30(r1), 30 not >40 → 30; B: 100→50(r1), 50>40 → 40
check("T6 condition on post-rule price", e.applyRules({"A": 60.0, "B": 100.0}),
      {"A": 30.0, "B": 40.0})

# T7: Single item, single rule
e = PricingEngine()
e.addRule("half", lambda p: True, lambda p: p / 2)
check("T7 single item", e.applyRules({"Z": 50.0}), {"Z": 25.0})

# T8: Empty cart
e = PricingEngine()
e.addRule("any", lambda p: True, lambda p: p - 1)
check("T8 empty cart", e.applyRules({}), {})

# T9: getRuleReport structure
e = PricingEngine()
e.addRule("bulk",    lambda p: p > 50,  lambda p: p * 0.9)
e.addRule("loyalty", lambda p: True,    lambda p: p - 2.0)
report = e.getRuleReport({"A": 60.0, "B": 30.0})
check("T9a 2 rules in report",       len(report), 2)
check("T9b bulk rule name",          report[0]["rule"], "bulk")
check("T9c bulk affects only A",     len(report[0]["affected"]), 1)
check("T9d loyalty affects both",    len(report[1]["affected"]), 2)

# T10: getRuleReport before/after values
e = PricingEngine()
e.addRule("ten_off", lambda p: True, lambda p: p - 10.0)
report = e.getRuleReport({"A": 100.0})
check("T10a before", report[0]["affected"][0]["before"], 100.0)
check("T10b after",  report[0]["affected"][0]["after"],   90.0)

# T11: Rule order gives different results
cart = {"A": 80.0}
e1 = PricingEngine()
e1.addRule("r1", lambda p: True,   lambda p: p - 10)
e1.addRule("r2", lambda p: p > 60, lambda p: p * 0.9)
check("T11a order1", e1.applyRules(cart), {"A": 63.0})  # 80→70→63

e2 = PricingEngine()
e2.addRule("r2", lambda p: p > 60, lambda p: p * 0.9)
e2.addRule("r1", lambda p: True,   lambda p: p - 10)
check("T11b order2", e2.applyRules(cart), {"A": 62.0})  # 80→72→62

# T12: Only some items qualify
e = PricingEngine()
e.addRule("premium", lambda p: p >= 100, lambda p: p * 0.8)
check("T12 partial match", e.applyRules({"cheap": 9.99, "mid": 50.0, "expensive": 150.0}),
      {"cheap": 9.99, "mid": 50.0, "expensive": 120.0})