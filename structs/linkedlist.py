# linked list class
class Node():
    def __init__(self, light_id=None, priority=None):
        self.light_id = light_id
        self.priority = priority
        self.next = None
