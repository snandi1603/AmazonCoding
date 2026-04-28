from collections import defaultdict
class InvalidTransitionError(Exception):
    pass
class Order:
    def __init__(self, order_id, items, customer_id, state="PENDING"):
        self.order_id = order_id
        self.items = items
        self.customer_id = customer_id
        self.status = state
        self.state_map = {("PENDING","CONFIRM"):"CONFIRMED", ("CONFIRMED","SHIP"):"SHIPPED",
                          ("SHIPPED","DELIVER"):"DELIVERED", ("PENDING","CANCEL"):"CANCELLED",
                          ("CONFIRMED","CANCEL"):"CANCELLED", ("SHIPPED","CANCEL"):"CANCELLED",
                         }
    def set_state(self, event):
        key = (self.status, event)
        if key not in self.state_map:
            raise InvalidTransitionError(f"Invalid event {event} for current state {self.status}")
        self.status = self.state_map[key]
        
class OrderSystem:
    def __init__(self):
        self.order_map = {}
        self.customer_map = defaultdict(list)
        pass
    def createOrder(self, orderId, items, customerId) -> Order:
        order = Order(orderId, items, customerId)
        self.order_map[orderId] = order
        self.customer_map[customerId].append(order)
        return order
    def processEvent(self, orderId, event):
        self.order_map[orderId].set_state(event)
    def getOrder(self, orderId) -> Order:
        return self.order_map[orderId]
    def getOrdersByCustomer(self, customerId) -> list[Order] :
        return self.customer_map[customerId]
    def getOrdersByStatus(self, status) -> list[Order]:
        res = []
        for _, order in self.order_map.items():
            if status == order.status:
                res.append(order)
        return res
    
def check(name, got, expected):
    ok = got == expected
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        print(f"       got      {got}")
        print(f"       expected {expected}")

def check_raises(name, fn):
    try:
        fn()
        print(f"[FAIL] {name} — expected InvalidTransitionError, got nothing")
    except InvalidTransitionError:
        print(f"[PASS] {name}")
    except Exception as e:
        print(f"[FAIL] {name} — wrong exception: {e}")

# T1: Full happy path
s = OrderSystem()
s.createOrder("O1", ["item1", "item2"], "C1")
check("T1a PENDING",   s.getOrder("O1").status, "PENDING")
s.processEvent("O1", "CONFIRM")
check("T1b CONFIRMED", s.getOrder("O1").status, "CONFIRMED")
s.processEvent("O1", "SHIP")
check("T1c SHIPPED",   s.getOrder("O1").status, "SHIPPED")
s.processEvent("O1", "DELIVER")
check("T1d DELIVERED", s.getOrder("O1").status, "DELIVERED")

# T2-T4: Cancel from each cancellable state
s = OrderSystem()
s.createOrder("O1", ["a"], "C1")
s.processEvent("O1", "CANCEL")
check("T2 cancel from PENDING", s.getOrder("O1").status, "CANCELLED")

s = OrderSystem()
s.createOrder("O1", ["a"], "C1")
s.processEvent("O1", "CONFIRM"); s.processEvent("O1", "CANCEL")
check("T3 cancel from CONFIRMED", s.getOrder("O1").status, "CANCELLED")

s = OrderSystem()
s.createOrder("O1", ["a"], "C1")
s.processEvent("O1", "CONFIRM"); s.processEvent("O1", "SHIP"); s.processEvent("O1", "CANCEL")
check("T4 cancel from SHIPPED", s.getOrder("O1").status, "CANCELLED")

# T5: Cannot cancel DELIVERED
s = OrderSystem()
s.createOrder("O1", ["a"], "C1")
s.processEvent("O1", "CONFIRM"); s.processEvent("O1", "SHIP"); s.processEvent("O1", "DELIVER")
check_raises("T5 cannot cancel DELIVERED", lambda: s.processEvent("O1", "CANCEL"))

# T6: Invalid transitions
s = OrderSystem()
s.createOrder("O1", ["a"], "C1")
check_raises("T6a SHIP before CONFIRM",   lambda: s.processEvent("O1", "SHIP"))
check_raises("T6b DELIVER before CONFIRM",lambda: s.processEvent("O1", "DELIVER"))
s.processEvent("O1", "CONFIRM")
check_raises("T6c CONFIRM again",         lambda: s.processEvent("O1", "CONFIRM"))
check_raises("T6d DELIVER before SHIP",   lambda: s.processEvent("O1", "DELIVER"))

# T7: No transitions from CANCELLED
s = OrderSystem()
s.createOrder("O1", ["a"], "C1")
s.processEvent("O1", "CANCEL")
check_raises("T7a confirm after cancel", lambda: s.processEvent("O1", "CONFIRM"))
check_raises("T7b ship after cancel",   lambda: s.processEvent("O1", "SHIP"))

# T8: getOrdersByCustomer
s = OrderSystem()
s.createOrder("O1", ["a"], "C1"); s.createOrder("O2", ["b"], "C1"); s.createOrder("O3", ["c"], "C2")
check("T8a C1 has 2",      len(s.getOrdersByCustomer("C1")), 2)
check("T8b C2 has 1",      len(s.getOrdersByCustomer("C2")), 1)
check("T8c unknown has 0", len(s.getOrdersByCustomer("C99")), 0)

# T9: getOrdersByStatus
s = OrderSystem()
s.createOrder("O1", ["a"], "C1"); s.createOrder("O2", ["b"], "C1"); s.createOrder("O3", ["c"], "C2")
s.processEvent("O1", "CONFIRM")
s.processEvent("O2", "CONFIRM"); s.processEvent("O2", "SHIP")
check("T9a PENDING=1",   len(s.getOrdersByStatus("PENDING")),   1)
check("T9b CONFIRMED=1", len(s.getOrdersByStatus("CONFIRMED")), 1)
check("T9c SHIPPED=1",   len(s.getOrdersByStatus("SHIPPED")),   1)
check("T9d DELIVERED=0", len(s.getOrdersByStatus("DELIVERED")), 0)

# T10: createOrder fields
s = OrderSystem()
o = s.createOrder("O1", ["x", "y"], "C1")
check("T10a order_id",    o.order_id,    "O1")
check("T10b items",       o.items,       ["x", "y"])
check("T10c customer_id", o.customer_id, "C1")
check("T10d status",      o.status,      "PENDING")

# T11: Multiple orders independent
s = OrderSystem()
s.createOrder("O1", ["a"], "C1"); s.createOrder("O2", ["b"], "C2")
s.processEvent("O1", "CONFIRM")
check("T11a O1 confirmed",    s.getOrder("O1").status, "CONFIRMED")
check("T11b O2 still PENDING",s.getOrder("O2").status, "PENDING")

# T12: getOrdersByStatus after cancellation
s = OrderSystem()
s.createOrder("O1", ["a"], "C1"); s.createOrder("O2", ["b"], "C1")
s.processEvent("O1", "CANCEL")
check("T12a cancelled=1", len(s.getOrdersByStatus("CANCELLED")), 1)
check("T12b pending=1",   len(s.getOrdersByStatus("PENDING")),   1)