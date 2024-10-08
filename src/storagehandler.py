from keyboard import write

class StorageHandler:
    def __init__(self, storage=None) -> None:
        if storage == None:
            self.storage = {}
        else:
            self.storage = storage

    def get(self, key):
        if key in self.storage:
            write(self.storage[key])        

    def set(self, key, value):
        self.storage[key] = value

    def getall(self):
        write(str(self.storage))