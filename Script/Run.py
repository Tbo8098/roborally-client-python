import pygame
import socket
import os
import json
from itemDescription import *

# ******************************************************************************
# **************************inital setup****************************************
# ******************************************************************************

pygame.init()

display_height = 1000
display_width = 1000

gameboard_height = 800
gameboard_width = 800

gameboard_starting_location = (7,7)

bgPath = "Script/Images"
gameBackground = pygame.image.load(f"{bgPath}/roborallybackground.png")

white = (255, 255, 255)
black = (0, 0, 0)

robotSize = (int(gameboard_height / 12), int(gameboard_width / 12))

robot1 = 'ScissorHand.png'

line2read = -1

squareSizeX = (gameboard_width + gameboard_starting_location[0]) / 12
squareSizeY = (gameboard_height + gameboard_starting_location[1]) / 12
print(squareSizeX, squareSizeY)

NESW = {
    'north': 0,
    'east': 90,
    'south': 180,
    'west': 270
}

SquareLocation = (6, 6)
location = SquareLocation[0] * squareSizeX, SquareLocation[1] * squareSizeY
gameDisplay = pygame.display.set_mode((display_height, display_width))
pygame.display.set_caption("RoboRally")

message_center = ((display_width / 2), (display_height / 2))

clock = pygame.time.Clock()

# ******************************************************************************
# ***************************functions******************************************
# ******************************************************************************


def waitForInput(printOnScreen):
    pygame.event.clear()
    userInput = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                if printOnScreen is True:
                    if key == 'return' or key == 'backspace':
                        message = userInput
                        message_location = ((display_width / 2), (display_height / 1.5))
                        message_display(message, message_location, white)

                        if key == 'return':
                            return userInput
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
                else:
                    return key


def message_display(message, location, color):
    basic_font = pygame.font.Font("Script/Fonts/Arial.ttf", 22)
    text = basic_font.render(message, True, color)
    textRec = text.get_rect()
    textRec.center = (location[0], location[1])
    gameDisplay.fill(white, textRec)
    gameDisplay.blit(text, textRec)
    pygame.display.update()


def navigate():
    global turn_number
    global players_info

    amount_of_turns = len(gamefile["turns"])

    print(amount_of_turns)
    userInput = waitForInput(False)
    if userInput == 'right':
        if turn_number < -1:
            turn_number += 1
            players_info = gamefile["turns"][turn_number]

    elif userInput == 'left':
        if turn_number > amount_of_turns - (amount_of_turns*2):
            turn_number -= 1
            players_info = gamefile["turns"][turn_number]
 
    else:
        print("not up or down")

    print(players_info)
    draw_to_board()



# *************************** New Game *****************************************

# ************************************ Load ************************************
 

gameBoard_path = '/Images/GameBoards'
robots_path = '/Images/Robots'
savedGame_path = '/SavedGames'


def loadJson():
    global gameBoard_in_use
    global number_of_players
    global players_info
    global game_loaded
    global turn_number
    global gamefile
    
    games_available = os.listdir('Script/SavedGames')
    message = f"the games available to load are {games_available}"
    message_display(message, message_center, black)
    printOnScreen = True
    userInput = waitForInput(printOnScreen)
    if userInput.isnumeric() is True:
        game_loaded =  'C:/Users/Spectre/Documents/Programming/roborally-client-python/Script' + \
            savedGame_path + '/' + games_available[int(userInput) - 1]
        file = open(game_loaded, 'r')
        gamefile = json.load(file)
        file.close()

        gameboard = gamefile["gameBoard_in_use"]
        gameboard_path = f"Script/Images/GameBoards/{gameboard}"
        active_boardgame = pygame.image.load(gameboard_path)
        gameBoard_in_use = pygame.transform.smoothscale(
            active_boardgame, (gameboard_height, gameboard_width))

        turn_number = -1
        number_of_players = gamefile["number_of_players"]
        players_info = gamefile["turns"][turn_number]

def makeJson():
    loadGame()
    newfile = open("Script/SavedGames/game3.txt", 'w')
    json.dump(players_info, newfile)
    print(players_info)


def draw_to_board():
    gameDisplay.blit(gameBoard_in_use, gameboard_starting_location)

    for index in range(number_of_players):
        robot = players_info[index]["robot"]
        robot_name = robot + '.png'
        robot_actual = pygame.image.load('Script/Images/Robots/' + robot_name)
        robot_actual = pygame.transform.smoothscale(robot_actual, (robotSize))
        
        coords = players_info[index]["coords"]
        coords_x = (int(coords[0]) - 1) * squareSizeX
        coords_y = (int(coords[1]) - 1) * squareSizeY
        
        direct = players_info[index]["direction"]
        robot_actual = pygame.transform.rotate(robot_actual, NESW.get(direct))

        gameDisplay.blit(robot_actual, (coords_x, coords_y))
    pygame.display.update()


# ************************************ Menus ************************************


def mainMenu():
    message = ">1. Load a Game >2. Start a new game >3. make Json"
    message_location = ((display_width / 2), (display_height / 2))
    message_display(message, message_location, black)
    printOnScreen = True
    userInput = waitForInput(printOnScreen)
    message_display(message, message_location, white)

    if userInput == '1':
        # TODO: make this go and load a game
        loadJson()

    elif userInput == '2':
        message_display(message, message_location, white)
        # buildNewGame()

    elif userInput == '3':
        # make json
        makeJson()

    else:
        return False
    
    return True


# **************************** Game Loop ***************************************

def gameLoop(mainMenuIsLoaded):
    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)

        if not mainMenuIsLoaded:
            mainMenuIsLoaded = mainMenu()

        else:
            gameDisplay.blit(gameBackground,(0,0))
            pygame.display.update()
            draw_to_board()
            navigate()
        

        pygame.display.update()
        clock.tick(60)


gameLoop(False)
pygame.quit()
quit()