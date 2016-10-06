## ##
import threading as th

## agent will inherit ##
class dynamics(th.Thread):
    def __init__(self):
        th.Thread.__init__(self)
        
        ## threading flag ##
        self.flag = True

        ## logical unit's moving flag ##
        self.act = False

    def init(self):
        pass

    def run(self):
        pass

    def draw(self, dc):
        pass

    def close(self):
        self.flag = False
        self.join()

    ## logical unit moving func ##
    def activate(self):
        self.act = (self.act + 1) % 2

    def stop(self):
        self.act = False