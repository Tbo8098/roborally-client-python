import pygame
import socket
import os

# ******************************************************************************
# **************************inital setup****************************************
# ******************************************************************************

pygame.init()

display_height = 800
display_width = 800

white = (255, 255, 255)
black = (0, 0, 0)

# gameBoardFileLocations = 'Images/GameBoards'
# gameBoard_basic = (gameBoardFileLocations + '/BasicBoard.png')
# gameBoard_in_use = pygame.image.load(gameBoard_basic)
# robot1 = pygame.image.load('Images/Robots/ScissorHand.png')

gameboard = "empty.png"
gameboard_path = f"Images/GameBoards/{gameboard}"
active_boardgame = pygame.image.load(gameboard_path)
gameBoard_in_use = pygame.transform.smoothscale(active_boardgame, (display_height, display_width))

robotSize = (int(display_height / 12), int(display_width / 12))

robot1 = pygame.image.load('Images/Robots/ScissorHand.png')
robot1 = pygame.transform.smoothscale(robot1, (robotSize))

robot2 = pygame.image.load('Images/Robots/MrFoots.png')
robot2 = pygame.transform.smoothscale(robot2, (robotSize))

squareSizeX = display_width / 12
squareSizeY = display_height / 12
startingPos = (0, 0)

SquareLocation = (6, 6)
location = SquareLocation[0] * squareSizeX, SquareLocation[1] * squareSizeY
gameDisplay = pygame.display.set_mode((display_height, display_width))
pygame.display.set_caption("RoboRally")

message_center = ((display_width / 2), (display_height / 2))

clock = pygame.time.Clock()

# ******************************************************************************
# ***************************functions******************************************
# ******************************************************************************


def waitForInput():
    global userInput
    pygame.event.clear()
    userInput = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                if key == 'return' or key == 'backspace':
                    message = userInput
                    message_location = ((display_width / 2), (display_height / 1.5))
                    message_display(message, message_location, white)

                    if key == 'return':
                        return
                    else:
                        userInput = ""
                        print("input cleared")

                elif key == 'space':
                    userInput += " "
                elif key == 'right shift' or key == 'left shift':
                    '''do nothing'''  # This is so the shift keys don't get inputted into the userInput
                else:
                    userInput += key
                    message = userInput
                    message_location = ((display_width / 2), (display_height / 1.5))
                    message_display(message, message_location, black)


def message_display(message, location, color):
    basic_font = pygame.font.Font("Fonts/Arial.ttf", 22)
    text = basic_font.render(message, True, color)
    textRec = text.get_rect()
    textRec.center = (location[0], location[1])
    gameDisplay.fill(white, textRec)
    gameDisplay.blit(text, textRec)
    pygame.display.update()

# *************************** New Game ******************************************

# ************************************ Load ************************************


gameBoard_path = '/Images/GameBoards'
robots_path = '/Images/Robots'
savedGame_path = '/SavedGames'


def loadGame():
    global gameboard

    games_available = os.listdir('SavedGames')
    message = f"the games available to load are {games_available}"
    message_display(message, message_center, black)
    waitForInput()
    if userInput.isnumeric() == True:
        game_to_load = 'C:/Users/Spectre/Documents/Programming/roborally-client-python/Script/' + \
            savedGame_path + '/' + games_available[int(userInput) - 1]
        file = open(game_to_load, 'r')
        line = file.read().splitlines()
        # load the board
        gameboard = line[0]
        print(gameboard_path, gameboard)
        gameRun = True
        gameLoop(gameRun)

        # read the last move

        # last_line = line[-1]
        # print(last_line)
        # message_display(message, message_center, white)
        # message_display(last_line, message_center, black)
        # waitForInput()
# ************************************ Menus ************************************


def mainMenu():
    message = """
    1. Load a Game
    2. Start a new game
    """
    message_location = ((display_width / 2), (display_height / 2))
    message_display(message, message_location, black)
    waitForInput()

    if userInput == '1':
        # TODO: make this go and load a game
        loadGame()

    elif userInput == '2':
        message_display(message, message_location, white)
        buildNewGame()


# **************************** Game Loop ****************************************

def gameLoop(gameRun):
    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)

        if not gameRun:
            mainMenu()

        gameDisplay.blit(gameBoard_in_use, (0, 0))

        pygame.display.update()
        clock.tick(60)


gameRun = False
gameLoop(gameRun)
pygame.quit()
quit()
