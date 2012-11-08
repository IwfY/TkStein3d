from threading import Thread

class TkView(Thread):
    def __init__(self, client, window):
        Thread.__init__(self)
        
        self.client = client
        self.window = window