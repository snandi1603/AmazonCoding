import heapq
# ── Paste your solution here ──────────────────────────────────────────────────
class Item:
    def __init__(self, name=None, qty=0, price=0):
        self.name = name
        self. qty = qty
        self.price = price
    def to_dict(self):
        return {"qty": self.qty, "price": self.price}
class AmazonCart:
    def __init__(self):
        self.hmap = {}
        self.minHeap = []
        self.coupon = set()
        self.is_checkout = False
        self.subtotal = 0
        self.discount = 0
        self.shipping = 5.99
    def add(self, item, qty, price):
        if self.is_checkout:
            return False
        if item not in self.hmap:
            self.hmap[item] = Item()
        self.hmap[item].name = item
        self.hmap[item].qty += qty
        self.hmap[item].price = price
        heapq.heappush(self.minHeap, (self.hmap[item].price, self.hmap[item].name))
        return True
    def remove(self, item, qty):
        if self.is_checkout:
            return False
        if item not in self.hmap:
            return True
        self.hmap[item].qty -= qty
        if self.hmap[item].qty <= 0:
            del self.hmap[item]
            if self.minHeap[0][1] == item:
                heapq.heappop(self.minHeap)
        return True
    def apply_coupon(self, coupon):
        if self.is_checkout:
            return False
        self.coupon.add(coupon)
        return True
    def apply_coupon_final(self, coupon):
        if coupon=="FREESHIP":
            self.shipping = 0
        if coupon=="SAVE10":
            self.discount += 0.1*self.subtotal
        if coupon == "BOGO":
            while self.minHeap and self.minHeap[0][1] not in self.hmap:
                heapq.heappop(self.minHeap)
            if self.minHeap:
                self.discount += (self.hmap[self.minHeap[0][1]].qty*self.hmap[self.minHeap[0][1]].price)/2
    def checkout(self):
        if self.is_checkout:
            return None
        self.is_checkout = True
        for _, item in self.hmap.items():
            self.subtotal += item.qty*item.price
        for coupon in self.coupon:
            self.apply_coupon_final(coupon)
        total_amount = self.shipping + self.subtotal - self.discount
        return {
            "items": {k:v.to_dict() for k,v in self.hmap.items()},
            "subtotal": self.subtotal,
            "discount": self.discount,
            "shipping": self.shipping,
            "total": total_amount
        }
        
def process(queries):
    ac = AmazonCart()
    final_str = "Invalid Input"
    for q in queries:
        qsplit = q.split()
        if qsplit[0]=="ADD": 
            if not ac.add(qsplit[1], int(qsplit[2]), float(qsplit[3])):
                break
        elif qsplit[0]=="REMOVE":
            if not ac.remove(qsplit[1], int(qsplit[2])):
                break
        elif qsplit[0]=="APPLY_COUPON":
            if not ac.apply_coupon(qsplit[1]):
                break
        elif qsplit[0] == "CHECKOUT":
            final_str = ac.checkout()
    return final_str


# ── Test runner ───────────────────────────────────────────────────────────────

def check(name, queries, expected):
    actual = process(queries)
    passed = True
    errors = []
    for key, val in expected.items():
        if key == "items":
            if actual.get("items") != val:
                passed = False
                errors.append(f"items: expected {val}, got {actual.get('items')}")
        else:
            if round(actual.get(key, -999), 2) != round(val, 2):
                passed = False
                errors.append(f"{key}: expected {val}, got {actual.get(key)}")
    if passed:
        print(f"  PASS  {name}")
    else:
        print(f"  FAIL  {name}")
        for e in errors:
            print(f"         {e}")

print("Running tests...\n")

# [1] Spec example
check("Spec example", [
    "ADD apple 3 1.50",
    "ADD bread 2 2.00",
    "REMOVE apple 1",
    "APPLY_COUPON SAVE10",
    "CHECKOUT"
], {"subtotal": 7.00, "discount": 0.70, "shipping": 5.99, "total": 12.29})

# [2] No coupons
check("No coupons", [
    "ADD milk 2 3.00",
    "CHECKOUT"
], {"subtotal": 6.00, "discount": 0.00, "shipping": 5.99, "total": 11.99})

# [3] FREESHIP only
check("FREESHIP only", [
    "ADD milk 2 3.00",
    "APPLY_COUPON FREESHIP",
    "CHECKOUT"
], {"subtotal": 6.00, "discount": 0.00, "shipping": 0.00, "total": 6.00})

