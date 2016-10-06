## pygame module ##
import pygame, sys
from pygame.locals import *

## user module ##
import bbrView
import bbrSetting as set

def main():
    ## pygame init ##
    pygame.init()

    screenSize = set.getACor([set.MAP_WIDTH, set.MAP_HEIGHT])

    dc = pygame.display.set_mode(screenSize)
    pygame.display.set_caption('BBR_Simulator')

    ## bbrView create ##
    view = bbrView.view()

    while True:
        ## new drawing ##
        dc.fill(set.WHITE)
        view.onDraw(dc)
        pygame.display.update()

        ## get events ##
        for event in pygame.event.get():
            if event.type == QUIT:
                view.onClose()
                pygame.quit()
                sys.exit()
            elif pygame.MOUSEBUTTONDOWN == event.type:
                pos = pygame.mouse.get_pos()
                view.onMouse(pos[0], pos[1])
            elif event.type == pygame.KEYDOWN:
                view.onKeyDown(event.key)


if __name__ == "__main__":
    main()




