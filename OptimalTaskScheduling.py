import heapq
class Task:
    def __init__(self, name, priority, duration, start_time = 0):
        self.name = name
        self.priority = priority
        self.duration = duration
        self.start_time = start_time

class TaskScheduler:
    def __init__(self):
        self.idle_queue = []  # List to hold tasks in the order they will be executed
        self.completed_tasks = []  # List to hold completed tasks
        self.now = 0
        self.curr_task = None
    def addTask(self, task, priority, duration):
        t = Task(task, priority, duration)
        heapq.heappush(self.idle_queue, (priority, task, t))
    
    def run_current_task(self, end_time):
        if not self.curr_task:
            return True
        if self.curr_task.start_time + self.curr_task.duration > end_time:
            return False
        self.now = self.curr_task.start_time + self.curr_task.duration
        self.completed_tasks.append(self.curr_task.name)
        self.curr_task = None
        return True
    
    def tick(self, n):
        end_time = self.now + n
        while self.now<end_time and self.run_current_task(end_time) and self.idle_queue:
            _, _, self.curr_task = heapq.heappop(self.idle_queue)
            self.curr_task.start_time = self.now
        self.now = end_time

    def peek(self) -> str:
        if self.curr_task:
            return self.curr_task.name
        return self.idle_queue[0][1] if self.idle_queue else None
        pass
    def getCompleted(self) -> list[str]:
        return self.completed_tasks
        
    
    
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
    print("\n[1] Spec example")
    s = TaskScheduler()
    s.addTask("T1", priority=2, duration=3)
    s.addTask("T2", priority=1, duration=5)
    s.addTask("T3", priority=2, duration=1)
    check("peek → T2 (lowest priority number)", s.peek(), "T2")
    s.tick(5)
    check("after tick(5): only T2 completed", s.getCompleted(), ["T2"])
    s.tick(1)
    check("after tick(1): T1 partial, nothing new completed", s.getCompleted(), ["T2"])
    s.tick(2)
    check("after tick(2): T1 completes", s.getCompleted(), ["T2", "T1"])
    s.tick(1)
    check("after tick(1): T3 completes", s.getCompleted(), ["T2", "T1", "T3"])

def test_peek_does_not_run_task():
    """peek() should not advance the clock or consume any task."""
    print("\n[2] peek does not consume task")
    s = TaskScheduler()
    s.addTask("T1", priority=1, duration=3)
    s.peek()
    s.peek()
    s.peek()
    check("getCompleted still empty after 3 peeks", s.getCompleted(), [])
    s.tick(3)
    check("task completes after tick(3)", s.getCompleted(), ["T1"])

def test_priority_order():
    """Lower priority number runs first."""
    print("\n[3] Priority ordering")
    s = TaskScheduler()
    s.addTask("Low",  priority=10, duration=1)
    s.addTask("High", priority=1,  duration=1)
    s.addTask("Mid",  priority=5,  duration=1)
    check("peek → High (priority 1)", s.peek(), "High")
    s.tick(1)
    check("peek → Mid (priority 5)",  s.peek(), "Mid")
    s.tick(1)
    check("peek → Low (priority 10)", s.peek(), "Low")
    s.tick(1)
    check("all completed in priority order", s.getCompleted(), ["High", "Mid", "Low"])

def test_priority_tie_alphabetical():
    """Same priority → alphabetical task ID."""
    print("\n[4] Priority tie → alphabetical")
    s = TaskScheduler()
    s.addTask("Zebra", priority=2, duration=1)
    s.addTask("Alpha", priority=2, duration=1)
    s.addTask("Mango", priority=2, duration=1)
    check("peek → Alpha (alphabetically first)", s.peek(), "Alpha")
    s.tick(1)
    check("peek → Mango", s.peek(), "Mango")
    s.tick(1)
    check("peek → Zebra", s.peek(), "Zebra")
    s.tick(1)
    check("completed in alpha order", s.getCompleted(), ["Alpha", "Mango", "Zebra"])

def test_tick_partial():
    """tick(n) where n < task duration — task not yet complete."""
    print("\n[5] Partial tick")
    s = TaskScheduler()
    s.addTask("T1", priority=1, duration=5)
    s.tick(3)
    check("not completed after partial tick", s.getCompleted(), [])
    check("peek still T1", s.peek(), "T1")
    s.tick(2)
    check("completed after remaining tick", s.getCompleted(), ["T1"])

def test_tick_overflow_into_next_task():
    """tick(n) where n > current task duration — should finish current and start next."""
    print("\n[6] Tick overflows into next task")
    s = TaskScheduler()
    s.addTask("T1", priority=1, duration=2)
    s.addTask("T2", priority=2, duration=3)
    s.tick(4)  # finishes T1 (2), then runs T2 for 2 units (1 remaining)
    check("T1 completed, T2 not yet", s.getCompleted(), ["T1"])
    s.tick(1)
    check("T2 now completed", s.getCompleted(), ["T1", "T2"])

def test_add_task_after_tick():
    """Tasks added after some ticks should join the queue correctly."""
    print("\n[7] Add task after tick")
    s = TaskScheduler()
    s.addTask("T1", priority=5, duration=3)
    s.tick(3)
    check("T1 done", s.getCompleted(), ["T1"])
    s.addTask("T2", priority=1, duration=2)
    check("peek → T2", s.peek(), "T2")
    s.tick(2)
    check("T2 done", s.getCompleted(), ["T1", "T2"])

def test_peek_empty():
    """peek on empty scheduler."""
    print("\n[8] peek empty")
    s = TaskScheduler()
    check("peek empty → None", s.peek(), None)

def test_getCompleted_empty():
    """getCompleted before any task finishes."""
    print("\n[9] getCompleted empty")
    s = TaskScheduler()
    s.addTask("T1", priority=1, duration=10)
    check("getCompleted → [] before finish", s.getCompleted(), [])

def test_large_tick():
    """Single large tick finishes all tasks."""
    print("\n[10] Large tick finishes all")
    s = TaskScheduler()
    s.addTask("T1", priority=1, duration=10)
    s.addTask("T2", priority=2, duration=20)
    s.addTask("T3", priority=3, duration=5)
    s.tick(10**9)
    check("all completed in priority order", s.getCompleted(), ["T1", "T2", "T3"])


# ─── Run all ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    tests = [
        test_spec_example,
        test_peek_does_not_run_task,
        test_priority_order,
        test_priority_tie_alphabetical,
        test_tick_partial,
        test_tick_overflow_into_next_task,
        test_add_task_after_tick,
        test_peek_empty,
        test_getCompleted_empty,
        test_large_tick,
    ]
    print(f"Running {len(tests)} test groups...\n")
    for t in tests:
        t()
    print("\nDone.")