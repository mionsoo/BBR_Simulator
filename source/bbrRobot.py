## ##
import pygame
import threading as th
import time
import math
from random import randrange

## user module ##
import bbrSetting as set
from bbrSonar import sonarModule
from bbrBehaviors import *
from bbrOrigin import dynamics

class agent(dynamics):
    def __init__(self, pos, size, speed):
        dynamics.__init__(self)
        ####                                                                 ####
        ## We have a malfunction in the robot error near zero degree           ##
        ## I know why it malfunctions But it did not fix because tiresome      ##
        ## So use Modify if you have a complaint                               ##
        ####                                                                 ####

        ## robot's basic information ##
        self.startPos = tuple(pos)
        self.size = size
        self.speed = speed
        
        ## can reset basic information
        self.pos = pos
        self.angle = None
        self.distances = None
        self.footprint = []

        ## modules ##
        self.SONAR = 0

        self.modules = [None, None]
        self.modules[self.SONAR] = sonarModule(15, 40)

        self.LEFT   = self.modules[self.SONAR].LEFT
        self.CENTER = self.modules[self.SONAR].CENTER
        self.RIGHT  = self.modules[self.SONAR].RIGHT

        ## behavior ##
        self.FORWARD = 0
        self.AVOID   = 1
        self.ADJUST  = 2

        self.behaviors = [None, None, None, None]
        self.behaviors[self.FORWARD] = forward(self)
        self.behaviors[self.AVOID]   = avoid(self)
        self.behaviors[self.ADJUST]  = adjust(self)
    
    def init(self):
        ## for esc_key ##
        self.pos = list(self.startPos)
        self.angle = 315.0
        self.distances = None
        self.footprint = []
        self.stop()

    def draw(self, dc):
        ## draw footprint ##
        if 1 < len(self.footprint) :
            for i in range(len(self.footprint)-1):
                pygame.draw.line(dc, set.WHITE, self.footprint[i], self.footprint[i+1], 3)       
        
        ## draw footprint circle ver ##
        #for fp in self.footprint:
        #    pygame.draw.circle(dc, set.BG_ROAD, fp, 3, 0)

        ## draw robot ##
        pygame.draw.circle(dc, set.BLUE, self.pos, self.size, 0)
        for module in self.modules:
            if module is None:
                continue
            module.draw(dc, tuple(self.pos), self.angle)

    def arbitrate(self):
        ## choice proper behavior ##
        action = []

        for behavior in self.behaviors:
            if behavior is None:
                continue
            behavior.run()

        for behavior in self.behaviors:
            if behavior is None:
                continue
            if behavior.fire == True:
                action = behavior.act

        return action[randrange(len(action))]

    def actuator(self, action):
        ## direct input to the motor func ##
        if action == self.LEFT:
            self.left()
        elif action == self.RIGHT:
            self.right()
        else:
            self.go()

    def run(self):
        count = 0
        while self.flag == True:
            ## work ##
            if self.act == True:
                self.distances = self.modules[self.SONAR].getDistances(tuple(self.pos), self.angle)

                action = self.arbitrate()
                self.actuator(action)

                ## store footprint ##
                if count == 5:
                    self.footprint.append(tuple(self.pos))
                    #print len(self.footprint)
                    count = 0
                count += 1

            time.sleep(0.03)

    def go(self):
        ## just go straight ##
        self.pos[0] -= int(self.speed * math.cos(math.radians(self.angle)))
        self.pos[1] -= int(self.speed * math.sin(math.radians(self.angle)))

    def right(self):
        ## change angle to right ##
        t = randrange(1, 3)

        for i in range(t):
            self.angle += 2
        self.angle = self.angle % 360

    def left(self):
        ## change angle to left ##
        t = randrange(1, 3)

        for i in range(t):
            self.angle -= 2
        self.angle = self.angle % 360
            

