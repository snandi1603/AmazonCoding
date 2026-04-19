# ── Paste your solution here ─────────────────────────────────────────────────

def find_similar(passwords, k):
    # I will have 3 helper functions
    # rule1(), rule2(), rule3()
    # If any of the rules return true that means the password is similar
    res = []
    def get_class(a: str):
        a = a.lower()
        if a in set(['a', 'i', 'e', 'o', 'u']):
            return 0
        if a.isdigit():
            return 1
        if a.isalpha():
            return 2
    def rule1(i, j):
        return passwords[i].lower() == passwords[j].lower()
    def rule2(i, j):
        pass1 = passwords[i].lower()
        pass2 = passwords[j].lower()
        if pass1.startswith(pass2) or pass2.startswith(pass1):
            return abs(len(pass1)-len(pass2))<=k
        return False
    def rule3(i, j):
        pass1 = passwords[i]
        pass2 = passwords[j]
        diff = []
        if len(pass1) != len(pass2):
            return False
        for x,y in zip(pass1, pass2):
            if x!=y:
                diff.append([x,y])
        if not diff:
            return True
        if len(diff) > 1:
            return False
        return get_class(diff[0][0]) == get_class(diff[0][1])
        
    for i in range(len(passwords)):
        for j in range(i, len(passwords)):
            if i==j:
                continue
            if rule1(i, j) or rule2(i,j) or rule3(i,j):
                res.append((passwords[i],passwords[j]))
    return res
    

# ── Test runner ───────────────────────────────────────────────────────────────

def check(name, passwords, k, expected):
    actual = find_similar(passwords, k)
    actual_set   = set(frozenset(p) for p in actual)
    expected_set = set(frozenset(p) for p in expected)
    if actual_set == expected_set:
        print(f"  PASS  {name}")
    else:
        print(f"  FAIL  {name}")
        print(f"         expected : {sorted(expected)}")
        print(f"         actual   : {sorted(actual)}")

print("Running tests...\n")

# [1] Spec example
check("Spec example",
    ["Hello", "hello", "Hell", "world", "w0rld"], 2,
    [("Hello","hello"), ("Hello","Hell"), ("hello","Hell")])

# [2] Rule 1
check("Rule1: exact case match",   ["abc", "ABC"], 0, [("abc","ABC")])
check("Rule1: mixed case",         ["PassWord", "password"], 0, [("PassWord","password")])
check("Rule1: different words",    ["cat", "dog"], 0, [])

# [3] Rule 2
check("Rule2: prefix diff=1 K=1",          ["cat", "cats"], 1, [("cat","cats")])
check("Rule2: prefix diff=2 K=2",          ["cat", "catch"], 2, [("cat","catch")])
check("Rule2: prefix diff=3 K=2 not similar", ["cat", "catches"], 2, [])
check("Rule2: K=0 no prefix",              ["cat", "cats"], 0, [])
check("Rule2: case-insensitive prefix",    ["HELL", "hello"], 2, [("HELL","hello")])
check("Rule2: both directions",            ["hello", "hell"], 1, [("hello","hell")])
check("Rule2: longer prefix of shorter",   ["cats", "cat"], 1, [("cats","cat")])

# [4] Rule 3
check("Rule3: vowel→vowel",              ["cat", "cot"], 0, [("cat","cot")])
check("Rule3: consonant→consonant",      ["bat", "cat"], 0, [("bat","cat")])
check("Rule3: digit→digit",              ["p1ss", "p2ss"], 0, [("p1ss","p2ss")])
check("Rule3: vowel→digit NOT similar",  ["cat", "c1t"], 0, [])
check("Rule3: vowel→consonant NOT similar", ["cat", "cbt"], 0, [])
check("Rule3: 2 diffs NOT similar",      ["cat", "dot"], 0, [])
check("Rule3: different lengths",        ["cat", "cats"], 0, [])
check("Rule3: o(vowel) vs 0(digit)",     ["world", "w0rld"], 0, [])
check("Rule3: consonant→consonant mid",  ["abc", "acc"], 0, [("abc","acc")])
check("Rule3: vowel→vowel start",        ["Abc", "Ebc"], 0, [("Abc","Ebc")])
check("Rule3: vowel→consonant NOT",      ["abc", "bbc"], 0, [])
check("Rule3: digit→digit",              ["a1c", "a9c"], 0, [("a1c","a9c")])
check("Rule3: 0 diffs caught by Rule1",  ["abc", "abc"], 0, [("abc","abc")])
check("Rule3: wrong digit positions",    ["p1ss", "ps1s"], 0, [])

# [5] Multiple rules
check("Multi: Rule1+Rule2 together",
    ["abc", "ABC", "ab", "xyz"], 1,
    [("abc","ABC"), ("abc","ab"), ("ABC","ab")])

# [6] Edge cases
check("Single password",    ["solo"], 5, [])
check("K=0 no prefix",      ["pre", "prefix"], 0, [])

print("\nDone.")