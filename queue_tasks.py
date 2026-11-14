from collections import deque
from typing import List

# 1
def first_uniq_char(s: str) -> int:
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    for i, ch in enumerate(s):
        if counts[ch] == 1:
            return i
    return -1

# 2
class MyStack:
    def __init__(self):
        self._main = deque()
        self._aux = deque()

    def push(self, x: int) -> None:
        self._aux.append(x)
        while self._main:
            self._aux.append(self._main.popleft())
        self._main, self._aux = self._aux, self._main

    def pop(self) -> int:
        return self._main.popleft()

    def top(self) -> int:
        return self._main[0]

    def empty(self) -> bool:
        return len(self._main) == 0

# 3
class RecentCounter:
    def __init__(self):
        self._requests = deque()

    def ping(self, t: int) -> int:
        self._requests.append(t)
        while self._requests[0] < t - 3000:
            self._requests.popleft()
        return len(self._requests)

# 4
class MyCircularDeque:
    def __init__(self, k: int):
        self._data = [0] * k
        self._cap = k
        self._front = 0
        self._size = 0

    def insertFront(self, value: int) -> bool:
        if self.isFull():
            return False
        self._front = (self._front - 1) % self._cap
        self._data[self._front] = value
        self._size += 1
        return True

    def insertLast(self, value: int) -> bool:
        if self.isFull():
            return False
        self._data[(self._front + self._size) % self._cap] = value
        self._size += 1
        return True

    def deleteFront(self) -> bool:
        if self.isEmpty():
            return False
        self._front = (self._front + 1) % self._cap
        self._size -= 1
        return True

    def deleteLast(self) -> bool:
        if self.isEmpty():
            return False
        self._size -= 1
        return True

    def getFront(self) -> int:
        return -1 if self.isEmpty() else self._data[self._front]

    def getRear(self) -> int:
        return -1 if self.isEmpty() else self._data[(self._front + self._size - 1) % self._cap]

    def isEmpty(self) -> bool:
        return self._size == 0

    def isFull(self) -> bool:
        return self._size == self._cap

# 5
class MyCircularQueue:
    def __init__(self, k: int):
        self._data = [0] * k
        self._cap = k
        self._head = 0
        self._size = 0

    def enQueue(self, value: int) -> bool:
        if self.isFull():
            return False
        self._data[(self._head + self._size) % self._cap] = value
        self._size += 1
        return True

    def deQueue(self) -> bool:
        if self.isEmpty():
            return False
        self._head = (self._head + 1) % self._cap
        self._size -= 1
        return True

    def Front(self) -> int:
        return -1 if self.isEmpty() else self._data[self._head]

    def Rear(self) -> int:
        return -1 if self.isEmpty() else self._data[(self._head + self._size - 1) % self._cap]

    def isEmpty(self) -> bool:
        return self._size == 0

    def isFull(self) -> bool:
        return self._size == self._cap

# 6
def moves_to_stamp(stamp: str, target: str) -> List[int]:
    m, n = len(stamp), len(target)
    windows = []
    done = [False] * n
    queue = deque()
    answer = []

    for i in range(n - m + 1):
        made, todo = set(), set()
        for j in range(m):
            if target[i + j] == stamp[j]:
                made.add(i + j)
            else:
                todo.add(i + j)
        windows.append((made, todo))
        if not todo:
            answer.append(i)
            for pos in range(i, i + m):
                if not done[pos]:
                    done[pos] = True
                    queue.append(pos)

    while queue:
        pos = queue.popleft()
        for w in range(max(0, pos - m + 1), min(n - m, pos) + 1):
            made, todo = windows[w]
            if pos in todo:
                todo.discard(pos)
                if not todo:
                    answer.append(w)
                    for p in made:
                        if not done[p]:
                            done[p] = True
                            queue.append(p)

    return answer[::-1] if all(done) else []

# 7
def max_sliding_window(nums: List[int], k: int) -> List[int]:
    dq = deque() 
    result = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result

# 8
def constrained_subset_sum(nums: List[int], k: int) -> int:
    dp = list(nums)
    dq = deque()
    best = nums[0]
    for i in range(len(nums)):
        if dq and dq[0] < i - k:
            dq.popleft()
        if dq and dp[dq[0]] > 0:
            dp[i] += dp[dq[0]]
        while dq and dp[dq[-1]] <= dp[i]:
            dq.pop()
        dq.append(i)
        best = max(best, dp[i])
    return best

if __name__ == "__main__":
    # 1
    assert first_uniq_char("leopard") == 0
    assert first_uniq_char("loveleopard") == 2
    assert first_uniq_char("aabb") == -1

    # 2
    st = MyStack()
    st.push(1); st.push(2)
    assert st.top() == 2
    assert st.pop() == 2
    assert st.empty() is False
    assert st.pop() == 1
    assert st.empty() is True

    # 3
    rc = RecentCounter()
    assert [rc.ping(t) for t in (1, 100, 3001, 3002)] == [1, 2, 3, 3]

    # 4
    d = MyCircularDeque(3)
    assert d.insertLast(1) is True
    assert d.insertLast(2) is True
    assert d.insertFront(3) is True
    assert d.insertFront(4) is False
    assert d.getRear() == 2
    assert d.isFull() is True
    assert d.deleteLast() is True
    assert d.insertFront(4) is True
    assert d.getFront() == 4
    d = MyCircularDeque(1)
    assert d.getFront() == -1 and d.getRear() == -1 and d.deleteFront() is False

    # 5
    cq = MyCircularQueue(3)
    assert cq.enQueue(1) and cq.enQueue(2) and cq.enQueue(3)
    assert cq.enQueue(4) is False
    assert cq.Rear() == 3
    assert cq.isFull() is True
    assert cq.deQueue() is True
    assert cq.enQueue(4) is True
    assert cq.Rear() == 4
    assert cq.Front() == 2

    # 6
    def stamp_result(stamp, moves, length):
        s = ["?"] * length
        for i in moves:
            s[i:i + len(stamp)] = list(stamp)
        return "".join(s)

    for stamp, target in (("abc", "ababc"), ("abca", "aabcaca"), ("ab", "ababab")):
        moves = moves_to_stamp(stamp, target)
        assert moves and len(moves) <= 10 * len(target)
        assert stamp_result(stamp, moves, len(target)) == target
    assert moves_to_stamp("ab", "ba") == []
    assert moves_to_stamp("abc", "abcba") == []  # останній символ мав би бути 'c'
    assert moves_to_stamp("a", "aaa") != []

    # 7
    assert max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
    assert max_sliding_window([1], 1) == [1]

    # 8
    assert constrained_subset_sum([10, 2, -10, 5, 20], 2) == 37
    assert constrained_subset_sum([-1, -2, -3], 1) == -1
    assert constrained_subset_sum([10, -2, -10, -5, 20], 2) == 23

    print("Усі тести пройдено")