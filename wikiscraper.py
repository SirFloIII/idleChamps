# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 04:15:32 2019

@author: Flo
"""

import requests
import lxml.html as lh
import yaml


urlbase = "https://idlechampions.gamepedia.com/"
subpage = "Champions"

page = requests.get(urlbase+subpage)

doc = lh.fromstring(page.content)

rows = doc.xpath('//tr')

header = rows[0].text_content().split("\n")[1::2]

champions = dict()

for row in rows[1:]:
    if len(row) != 15:
        break
    l = row.text_content().split("\n")[1::2]
    ll = []
    for i in l:
        try:
            ll.append(float(i) if "e" in i else int(i))
        except ValueError:
            ll.append(i)
    champ = dict(zip(header, ll))
    del champ["Icon"]
    champions[champ["Name"]] = champ
    
with open("champions.yaml", "w") as stream:
    yaml.dump(champions, stream)


for champ in champions:

    page = requests.get(urlbase+champ)

    doc = lh.fromstring(page.content)
    
    rows = doc.xpath('//tr')
    
    lvltable = False
    
    stats = []
    
    for rawRow in rows:
        row = rawRow.text_content().split("\n")[1::2]
#        print(row)
        if row[0] == "Level":
            header = row
            lvltable = True
        elif lvltable:
            if row[0] == "Total:":
                break
            else:
                
                if "Spec" in row[2]:
                    tag = "Spec"
                elif "Unlock" in row[2]:
                    tag = "Unlock"
                elif row[2]:
                    tag = "SelfDmg"
                elif row[3]:
                    tag = "AllDmg"
                else:
                    tag = "Skill"
                
                stats.append([int(row[0]), float(row[1]), tag])
    
    with open("Champions\\" + champ + ".yaml", "w") as stream:
        yaml.dump(stats, stream)
    
    





























