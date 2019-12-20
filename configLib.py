# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 05:49:52 2019

@author: Flo
"""

import yaml

def createConfig(name = "config.yaml"):
    
    with open("champions.yaml", "r") as f:
        champs = yaml.load(f)
    
    config = dict()
    
    print("Select Champs for each Slot!")
    print("0 for None, >0 else\n")
    selectedChamps = dict()
    
    for i in range(1, 13):
        l = [champ for champ in champs if champs[champ]["Slot"] == i]
        print(i, l)
        k = int(input())
        print("\n")
        if k == 0:
            pass
#            selectedChamps[i] = None
        else:
            selectedChamps[i] = l[k - 1]
    
    config["Champions"] = selectedChamps
    
    print("\nSpecs!\n")
    
    config["Spec"] = dict()
    
    for index, champ in selectedChamps.items():
        if champ:
            config["Spec"][index] = []
            with open("Champions\\" + champ + ".yaml", "r") as f:
                stats = yaml.load(f)
            for line in stats:
                if line[2] == "Spec":
                    k = input("Choose Spec for " + str(champ) + " at Lvl " + str(line[0]))
                    c = input("out of how many Choices?")
                    print("\n")
                    config["Spec"][index].append([k, c])
    
    
    print("Select Formation Save Slot!")
    print("(1-3)")
    k = input()
    print("\n")
    
    config["Formation Slot"] = int(k)
    
    with open(name, "w") as f:
        yaml.dump(config, f)

def loadConfig(name = "config.yaml"):
    
    with open(name, "r") as f:
        return yaml.load(f)

def loadStats(config):

    stats = dict()
    
    for index, champ in config["Champions"].items():
        with open("Champions\\" + champ + ".yaml", "r") as f:
            stats[index] = yaml.load(f)
    
    return stats










































