class Session:
    def __init__(self, name, start_time, duration, capacity, activated=True, id = None):
        self.name = name
        self.start_time = start_time
        self.duration = duration
        self.capacity = capacity
        self.activated = activated
        self.id = id