from collections import deque

class KeyboardDataCollector:
    def __init__(self) -> None:
        self.keys = deque()

    def collect(self, event):
        key = event.name
        self.keys.append(key)

    def get_all(self):
        while self.keys:
            yield self.keys.popleft()