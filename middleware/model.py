import time 

class Todo:
    def __init__(self, description, task, category, mltype, monitors, server, path, seconds,
                 date_added=None, date_completed=None,
                 status=None, sent=None, position=None):
        self.description = description
        self.task = task
        self.category = category
        self.monitors = monitors
        self.mltype = mltype
        self.server = server
        self.path = path 
        self.seconds = seconds
        self.date_added = date_added if date_added is not None else round(time.time())
        self.date_completed = date_completed if date_completed is not None else None
        self.status = status if status is not None else 1  # 1 = open, 2 = completed
        self.sent = sent if sent is not None else 1  # 1= not sent, 2 = sent
        self.position = position if position is not None else None

    def __repr__(self) -> str:
        return "({},{},{},{},{},{},{},{},{},{},{},{},{})".format(self.description,self.task, self.category, self.mltype,self.monitors, self.server, self.path, self.seconds, self.date_added, self.date_completed, self.status, self.sent, self.position)