# [4] SAVE10 only
check("SAVE10 only", [
    "ADD item1 1 10.00",
    "APPLY_COUPON SAVE10",
    "CHECKOUT"
], {"subtotal": 10.00, "discount": 1.00, "shipping": 5.99, "total": 14.99})

# [5] BOGO — cheapest item discounted
# cheap: 4*1.00=4.00, expensive: 2*5.00=10.00, subtotal=14
# BOGO: cheapest=cheap at $1.00, discount = 1.00*4/2 = $2.00
check("BOGO cheapest item", [
    "ADD cheap 4 1.00",
    "ADD expensive 2 5.00",
    "APPLY_COUPON BOGO",
    "CHECKOUT"
], {"subtotal": 14.00, "discount": 2.00, "shipping": 5.99, "total": 17.99})

# [6] All three coupons stacked
# subtotal=14, SAVE10=1.40, BOGO=cheap(2*2/2)=2.00, FREESHIP=0
check("All coupons stacked", [
    "ADD cheap 2 2.00",
    "ADD pricey 1 10.00",
    "APPLY_COUPON SAVE10",
    "APPLY_COUPON FREESHIP",
    "APPLY_COUPON BOGO",
    "CHECKOUT"
], {"subtotal": 14.00, "discount": 3.40, "shipping": 0.00, "total": 10.60})

# [7] REMOVE more than available → qty=0, item removed
check("REMOVE excess qty", [
    "ADD apple 2 1.50",
    "REMOVE apple 10",
    "CHECKOUT"
], {"items": {}, "subtotal": 0.00, "discount": 0.00, "shipping": 5.99, "total": 5.99})

# [8] REMOVE exact qty
check("REMOVE exact qty", [
    "ADD apple 3 1.50",
    "REMOVE apple 3",
    "CHECKOUT"
], {"items": {}, "subtotal": 0.00, "discount": 0.00, "shipping": 5.99, "total": 5.99})

# [9] Queries after CHECKOUT are ignored
check("Queries after CHECKOUT ignored", [
    "ADD apple 2 1.50",
    "CHECKOUT",
    "ADD bread 5 10.00",
    "APPLY_COUPON SAVE10"
], {"subtotal": 3.00, "shipping": 5.99, "total": 8.99})

# [10] ADD same item twice — qty accumulates
check("ADD same item twice", [
    "ADD apple 2 1.50",
    "ADD apple 3 1.50",
    "CHECKOUT"
], {"items": {"apple": {"qty": 5, "price": 1.50}}, "subtotal": 7.50, "shipping": 5.99, "total": 13.49})

# [11] BOGO single item
# BOGO: 3.00*4/2 = 6.00 discount
check("BOGO single item", [
    "ADD item1 4 3.00",
    "APPLY_COUPON BOGO",
    "CHECKOUT"
], {"subtotal": 12.00, "discount": 6.00, "shipping": 5.99, "total": 11.99})

# [12] BOGO after cheapest removed — next cheapest applies
# cheap removed, min is mid at $3.00, BOGO: 3*2/2=3.00
check("BOGO after cheapest removed", [
    "ADD cheap 2 1.00",
    "ADD mid   2 3.00",
    "REMOVE cheap 2",
    "APPLY_COUPON BOGO",
    "CHECKOUT"
], {"subtotal": 6.00, "discount": 3.00, "shipping": 5.99, "total": 8.99})

# [13] Duplicate coupon ignored
check("Duplicate coupon ignored", [
    "ADD apple 2 5.00",
    "APPLY_COUPON SAVE10",
    "APPLY_COUPON SAVE10",
    "CHECKOUT"
], {"subtotal": 10.00, "discount": 1.00, "shipping": 5.99, "total": 14.99})

# [14] Empty cart checkout
check("Empty cart checkout", [
    "CHECKOUT"
], {"subtotal": 0.00, "discount": 0.00, "shipping": 5.99, "total": 5.99})

# [15] BOGO on empty cart — no crash
check("BOGO on empty cart", [
    "APPLY_COUPON BOGO",
    "CHECKOUT"
], {"subtotal": 0.00, "discount": 0.00, "shipping": 5.99, "total": 5.99})

# [16] SAVE10 + FREESHIP
check("SAVE10 + FREESHIP", [
    "ADD item1 2 10.00",
    "APPLY_COUPON SAVE10",
    "APPLY_COUPON FREESHIP",
    "CHECKOUT"
], {"subtotal": 20.00, "discount": 2.00, "shipping": 0.00, "total": 18.00})

print("\nDone.")