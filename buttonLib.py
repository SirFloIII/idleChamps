# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 20:43:27 2019

@author: Flo
"""

import yaml

buttons = ["Toggle Auto Progress Upper Left",
           "Toggle Auto Progress Lower Right",
           "Gold Upper Left",
           "Gold Lower Right",
           "Left Upper Clicking Area",
           "Right Lower Clicking Area",
           "Close Ad",
           "Scroll Left",
           "Scroll Right",
           "Lvl Champ 0",
           "Lvl Champ 1",
           "Lvl Champ 2",
           "Lvl Champ 3",
           "Lvl Champ 4",
           "Lvl Champ 5",
           "Lvl Champ 6",
           "Toggle Buy Mode",
           "Spec: 1 of 2",
           "Spec: 2 of 2",
           "Spec: 1 of 3",
           "Spec: 2 of 3",
           "Spec: 3 of 3",
           "Spec: 1 of 5",
           "Spec: 2 of 5",
           "Spec: 3 of 5",
           "Spec: 4 of 5",
           "Spec: 5 of 5",
           "Complete Adventure",
           "Confirm Complete Adventure",
           "Cancel Complete Adventure",
           "Continue",
           "Campaign: Grand Tour",
           "Campaign: Tomb",
           "Campaign: Dragon",
           "Campaign: Descent",
           "Campaign: Center Icon",
           "Campaign: Mission 1",
           "Campaign: Mission 1.1",
           "Campaign: Mission 1.2",
           "Campaign: Mission 1.3",
           "Campaign: Mission 2",
           "Campaign: Mission 2.1",
           "Campaign: Mission 2.2",
           "Campaign: Mission 2.3",
           "Campaign: Mission 3",
           "Campaign: Start Mission",
           "Familiar: Bag",
           "Familiar: Click Spot 0",
           "Familiar: Click Spot 1",
           "Familiar: Click Spot 2",
           "Familiar: Click Spot 3",
           "Familiar: Click Spot 4",
           "Familiar: Click Spot 5",
           ]

def calibrate(fromScratch = False):
    import keyboard
    import mouse
    
    if fromScratch:
        buttonPos = dict()
    else:
        buttonPos = loadButtonPos()
        
    for button in buttons:
        if button not in buttonPos:
            print(button)
            keyboard.wait("F2")
            buttonPos[button] = list(mouse.get_position())
            print(buttonPos[button])
    
    with open("buttonPos.yaml", "w") as stream:
        yaml.dump(buttonPos, stream)
    
    return buttonPos

def loadButtonPos():
    with open("buttonPos.yaml", "r") as stream:
        return yaml.load(stream)

if __name__ == "__main__":
    
    calibrate()
    
    
    
    
    
    
    
    
    











