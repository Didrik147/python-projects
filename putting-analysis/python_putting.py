# -*- coding: utf-8 -*-

import json
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import os
import scipy

most_recent_file = None
most_recent_time = 0

"""
for entry in os.scandir():
    if entry.is_file() and "putt-maister-data-export" in entry.name:
        # get the modification time of the file using entry.stat().st_mtime_ns
        mod_time = entry.stat().st_mtime_ns
        if mod_time > most_recent_time:
            # update the most recent file and its modification time
            most_recent_file = entry.name
            most_recent_time = mod_time
"""

for entry in os.scandir():
    if entry.is_file() and "putt-maister-data-export" in entry.name:
        filename = entry.name
        L = filename.split('-')
        t = int(L[-1].split('.')[0])
        if t > most_recent_time:
            most_recent_file = entry.name
            most_recent_time = t


dt = datetime.utcfromtimestamp(t/1000).strftime('%Y-%m-%d')
print("Last updated")
print(dt)

print()

filename = most_recent_file
#filename = "putt-maister-data-export-1681116805115.json"

discs = ['Keystone', 'Deputy', 'Pure', 'Judge', 'Reko']
#discs.append('Shield')
discs.append('All')

discDict = {}

for disc in discs:
    tempDict = {}
    for m in range(4,9+1):    
        tempDict[f'{m}m'] = [0,0]
        
    discDict[disc] = tempDict


with open(filename, 'r') as f:
    data = json.load(f)


def add(disc, distance, nsuccess, ntried=4):
    global discDict
    discDict[disc][distance][0] += nsuccess
    discDict[disc][distance][1] += ntried

    

# Manually adding data
disc = "Keystone"
add(disc, "5m", 2)
add(disc, "6m", 3)
add(disc, "7m", 2)
add(disc, "8m", 2)
add(disc, "9m", 1)

disc = "Deputy"
add(disc, "5m", 2)
add(disc, "6m", 3)
add(disc, "7m", 3)
add(disc, "8m", 1)
add(disc, "9m", 3)

disc = "Pure"
add(disc, "5m", 4)
add(disc, "6m", 3)
add(disc, "7m", 2)
add(disc, "8m", 1)
add(disc, "9m", 1)


disc = "Judge"
add(disc, "5m", 3)
add(disc, "6m", 4)
add(disc, "7m", 4)
add(disc, "8m", 2)
add(disc, "9m", 1)


disc = "Shield"
if disc in discs:
    add(disc, "5m", 4)
    add(disc, "6m", 3)
    add(disc, "7m", 4)
    add(disc, "8m", 4)
    add(disc, "9m", 1)


disc = "Keystone"
add(disc, "5m", 4)
add(disc, "6m", 3)
add(disc, "7m", 3)
add(disc, "8m", 1)
add(disc, "9m", 3)


disc = "Deputy"
add(disc, "5m", 4)
add(disc, "6m", 3)
add(disc, "7m", 4)
add(disc, "8m", 3)
add(disc, "9m", 1)



total_putts = 0
total_hits = 0


# Not a good way to do it, but it works
for d in data["exportData"]["data"].values():
    ntried = d["putts"]
    t = d['created']/1000
    dt = datetime.utcfromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')
    
    #print(f"Created: {dt}")
    tags = d["tags"]
    disc = ""
    if len(tags) > 0:
        disc = tags[0]['translationKey']
        #if disc in discs:
            #print(f"Disc: {disc}")
    
    if d["rounds"] == 1:
        for i in range(len(d["distance"]["meters"])):
            m = d["distance"]["meters"][i]
            
            success = d["scores"][f'{i+1}']["score"]
            total_putts += ntried
            total_hits += success
            #print(f'{m}m: {success}/{ntried}')
            
            if disc in discs:
                discDict[disc][f'{m}m'][0] += success
                discDict[disc][f'{m}m'][1] += ntried
                
            discDict['All'][f'{m}m'][0] += success
            discDict['All'][f'{m}m'][1] += ntried
                
    elif d["rounds"] > 1:
        m = d["distance"]["meters"][0]
        for j in range(len(d["scores"])):
            success = d["scores"][f'{j+1}']["score"]
            total_putts += ntried
            total_hits += success
            
            #print(f'{m}m: {success}/{ntried}')
            
            if disc in discs:
                discDict[disc][f'{m}m'][0] += success
                discDict[disc][f'{m}m'][1] += ntried
                
            discDict['All'][f'{m}m'][0] += success
            discDict['All'][f'{m}m'][1] += ntried

    
    #print()
    

