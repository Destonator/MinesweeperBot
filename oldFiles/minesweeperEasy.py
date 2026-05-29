import mss
import mss.tools
from PIL import Image
import pyautogui
import random
import time
from pynput import keyboard
import threading
#Easy mode, Minesweeper window pinned right
##########
#Variables
##########
left = 1120
top = 450
width = 445 #10 cells across
height = 360 #8 cells tall

cellWidth = width / 10
cellHeight = height / 8

gameActive = False
gameWon = False

pyautogui.FAILSAFE = True

###########################
#Emergency Escape Click Esc
###########################
running = True
def on_press(key):
    global running
    try:
        if key == keyboard.Key.esc:
            print("ESC pressed, stopping...")
            running = False
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
    rx = cellWidth*0.5 + x*cellWidth    
    ry = cellHeight*0.5 + y*cellHeight
    pixel = img.getpixel((rx, ry))
    return pixel#in (r, g, b)

def cell_to_cords(x, y):
    rx = left + cellWidth*0.5 + x*cellWidth    
    ry = top + cellHeight*0.5 + y*cellHeight
    return rx, ry

def click_cell(x, y):
    pyautogui.moveTo(cell_to_cords(x, y)) #, duration=0.5*random.random()
    time.sleep(0.001)
    pyautogui.click()#clicks cell

def not_green(x, y):
    if (cell_to_color(x, y) == (180, 213, 102)):
        return False
    elif (cell_to_color(x, y) == (172, 207, 95)):
        return False
    else:
        return True

def check_game_state():
    if(cell_to_color(3, 6) == (84, 115, 54)):
        if(cell_to_color(2, 4) == (178, 214, 96)):
            print("Game Won")
            global gameWon
            gameWon = True
        else:
            print("Game Lost")
        return False
    else:
        return True
    
def reload_frame():
    with mss.mss() as sct:
        monitor = {"left": left,
                "top": top,
                "width": width,
                "height": height}
        screenshot = sct.grab(monitor)
        mss.tools.to_png(screenshot.rgb, screenshot.size, output="screenshot.png")
        return Image.open("screenshot.png")
#####
#Code
#####

img = reload_frame()
gameActive = check_game_state()

pyautogui.moveTo(cell_to_cords(5, 4)) #, duration=0.5*random.random()
time.sleep(0.01)
pyautogui.click()#enters window
pyautogui.click()#clicks cell

cellsSeen = list()

while(running):
    img = reload_frame()
    gameActive = check_game_state()
    if(gameWon == True):
        break
    if(not gameActive):
        cellsSeen.clear()
        click_cell(3, 6)#Restarts Game
    else:
        checkingCells = True
        count = 0

        while(checkingCells):
            nextCell = (random.randint(0, 9), random.randint(0, 7))
            if(cellsSeen.__contains__(nextCell)):
                print("cell already seen")
            elif(not_green(nextCell[0], nextCell[1])):
                cellsSeen.append(nextCell)
                print(nextCell[0])
                print(nextCell[1])
                print("cell not green, skipping")
            else:
                checkingCells = False
                cellsSeen.append(nextCell)
                click_cell(nextCell[0], nextCell[1])
            count += 1
            if count > 10:
                break
            time.sleep(0.001)
    time.sleep(0.001)


    


