import { useState, useEffect } from "react";

// ─── Question data: globally sorted by Amazon frequency rank ───────────────
// Each question: [rank, lcNum, title, acceptance, difficulty, category]
const ALL_QUESTIONS = [
  [1,1,"Two Sum","57.2%","Easy","Arrays / Hashing"],
  [2,3,"Longest Substring Without Repeating Characters","38.7%","Medium","Sliding Window / Two Pointers"],
  [3,42,"Trapping Rain Water","67.0%","Hard","Stack / Monotonic Stack"],
  [4,146,"LRU Cache","47.0%","Medium","Design"],
  [5,11,"Container With Most Water","59.7%","Medium","Sliding Window / Two Pointers"],
  [6,2,"Add Two Numbers","48.1%","Medium","Linked List"],
  [7,14,"Longest Common Prefix","47.3%","Easy","String"],
  [8,121,"Best Time to Buy and Sell Stock","56.5%","Easy","Dynamic Programming"],
  [9,5,"Longest Palindromic Substring","37.5%","Medium","Dynamic Programming"],
  [10,15,"3Sum","38.8%","Medium","Sliding Window / Two Pointers"],
  [11,200,"Number of Islands","64.0%","Medium","Graph / BFS / DFS"],
  [12,875,"Koko Eating Bananas","49.8%","Medium","Binary Search"],
  [13,4,"Median of Two Sorted Arrays","46.1%","Hard","Binary Search"],
  [14,56,"Merge Intervals","51.4%","Medium","Sorting / Greedy"],
  [15,49,"Group Anagrams","72.3%","Medium","Arrays / Hashing"],
  [16,23,"Merge k Sorted Lists","59.1%","Hard","Sorting / Greedy"],
  [17,169,"Majority Element","66.2%","Easy","Arrays / Hashing"],
  [18,128,"Longest Consecutive Sequence","47.0%","Medium","Arrays / Hashing"],
  [19,560,"Subarray Sum Equals K","47.0%","Medium","Sorting / Greedy"],
  [20,9,"Palindrome Number","60.4%","Easy","Arrays / Hashing"],
  [21,20,"Valid Parentheses","43.9%","Easy","Stack / Monotonic Stack"],
  [22,22,"Generate Parentheses","78.4%","Medium","Backtracking / Recursion"],
  [24,17,"Letter Combinations of a Phone Number","65.7%","Medium","Backtracking / Recursion"],
  [25,21,"Merge Two Sorted Lists","68.1%","Easy","Linked List"],
  [26,70,"Climbing Stairs","54.0%","Easy","Dynamic Programming"],
  [27,136,"Single Number","77.5%","Easy","Arrays / Hashing"],
  [28,162,"Find Peak Element","46.8%","Medium","Binary Search"],
  [29,994,"Rotting Oranges","58.3%","Medium","Graph / BFS / DFS"],
  [30,33,"Search in Rotated Sorted Array","44.3%","Medium","Binary Search"],
  [31,69,"Sqrt(x)","41.6%","Easy","Binary Search"],
  [32,904,"Fruit Into Baskets","50.7%","Medium","Sliding Window / Two Pointers"],
  [33,41,"First Missing Positive","42.6%","Hard","Arrays / Hashing"],
  [34,53,"Maximum Subarray","53.1%","Medium","Dynamic Programming"],
  [35,236,"Lowest Common Ancestor of a Binary Tree","68.9%","Medium","Trees"],
  [36,239,"Sliding Window Maximum","48.5%","Hard","Sliding Window / Two Pointers"],
  [37,1929,"Concatenation of Array","90.5%","Easy","Arrays / Hashing"],
  [38,79,"Word Search","47.0%","Medium","Backtracking / Recursion"],
  [40,51,"N-Queens","75.1%","Hard","Backtracking / Recursion"],
  [41,88,"Merge Sorted Array","54.5%","Easy","Sorting / Greedy"],
  [43,767,"Reorganize String","56.9%","Medium","Sorting / Greedy"],
  [44,26,"Remove Duplicates from Sorted Array","62.5%","Easy","Arrays / Hashing"],
  [45,35,"Search Insert Position","50.9%","Easy","Binary Search"],
  [47,242,"Valid Anagram","67.9%","Easy","Arrays / Hashing"],
  [48,347,"Top K Frequent Elements","66.1%","Medium","Sorting / Greedy"],
  [49,18,"4Sum","40.2%","Medium","Sliding Window / Two Pointers"],
  [50,28,"Find the Index of the First Occurrence in a String","46.4%","Easy","String"],
  [52,75,"Sort Colors","69.3%","Medium","Sorting / Greedy"],
  [53,78,"Subsets","82.1%","Medium","Backtracking / Recursion"],
  [54,155,"Min Stack","57.9%","Medium","Stack / Monotonic Stack"],
  [55,217,"Contains Duplicate","64.2%","Easy","Arrays / Hashing"],
  [57,31,"Next Permutation","44.9%","Medium","Sorting / Greedy"],
  [58,74,"Search a 2D Matrix","53.7%","Medium","Binary Search"],
  [60,207,"Course Schedule","51.0%","Medium","Graph / BFS / DFS"],
  [61,283,"Move Zeroes","63.7%","Easy","Arrays / Hashing"],
  [64,13,"Roman to Integer","66.4%","Easy","String"],
  [66,36,"Valid Sudoku","64.3%","Medium","Matrix / Grid"],
  [67,62,"Unique Paths","66.7%","Medium","Dynamic Programming"],
  [69,138,"Copy List with Random Pointer","62.6%","Medium","Linked List"],
  [70,143,"Reorder List","64.8%","Medium","Linked List"],
  [72,424,"Longest Repeating Character Replacement","59.2%","Medium","Sliding Window / Two Pointers"],
  [74,6,"Zigzag Conversion","53.7%","Medium","String"],
  [75,19,"Remove Nth Node From End of List","51.2%","Medium","Linked List"],
  [76,45,"Jump Game II","42.6%","Medium","Sorting / Greedy"],
  [77,54,"Spiral Matrix","56.4%","Medium","Matrix / Grid"],
  [78,124,"Binary Tree Maximum Path Sum","42.1%","Hard","Trees"],
  [79,198,"House Robber","53.0%","Medium","Dynamic Programming"],
  [81,735,"Asteroid Collision","47.4%","Medium","Stack / Monotonic Stack"],
  [82,1004,"Max Consecutive Ones III","67.4%","Medium","Sliding Window / Two Pointers"],
  [84,34,"Find First and Last Position of Element in Sorted Array","48.5%","Medium","Binary Search"],
  [86,135,"Candy","48.1%","Hard","Sorting / Greedy"],
  [88,209,"Minimum Size Subarray Sum","51.3%","Medium","Sliding Window / Two Pointers"],
  [89,238,"Product of Array Except Self","68.7%","Medium","Arrays / Hashing"],
  [91,297,"Serialize and Deserialize Binary Tree","60.5%","Hard","Trees"],
  [92,322,"Coin Change","48.1%","Medium","Dynamic Programming"],
  [94,485,"Max Consecutive Ones","64.8%","Easy","Arrays / Hashing"],
  [95,496,"Next Greater Element I","75.9%","Easy","Stack / Monotonic Stack"],
  [98,58,"Length of Last Word","58.5%","Easy","String"],
  [99,76,"Minimum Window Substring","47.1%","Hard","Sliding Window / Two Pointers"],
  [100,98,"Validate Binary Search Tree","35.5%","Medium","Trees"],
  [103,139,"Word Break","49.2%","Medium","Dynamic Programming"],
  [104,151,"Reverse Words in a String","55.8%","Medium","String"],
  [105,199,"Binary Tree Right Side View","69.7%","Medium","Trees"],
  [106,215,"Kth Largest Element in an Array","68.8%","Medium","Sorting / Greedy"],
  [107,253,"Meeting Rooms II","52.6%","Medium","Sorting / Greedy"],
  [108,295,"Find Median from Data Stream","54.3%","Hard","Sorting / Greedy"],
  [109,503,"Next Greater Element II","68.1%","Medium","Stack / Monotonic Stack"],
  [112,39,"Combination Sum","76.2%","Medium","Backtracking / Recursion"],
  [113,46,"Permutations","81.7%","Medium","Backtracking / Recursion"],
  [114,55,"Jump Game","40.6%","Medium","Sorting / Greedy"],
  [115,67,"Add Binary","57.8%","Easy","String"],
  [116,73,"Set Matrix Zeroes","62.6%","Medium","Matrix / Grid"],
  [117,84,"Largest Rectangle in Histogram","49.5%","Hard","Stack / Monotonic Stack"],
  [118,122,"Best Time to Buy and Sell Stock II","70.9%","Medium","Dynamic Programming"],
  [119,134,"Gas Station","47.7%","Medium","Sorting / Greedy"],
  [121,206,"Reverse Linked List","80.4%","Easy","Linked List"],
  [123,543,"Diameter of Binary Tree","65.2%","Easy","Trees"],
  [125,621,"Task Scheduler","62.8%","Medium","Sorting / Greedy"],
  [127,658,"Find K Closest Elements","49.5%","Medium","Binary Search"],
  [128,852,"Peak Index in a Mountain Array","66.9%","Medium","Binary Search"],
  [129,1011,"Capacity To Ship Packages Within D Days","73.6%","Medium","Binary Search"],
  [130,32,"Longest Valid Parentheses","38.3%","Hard","Stack / Monotonic Stack"],
  [134,212,"Word Search II","38.2%","Hard","Backtracking / Recursion"],
  [136,410,"Split Array Largest Sum","60.0%","Hard","Dynamic Programming"],
  [139,696,"Count Binary Substrings","70.3%","Easy","String"],
  [140,739,"Daily Temperatures","68.5%","Medium","Stack / Monotonic Stack"],
  [145,987,"Vertical Order Traversal of a Binary Tree","53.4%","Hard","Trees"],
  [155,219,"Contains Duplicate II","51.0%","Easy","Arrays / Hashing"],
  [157,240,"Search a 2D Matrix II","57.0%","Medium","Matrix / Grid"],
  [158,300,"Longest Increasing Subsequence","59.2%","Medium","Dynamic Programming"],
  [162,567,"Permutation in String","48.6%","Medium","Sliding Window / Two Pointers"],
  [163,931,"Minimum Falling Path Sum","60.8%","Medium","Dynamic Programming"],
  [164,981,"Time Based Key-Value Store","49.8%","Medium","Design"],
  [167,1423,"Maximum Points You Can Obtain from Cards","57.4%","Medium","Sliding Window / Two Pointers"],
  [171,1482,"Minimum Number of Days to Make m Bouquets","56.4%","Medium","Binary Search"],
  [178,72,"Edit Distance","60.3%","Medium","Dynamic Programming"],
  [181,131,"Palindrome Partitioning","73.8%","Medium","Backtracking / Recursion"],
  [182,133,"Clone Graph","64.9%","Medium","Graph / BFS / DFS"],
  [184,152,"Maximum Product Subarray","36.1%","Medium","Dynamic Programming"],
  [185,179,"Largest Number","42.7%","Medium","Sorting / Greedy"],
  [189,312,"Burst Balloons","63.1%","Hard","Dynamic Programming"],
  [193,547,"Number of Provinces","70.1%","Medium","Graph / BFS / DFS"],
  [200,863,"All Nodes Distance K in Binary Tree","67.5%","Medium","Trees"],
  [207,29,"Divide Two Integers","19.5%","Medium","Arrays / Hashing"],
  [209,57,"Insert Interval","44.9%","Medium","Sorting / Greedy"],
  [210,63,"Unique Paths II","44.3%","Medium","Dynamic Programming"],
  [211,64,"Minimum Path Sum","68.0%","Medium","Dynamic Programming"],
  [213,92,"Reverse Linked List II","51.2%","Medium","Linked List"],
  [214,99,"Recover Binary Search Tree","59.1%","Medium","Trees"],
  [217,130,"Surrounded Regions","44.9%","Medium","Graph / BFS / DFS"],
  [219,140,"Word Break II","55.2%","Hard","Dynamic Programming"],
  [223,210,"Course Schedule II","55.1%","Medium","Graph / BFS / DFS"],
  [225,226,"Invert Binary Tree","79.9%","Easy","Trees"],
  [226,235,"Lowest Common Ancestor of a BST","70.2%","Medium","Trees"],
  [230,315,"Count of Smaller Numbers After Self","43.4%","Hard","Sorting / Greedy"],
  [233,416,"Partition Equal Subset Sum","49.3%","Medium","Dynamic Programming"],
  [234,417,"Pacific Atlantic Water Flow","60.7%","Medium","Graph / BFS / DFS"],
  [235,443,"String Compression","59.7%","Medium","String"],
  [238,460,"LFU Cache","48.8%","Hard","Design"],
  [239,518,"Coin Change II","60.3%","Medium","Dynamic Programming"],
  [241,595,"Big Countries","68.4%","Easy","SQL / Database"],
  [242,721,"Accounts Merge","61.0%","Medium","Graph / BFS / DFS"],
  [248,1008,"Construct BST from Preorder Traversal","84.1%","Medium","Trees"],
  [249,1091,"Shortest Path in Binary Matrix","51.2%","Medium","Graph / BFS / DFS"],
  [252,1382,"Balance a Binary Search Tree","86.3%","Medium","Trees"],
  [255,2385,"Amount of Time for Binary Tree to Be Infected","65.2%","Medium","Trees"],
  [259,24,"Swap Nodes in Pairs","69.1%","Medium","Linked List"],
  [260,37,"Sudoku Solver","65.4%","Hard","Backtracking / Recursion"],
  [261,59,"Spiral Matrix II","74.8%","Medium","Matrix / Grid"],
  [263,91,"Decode Ways","37.7%","Medium","Dynamic Programming"],
  [266,102,"Binary Tree Level Order Traversal","72.3%","Medium","Trees"],
  [267,103,"Binary Tree Zigzag Level Order Traversal","63.3%","Medium","Trees"],
  [268,104,"Maximum Depth of Binary Tree","78.0%","Easy","Trees"],
  [274,177,"Nth Highest Salary","38.9%","Medium","SQL / Database"],
  [275,178,"Rank Scores","67.4%","Medium","SQL / Database"],
  [280,221,"Maximal Square","50.1%","Medium","Dynamic Programming"],
  [283,269,"Alien Dictionary","37.1%","Hard","Graph / BFS / DFS"],
  [285,329,"Longest Increasing Path in a Matrix","56.4%","Hard","Matrix / Grid"],
  [291,392,"Is Subsequence","48.9%","Easy","String"],
  [292,394,"Decode String","62.4%","Medium","Stack / Monotonic Stack"],
  [293,402,"Remove K Digits","36.5%","Medium","Stack / Monotonic Stack"],
  [298,528,"Random Pick with Weight","49.0%","Medium","Design"],
  [306,704,"Binary Search","60.6%","Easy","Binary Search"],
  [310,827,"Making A Large Island","56.4%","Hard","Graph / BFS / DFS"],
  [311,853,"Car Fleet","54.9%","Medium","Stack / Monotonic Stack"],
  [317,1209,"Remove All Adjacent Duplicates in String II","61.1%","Medium","Stack / Monotonic Stack"],
  [318,1235,"Maximum Profit in Job Scheduling","54.7%","Hard","Dynamic Programming"],
  [321,1319,"Number of Operations to Make Network Connected","66.3%","Medium","Graph / BFS / DFS"],
  [322,1339,"Maximum Product of Splitted Binary Tree","55.7%","Medium","Trees"],
  [374,442,"Find All Duplicates in an Array","76.8%","Medium","Arrays / Hashing"],
];

