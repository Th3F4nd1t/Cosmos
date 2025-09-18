from tools.terminal.decorators import user_run, system_run


class UserAttentionQueue:
    @system_run
    def __init__(self):
        self.queue = []
        self.last_idn = 0

    @system_run
    def force_add(self, item:str, options:list[str]|None = None) -> int:
        """
        Options should be a list of strings, the response will be the index of the selected option or if no options are provided, then a string response will be given.
        """
        self.last_idn += 1
        self.queue.append([item, options, self.last_idn, None]) # Item, options, idn, response
        self.queue.sort(key=lambda x: x[2], reverse=True)
        return self.last_idn
    
    @system_run
    def add(self, item:str, options:list[str]|None = None) -> int:
        """
        Adds an item to the queue and returns the idn if the item is not already in the queue. Based on item text.
        """
        for i in self.queue:
            if i[0] == item:
                return i[2]
        
        return self.force_add(item, options)
    
    @system_run
    def get(self, idn:int = None) -> tuple|None:
        if idn is not None:
            for item in self.queue:
                if item[2] == idn:
                    return item
        
        for item in self.queue:
            if item[3] is None:
                return item
            
        return None
    
    @system_run
    def get_all(self) -> list:
        """
        Returns all items in the queue.
        """
        return self.queue

    @system_run
    def remove(self, idn:int) -> bool:
        for item in self.queue:
            if item[2] == idn:
                self.queue.remove(item)
                return True
        return False

    @system_run
    def set_response(self, idn:int, response:int|str) -> bool:
        for item in self.queue:
            if item[2] == idn:
                item[3] = response
                return True
        return False
