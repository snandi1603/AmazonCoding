from collections import namedtuple
class ValidationResult:
    def __init__(self, is_valid, failed_step):
        self.is_valid = is_valid
        self.failed_step = failed_step
        
def validate(csum: str) -> ValidationResult:
    def rule1(csum):
        return len(csum)==16
    def rule2(csum):
        first2 = csum[:2]
        digits10 = csum[2:12]
        last = csum[12:]
        if any(f.isdigit() for f in first2):
            return False
        first2upper = first2.upper()
        if first2upper != first2:
            return False
        for d in digits10:
            if not d.isdigit():
                return False
        if any(f.isdigit() for f in last):
            return False
        lastupper = last.upper()
        return lastupper==last
    def rule3(csum):
        digits10 = csum[2:12]
        res = 0
        for d in digits10:
            res += int(d)
        return res%7==0
    def rule4(csum):
        digits10 = csum[2:12]
        letters = csum[:2]+csum[12:]
        res = 0
        for l in letters:
            res += (ord(l)-ord('A')+1)
        return res%10==int(digits10[-1])
    def rule5(csum):
        digits10 = csum[2:12]
        odd_count = 0
        even_count=0
        for d in digits10:
            if int(d)%2:
                odd_count+=1
            else:
                even_count+=1
        return odd_count==even_count
    if rule1(csum)==False:
        return ValidationResult(is_valid=False, failed_step=1)
    if rule2(csum)==False:
        return ValidationResult(is_valid=False, failed_step=2)
    if rule3(csum)==False:
        return ValidationResult(is_valid=False, failed_step=3)
    if rule4(csum)==False:
        return ValidationResult(is_valid=False, failed_step=4)
    if rule5(csum)==False:
        return ValidationResult(is_valid=False, failed_step=5)
    return ValidationResult(is_valid=True, failed_step=0)


# ── Test runner ───────────────────────────────────────────────────────────────

def check(name, code, expected_valid, expected_step):
    result = validate(code)
    if result.is_valid == expected_valid and result.failed_step == expected_step:
        print(f"  PASS  {name}")
    else:
        print(f"  FAIL  {name}")
        print(f"         expected : is_valid={expected_valid}, failed_step={expected_step}")
        print(f"         actual   : is_valid={result.is_valid}, failed_step={result.failed_step}")

print("Running tests...\n")

# Step 1 — length
check("Step1: too short",          "AB123456789CDEF",   False, 1)
check("Step1: too long",           "AB1234567890CDEFF", False, 1)
check("Step1: empty string",       "",                  False, 1)

# Step 2 — character format
check("Step2: first 2 are digits", "121234567890CDEF",  False, 2)
check("Step2: first 2 lowercase",  "ab1234567890CDEF",  False, 2)
check("Step2: middle has letter",  "AB123456789XCDEF",  False, 2)
check("Step2: last 4 are digits",  "AB12345678901234",  False, 2)
check("Step2: last 4 lowercase",   "AB1234567890cdef",  False, 2)

# Step 3 — digit sum divisible by 7
check("Step3: sum=45, 45%7!=0",    "AB1234567890CDEF",  False, 3)

# Step 4 — letter checksum
# digits 0000000007 → sum=7 ✓, letters ABAB GA=14, last=4 ≠ 7 → fails step4
check("Step4: letter checksum fail", "AB0000000007ABGA", False, 4)

# Step 5 — parity (5 odd, 5 even digits)
# digits 0000000034 → sum=7 ✓, last digit=4 matches letter sum ✓, but odds=1 → fails step5
check("Step5: parity fails",       "AB0000000034ABGA",  False, 5)

# All steps pass
# digits 1357124624 → sum=35 ✓, 10th digit=4, letters ABABGA sum=14 last=4 ✓
# odds: 1,3,5,7,1=5 ✓  evens: 2,4,6,2,4=5 ✓
check("All steps pass",            "AB1357124624ABGA",  True,  0)

# Spec examples
check("Spec ex1: fails step3",     "AB1234567890CDEF",  False, 3)
check("Spec ex2: fails step4",     "AB0000000007ABGA",  False, 4)

# Order enforcement
check("Order: step1 before step2", "A",                 False, 1)
check("Order: step2 before step3", "ab1234567890CDEF",  False, 2)

print("\nDone.")