// ─── Category metadata ──────────────────────────────────────────────────────
const CAT_META = {
  "Arrays / Hashing":             { count: 22, color: "#636EFA", emoji: "🗂️" },
  "Dynamic Programming":          { count: 16, color: "#EF553B", emoji: "📐" },
  "Sliding Window / Two Pointers":{ count: 9,  color: "#AB63FA", emoji: "🪟" },
  "Stack / Monotonic Stack":      { count: 9,  color: "#B6E880", emoji: "📚" },
  "Sorting / Greedy":             { count: 9,  color: "#FECB52", emoji: "🔢" },
  "Binary Search":                { count: 8,  color: "#00CC96", emoji: "🔍" },
  "Trees":                        { count: 8,  color: "#19D3F3", emoji: "🌳" },
  "Graph / BFS / DFS":            { count: 7,  color: "#FF6692", emoji: "🕸️" },
  "String":                       { count: 7,  color: "#72B7B2", emoji: "🔤" },
  "Linked List":                  { count: 5,  color: "#FFA15A", emoji: "🔗" },
  "Backtracking / Recursion":     { count: 5,  color: "#FF97FF", emoji: "🔄" },
  "Matrix / Grid":                { count: 5,  color: "#E45756", emoji: "🔲" },
  "Design":                       { count: 4,  color: "#54A24B", emoji: "⚙️" },
  "SQL / Database":               { count: 3,  color: "#8C8C8C", emoji: "🗄️" },
};

