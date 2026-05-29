import mss
import mss.tools
from PIL import Image
import pyautogui
import random
import time
from pynput import keyboard
import threading
from priority_queue import PriorityQueue
from PIL import Image
#Minesweeper window pinned right
#CHANGE THIS FOR DEBUG mode
DEBUG = False
LOOPING = False
###############################################################
#Variables
###############################################################
mode = 0 #0 easy, 1 medium, 2 hard

if(mode ==0):#EASY
    LEFT = 1117
    TOP = 449
    WIDTH = 449 #10 cells across
    HEIGHT = 361 #8 cells tall

    COLS = 10
    ROWS = 8

    CELLWIDTH = WIDTH / COLS
    CELLHEIGHT = HEIGHT / ROWS

    #offsets for pixel sampling
    OX = 2
    OY = 0

    RESTARTX = 3
    RESTARTY = 6
    CHECKWINX = 2
    CHECKWINY = 4

if(mode ==1):#MEDIUM
    LEFT = 1072
    TOP = 419
    WIDTH = 539 
    HEIGHT = 420

    COLS = 18
    ROWS = 14

    CELLWIDTH = WIDTH / COLS
    CELLHEIGHT = HEIGHT / ROWS

    #offsets for pixel sampling
    OX = 2
    OY = -2

    RESTARTX = 10
    RESTARTY = 10
    CHECKWINX = 5
    CHECKWINY = 7.5

if(mode ==2):#HARD
    LEFT = 1042
    TOP = 379
    WIDTH = 599 #10 cells across
    HEIGHT = 501 #8 cells tall

    COLS = 24
    ROWS = 20

    CELLWIDTH = WIDTH / COLS
    CELLHEIGHT = HEIGHT / ROWS

    #offsets for pixel sampling
    OX = 1
    OY = 0

gameActive = False
gameWon = False

UNKNOWN = -1
MINE = -2

board = [[UNKNOWN for _ in range(COLS)] for _ in range(ROWS)]
cellsToVisit = PriorityQueue()

##############################################################
#Emergency Escape Click Esc
##############################################################
running = True     
def on_press(key):
    global running
    global LOOPING
    try:
        if key == keyboard.Key.esc:
            print("ESC pressed, stopping...")
            running = False
            LOOPING = False
            return False  # stop listener
    except:
        pass

# Start listener in background thread
listener = keyboard.Listener(on_press=on_press)
listener.start()

##########
#Functions
##########
def cell_to_color(x, y):
    rx = CELLWIDTH*0.5 + x*CELLWIDTH + OX#minus 5 to go where color is    
    ry = CELLHEIGHT*0.5 + y*CELLHEIGHT + OY
    pixel = img.getpixel((int(rx), int(ry)))
    return pixel#in (r, g, b)

def cell_to_cords(x, y):
    rx = LEFT + CELLWIDTH*0.5 + x*CELLWIDTH   
    ry = TOP + CELLHEIGHT*0.5 + y*CELLHEIGHT
    return rx, ry

def click_cell(x, y):
    pyautogui.moveTo(cell_to_cords(x, y)) #, duration=0.5*random.random()
    time.sleep(0.0001)
    pyautogui.click()#clicks cell

def green(x, y):
    if (cell_to_color(x, y) == (180, 213, 102)):
        return True
    elif (cell_to_color(x, y) == (172, 207, 95)):
        return True
    else:
        return False
    
def zero(x, y):
    if (cell_to_color(x, y) == (224, 195, 164)):
        return True
    elif (cell_to_color(x, y) == (210, 185, 157)):
        return True
    else:
        return False

def one(x, y):
    return cell_to_color(x, y) == (54, 119, 204)

def two(x, y):
    return cell_to_color(x, y) == (80, 140, 70)

def three(x,y):
    return cell_to_color(x, y) == (195, 63, 56)

def four(x,y):
    return cell_to_color(x, y) == (113, 44, 156)

def five(x,y):
    if cell_to_color(x, y) == (241, 148, 55):
        return True
    elif cell_to_color(x, y) == (241, 148, 54):
        return True

