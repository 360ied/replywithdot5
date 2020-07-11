class Counter:

    def __init__(self):
        self.counters = {}

    def increment_counter(self, counter):
        try:
            self.counters[counter] += 1
        except KeyError:
            self.counters[counter] = 1

    def get_total_count(self) -> int:
        count: int = 0
        for key, value in self.counters.items():
            count += value
        return count

    def get_total_integer_count(self) -> int:
        count: int = 0
        for key, value in self.counters.items():
            if value is int:
                count += value
            return count