const DIFFICULTY_COLOR = { Easy: "#00b8a3", Medium: "#ffc01e", Hard: "#ff375f" };
const DIFFICULTY_BG    = { Easy: "#003d37", Medium: "#3d2f00", Hard: "#3d0010" };

// ─── Build quiz sequence: global rank order (questions already sorted) ───────
// We keep global frequency order so most-asked questions come first naturally.
// Category coverage is implicit: high-freq categories dominate early rounds.
const QUIZ_SEQUENCE = [...ALL_QUESTIONS].sort((a, b) => a[0] - b[0]);

const TOTAL = QUIZ_SEQUENCE.length;
const PER_BATCH = 5;

// ─── Hints / approaches per LC number ───────────────────────────────────────
const HINTS = {
  1:   "Use a hash map to store (target - num) as you iterate. O(n).",
  3:   "Sliding window with a set; expand right, shrink left when duplicate found.",
  42:  "Use a monotonic stack. For each bar, pop when current > top and compute trapped water.",
  146: "Combine HashMap + doubly-linked list. Head=LRU, Tail=MRU.",
  11:  "Two pointers from both ends. Move the shorter side inward.",
  2:   "Traverse both lists simultaneously with a carry variable.",
  14:  "Compare characters column by column across all strings. Stop at first mismatch.",
  121: "Track min price seen so far; update max profit = price - minPrice.",
  5:   "Expand around center for each character (and each pair). O(n²). Or Manacher O(n).",
  15:  "Sort first. Fix one element, use two pointers for the other two. Skip duplicates.",
  200: "BFS/DFS from each unvisited '1', mark all connected land as visited.",
  875: "Binary search on eating speed k in range [1, max(piles)]. Check feasibility.",
  4:   "Binary search on the smaller array. Partition both arrays so left half has (m+n)/2 elements.",
  56:  "Sort by start time. Merge when current.start ≤ prev.end.",
  49:  "Sort each word's characters as key → group by key in a HashMap.",
  23:  "Use a min-heap of (val, listNode). Pop min, push next node.",
  169: "Boyer–Moore Voting: candidate + count. If count=0 pick new candidate.",
  128: "Put all nums in a set. For each num where num-1 not in set, count streak forward.",
  560: "Prefix sum + HashMap. Count how many prefix sums equal (currentSum - k).",
  9:   "Reverse second half of digits and compare with first half.",
  20:  "Stack: push open brackets, pop and match on close brackets.",
  22:  "Backtrack: add '(' if open < n, add ')' if close < open.",
  17:  "Backtrack: map each digit to letters, build combinations character by character.",
  21:  "Compare heads, attach smaller, recurse.",
  70:  "dp[i] = dp[i-1] + dp[i-2]. Base: dp[1]=1, dp[2]=2.",
  136: "XOR all numbers. Pairs cancel out, leaving the single number.",
  162: "Binary search: if mid > mid+1, peak is in left half; else right half.",
  994: "Multi-source BFS from all rotten oranges simultaneously.",
  33:  "Binary search: determine which half is sorted, check if target is in that half.",
  69:  "Binary search for floor(sqrt(x)). Use long to avoid overflow.",
  904: "Sliding window with a count map of at most 2 fruit types.",
  41:  "Cycle sort / index marking. After placing all positives, scan for first missing.",
  53:  "Kadane's: dp[i] = max(num, dp[i-1]+num). Track running max.",
  236: "Recurse: if root==p or root==q return root. LCA is where left and right are both non-null.",
  239: "Monotonic deque of indices. Remove front if out of window; remove back if ≤ current.",
  1929:"Simply double the array: return nums + nums.",
  79:  "DFS + backtracking. Mark visited in-place with '#', restore after.",
  51:  "Backtrack row by row. Track column, diagonal, anti-diagonal sets for validity.",
  88:  "Start from the end of both arrays, place larger element at end of merged array.",
  767: "Max-heap by frequency. Greedily pick most frequent that differs from last placed.",
  26:  "Two pointers: slow tracks unique count, fast scans ahead.",
  35:  "Standard binary search. Return lo if not found.",
  242: "Sort both strings and compare, or use a character count array.",
  347: "Bucket sort by frequency (O(n)) or min-heap of size k.",
  18:  "Sort. Fix two outer pointers, use two-pointer for inner pair. Skip duplicates.",
  28:  "KMP or built-in find. Know how to explain KMP failure table.",
  75:  "Dutch National Flag: three-way partition with lo/mid/hi pointers.",
  78:  "Bit masking (2^n subsets) or backtrack including/excluding each element.",
  155: "Two stacks: main + min-stack (push to min when ≤ current min).",
  217: "Put into a set; return true if size < length.",
  31:  "Find rightmost ascending pair, find next greater from right, swap, reverse suffix.",
  74:  "Binary search treating 2D matrix as 1D: mid = row*n + col.",
  207: "Topological sort (Kahn's BFS or DFS cycle detection with 3 states).",
  283: "Two pointers: fill non-zeros from front, then fill rest with zeros.",
  13:  "Map symbols to values; add value, but subtract 2*prev if current > prev.",
  36:  "Three sets (row, col, box). Box index = (r/3)*3 + c/3.",
  62:  "dp[i][j] = dp[i-1][j] + dp[i][j-1]. Or combinatorics: C(m+n-2, m-1).",
  138: "Two passes: first create all nodes in a map, second wire .next and .random.",
  143: "Find middle (slow/fast), reverse second half, merge two halves.",
  424: "Sliding window: window is valid when (window_len - maxFreq) ≤ k.",
  6:   "Assign each char to row index using zigzag pattern, then concatenate rows.",
  19:  "Two pointers: advance fast by n+1 steps, then move both until fast reaches null.",
  45:  "Greedy BFS: track current reach and next reach. Increment jumps when reaching boundary.",
  54:  "Simulate with direction array. Shrink boundaries after each direction.",
  124: "DFS. At each node: gain = max(0, left) + max(0, right) + val. Track global max.",
  198: "dp[i] = max(dp[i-2]+nums[i], dp[i-1]).",
  735: "Stack: for each asteroid, resolve collisions. Negative destroys positive top.",
  1004:"Sliding window: count zeros in window; when zeros > k, shrink left.",
  34:  "Two binary searches: one for leftmost, one for rightmost position.",
  135: "Two passes: left-to-right (enforce left < right rule), right-to-left (enforce right < left rule).",
  209: "Sliding window: shrink from left while sum ≥ target, track min length.",
  238: "Two passes: left products then right products. No division needed.",
  297: "BFS/DFS with string encoding. Use '#' for null nodes during serialization.",
  322: "dp[i] = min(dp[i - coin] + 1) for all coins. dp[0]=0, rest=infinity.",
  485: "Single pass: count consecutive ones, update max.",
  496: "Monotonic stack + HashMap. Process from right to left.",
  58:  "Trim trailing spaces, scan from right until space found.",
  76:  "Sliding window with character count map. Expand right; when valid, shrink left.",
  98:  "DFS with min/max bounds. Each node must satisfy min < val < max.",
  139: "dp[i] = true if any dp[j] is true and word[j..i] is in dict.",
  151: "Split by spaces, filter empties, reverse array, join with single space.",
  199: "BFS level order. At each level, record the last node's value.",
  215: "QuickSelect (O(n) avg) or min-heap of size k.",
  253: "Sort meetings. Use min-heap of end times. Overlap when heap.top ≤ start.",
  295: "Two heaps: max-heap for lower half, min-heap for upper half. Balance sizes.",
  503: "Monotonic stack with circular trick: iterate 2n times using mod.",
  39:  "Backtrack: try each candidate from current index (allow reuse). Prune when sum > target.",
  46:  "Backtrack: swap current index with each subsequent index, recurse, swap back.",
  55:  "Greedy: track furthest reachable index. Return false if you're stuck.",
  67:  "Simulate binary addition from right to left with carry.",
  73:  "Record which rows/cols have zeros in first pass; zero them in second pass.",
  84:  "Monotonic stack: for each bar, pop and compute area using current index as right boundary.",
  122: "Greedy: capture every upward price movement.",
  134: "Greedy: start from station 0. If total gas ≥ total cost, solution exists. Track start.",
  206: "Iterative: prev→curr→next pointer dance. Or recursive.",
  543: "DFS: depth at each node = 1 + max(left, right). Diameter = max(left+right).",
  621: "Count frequencies. Max freq element + gaps. Answer = max(n, (maxFreq-1)*(k+1)+countOfMaxFreq).",
  658: "Binary search for left boundary. Then take k elements starting from there.",
  852: "Binary search: if mid < mid+1, peak is to the right.",
  1011:"Binary search on capacity. Check if all packages ship within D days.",
  32:  "Stack of indices. Push -1 first as base. Pop on ')' and compute width.",
  212: "Trie + DFS on board. Prune visited paths. Remove matched words from trie.",
  410: "Binary search on answer (max sum). Check if we can split into ≤ m subarrays.",
  739: "Monotonic stack of indices. Pop when hotter day found; record distance.",
  987: "DFS collecting (col, depth, val) tuples. Sort by col, then depth, then val.",
  300: "dp[i] = 1 + max(dp[j] for j<i where nums[j]<nums[i]). O(n²) or patience sort O(n log n).",
  981: "HashMap of key → sorted list of (timestamp, value). Binary search on timestamps.",
  1423:"Sliding window: total sum - minimum window of (n-k) elements.",
  1482:"Binary search on days. Check if we can make m bouquets in given days.",
  72:  "dp[i][j] = edit distance between word1[:i] and word2[:j]. Three operations.",
  131: "Backtrack: check if substring is palindrome, if so recurse from next index.",
  133: "BFS/DFS with HashMap<original, clone>. Clone neighbors recursively.",
  152: "Track max and min product (negatives can flip). dp[i] max/min = best of 3 options.",
  179: "Custom comparator: compare a+b vs b+a as strings.",
  312: "dp[i][j] = max coins from bursting all balloons between i and j (exclusive).",
  547: "Union-Find or DFS. Count connected components.",
  57:  "Find insert position with binary search. Merge with neighbors if overlapping.",
  63:  "dp[i][j] = dp[i-1][j] + dp[i][j-1] (skip if obstacle).",
  64:  "dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1]).",
  92:  "Find the (m-1)th and (n+1)th nodes. Reverse between them.",
  99:  "Morris traversal or DFS inorder. Find two swapped nodes; swap their values.",
  130: "DFS/BFS from border 'O' cells, mark as safe. Flip remaining 'O' to 'X'.",
  140: "Backtrack with memoization. Or dp[i] = list of valid sentences from index i.",
  210: "Topological sort (Kahn's). Return order only if all nodes are visited.",
  226: "Swap left and right children at every node recursively.",
  235: "BST property: if both < root go left, both > root go right, else root is LCA.",
  315: "Merge sort or BIT/Fenwick tree. Count inversions.",
  416: "0/1 knapsack: dp[j] = can we make sum j using subset of nums.",
  417: "BFS/DFS from Pacific border and Atlantic border separately. Return intersection.",
  443: "Two pointers: read pointer scans, write pointer compresses in-place.",
  460: "HashMap + doubly-linked list + frequency map. Maintain min frequency.",
  518: "Unbounded knapsack: dp[j] += dp[j - coin].",
  721: "Union-Find: merge accounts by email. Group all emails per component.",
  1091:"BFS from (0,0). Track shortest path to (n-1,n-1).",
  1382:"In-order traversal to get sorted array, then build balanced BST recursively.",
  2385:"BFS from infected node. Track time = max distance to any node.",
  24:  "For each pair: prev.next = second, second.next = first, first.next = next pair.",
  37:  "Backtrack: find next empty cell, try 1-9, validate, recurse.",
  59:  "Simulate spiral: shrink top/bottom/left/right boundaries after each direction.",
  91:  "dp[i] = dp[i-1] (single digit) + dp[i-2] (if valid two digits). Watch '0' and '26'.",
  102: "BFS with queue. Process level by level, recording each level's values.",
  103: "BFS level order + alternate direction using a flag per level.",
  104: "Recursive: 1 + max(height(left), height(right)). Base: null → 0.",
  221: "dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1 if cell is '1'.",
  269: "Topological sort. Build graph from adjacent differing characters in sorted words.",
  285: "DFS + memoization on grid. dp[r][c] = longest path starting from (r,c).",
  392: "Two pointers: advance subseq pointer when characters match.",
  394: "Stack-based: push multiplier and current string on '[', pop and repeat on ']'.",
  402: "Monotonic stack: maintain increasing sequence, remove k larger elements.",
  704: "Classic binary search: lo=0, hi=n-1, mid=(lo+hi)/2.",
  827: "Union-Find or BFS. Find largest island, then for each water cell check adjacent islands.",
  853: "Simulate: stack of car fleet speeds. If car catches fleet ahead, merge.",
  1209:"Stack: push (char, count). If count==k, pop.",
  1235:"dp + binary search. Sort by end time. dp[i] = max profit ending at job i.",
  1319:"Union-Find. After connecting all edges, check if components == 1. Need at least n-1 edges.",
  1339:"DFS: for each subtree, product = subtreeSum * (totalSum - subtreeSum). Find max.",
  442: "For each num, negate nums[|num|-1] to mark visited. Duplicates have already-negative index.",
};