def check_game_state():
    if(cell_to_color(RESTARTX, RESTARTY) == (84, 115, 54)):
        if(cell_to_color(CHECKWINX, CHECKWINY) == (178, 214, 96)):
            print("---------")
            print("Game Won")
            global gameWon
            gameWon = True
        else:
            print("---------")
            print("Game Lost")
        return False
    else:
        return True
    
def reload_frame():
    with mss.mss() as sct:
        monitor = {"left": LEFT,
                "top": TOP,
                "width": WIDTH,
                "height": HEIGHT}
        screenshot = sct.grab(monitor)
        mss.tools.to_png(screenshot.rgb, screenshot.size, output="screenshot.png")
        return Image.open("screenshot.png")
    
def random_queue():
    global cellsToVisit
    cellsToVisit = PriorityQueue()
    for x in range (COLS):
        for y in range(ROWS):
            cell = (x, y)
            cellsToVisit.put(cell, random.random())

def update_board_state():
    for x in range (COLS):
        for y in range(ROWS):
            if board[y][x] == UNKNOWN:
                if (zero(x, y)):
                    board[y][x] = 0
                elif(one(x, y)):
                    board[y][x] = 1
                elif(two(x, y)):
                    board[y][x] = 2
                elif(three(x, y)):
                    board[y][x] = 3
                elif(four(x, y)):
                    board[y][x] = 4
                elif(five(x, y)):
                    board[y][x] = 5
                elif(green(x, y)):
                    board[y][x] = UNKNOWN
                else:
                    board[y][x] = UNKNOWN
    for x in range (COLS):
        for y in range(ROWS):
            if board[y][x] > 0:
                mark_mines(x, y)
    for x in range (COLS):
        for y in range(ROWS):
            if board[y][x] > 0:
                move_safe_up_in_queue(x, y)
                    
        
def print_board():
    print("---------------------------")
    for row in board:
        print(" ".join(f"{cell:2}" for cell in row))

def get_neighbors(x, y):
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nx, ny = x + dc, y + dr
            if 0 <= nx < COLS and 0 <= ny < ROWS:
                neighbors.append((nx, ny))
    return neighbors

def count_mines(x, y):
    return sum(1 for nx, ny in get_neighbors(x, y) if board[ny][nx] == MINE)

def count_unknown(x, y):
    return sum(1 for nx, ny in get_neighbors(x, y) if board[ny][nx] == UNKNOWN)

#B1 pattern
def mark_mines(x, y):
    val = board[y][x]
    if(val <= 0):
        return
    u = count_unknown(x, y)
    if(((count_mines(x, y) + u) == val) and u > 0):
            for nx, ny in get_neighbors(x, y):
                if board[ny][nx] == UNKNOWN:
                    board[ny][nx] = MINE

#B2 pattern
def move_safe_up_in_queue(x, y):
    val = board[y][x]
    if(val<= 0):
        return
    if(count_mines(x, y) == val):
        for nx, ny in get_neighbors(x, y):
                if board[ny][nx] == UNKNOWN:
                    cell = (nx, ny)
                    cellsToVisit.put(cell, 0)

def get_unknown_neighbors(x, y):
    return [(nx, ny) for nx, ny in get_neighbors(x, y)
            if board[ny][nx] == UNKNOWN]

def remaining_mines(x, y):
    return board[y][x] - count_mines(x, y)

def advanced_search():
    retVal = False
    for x1 in range(COLS):
        for y1 in range(ROWS):
            val1 = board[y1][x1]
            if val1 <= 0:
                continue

            set1 = set(get_unknown_neighbors(x1, y1))
            rem1 = remaining_mines(x1, y1)

            for x2 in range(COLS):
                for y2 in range(ROWS):
                    if (x1, y1) == (x2, y2):
                        continue

                    val2 = board[y2][x2]
                    if val2 <= 0:
                        continue

                    set2 = set(get_unknown_neighbors(x2, y2))
                    rem2 = remaining_mines(x2, y2)

                    if set1.issubset(set2):
                        # Case: same mine count, extra cells safe
                        if rem1 == rem2:
                            extra = set2 - set1
                            for cx, cy in extra:
                                cellsToVisit.put((cx, cy), 0)
                                retVal = True
                        # Case: difference = mines, extra cells are mines
                        elif rem2 - rem1 == len(set2 - set1):
                            extra = set2 - set1
                            for cx, cy in extra:
                                board[cy][cx] = MINE
                                retVal = True
    return retVal

