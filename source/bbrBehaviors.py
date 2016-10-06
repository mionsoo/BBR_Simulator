from random import randrange

class behavior:
    def __init__(self, robot):
        self.fire = True
        self.act = None
        self.robot = robot

    def run(self):
        pass

class forward(behavior):
    def __init__(self, robot):
        behavior.__init__(self, robot)

    def run(self):
        self.act = [self.robot.CENTER]

class adjust(behavior):
    def __init__(self, robot):
        behavior.__init__(self, robot)
        self.fire = False

    def run(self):
        pass

class avoid(behavior):
    def __init__(self, robot):
        behavior.__init__(self, robot)
    
    def run(self):
        self.fire = True

        pos = tuple(self.robot.distances)

        sideMax    = 25
        centerMax  = 35

        LEFT   = 1
        CENTER = 3
        RIGHT  = 5

        block = 0

        if self.robot.behaviors[self.robot.ADJUST] != None:
            preFire = self.robot.behaviors[self.robot.ADJUST].fire
            self.robot.behaviors[self.robot.ADJUST].fire = False

        if pos[self.robot.LEFT] <= sideMax:
            block |= LEFT
        if pos[self.robot.RIGHT] <= sideMax:
            block |= RIGHT
        if pos[self.robot.CENTER] <= centerMax:
            block |= CENTER
        
        if block == CENTER:        
            if(pos[self.robot.LEFT] < pos[self.robot.RIGHT]):
                if self.act is None:
                    self.act = [self.robot.RIGHT]
            else:
                if self.act is None:
                    self.act = [self.robot.LEFT]                   

        elif (block == LEFT) or (block == LEFT | CENTER):
            if self.act is None:
                self.act = [self.robot.RIGHT]
        elif (block == RIGHT) or (block == RIGHT | CENTER):
            if self.act is None:
                self.act = [self.robot.LEFT]
        elif block == (LEFT | CENTER | RIGHT):
            if self.act is None:
                self.act = [self.robot.RIGHT, self.robot.LEFT]
        else:
            if self.robot.behaviors[self.robot.ADJUST] != None:
                self.robot.behaviors[self.robot.ADJUST].fire = preFire
            self.act = None
            self.fire = False

