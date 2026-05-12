class Task:
    def __init__(self, id, duration, deadline=None, priority=0):
        self.id = id
        self.duration = duration
        self.deadline = deadline
        self.priority = priority