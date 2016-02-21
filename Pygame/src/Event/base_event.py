class BaseEvent():
    def __init__(self):
        self.priority = 0

    def __lt__(self, b):
        return self.priority < b.priority
    
    def do_action(self):
        pass
