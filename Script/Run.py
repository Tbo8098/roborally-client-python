import pygame

pygame.init()

display_height = 800
display_width = 800

white = (255,255,255)

gameBoard = pygame.image.load('Images/gameBoardBG.png')
robot1 = pygame.image.load('Images/Robots/ScissorHand.png')
robot2 = pygame.image.load('Images/Robots/MrFoots.png')
# TODO: define a square
# TODO: define direction in which the robot is facing

#one square is 70,74 px

squareSizeX = 65
squareSizeY = 65
startingPos = (0,0)

SquareLocation = (3,4)
location = SquareLocation[0]*squareSizeX, SquareLocation[1]*squareSizeY

def input():
    # TODO: add an imput string which contains the turnNumber,player,loc,
    pass




gameDisplay = pygame.display.set_mode((display_height,display_width))
pygame.display.set_caption("RoboRally")
clock = pygame.time.Clock()

def gameLoop():
    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

        gameDisplay.fill(white)
        gameDisplay.blit(gameBoard,(0,0))
        gameDisplay.blit(robot2,startingPos)
        gameDisplay.blit(robot1,location)
        pygame.display.update()
        clock.tick(60)
gameLoop()
pygame.quit()
quit()
