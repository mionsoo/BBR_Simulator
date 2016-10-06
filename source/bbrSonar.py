import pygame
import math

import bbrSetting as set

class sonar:
    def __init__(self, term):
        self.maxDistance = 320
        self.term = term

    def checkMaxDis(self, xpos, ypos):
        flag = True

        if xpos <= 0:
            flag = False
        if ypos <= 0:
            flag = False
        if set.MAP_WIDTH <= xpos:
            flag = False
        if set.MAP_HEIGHT <= ypos:
            flag = False

        return flag

    def getDistance(self, pos, angle):
        unit_measure = 3
        distance = 0.0

        x = pos[0]
        y = pos[1]

        while True:
            x -= int(unit_measure * math.cos(math.radians(angle + self.term)))
            y -= int(unit_measure * math.sin(math.radians(angle + self.term)))
            distance += unit_measure

            xpos = x / set.CELL_SIZE
            ypos = y / set.CELL_SIZE

            flag = self.checkMaxDis(xpos, ypos)

            if flag == False:
                break
            if set.map[ypos][xpos] == set.WALL:
                break
            if self.maxDistance <= distance:
                distance -= 3
                break

        return distance - 20

class sonarModule:
    def __init__(self, size, interval):

        ## module basic data ##
        self.size = size
        self.interval = interval

        ## sonars ##
        self.LEFT   = 0
        self.CENTER = 1
        self.RIGHT  = 2

        self.sonars = [None, None, None, None]
        self.sonars[self.LEFT]   = sonar(-self.interval)
        self.sonars[self.CENTER] = sonar(0)
        self.sonars[self.RIGHT]  = sonar(self.interval)        

    def getDistances(self, pos, angle):
        leftAngle = (angle - self.interval) % 360
        rightAngle = (angle + self.interval) % 360
        distances = []

        for sonar in self.sonars:
            if sonar is None:
                continue
            distances.append(sonar.getDistance(pos, angle))

        return distances

    def draw(self, dc, pos, angle):
        leftAngle = (angle - self.interval) % 360
        rightAngle = (angle + self.interval) % 360
        drawSize = 4

        for sonar in self.sonars:
            if sonar is None:
                continue
            tx = pos[0] - int(self.size * math.cos(math.radians(angle + sonar.term)))
            ty = pos[1] - int(self.size * math.sin(math.radians(angle + sonar.term)))
            pygame.draw.circle(dc, set.RED, (tx, ty), drawSize, 0)