#####
#Code
#####

img = reload_frame()
gameActive = check_game_state()

pyautogui.moveTo(cell_to_cords(2, 12)) #, duration=0.5*random.random()
time.sleep(0.01)
pyautogui.click()#enters window
pyautogui.click()#clicks cell

if(DEBUG):
    running = False
    update_board_state()
    print_board()
    print(cell_to_color(2, 12))
    #(178, 214, 96)
    img = Image.open("screenshot.png")
    pixels = img.load()
    for x in range (COLS):
        for y in range(ROWS):
            px, py = cell_to_cords(x, y) 
            pixels[px - LEFT + OX, py - TOP + OY] = (255, 0, 0)
    img.save("sampleShown.png")

    while LOOPING:
        time.sleep(1)
        img = reload_frame()
        update_board_state()
        print_board()

#random_queue()
wins = 0
loses = 0
games = 0
guessed = False
guesses = 0
bestTime = 100
cellsSeen = list()
game_start_time = time.time()
times = list()
game_time = None

while(running):
    img = reload_frame()
    gameActive = check_game_state()
    if(not gameActive):
        if(gameWon == True):
            #break
            wins += 1
            if(game_time):
                print("Time: ", round(game_time, 3), "s")
                times.append(game_time)
                averageTime = sum(times) / len(times)
                print("Average Time: ", round(averageTime, 3), "s")
                if game_time < bestTime: 
                    bestTime = game_time
                    print("New Best!")
                print("Best Time: ", round(bestTime, 3), "s")
        
            time.sleep(0.5)
        else:
            loses += 1
        games += 1
        if(guessed):
            guesses += 1
            guessed = False
        
        print("Wins: ", wins)
        print("Loses: ", loses)
        print("Win Rate: ", int(100*(wins/games)), "%")
        print("Guess Rate: ", int(100*(guesses/games)), "%")

        #random_queue()
        cellsToVisit = PriorityQueue()
        cellsSeen.clear()
        #random_queue()#gives it a list of random points to click if no gaurenteed safe spots
        board = [[UNKNOWN for _ in range(COLS)] for _ in range(ROWS)]
        gameWon = False
        click_cell(RESTARTX, RESTARTY)#Restart Button
        time.sleep(0.1)
        click_cell(int(ROWS/2), int(COLS/2))#Start with center
        print("Started Timer")
        game_start_time = time.time()
        time.sleep(0.5)#Animation Delay

    else:
        update_board_state()
        if cellsToVisit.empty():
            if(all(cell != UNKNOWN for row in board for cell in row)):
                print("Stopped Timer")
                game_time = time.time() - game_start_time
                while(gameActive == True):
                    img = reload_frame()
                    gameActive = check_game_state()                    
                    time.sleep(0.1)
            else:
                print("doing advanced search")
                if not advanced_search():
                    time.sleep(0.5)
                    print("guessing")
                    guessed = True
                    found = False
                    for y in range(ROWS):
                        if found:
                            break
                        for x in range(COLS):
                            if board[y][x] == UNKNOWN:
                                randCell = x, y
                                cellsToVisit.put(randCell, 0)
                                found = True
                                break
        #print_board()
        checkingCells = True
        while(checkingCells and running):
            if cellsToVisit.empty():
                #Either check for more advanced patterns or randomly guess
                #random_queue()
                #print("no cells, random guess")
                checkingCells = False
            else:
                nextCell = cellsToVisit.get()
                #Only waste time clicking unknown cells
                if cellsSeen.__contains__(nextCell):
                    pass
                elif(board[nextCell[1]][nextCell[0]] == UNKNOWN):
                    #checkingCells = False
                    cellsSeen.append(nextCell)
                    click_cell(nextCell[0], nextCell[1])
            #time.sleep(0.001)
    #time.sleep(0.001)
