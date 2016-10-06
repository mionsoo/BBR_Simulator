## ##
import threading as th
import math
import time

## user module ##
from bbrList import *
from bbrOrigin import dynamics
import bbrSetting as set

class agent(dynamics):
    def __init__(self, robot):
        dynamics.__init__(self)

        self.robot = robot
        self.route = None
        self.goal  = None

        self.point = None

    def init(self):
        self.route = None
        self.point = None
        self.goal  = None

    def checkPoint(self, point):
        if point is None:
            return None

        p = None
        if set.map[point[1]][point[0]] == set.WALL:
            num = self.getSame(self.route, point)

            while num < len(self.route):
                p = self.route[num]
                if set.map[p[1]][p[0]] != set.WALL:
                    return p

                num += 1
        return point


    def run(self):
        while self.flag == True: 

            if self.robot.behaviors[self.robot.ADJUST] is None:
                break
               
            if self.route is None or self.goal is None:
                time.sleep(0.4)
                continue

            pos = tuple(set.getLCor(self.robot.pos))

            ## check is goal ##
            if self.isGoal(pos, self.goal):
                self.robot.stop()

            ## getNextPoint ##
            if (self.isGoal(pos, self.point)) or (self.point == None):
                self.point = self.getNextPoint(self.point)

            ## check wall on  the point ##
            self.point = self.checkPoint(self.point)
                
            #set.map[self.point[1]][self.point[0]] = set.TEMP
            
            ## send to robot adjust ##
            self.adjust(pos, self.point)

            time.sleep(0.4)

    def routePlanning(self):
        rPos = tuple(set.getLCor(self.robot.pos))

        if self.route != None:
            for r in self.route:
                set.map[r[1]][r[0]] = set.ROAD

        self.route = astar(set.map).run(rPos, self.goal)

        self.route.reverse()
        for r in self.route:
            if self.goal != r:
                set.map[r[1]][r[0]] = set.ROUTE

        self.point = self.route[0]

    def isGoal(self, pos, goal):
        if goal is None:
            return False

        for y in range(-2, 3, 1):
            for x in range(-2, 3, 1):
                tx = goal[0] + x
                ty = goal[1] + y

                if pos == (tx, ty):
                    return True
        return False

    def getSame(self, dataSet, sData):
        num = 0

        while True:
            if dataSet[num] == sData:
                return num
            num += 1

    def getNextPoint(self, point):
        if point is None:
            point = self.route[0]

        #if self.goal == point:
        #    return self.goal

        num = self.getSame(self.route, point)
        if len(self.route) <= num+1:
            return self.route[num]

        pDir = self.getDirection(tuple(self.route[num]), tuple(self.route[num+1]))
        num += 1
        
        count = 0
        for i in range(num, num + 9, 1):
            if len(self.route) <= i+1:
                return self.route[i]

            nDir = self.getDirection(self.route[i], self.route[i+1])
            if pDir != nDir:
                if 6 <= count:
                    return self.route[i+1]

            count += 1
            point = self.route[i]

        return point

    def adjust(self, pos, point):
        term = 30
        angle = self.getAngle(pos, point)
         
        if ((angle - term) % 360 < self.robot.angle) and (self.robot.angle < (angle + term) % 360):
            self.robot.behaviors[self.robot.ADJUST].fire = False
        else:
            if self.robot.angle < angle:
                self.robot.behaviors[self.robot.ADJUST].fire = True
                self.robot.behaviors[self.robot.ADJUST].act = [self.robot.RIGHT]
            #if angle < self.robot.angle:
            else:
                self.robot.behaviors[self.robot.ADJUST].fire = True
                self.robot.behaviors[self.robot.ADJUST].act = [self.robot.LEFT]

    def getAngle(self, sPos, dPos):
        vPos = [sPos[0] - dPos[0], sPos[1] - dPos[1]]
        rad = math.atan2(vPos[1], vPos[0])
        degree = int((rad*180)/math.pi)

        return degree % 360

    def getDirection(self, pre, now):
        HOR = 1
        VER = 3

        tx = pre[0] - now[0]
        ty = pre[1] - now[1]

        dir = 0

        if tx < 0:
            dir += HOR
        elif 0 < tx:
            dir -= HOR

        if ty < 0:
            dir += VER
        elif 0 < ty:
            dir -= VER

        return dir