// ─── Main App ────────────────────────────────────────────────────────────────
export default function AmazonQuiz() {
  const [answered, setAnswered] = useState({}); // { rank: 'solved'|'unsolved'|'skip' }
  const [batchIdx, setBatchIdx] = useState(0);  // which batch of 5 we're on
  const [showHint, setShowHint] = useState({}); // { rank: true/false }
  const [view, setView] = useState("quiz");     // 'quiz' | 'progress'
  const [filter, setFilter] = useState("all");  // 'all' | 'unsolved' | 'solved' | 'skip'

  // Questions not yet answered (for "remaining" count)
  const unanswered = QUIZ_SEQUENCE.filter(q => !answered[q[0]]);
  const currentBatch = QUIZ_SEQUENCE.slice(batchIdx * PER_BATCH, (batchIdx + 1) * PER_BATCH);
  const totalBatches = Math.ceil(TOTAL / PER_BATCH);

  const mark = (rank, status) => {
    setAnswered(prev => ({ ...prev, [rank]: status }));
  };

  const toggleHint = (rank) => {
    setShowHint(prev => ({ ...prev, [rank]: !prev[rank] }));
  };

  const allBatchAnswered = currentBatch.every(q => answered[q[0]]);

  // Progress stats
  const solved = Object.values(answered).filter(v => v === "solved").length;
  const unsolved = Object.values(answered).filter(v => v === "unsolved").length;
  const skipped = Object.values(answered).filter(v => v === "skip").length;
  const total_done = solved + unsolved + skipped;
  const pct = Math.round((total_done / TOTAL) * 100);

  // Category progress
  const catProgress = {};
  Object.keys(CAT_META).forEach(cat => {
    const qs = QUIZ_SEQUENCE.filter(q => q[5] === cat);
    catProgress[cat] = {
      total: qs.length,
      solved: qs.filter(q => answered[q[0]] === "solved").length,
      unsolved: qs.filter(q => answered[q[0]] === "unsolved").length,
      skip: qs.filter(q => answered[q[0]] === "skip").length,
    };
  });

  // 5-day plan estimate
  const qPerDay = Math.ceil(TOTAL / 5);
  const currentDay = Math.min(5, Math.floor(total_done / qPerDay) + 1);

  const styles = {
    app: {
      minHeight: "100vh",
      background: "linear-gradient(135deg, #0f1117 0%, #1a1d27 100%)",
      color: "#e0e0e0",
      fontFamily: "'Segoe UI', Arial, sans-serif",
      padding: "0",
    },
    header: {
      background: "#1a1d27",
      borderBottom: "1px solid #2a2d3a",
      padding: "16px 24px",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      flexWrap: "wrap",
      gap: "12px",
      position: "sticky",
      top: 0,
      zIndex: 100,
    },
    title: {
      fontSize: "1.2rem",
      fontWeight: 700,
      color: "#fff",
      display: "flex",
      alignItems: "center",
      gap: "8px",
    },
    navBtn: (active) => ({
      padding: "6px 16px",
      borderRadius: "20px",
      border: "none",
      cursor: "pointer",
      fontWeight: 600,
      fontSize: "0.85rem",
      background: active ? "#636EFA" : "#252836",
      color: active ? "#fff" : "#aaa",
      transition: "all 0.2s",
    }),
    progressBar: {
      background: "#252836",
      borderRadius: "8px",
      height: "6px",
      width: "180px",
      overflow: "hidden",
    },
    progressFill: {
      height: "100%",
      background: "linear-gradient(90deg, #636EFA, #EF553B)",
      borderRadius: "8px",
      transition: "width 0.4s",
      width: `${pct}%`,
    },
    main: {
      maxWidth: "860px",
      margin: "0 auto",
      padding: "24px 16px",
    },
    batchNav: {
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      marginBottom: "20px",
      background: "#1a1d27",
      borderRadius: "12px",
      padding: "14px 20px",
    },
    batchInfo: {
      fontSize: "0.9rem",
      color: "#aaa",
    },
    card: {
      background: "#1a1d27",
      borderRadius: "14px",
      padding: "20px",
      marginBottom: "14px",
      border: "1px solid #2a2d3a",
      transition: "border-color 0.2s",
    },
    cardAnswered: (status) => ({
      borderColor: status === "solved" ? "#00b8a340" : status === "unsolved" ? "#ff375f40" : "#ffc01e40",
      background: status === "solved" ? "#0f2a27" : status === "unsolved" ? "#2a0f13" : "#2a2008",
    }),
    qHeader: {
      display: "flex",
      alignItems: "center",
      gap: "10px",
      marginBottom: "12px",
      flexWrap: "wrap",
    },
    rankBadge: {
      background: "#252836",
      padding: "2px 8px",
      borderRadius: "6px",
      fontSize: "0.75rem",
      color: "#888",
      fontWeight: 600,
    },
    lcBadge: {
      background: "#636EFA22",
      color: "#636EFA",
      padding: "2px 8px",
      borderRadius: "6px",
      fontSize: "0.75rem",
      fontWeight: 700,
    },
    diffBadge: (d) => ({
      background: DIFFICULTY_BG[d],
      color: DIFFICULTY_COLOR[d],
      padding: "2px 10px",
      borderRadius: "6px",
      fontSize: "0.75rem",
      fontWeight: 600,
    }),
    catBadge: (cat) => ({
      background: CAT_META[cat]?.color + "22",
      color: CAT_META[cat]?.color,
      padding: "2px 10px",
      borderRadius: "6px",
      fontSize: "0.72rem",
      fontWeight: 600,
    }),
    qTitle: {
      fontSize: "1.05rem",
      fontWeight: 700,
      color: "#fff",
      marginBottom: "14px",
      lineHeight: 1.4,
    },
    acceptRow: {
      fontSize: "0.78rem",
      color: "#777",
      marginBottom: "14px",
    },
    actionRow: {
      display: "flex",
      gap: "8px",
      flexWrap: "wrap",
      alignItems: "center",
    },
    btn: (type) => {
      const colors = {
        solved: { bg: "#003d37", border: "#00b8a3", text: "#00b8a3", hbg: "#004d47" },
        unsolved: { bg: "#3d0010", border: "#ff375f", text: "#ff375f", hbg: "#4d0015" },
        skip: { bg: "#3d3200", border: "#ffc01e", text: "#ffc01e", hbg: "#4d3f00" },
        hint: { bg: "#1e2030", border: "#636EFA", text: "#636EFA", hbg: "#252840" },
        lc: { bg: "#1e2030", border: "#FFA15A", text: "#FFA15A", hbg: "#252840" },
      };
      const c = colors[type];
      return {
        padding: "7px 16px",
        borderRadius: "8px",
        border: `1px solid ${c.border}`,
        background: c.bg,
        color: c.text,
        cursor: "pointer",
        fontSize: "0.82rem",
        fontWeight: 600,
        transition: "background 0.15s",
      };
    },
    hintBox: {
      marginTop: "12px",
      background: "#252836",
      borderRadius: "10px",
      padding: "12px 16px",
      borderLeft: "3px solid #636EFA",
      fontSize: "0.85rem",
      color: "#ccc",
      lineHeight: 1.6,
    },
    statusIcon: (status) => ({
      fontSize: "1.1rem",
      marginLeft: "auto",
    }),
    progressSection: {
      marginBottom: "28px",
    },
    sectionTitle: {
      fontSize: "1rem",
      fontWeight: 700,
      color: "#fff",
      marginBottom: "14px",
    },
    statsGrid: {
      display: "grid",
      gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))",
      gap: "12px",
      marginBottom: "20px",
    },
    statCard: (color) => ({
      background: "#1a1d27",
      borderRadius: "12px",
      padding: "16px",
      border: `1px solid ${color}33`,
      textAlign: "center",
    }),
    statNum: (color) => ({
      fontSize: "2rem",
      fontWeight: 800,
      color: color,
    }),
    statLabel: {
      fontSize: "0.78rem",
      color: "#777",
      marginTop: "4px",
    },
    catRow: {
      background: "#1a1d27",
      borderRadius: "10px",
      padding: "12px 16px",
      marginBottom: "8px",
      border: "1px solid #2a2d3a",
    },
    catRowHeader: {
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      marginBottom: "8px",
    },
    catBarOuter: {
      background: "#252836",
      borderRadius: "4px",
      height: "6px",
      overflow: "hidden",
    },
    dayPlan: {
      background: "#1a1d27",
      borderRadius: "12px",
      padding: "16px 20px",
      border: "1px solid #2a2d3a",
      marginBottom: "20px",
    },
  };

  if (view === "progress") {
    return (
      <div style={styles.app}>
        <div style={styles.header}>
          <div style={styles.title}>
            <span>🚀</span> Amazon Interview Quiz
          </div>
          <div style={{ display: "flex", gap: "8px", alignItems: "center" }}>
            <button style={styles.navBtn(false)} onClick={() => setView("quiz")}>📝 Quiz</button>
            <button style={styles.navBtn(true)}>📊 Progress</button>
            <div>
              <div style={styles.progressBar}><div style={styles.progressFill} /></div>
              <div style={{ fontSize: "0.7rem", color: "#777", textAlign: "center", marginTop: "2px" }}>
                {pct}% done
              </div>
            </div>
          </div>
        </div>
        <div style={styles.main}>
          <div style={styles.progressSection}>
            <div style={styles.dayPlan}>
              <div style={{ fontSize: "0.85rem", color: "#aaa", marginBottom: "8px" }}>
                📅 5-Day Plan — ~{qPerDay} questions/day
              </div>
              <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
                {[1,2,3,4,5].map(day => {
                  const dayStart = (day - 1) * qPerDay;
                  const dayEnd = Math.min(day * qPerDay, TOTAL);
                  const dayQs = QUIZ_SEQUENCE.slice(dayStart, dayEnd);
                  const daySolved = dayQs.filter(q => answered[q[0]]).length;
                  const isDone = daySolved === dayQs.length;
                  const isCurrent = day === currentDay;
                  return (
                    <div key={day} style={{
                      flex: "1 1 80px",
                      background: isDone ? "#0f2a27" : isCurrent ? "#252836" : "#1e2030",
                      border: `1px solid ${isDone ? "#00b8a3" : isCurrent ? "#636EFA" : "#2a2d3a"}`,
                      borderRadius: "10px",
                      padding: "10px",
                      textAlign: "center",
                    }}>
                      <div style={{ fontSize: "0.8rem", fontWeight: 700, color: isDone ? "#00b8a3" : isCurrent ? "#636EFA" : "#aaa" }}>
                        {isDone ? "✅" : isCurrent ? "⚡" : "📋"} Day {day}
                      </div>
                      <div style={{ fontSize: "1.1rem", fontWeight: 800, color: "#fff", marginTop: "4px" }}>
                        {daySolved}/{dayQs.length}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
            <div style={styles.statsGrid}>
              <div style={styles.statCard("#00b8a3")}>
                <div style={styles.statNum("#00b8a3")}>{solved}</div>
                <div style={styles.statLabel}>✅ Solved</div>
              </div>
              <div style={styles.statCard("#ff375f")}>
                <div style={styles.statNum("#ff375f")}>{unsolved}</div>
                <div style={styles.statLabel}>❌ Need Review</div>
              </div>
              <div style={styles.statCard("#ffc01e")}>
                <div style={styles.statNum("#ffc01e")}>{skipped}</div>
                <div style={styles.statLabel}>⏭️ Skipped</div>
              </div>
              <div style={styles.statCard("#636EFA")}>
                <div style={styles.statNum("#636EFA")}>{TOTAL - total_done}</div>
                <div style={styles.statLabel}>⏳ Remaining</div>
              </div>
            </div>
          </div>

          <div style={styles.sectionTitle}>Category Progress</div>
          {Object.entries(CAT_META)
            .sort((a,b) => b[1].count - a[1].count)
            .map(([cat, meta]) => {
              const cp = catProgress[cat];
              const donePct = cp.total > 0 ? Math.round(((cp.solved + cp.unsolved + cp.skip) / cp.total) * 100) : 0;
              const solvedPct = cp.total > 0 ? Math.round((cp.solved / cp.total) * 100) : 0;
              return (
                <div key={cat} style={styles.catRow}>
                  <div style={styles.catRowHeader}>
                    <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                      <span>{meta.emoji}</span>
                      <span style={{ fontWeight: 600, fontSize: "0.9rem" }}>{cat}</span>
                    </div>
                    <div style={{ display: "flex", gap: "10px", fontSize: "0.78rem", color: "#888" }}>
                      <span style={{ color: "#00b8a3" }}>{cp.solved}✓</span>
                      <span style={{ color: "#ff375f" }}>{cp.unsolved}✗</span>
                      <span style={{ color: "#ffc01e" }}>{cp.skip}⏭</span>
                      <span>/ {cp.total}</span>
                    </div>
                  </div>
                  <div style={styles.catBarOuter}>
                    <div style={{
                      height: "100%",
                      width: `${donePct}%`,
                      background: `linear-gradient(90deg, ${meta.color}, ${meta.color}88)`,
                      borderRadius: "4px",
                      transition: "width 0.4s",
                    }} />
                  </div>
                  <div style={{ fontSize: "0.72rem", color: "#666", marginTop: "4px" }}>
                    {donePct}% covered · {solvedPct}% solved
                  </div>
                </div>
              );
            })}
        </div>
      </div>
    );
  }

  // Quiz view
  return (
    <div style={styles.app}>
      <div style={styles.header}>
        <div style={styles.title}>
          <span>🚀</span> Amazon Interview Quiz
          <span style={{ fontSize: "0.8rem", color: "#888", fontWeight: 400 }}>
            Top {TOTAL} questions by frequency
          </span>
        </div>
        <div style={{ display: "flex", gap: "8px", alignItems: "center", flexWrap: "wrap" }}>
          <button style={styles.navBtn(true)}>📝 Quiz</button>
          <button style={styles.navBtn(false)} onClick={() => setView("progress")}>📊 Progress</button>
          <div>
            <div style={styles.progressBar}><div style={styles.progressFill} /></div>
            <div style={{ fontSize: "0.7rem", color: "#777", textAlign: "center", marginTop: "2px" }}>
              {total_done}/{TOTAL} done ({pct}%)
            </div>
          </div>
        </div>
      </div>

      <div style={styles.main}>
        {/* Batch navigation */}
        <div style={styles.batchNav}>
          <div>
            <div style={{ fontWeight: 700, fontSize: "1rem", color: "#fff" }}>
              Batch {batchIdx + 1} of {totalBatches}
            </div>
            <div style={styles.batchInfo}>
              Questions #{batchIdx * PER_BATCH + 1}–{Math.min((batchIdx + 1) * PER_BATCH, TOTAL)} by Amazon frequency rank
            </div>
          </div>
          <div style={{ display: "flex", gap: "8px" }}>
            <button
              style={{
                ...styles.btn("hint"),
                opacity: batchIdx === 0 ? 0.3 : 1,
                cursor: batchIdx === 0 ? "not-allowed" : "pointer",
              }}
              onClick={() => batchIdx > 0 && setBatchIdx(b => b - 1)}
            >← Prev</button>
            <button
              style={{
                ...styles.btn("solved"),
                opacity: batchIdx >= totalBatches - 1 ? 0.3 : 1,
                cursor: batchIdx >= totalBatches - 1 ? "not-allowed" : "pointer",
              }}
              onClick={() => batchIdx < totalBatches - 1 && setBatchIdx(b => b + 1)}
            >Next →</button>
          </div>
        </div>

        {/* Category mix info for this batch */}
        <div style={{
          background: "#1a1d2799",
          borderRadius: "10px",
          padding: "10px 16px",
          marginBottom: "18px",
          fontSize: "0.8rem",
          color: "#888",
          display: "flex",
          flexWrap: "wrap",
          gap: "8px",
          alignItems: "center",
        }}>
          <span>🎯 This batch covers:</span>
          {[...new Set(currentBatch.map(q => q[5]))].map(cat => (
            <span key={cat} style={styles.catBadge(cat)}>
              {CAT_META[cat]?.emoji} {cat}
            </span>
          ))}
        </div>

        {/* Question cards */}
        {currentBatch.map((q, idx) => {
          const [rank, lcNum, title, acceptance, difficulty, category] = q;
          const status = answered[rank];
          const hinted = showHint[rank];
          const lcUrl = `https://leetcode.com/problems/${title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '')}/`;

          return (
            <div
              key={rank}
              style={{
                ...styles.card,
                ...(status ? styles.cardAnswered(status) : {}),
              }}
            >
              <div style={styles.qHeader}>
                <span style={styles.rankBadge}>#{rank}</span>
                <span style={styles.lcBadge}>LC {lcNum}</span>
                <span style={styles.diffBadge(difficulty)}>{difficulty}</span>
                <span style={styles.catBadge(category)}>
                  {CAT_META[category]?.emoji} {category}
                </span>
                {status && (
                  <span style={{ marginLeft: "auto", fontSize: "1.2rem" }}>
                    {status === "solved" ? "✅" : status === "unsolved" ? "❌" : "⏭️"}
                  </span>
                )}
              </div>

              <div style={styles.qTitle}>{idx + 1}. {title}</div>
              <div style={styles.acceptRow}>Acceptance: {acceptance}</div>

              <div style={styles.actionRow}>
                <button
                  style={{
                    ...styles.btn("solved"),
                    background: status === "solved" ? "#005f4a" : undefined,
                  }}
                  onClick={() => mark(rank, "solved")}
                >
                  ✅ Solved
                </button>
                <button
                  style={{
                    ...styles.btn("unsolved"),
                    background: status === "unsolved" ? "#5f0015" : undefined,
                  }}
                  onClick={() => mark(rank, "unsolved")}
                >
                  ❌ Need Review
                </button>
                <button
                  style={{
                    ...styles.btn("skip"),
                    background: status === "skip" ? "#5f4f00" : undefined,
                  }}
                  onClick={() => mark(rank, "skip")}
                >
                  ⏭️ Skip
                </button>
                <button
                  style={styles.btn("hint")}
                  onClick={() => toggleHint(rank)}
                >
                  {hinted ? "🙈 Hide Hint" : "💡 Hint"}
                </button>
                <a
                  href={lcUrl}
                  target="_blank"
                  rel="noreferrer"
                  style={{ ...styles.btn("lc"), textDecoration: "none" }}
                >
                  🔗 LeetCode
                </a>
              </div>

              {hinted && HINTS[lcNum] && (
                <div style={styles.hintBox}>
                  <strong style={{ color: "#636EFA" }}>💡 Approach:</strong> {HINTS[lcNum]}
                </div>
              )}
              {hinted && !HINTS[lcNum] && (
                <div style={styles.hintBox}>
                  <strong style={{ color: "#636EFA" }}>💡 Tip:</strong> Check the LeetCode editorial and top solutions for this problem.
                </div>
              )}
            </div>
          );
        })}

        {/* Next batch prompt */}
        {allBatchAnswered && batchIdx < totalBatches - 1 && (
          <div style={{
            background: "#0f2a27",
            border: "1px solid #00b8a3",
            borderRadius: "12px",
            padding: "16px 20px",
            textAlign: "center",
            marginTop: "8px",
          }}>
            <div style={{ fontSize: "1rem", fontWeight: 700, color: "#00b8a3", marginBottom: "8px" }}>
              🎉 Batch {batchIdx + 1} complete!
            </div>
            <div style={{ fontSize: "0.85rem", color: "#aaa", marginBottom: "12px" }}>
              {solved + unsolved + skipped} of {TOTAL} total questions done
            </div>
            <button
              style={{ ...styles.btn("solved"), padding: "10px 28px", fontSize: "0.9rem" }}
              onClick={() => { setBatchIdx(b => b + 1); window.scrollTo(0, 0); }}
            >
              Next Batch →
            </button>
          </div>
        )}

        {/* Final completion */}
        {total_done === TOTAL && (
          <div style={{
            background: "linear-gradient(135deg, #0f2a27, #1a2d45)",
            border: "1px solid #636EFA",
            borderRadius: "14px",
            padding: "24px",
            textAlign: "center",
            marginTop: "16px",
          }}>
            <div style={{ fontSize: "2rem", marginBottom: "8px" }}>🏆</div>
            <div style={{ fontSize: "1.2rem", fontWeight: 800, color: "#fff", marginBottom: "6px" }}>
              All {TOTAL} questions reviewed!
            </div>
            <div style={{ fontSize: "0.9rem", color: "#aaa" }}>
              {solved} solved · {unsolved} need review · {skipped} skipped
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
