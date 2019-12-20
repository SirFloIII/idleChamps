# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 18:02:33 2019

@author: Flo
"""

#import pyautogui
import keyboard
import mouse
import pygetwindow as win
import buttonLib
import time
#from tqdm import tqdm
import pytesseract
import desktopmagic.screengrab_win32 as screenshot
import configLib

buttonPos = buttonLib.loadButtonPos()
config = configLib.loadConfig()
stats = configLib.loadStats(config)


idle = win.getWindowsWithTitle("Idle Champions")[0]
idle.moveTo(-1920,0)

def pressButton(button, dt = 0.1):
    #print("Clicking:", button)
    mouse.move(*buttonPos[button], duration = dt)
    time.sleep(0.05)
    mouse.click()
    time.sleep(0.05)

def pressButtonSequence(buttons, dt = 0.5):
    for button in buttons:
        pressButton(button)
        time.sleep(dt)

def focus():
    try:
        idle.activate()
    except win.PyGetWindowException:
        if idle.isActive:
            pass
        else:
            keyboard.press_and_release("ALT+TAB")
            assert idle.isActive
        
def lvlChamp(k):
    """
    k = 0 ... Clicking damage
    k > 0 ... Champ slot
    """
    
    if k == 0:
        pressButtonSequence(["Scroll Left"] + ["Lvl Champ " + str(k)])
    else:
        focus()
        keyboard.press_and_release("F"+str(k))
    
x, y = buttonPos["Left Upper Clicking Area"]
dx, dy = buttonPos["Right Lower Clicking Area"]
dx, dy = dx - x, dy - y

def placeFamiliarsOnClickingPos(n = 1):
    #n = number of familiars
    #does only work at the start of a round
    for i in range(min(6,n)):
        mouse.drag(*buttonPos["Familiar: Bag"],
                   *buttonPos["Familiar: Click Spot " + str(i)],
                   duration = 0.2)
        time.sleep(0.2)

def restartMadWizard():
    pressButtonSequence(["Close Ad",
                         "Close Ad",
                         "Complete Adventure",
                         "Confirm Complete Adventure"])
    time.sleep(15)
    pressButton("Continue")
    time.sleep(3)
    pressButtonSequence(["Campaign: Grand Tour",
                         "Campaign: Center Icon",
                         "Campaign: Mission 2",
                         "Campaign: Start Mission"])
    time.sleep(10)


formationHotkeys = {1:"q", 2:"w", 3:"e"}
def setFormation():
    focus()
    f = config["Formation Slot"]
    keyboard.press_and_release(formationHotkeys[f])

def playMadWizard(condition):
    restartMadWizard()
    placeFamiliarsOnClickingPos()
    
    pressButtonSequence(["Lvl Champ 0"]*10)
    
    playClickingStyle(timeCondition(2))
    
    pressButton("Left Upper Clicking Area")
    for i in range(1, 7):
        lvlChamp(i)
    
    playClickingStyle(condition)
    
    
#    upgradeCount = {i:0 for i in config["Champions"]}
#    upgradeCount[1] = 1
#    
#    specCount = {i:0 for i in config["Champions"]}
#    
#    
#    while condition():
#        if control_allowed:
#            upgradeCosts = {i:stats[i][upgradeCount[i]][1] for i in config["Champions"]}
#            cheapestChamp = min(upgradeCosts.items(), key = lambda x:x[1])[0]
#            
#            if getGold() > upgradeCosts[cheapestChamp]:
#                lvlChamp(cheapestChamp)
#                setFormation()
#                if stats[cheapestChamp][upgradeCount[cheapestChamp]][2] == "Spec":
#                    spec = config["Spec"][cheapestChamp][specCount[cheapestChamp]]
#                    pressButton(f"Spec: {spec[0]} of {spec[1]}", dt = 0.5)
#                    specCount[cheapestChamp] += 1
#                upgradeCount[cheapestChamp] += 1
#            else:
#                time.sleep(10)
#        else:
#            time.sleep(1)

def clickingLoop(n):
    if control_allowed:
        for i in range(n):
            mouse.move(x + 10*i%dx, y + 50*i%dy, duration = 0.05)
            mouse.click()
        lvlChamp(0)
    else:
        time.sleep(10)
   
def playClickingStyle(condition):
    while condition():
        clickingLoop(50)
        
def timeCondition(duration):
    startTime = time.time()
    return lambda: time.time() - startTime < duration * 60


def getGold():
    try:
        img = screenshot.getRectAsImage((*buttonPos["Gold Upper Left"],
                                         *buttonPos["Gold Lower Right"]))
        string = pytesseract.image_to_string(img)
        if len(string) == 7:
            gold = float(string[:4]) * 10 ** int(string[-2:])
        else:
            gold = float(string)
        return gold
    except:
        return 0

#playClickingStyle(timeCondition(1))
    

#pressButton("Left Upper Clicking Area")
#for i in range(1, 7):
#    lvlChamp(i)

try:
    control_allowed = False
    def toggle(*args):
        global control_allowed
        control_allowed = not control_allowed
        print("control_allowed:", control_allowed)
        
    keyboard.on_press_key("rollen-feststell", toggle)
    
    print("Waiting for Control Permission...")
    
    while True:
               
        while not control_allowed:
            time.sleep(1)
            
        focus()
        print("Starting new Mad Wizard Run.")
        playMadWizard(timeCondition(30))
    
finally:
    keyboard.unhook_all()
    
