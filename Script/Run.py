import pygame

pygame.init()

display_height = 400
display_width = 400

white = (255, 255, 255)
black = (0, 0, 0)

gameBoard = pygame.image.load('Images/gameBoardBG.png')
gameBoard = pygame.transform.smoothscale(
    gameBoard, (display_height, display_width))

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

clock = pygame.time.Clock()


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


def buildNewGame():
    print("new game")
    message = "Name of game?"
    message_location = ((display_width / 2), (display_height / 2))
    message_display(message, message_location, black)
    waitForInput()
    nameOfGame = userInput
    print(nameOfGame)
    message_display(message, message_location, white)

    message = "How many players?"
    message_location = ((display_width / 2), (display_height / 2))
    message_display(message, message_location, black)
    waitForInput()
    amountOfPlayers = userInput
    print(amountOfPlayers)
    message_display(message, message_location, white)


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
        print("Go to loading screen")

    elif userInput == '2':
        message_display(message, message_location, white)
        buildNewGame()


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

        gameDisplay.blit(gameBoard, (0, 0))

        pygame.display.update()
        clock.tick(60)


gameRun = False
gameLoop(gameRun)
pygame.quit()
quit()
