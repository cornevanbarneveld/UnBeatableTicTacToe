import random
import numpy as np
import copy
import pygame


## pygame design
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
WINDOW_HEIGHT = 700
WINDOW_WIDTH = 700
CELL_WIDTH = 150
CELL_HEIGHT = 150

X = "X"
O = "O"
gameStatus = None
rectangles = []
board = np.array([
    [None, None, None],
    [None, None, None],
    [None, None, None]
    ])


def init_game():
    global playerfigure
    global computerfigure
    global players_turn
    if bool(random.getrandbits(1)) == True:
        playerfigure = X
        computerfigure = O
    else:
        playerfigure = O
        computerfigure = X  
    players_turn = bool(random.getrandbits(1))
    drawGrid()

def init_pygame():
    global SCREEN
    global font 
    pygame.init()
    font = pygame.font.SysFont('Comic Sans MS', 48)
    SCREEN = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
    ChooseFig = font.render("Select game mode", True, (200,200,200))
    LocalText = font.render("Local", True, (200,200,200) )
    ComputerText = font.render("Computer", True, (200,200,200))
    SCREEN.blit(ChooseFig, (150, 100))
    SCREEN.blit(LocalText, (100, 300))
    SCREEN.blit(ComputerText, (400, 300))

def main():
    while True:
        if gameStatus == None:
            load_game()      
        else: 
            if has_game_ended(board) == True:
                end_game()
            if (gameMode == "Computer" and not players_turn):
                bestMove = minimax()
                place_figure(bestMove[0], bestMove[1])   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and gameStatus == True:
                    pos = pygame.mouse.get_pos()
                    for rect in rectangles:
                        if rect.collidepoint(pos):
                            if ispositionOccupied(rectangles.index(rect)) == False:
                                if (gameMode == "Computer" and players_turn) or gameMode == "Local":
                                    indexRect = getIndexForRect(rectangles.index(rect))
                                    place_figure(indexRect[0], indexRect[1])                    
        pygame.display.flip()
    

def load_game():
    global gameStatus
    global gameMode
    init_pygame()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if pos[0] > 90 and pos[0] < 230 and pos[1] > 300  and pos[1] < 370:
                gameStatus = True
                gameMode = "Local"
                SCREEN.fill((0,0,0))
                init_game()      
            if pos[0] > 390 and pos[0] < 620 and pos[1] > 300  and pos[1] < 370:
                gameStatus = True
                gameMode = "Computer"
                SCREEN.fill((0,0,0))
                init_game()  
                if not players_turn:
                    make_first_move_computer()

def end_game():
    global gameStatus
    gameStatus = False
    font_end_game = pygame.font.SysFont('Comic Sans MS', 23)
    endgame_text = font_end_game.render("The game has ended, press space to go back to menu", True, (200,200,200))
    SCREEN.blit(endgame_text, (48, 40))
    while True:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    SCREEN.fill((0,0,0))
                    clear_board()
                    gameStatus = None
                    main()
    
#the algorithm will calculate all the possible options and this will take a long time
#since the board is empty all four corners are the best options
#the algorithm will place the figure in the first corner every time (top left)
#to make the game a little more interesting and faster one of the four corners will be picked randomly
def make_first_move_computer():
    corner = random.randint(1,4)
    locationx = None
    locationy = None
    if corner == 1:
        locationx = 0
        locationy = 0
    elif corner == 2:
        locationx = 0
        locationy = 2
    elif corner == 3:
        locationx = 2
        locationy = 0
    elif corner == 4:
        locationx = 2
        locationy = 2
    place_figure(locationx, locationy)


def place_figure(locationx, locationy):
    global players_turn
    rectangle = rectangles[getNunmberMatrix(locationx, locationy) -1]
    board[locationx, locationy] = get_current_figure()
    figure = font.render(get_current_figure(), True, (0,0,0) )
    SCREEN.blit(figure, (rectangle.x + 55, rectangle.y + 45))
    players_turn = not players_turn

def clear_board():
    global board
    board = np.array([
    [None, None, None],
    [None, None, None],
    [None, None, None]
    ])

def getNunmberMatrix(row, collumn):
    number = 0
    if (row > 0):
        number += 3*row
    for inty in range(collumn + 1):
        number += 1
    return number

