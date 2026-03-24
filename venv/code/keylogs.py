class Keylogs:
    def __init__(self):
        self.keys = []
    
    def add_key(self, key):
        if key not in self.keys:
            self.keys.append(key)
    
    def remove_key(self, key):
        if key in self.keys:
            self.keys.remove(key)
    
    def is_pressed(self, key):
        return key in self.keys