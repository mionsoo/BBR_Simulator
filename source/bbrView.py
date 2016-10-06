# pygame module
import pygame, sys

# user module
import bbrSetting as set
import bbrRobot
import bbrEx

class view():
    def __init__(self):

        ## transform Scene ##
        self.SIMULATION = 0
        self.MANUAL = 1
        self.act = self.MANUAL

        ## transform mouse check ##
        self.mouseType = set.GOAL

        ## agent registration ##
        self.ROBOT = 0
        self.EX    = 1

        self.agents = [None, None, None, None, None]
        self.agents[self.ROBOT] = bbrRobot.agent([40, 40], 15, 4)
        self.agents[self.EX] = bbrEx.agent(self.agents[self.ROBOT])     
           
        ## agent thread start ##
        for agent in self.agents:
            if agent is None:
                continue
            agent.start()

        ## insert 0 by mapSize ##
        self.pushMapWithSize()

        ## init ##
        self.onInit()     
    
    def pushMapWithSize(self):
        for i in range(set.MAP_HEIGHT):
            tMap = []
            for j in range(set.MAP_WIDTH):
                tMap.append(set.ROAD)
            set.map.append(tMap)

    ## onMain ##
    def onInit(self):
        self.initMap()

        for agent in self.agents:
            if agent is None:
                continue
            agent.init()

    def onClose(self):
        ## agent thread close ##
        for agent in self.agents:
            if agent is None:
                continue
            agent.close()

    def onDraw(self, dc):            
        ## draw agents ##
        if self.act == self.SIMULATION:
            self.drawMap(dc)

            for agent in self.agents:
                if agent is None:
                    continue
                agent.draw(dc)
        elif self.act == self.MANUAL:
            self.drawManual(dc)

    def onMouse(self, x, y):
        pos = set.getLCor([x, y])

        if self.act == self.SIMULATION:
            ## change the selected coordinates to mouseType ##
            if self.mouseType == set.GOAL:
                if set.map[pos[1]][pos[0]] == set.WALL:
                    return

                set.map[pos[1]][pos[0]] = self.mouseType
                if self.agents[self.EX] != None:
                    self.agents[self.EX].goal = pos
                    self.agents[self.EX].routePlanning()
            else:
                set.map[pos[1]][pos[0]] = self.mouseType

    def onKeyDown(self, key):
        ######################################
        ##  spacebar  is change robot's act ##
        ##  backspace is init               ##
        ##  enter_key is change Scene       ##
        ##  1_key is set mouseType to road  ##
        ##  2_key is set mouseType to wall  ##
        ##  3_key is set mousetype to goal  ##
        ##  s_key is save map               ##     
        ######################################

        ## common key ##
        if key == pygame.K_RETURN:
            if self.act == self.MANUAL:
                self.act = self.SIMULATION
            else:
                self.act = self.MANUAL
        elif key == pygame.K_ESCAPE:
            self.onClose()
            pygame.quit()
            sys.exit()

        ## simulator key ##
        if self.act == self.SIMULATION:
            if key == pygame.K_SPACE:
                if self.agents[self.ROBOT] != None:
                    self.agents[self.ROBOT].activate()
                    print "robot active"
            elif key == pygame.K_BACKSPACE:
                self.onInit()
                print "reset"
            elif key == pygame.K_1:
                self.mouseType = set.ROAD
                print "mouseType is road"
            elif key == pygame.K_2:
                self.mouseType = set.WALL
                print "mouseType is wall"
            elif key == pygame.K_3:
                self.mouseType = set.GOAL
                print "mouseType is goal"
            elif key == pygame.K_s:
                self.saveMapping()
                print "save File"

    ## mapFunc ##
    def initMap(self):
        ## reset mapData
        for y in range(set.MAP_HEIGHT):
            for x in range(set.MAP_WIDTH):
                set.map[y][x] = set.ROAD

        ## load mapData ##
        self.loadMapping()

        ## boundary
        for i in range(set.MAP_WIDTH):
            set.map[0][i] = set.WALL
            set.map[set.MAP_HEIGHT-1][i] = set.WALL

        for i in range(set.MAP_HEIGHT):
            set.map[i][0] = set.WALL
            set.map[i][set.MAP_WIDTH-1] = set.WALL

    def drawMap(self, dc):
        # term is block's interval
        term = 0

        ## check mapData and draw what color to match ##
        for y in range(set.MAP_HEIGHT):
            for x in range(set.MAP_WIDTH):
                pos = set.getACor([x, y])
                size = ([pos[0], pos[1], set.CELL_SIZE - term, set.CELL_SIZE - term])

                if set.map[y][x] == set.ROAD:
                    pygame.draw.rect(dc, set.BG_ROAD, size, 0)
                    #pygame.draw.rect(dc, set.WHITE, size, 0)
                elif set.map[y][x] == set.WALL:
                    pygame.draw.rect(dc, set.BLACK, size, 0)
                elif set.map[y][x] == set.GOAL:
                    pygame.draw.rect(dc, set.RED, size, 0)
                elif set.map[y][x] == set.ROUTE:
                    pygame.draw.rect(dc, set.BG_COLOR, size, 0)
                elif set.map[y][x] == set.TEMP:
                    pygame.draw.rect(dc, set.YELLOW, size, 0)            
              
    def drawManual(self, dc):
        # initialize font
        myfont = pygame.font.SysFont("monospace", 30)

        ######################################
        ##  spacebar  is change robot's act ##
        ##  backspace is init               ##
        ##  enter_key is change Scene       ##
        ##  esc_key   is quit               ##
        ##  1_key is set mouseType to road  ##
        ##  2_key is set mouseType to wall  ##
        ##  3_key is set mousetype to goal  ##
        ##  s_key is save map               ##     
        ######################################

        texts = [
            "--------------------",
            " == common key ==",
            "--------------------",
            "[esc] is quit",
            "[enter] is change scene",
            "",
            "--------------------",
            " == simulator key ==",
            "--------------------",
            "[space_bar] is change robot's act",
            "[backspace] is reset simulation",
            "[1] is set MouseType to road",
            "[2] is set MouseType to wall",
            "[3] is set MouseType to goal",
            "[s] is save map",
            "",
            " PRESS ENTER"
            ]

        textX = 100
        textY = 140

        # render text
        label = myfont.render("Manual", 3, set.BLACK)
        dc.blit(label, (200, 100))

        myfont = pygame.font.SysFont("monospace", 20)

        for t in texts:
            label = myfont.render(t, 3, set.BLACK)
            dc.blit(label, (textX, textY))
            textY += 20

    ## mapData process by fIO ##
    def saveMapping(self):
        fname = "map_" + str(set.MAP_WIDTH) + "_" + str(set.MAP_HEIGHT)
        f = open(fname, 'w')

        for y in range(set.MAP_HEIGHT):
            for x in range(set.MAP_WIDTH):
                if set.map[y][x] == set.WALL:
                    f.write("%d" % set.WALL)
                else:
                    f.write("%d" % set.ROAD)
            f.write("\n")
        f.close()

    def loadMapping(self):
        fname = "map_" + str(set.MAP_WIDTH) + "_" + str(set.MAP_HEIGHT)
        try:
            f = open(fname, 'r')

            for y in range(set.MAP_HEIGHT):
                data = f.readline()
                for x in range(set.MAP_WIDTH):
                    set.map[y][x] = int(data[x])
            f.close()

            return 0
        except:
            print "not found file"
            return -1

    
