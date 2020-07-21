class Node:
    def __init__(self, my_id, addr):
        self.id = my_id
        self.addr = addr

    def __eq__(self, other):
        if type(other) is type(self):
            return self.id == other.id

        return False

    def __lt__(self, other):
        if type(other) is type(self):
            return self.id < other.id
        
        raise NotImplementedError

    def __le__(self, other):
        if type(other) is type(self):
            return self.id <= other.id
        
        raise NotImplementedError

    def __gt__(self, other):
        if type(other) is type(self):
            return self.id > other.id
        
        raise NotImplementedError

    def __ge__(self, other):
        if type(other) is type(self):
            return self.id >= other.id
        
        raise NotImplementedError 

    def __ne__(self, other):
        if type(other) is type(self):
            return self.id != other.id
        
        return True 

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return "<Node id:%s addr:%s>" % (self.id, self.addr)

    def __str__(self):
        return "<Node id:%s addr:%s>" % (self.id, self.addr)