# Since I only have data for C1X, putting percentage is the same as C1X percentage
total_percent = (total_hits/total_putts)*100
print("Total hits:", total_hits)
print("Total putts:", total_putts)
print(f'Total C1X percentage: {total_percent:.1f}%')
"""
This gives the wrong percentage, for some reason.
"""

C1Xdict = {}

    
for disc in discDict.keys():
    l = []
    for p in discDict[disc].values():
        if p[1] > 0:
            l.append(p[0]/p[1])
    
    if len(l) > 0:
        C1Xdict[disc] = np.mean(l)*100
    
    
    
    
discColorDict = {
    "Keystone" : '#888888',
    "Deputy" : '#3333ff',
    'Pure' : '#FF69B4',
    'Judge' : '#990000',
    'Reko' : '#eeee00',
    'Shield' : '#ff0000',
    'All' : '#00cc00'
}
    
#colorList = ['#888', '#3333ff', '#FF69B4', '#900', '#f00']
#colorList = ['#888', '#3333ff', '#FF69B4', '#900']
#colorList = ['#888888', '#3333ff', '#FF69B4', '#990000', '#eeee00']

colorList = []

for d in discColorDict.keys():
    if d in discs:
        colorList.append(discColorDict[d])        


# All discs
#colorList.append('#00cc00')

"""
plt.bar(range(len(C1Xdict)), list(C1Xdict.values()), color=colorList, edgecolor='black')
plt.xticks(range(len(C1Xdict)), list(C1Xdict.keys()))
plt.ylabel("C1X putting percentage")
plt.show()
"""

x = list(range(4,8+1))
distList = []
for m in x:
    distList.append(f'{m}m')



ax = plt.figure().gca()
i = 0

for disc in discs:
    y = []
    for dist in distList:
        if discDict[disc][dist][1] == 0:
            percent = 0
        else:
            percent = discDict[disc][dist][0]/discDict[disc][dist][1]
            percent *= 100
            
        y.append(percent)
            
    plt.plot(x, y, '-o', color=colorList[i], label=disc)
    i += 1

"""
plt.xlabel("Distance [m]")
plt.ylabel('Putts made [%]')
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
plt.legend()
plt.show()
"""


x = []
y = []
percentages = []
colors = []
for dist in discDict["All"].keys():
    if dist != "9m":
        x.append(int(dist.split('m')[0]))
        v = discDict["All"][dist]
        y.append(100*v[0]/v[1])
    
        percentages.append(100*discDict["All"][dist][0]/discDict["All"][dist][1])
        if percentages[-1] > 50:
            colors.append("green")
        else:
            colors.append("red")



x = np.array(x)
y = np.array(y)
print()

disc = "Deputy"
print(disc)
print(discDict[disc])

"""
reg = np.polyfit(x,y,1)
a = reg[0]
b = reg[1]
yfit = a*x + b

print(f"a = {a:.0f}")
"""

"""
slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x, y)

yfit = slope*x + intercept

print(f"Slope: {slope:.0f}")
print(f"R2: {r_value**2:.4f}")


plt.plot(x,y, label="Data")
plt.plot(x, yfit, 'r', label="Linear model")
plt.legend()
plt.xlabel("Distance [m]")
plt.ylabel('Putts made [%]')
plt.ylim(0, 100)
plt.show()


plt.bar(distList, percentages, color=colors)
plt.axhline(y=50, color="black")
plt.yticks(np.arange(0, 100+1, step=10))
plt.xlabel("Distance")
plt.ylabel("Putts made [%]")
plt.show()
"""