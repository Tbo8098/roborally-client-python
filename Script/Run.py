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

robotSize = (int(display_height / 12), int(display_width / 12))

robot1 = 'ScissorHand.png'

line2read = -1

squareSizeX = display_width / 12
squareSizeY = display_height / 12

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
                    if printOnScreen is True:
                        message = userInput
                        message_location = ((display_width / 2), (display_height / 1.5))
                        message_display(message, message_location, black)


def message_display(message, location, color):
    basic_font = pygame.font.Font("Script/Fonts/Arial.ttf", 22)
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
    global gameBoard_in_use
    global number_of_players
    global players_info
    global game_loaded

    players_info = {}

    games_available = os.listdir('Script/SavedGames')
    message = f"the games available to load are {games_available}"
    message_display(message, message_center, black)
    printOnScreen = True
    userInput = waitForInput(printOnScreen)
    if userInput.isnumeric() == True:
        game_loaded = 'C:/Users/Spectre/Documents/Programming/roborally-client-python/Script' + \
            savedGame_path + '/' + games_available[int(userInput) - 1]
        file = open(game_loaded, 'r')
        line = file.read().splitlines()
        last_line = line[-1]
        player_info = line[1]

        # load the board
        gameboard = line[0]
        gameboard_path = f"Script/Images/GameBoards/{gameboard}"
        active_boardgame = pygame.image.load(gameboard_path)
        gameBoard_in_use = pygame.transform.smoothscale(
            active_boardgame, (display_height, display_width))

        # Load the players names
        word = ""
        player_num = 1

        for letter_in_player_info in player_info:
            if letter_in_player_info == " " or letter_in_player_info == "<":
                if word[0].isalpha() == True:
                    players_info['player' + str(player_num)
                                 ] = {'name': word, 'robot': 'robot'+str(player_num)}
                    number_of_players = player_num
                word = ""
                player_num += 1
            else:
                word += letter_in_player_info
        print(players_info.items())
        file.close()
        loadLine(-1)

        # read the last move


def loadLine(line2read):
    global game_loaded
    file = open(game_loaded, 'r')
    line = file.read().splitlines()
    move = line[line2read]
    player_info = line[1]

    count = 0
    while count >= 0:
        count = move.find('player', count + 1)
        if count != -1:
            plr_num = move[count + 6]

            plr_coord_x_start = move.find("X", count)+2
            plr_coord_x_end = move.find(" ", plr_coord_x_start)
            plr_coord_x = move[plr_coord_x_start:plr_coord_x_end]

            plr_coord_y_start = move.find("Y", count)+2
            plr_coord_y_end = move.find(" ", plr_coord_y_start)
            plr_coord_y = move[plr_coord_y_start:plr_coord_y_end]
            print(f"x coord: {plr_coord_x} and y coord: {plr_coord_y}")

            plr_coord = [plr_coord_y, plr_coord_x]
            players_info.get('player' + plr_num).update({'coords': plr_coord})

            plr_direction_loction_start = move.find("D:", count)+2
            plr_direction_loction_end = move.find(" " or "<", plr_direction_loction_start)
            plr_direction = move[plr_direction_loction_start:plr_direction_loction_end]
            players_info.get('player' + plr_num).update({'direction': plr_direction})

            print(players_info.get('player' + plr_num).values())
            print(players_info)

    file.close()


def navigate():
    global line2read
    printOnScreen = False
    userInput = waitForInput(printOnScreen)
    if userInput == 'up':
        line2read = line2read - 1
        print(line2read)
        loadLine(line2read)


def draw_to_board():
    gameDisplay.blit(gameBoard_in_use, (0, 0))

    for index in range(number_of_players):
        player = players_info.get('player' + str(index + 1)).get('name')
        robot = players_info.get('player' + str(index + 1)).get('robot')
        robot_name = robot + '.png'
        robot_actual = pygame.image.load('Script/Images/Robots/' + robot_name)
        robot_actual = pygame.transform.smoothscale(robot_actual, (robotSize))
        coords = players_info.get('player' + str(index + 1)).get('coords')
        coords_x = (int(coords[0]) - 1) * squareSizeX
        coords_y = (int(coords[1]) - 1) * squareSizeY
        direction = players_info.get('player' + str(index + 1)).get('direction')

        gameDisplay.blit(robot_actual, (coords_x, coords_y))
    pygame.display.update()


# ************************************ Menus ************************************


def mainMenu():
    message = """
    1. Load a Game
    2. Start a new game
    """
    message_location = ((display_width / 2), (display_height / 2))
    message_display(message, message_location, black)
    printOnScreen = True
    userInput = waitForInput(printOnScreen)

    if userInput == '1':
        # TODO: make this go and load a game
        loadGame()

    elif userInput == '2':
        message_display(message, message_location, white)
        # buildNewGame()
    
    return True


# **************************** Game Loop ***************************************

def gameLoop(mainMenuIsLoaded):
    gameExit = False

    while not gameExit:
        # check for quit
        # Load the game if not loaded
        #   draw board loaded
        # navigate
        #   draw board loaded
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)

        if not mainMenuIsLoaded:
            mainMenuIsLoaded = mainMenu()

        else:
            navigate()

        draw_to_board()
        

        pygame.display.update()
        clock.tick(60)


gameLoop(False)
pygame.quit()
quit()
