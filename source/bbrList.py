## user module ##
import bbrSetting as set

class node:
    def __init__(self, g = None, h = None, pos = None, pre = None):
        self.pos = pos
        self.g = g
        self.h = h
        self.f = self.g + self.h
        self.pre = pre
        self.next = None


class linkedList():
    def __init__(self):
        self.head = None

    def appendNode(self, newNode):
        if self.head is None:
            self.head = newNode
        else:
            tNode = self.head
            while tNode.next != None:
                tNode = tNode.next
            tNode.next = newNode

    def printAllNode(self):
        if self.isEmpty():
            print "is empty"
            return

        tNode = self.head

        while tNode != None:
            print tNode.f
            tNode = tNode.next

    def isEmpty(self):
        return self.head is None

class starList(linkedList):
    def __init__(self):
        linkedList.__init__(self)

    def deleteNode(self, dNode):
        tNode = self.head

        while tNode.next != None:
            if tNode.next == dNode:
                tNode.next = dNode.next
            tNode = tNode.next

    def checkSamePos(self, pos):
        tNode = self.head

        while tNode != None:
            if tNode.pos == pos:
                return True
            tNode = tNode.next

        return False

class openList(starList):
    def __init__(self):
        starList.__init__(self)
        self.appendNode(node(0, 0))

    def sortedInsert(self, nNodes):
        for nNode in nNodes:
            tNode = self.head

            while tNode.next != None:
                if tNode.next.pos == nNode.pos:
                    if nNode.f < tNode.next.f:
                        dNode = tNode.next
                        nNode.next = dNode.next
                        tNode.next = nNode
                    break
                elif nNode.f < tNode.next.f:
                    pNode = tNode.next
                    nNode.next = pNode
                    tNode.next = nNode
                    break

                tNode = tNode.next

            if tNode.next == None:
                tNode.next = nNode

class closeList(starList):
    def __init__(self):
        starList.__init__(self)
        self.appendNode(node(0, 0))

    def sortedInsert(self, nNodes):
        for nNode in nNodes:
            tNode = self.head

            while tNode.next != None:
                if nNode.f < tNode.next.f:
                    break
                tNode = tNode.next

            nNode.next = tNode.next
            tNode.next = nNode

class astar():
    def __init__(self, map):
        self.open = openList()
        self.close = closeList()
        self.map = map

        # pNode is work place
        self.pNode = self.open.head

    def step(self):
        if self.pNode != self.open.head:
            tNodes = []
            tNodes.append(self.pNode)
            self.close.sortedInsert(tNodes)

        self.pNode = self.open.head.next
        self.open.head.next = self.open.head.next.next
    
    def compute_h(self, pos, goal):
        cx = abs(goal[0] - pos[0])
        cy = abs(goal[1] - pos[1])
        
        return cx + cy

    def run(self, sPos, goal):
        if goal == None:
            print "no goal"
            return

        nNodes = []

        #insert startNode
        nNodes.append(node(0, self.compute_h(sPos, goal), sPos))
        self.open.sortedInsert(nNodes)

        while self.open.head.next != None:
            self.step()

            if self.pNode.pos == goal:
                break

            nNodes = []
            for i in range(-1, 2, 1):
                for j in range(-1, 2, 1):
                    # No Change
                    if i == 0 and j == 0:
                        continue

                    ## if you want 4 direction check ##
                    
                    if i == -1 and j == -1:
                        continue
                    if i == 1 and j == 1:
                        continue
                    if i == -1 and j == 1:
                        continue
                    if i == 1 and j == -1:
                        continue
                    

                    pos = []
                    pos.append(self.pNode.pos[0] + j)
                    pos.append(self.pNode.pos[1] + i)

                    if (pos[0] < 0) or (pos[1] < 0):
                        continue
                    if (set.MAP_WIDTH <= pos[0]) or (set.MAP_HEIGHT <= pos[1]):
                        continue

                    if set.map[pos[1]][pos[0]] == 1:
                        continue

                    if self.close.checkSamePos(pos):
                        continue

                    # Insert Node to openList
                    nNodes.append(node(self.pNode.g+1, self.compute_h(pos, goal), pos, self.pNode))
            self.open.sortedInsert(nNodes)
        #print "aStar end"

        route = []

        #self.pNode = self.pNode.pre
        while self.pNode.pre != None:
            route.append(self.pNode.pos)
            self.pNode = self.pNode.pre

        return route