
## mapData
ROAD  = 0
WALL  = 1
GOAL  = 2
ROUTE = 3
TEMP  = 4

## rgbColor
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TERM_RED   = (241, 91, 91)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
YELLOW = (255, 255, 0)
BG_ROAD = (255, 178, 217)
BG_COLOR = (171, 242, 0)

## map information
map = []
MAP_WIDTH = 50
MAP_HEIGHT = 50
CELL_SIZE  = 13

## func change to logical Coordination
def getLCor(ac):
    return [ac[0] / CELL_SIZE, ac[1] / CELL_SIZE]

## func change to absolute Coordination
def getACor(lc):
    return [lc[0] * CELL_SIZE, lc[1] * CELL_SIZE]