def getIndexForRect(placeNumber):
    count = 0
    for row in range(3):
        for item in range(3):
            if placeNumber == count:
                return [row, item]
            count += 1        

def get_current_figure():
    if players_turn:
        return playerfigure
    return computerfigure

def ispositionOccupied(placeNumber):
    indexRect = getIndexForRect(placeNumber)
    if board[indexRect[0], indexRect[1]] == None:
        return False
    return True
    
def drawGrid():    
    for row in range(3):
        marginrow = 10 * row
        for sqaure in range(3):
            marginsquare = 10 * sqaure
            CELL_POSITION_WIDTH = CELL_WIDTH * sqaure + marginsquare
            CELL_POSITION_HEIGHT = CELL_HEIGHT * row + marginrow
            MARGIN_FOR_CENTER_WIDTH = (WINDOW_WIDTH - (CELL_WIDTH * 3 + 30)) /2
            MARGIN_FOR_CENTER_HEIGTH = (WINDOW_HEIGHT - (CELL_HEIGHT * 3 + 30)) /2
            rect = pygame.Rect(CELL_POSITION_WIDTH + MARGIN_FOR_CENTER_WIDTH, CELL_POSITION_HEIGHT + MARGIN_FOR_CENTER_HEIGTH,
                               CELL_WIDTH, CELL_HEIGHT)
            pygame.draw.rect(SCREEN, WHITE, rect)
            rectangles.append(rect)



def has_game_ended(boardend):
    global winner
    winner = None
    #check hotizontal
    for row in boardend:
        if all(element == X for element in row):
            winner = X
            return True
        elif all(element == O for element in row):
            winner = O
            return True

    #check vertical
    for row in boardend.T:
        if all(element == X for element in row):
            winner = X
            return True
        elif all(element == O for element in row):
            winner = O
            return True

    # check diagonal
    if boardend[0,0] == boardend[1,1] == boardend[2, 2] and board[0,0] != None:
        if boardend[0,0] == O:
            winner = O
        else:
            winner = X
        return True
    elif boardend[0, 2] == boardend[1,1] == boardend[2, 0] and boardend[0,2] != None:
        winner = O
        if boardend[0,2] == O:
            winner = O
        else:
            winner = X
        return True

    #check if board is full
    isBoardFull = True
    for row in boardend:
        for item in row:
            if item == None:
                isBoardFull = False
    if isBoardFull:
        return True
    return False

def getPossibleMoves(board):
    moves = []
    for row in range(3):
        for item in range(3):
            if board[row, item] == None:
                moves.append([row, item])
    return moves

#-----------------------------------------
# minimax algorithm
#-----------------------------------------

def minimax():
    minimaxboard = copy.copy(board)
    return maximize(minimaxboard)[0]

def maximize(gameboard):
    if has_game_ended(gameboard):
        return None, calculateUtilty(gameboard)
    maxutility = -2
    bestMove = [None, None]
    for move in getPossibleMoves(gameboard):
        newBoard = copy.copy(gameboard)
        newBoard[move[0], move[1]] = computerfigure
        utility = minimize(newBoard)[1]
        if utility != None and utility > maxutility:
            maxutility = utility         
            bestMove = [move[0], move[1]]
    return [bestMove, maxutility]         
    
def minimize(gameboard):
    if has_game_ended(gameboard):
        return None, calculateUtilty(gameboard)
    bestMove = [None, None]
    minimumutility = 2
    for move in getPossibleMoves(gameboard):
        newBoard = copy.copy(gameboard)
        newBoard[move[0], move[1]] = playerfigure
        utility = (maximize(newBoard)[1])
        if utility != None and utility < minimumutility:
             minimumutility = utility
             bestMove = [move[0], move[1]]
    return [bestMove, minimumutility]


def calculateUtilty(gameboard):
    if has_game_ended(gameboard):
        if winner == playerfigure:
            return -1
        elif winner == computerfigure:
            return 1
        else:
            return 0
    return None

def isBoardFull():
    isBoardFull = True
    for row in board:
        for item in row:
            if item == None:
                isBoardFull = False
    if isBoardFull:
        return True
    return False

main()