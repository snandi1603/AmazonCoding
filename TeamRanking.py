import heapq
from collections import defaultdict
import unittest
class Team:
    def __init__(self, name):
        self.name = name
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.points = 0
class TeamRanking:
    def __init__(self):
        self.best = None
        self.hmap = {}
    def rankTeams(self, name):
        return (-self.hmap[name].wins, -self.hmap[name].points, name)
    def addMatch(self, team1, team2, score1, score2):
        if team1 not in self.hmap:
            self.hmap[team1] = Team(team1)
        if team2 not in self.hmap:
            self.hmap[team2] = Team(team2)
        self.hmap[team1].points += score1
        self.hmap[team2].points += score2

        if score1 > score2:
            self.hmap[team1].wins += 1
            self.hmap[team2].losses += 1
        elif score1 < score2:
            self.hmap[team1].losses += 1
            self.hmap[team2].wins += 1
        else:
            self.hmap[team1].draws += 1
            self.hmap[team2].draws += 1
        if self.best is None:
            self.best = team1 if self.rankTeams(team1) < self.rankTeams(team2) else team2
        else:
            self.best = min(self.best, team1, team2, key=self.rankTeams)
    def findFirst(self):
        return self.best
    def getTeam(self, team):
        if team not in self.hmap:
            return None
        return (self.hmap[team].wins, self.hmap[team].losses, self.hmap[team].points)
    
# ─── Test runner ─────────────────────────────────────────────────────────────

def check(name, actual, expected):
    if actual == expected:
        print(f"  PASS  {name}")
    else:
        print(f"  FAIL  {name}")
        print(f"         expected : {expected}")
        print(f"         actual   : {actual}")

# ─── Test cases ──────────────────────────────────────────────────────────────

def test_spec_example():
    """Exact example from the problem statement."""
    print("\n[1] Spec example")
    tr = TeamRanking()
    tr.addMatch("Alpha", "Beta",  3, 1)
    tr.addMatch("Alpha", "Gamma", 2, 3)
    tr.addMatch("Beta",  "Gamma", 1, 2)
    check("findFirst → Gamma (2 wins)",     tr.findFirst(),        "Gamma")
    check("getTeam Alpha → (1, 1, 5)",      tr.getTeam("Alpha"),   (1, 1, 5))
    check("getTeam Beta  → (0, 2, 2)",      tr.getTeam("Beta"),    (0, 2, 2))
    check("getTeam Gamma → (2, 0, 5)",      tr.getTeam("Gamma"),   (2, 0, 5))

def test_wins_beat_points():
    """Team with more wins ranks above team with more points."""
    print("\n[2] Wins beat points")
    tr = TeamRanking()
    tr.addMatch("Alpha", "Beta",  3, 1)   # Alpha: 1W 3pts
    tr.addMatch("Gamma", "Delta", 1, 0)   # Gamma: 1W 1pt
    tr.addMatch("Gamma", "Alpha", 2, 1)   # Gamma: 2W 3pts | Alpha: 1W 4pts
    check("findFirst → Gamma (2W beats 1W even with fewer pts)", tr.findFirst(), "Gamma")

def test_points_tiebreak():
    """Same wins → higher points wins."""
    print("\n[3] Points tiebreak")
    tr = TeamRanking()
    tr.addMatch("A", "X", 5, 1)   # A: 1W 5pts
    tr.addMatch("B", "X", 3, 1)   # B: 1W 3pts
    check("findFirst → A (same wins, more points)", tr.findFirst(), "A")

def test_alphabetical_tiebreak():
    """Same wins, same points → alphabetically first name wins."""
    print("\n[4] Alphabetical tiebreak")
    tr = TeamRanking()
    tr.addMatch("Zebra", "X", 3, 1)   # Zebra: 1W 3pts
    tr.addMatch("Alpha", "X", 3, 1)   # Alpha: 1W 3pts
    check("findFirst → Alpha (alphabetically before Zebra)", tr.findFirst(), "Alpha")

def test_leader_changes():
    """Leader should update as new results come in."""
    print("\n[5] Leader changes over time")
    tr = TeamRanking()
    tr.addMatch("A", "B", 3, 1)
    check("after match 1: A leads", tr.findFirst(), "A")
    tr.addMatch("B", "A", 5, 0)   # B now has 1W; A still 1W but B has more pts? No — same wins, B:6pts A:3pts
    check("after match 2: B leads (same wins, more pts)", tr.findFirst(), "B")
    tr.addMatch("B", "C", 3, 1)   # B now 2W
    check("after match 3: B still leads (2W)", tr.findFirst(), "B")

def test_draw_not_counted_as_win():
    """Draws should not increment wins."""
    print("\n[6] Draw handling")
    tr = TeamRanking()
    tr.addMatch("A", "B", 2, 2)
    check("A stats after draw: (0 wins, 0 losses, 2 pts)", tr.getTeam("A"), (0, 0, 2))
    check("B stats after draw: (0 wins, 0 losses, 2 pts)", tr.getTeam("B"), (0, 0, 2))

def test_unknown_team():
    """getTeam on a team that never played returns None."""
    print("\n[7] Unknown team")
    tr = TeamRanking()
    check("getTeam unknown → None", tr.getTeam("Ghost"), None)

def test_findFirst_empty():
    """findFirst on empty system returns None."""
    print("\n[8] Empty system")
    tr = TeamRanking()
    check("findFirst empty → None", tr.findFirst(), None)

def test_multiple_matches_same_pair():
    """Two teams play each other multiple times — stats accumulate."""
    print("\n[9] Same pair plays multiple times")
    tr = TeamRanking()
    tr.addMatch("A", "B", 3, 1)   # A: 1W 3pts | B: 0W 1pt
    tr.addMatch("B", "A", 4, 0)   # B: 1W 5pts | A: 1W 3pts
    tr.addMatch("A", "B", 2, 1)   # A: 2W 5pts | B: 1W 6pts
    check("A stats: (2W, 1L, 5pts)", tr.getTeam("A"), (2, 1, 5))
    check("B stats: (1W, 2L, 6pts)", tr.getTeam("B"), (1, 2, 6))
    check("findFirst → A (2W beats 1W)", tr.findFirst(), "A")

def test_large_scores():
    """Scores at constraint boundary (100)."""
    print("\n[10] Large scores")
    tr = TeamRanking()
    tr.addMatch("A", "B", 100, 99)
    check("A stats: (1W, 0L, 100pts)", tr.getTeam("A"), (1, 0, 100))
    check("B stats: (0W, 1L, 99pts)",  tr.getTeam("B"), (0, 1, 99))
    check("findFirst → A",             tr.findFirst(), "A")


# ─── Run all ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    tests = [
        test_spec_example,
        test_wins_beat_points,
        test_points_tiebreak,
        test_alphabetical_tiebreak,
        test_leader_changes,
        test_draw_not_counted_as_win,
        test_unknown_team,
        test_findFirst_empty,
        test_multiple_matches_same_pair,
        test_large_scores,
    ]
    print(f"Running {len(tests)} test groups...")
    for t in tests:
        t()
    print("\nDone.")