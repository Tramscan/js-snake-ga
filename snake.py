# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 10:23:46 2016
@author: lab301-user28
"""

import os
from selenium import webdriver
import win32com.client as comctl
from random import randint
import time
import random
import math
e=open('popFit.txt', 'w')
f=open('maxFit.txt', 'w')
save=open('savedPopulation.txt', 'w')
log=open('log1.txt','w')
chromedriver="C:/Python34/Scripts/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver

wsh = comctl.Dispatch("WScript.Shell")
wsh.AppActivate("http://www.me.umn.edu/~dockt036/snake.html")


driver = webdriver.Chrome(executable_path='C:/Python34/Scripts/chromedriver')
driver.get('http://www.me.umn.edu/~dockt036/snake.html')
hidden_element = driver.find_element_by_id('sbTryAgain0')
element=driver.find_element_by_xpath("(//div[@class='snake-panel-component'])[2]")
def correctDir(moveArr):
    newArr=[]
    newArr.append(moveArr[0])
    for move in moveArr:
        movIndex=moveArr.index(move)
        newArrInd=movIndex+1
        if(move=="{RIGHT}"):
            newArr.append(random.choice(["{UP}","{DOWN}"]))
            moveArr[movIndex+1]=newArr[newArrInd]
        if(move=="{LEFT}"):
            newArr.append(random.choice(["{UP}","{DOWN}"]))
            moveArr[movIndex+1]=newArr[newArrInd]
        if(move=="{UP}"):
            newArr.append(random.choice(["{RIGHT}","{LEFT}"]))
            moveArr[movIndex+1]=newArr[newArrInd]
        if(move=="{DOWN}"):
            newArr.append(random.choice(["{RIGHT}","{LEFT}"]))
            moveArr[movIndex+1]=newArr[newArrInd]
    return newArr
    
def createIndividual(length,mintim, maxtim): # creates array of arrays (individual = [[wait time(ex. float 0.3), wait time, etc][direction (ex. int 1, 1 corresponds to right), directon,][fitness of individual]])
    return [[random.uniform(mintim,maxtim) for x in range(length)],[randint(0,3) for x in range(length)],[]]
    
def changeInt(int1):#converts integer from array to corresponding direction that can be sent as a key
    if(int1==0):
        return '{UP}'
    elif(int1==1):
        return '{RIGHT}'
    elif(int1==2):
        return '{DOWN}'
    elif(int1==3):
        return '{LEFT}'
    else:
        return int1

def run(ind):#runs through the movement code (2 arrays, one for wait time, one for direction of snake)
    for x in range(len(ind[0])):
        if hidden_element.is_displayed():#if the snake dies, start next individual
            break
            wsh.SendKeys(" ")
        time.sleep(ind[0][x])
        if hidden_element.is_displayed():#if the snake dies, start next individual
            break
            wsh.SendKeys(" ")
        wsh.SendKeys(ind[1][x])
        if hidden_element.is_displayed():#if the snake dies, start next individual
            break
            wsh.SendKeys(" ")
        print(ind[1][x])#prints what keys are being pressed
        log.write(str(ind[1][x]))
        log.write("\n")
        if hidden_element.is_displayed():#if the snake dies, start next individual
            break
            wsh.SendKeys(" ")
    
def indfit(time): #finds individual's fitness
    points=element.text
    for i in points:
        if(points[points.index(i)-1]==" " and points[points.index(i)-2]==":"):
            pts=float(points[points.index(i):])
            return math.pow(time,pts)
            break #if the snake gets a point, the fitness goes up exponentially so it can favor code that can get the most amount of points
def createPopulation(size, length, mintim, maxtim): #creates a population of individuals (array of array of arrays)
    print("creating population of size ",size," and length ",length,"...")
    log.write(("creating population of size "+str(size)+" and length "+str(length)+"..."))
    log.write("\n")
    population=[]
    for x in range(size):
        print("creating individual",x,"...")
        log.write(("creating individual"+str(x)+"..."))
        log.write("\n")
        population.append(createIndividual(length, mintim, maxtim))
        
    return population

def cyclePop(pop): #runs the code
    print("cycling population...")
    log.write("cycling population...")
    log.write("\n")
    index1=0
    print("changing all values to computer readable code...")
    log.write("changing all values to computer readable code...")
    log.write("\n")
    for indiv in range(len(pop)):
        for dirint in range(len(pop[indiv][1])):
            pop[indiv][1][dirint]=changeInt(pop[indiv][1][dirint])
    for x in pop:
        print("running individual",index1+1,"...")
        log.write(("running individual"+str(index1+1)+"..."))
        log.write("\n")
        start_time=time.time()
        pop1=pop[index1]
        run(pop1)
        pop[index1][2]=indfit(time.time()-start_time)
        print("Fitness of individual ",(index1+1),": ",pop[index1][2])
        log.write(("Fitness of individual "+str(index1+1)+": "+str(pop[index1][2])))
        log.write("\n")
        wsh.SendKeys(" ")
        index1+=1
    print("Population Fitness: ",popFitScore(pop))
    log.write(("Population Fitness: "+str(popFitScore(pop))))
    log.write("\n")
    e.write(str(str(popFitScore(pop))+'\n'))
def popFitScore(pop): # finds the fitness score of the population (this will return every time to show evolution in progress)
    print("getting a fitness for this population...")
    log.write("getting a fitness for this population...")
    log.write("\n")
    sum1=0
    for j in pop:
        sum1+=j[2]
    return sum1/len(pop)
def sort(items):
    print("sorting population...")
    log.write("sorting population...")
    log.write("\n")
    fitArr=[]
    newArr=[]
    [fitArr.append(i[2]) for i in items]
    fitArr.sort(reverse=True)
    [newArr.append(m) for n in fitArr for m in items if(n==m[2])]
    return newArr
def mixtraitscross(ind1,ind2): #mixes traits by swapping the traits of two individuals
    print("crossmixing traits...")
    log.write("crossmixing traits...")
    log.write("\n")
    index1=0
    for i in ind1: #cycles through population
        if index1%2==1: #every other value
            ind1[index1]=ind2[index1] #sets value
        index1+=1
def mixtraitsavg(ind1,ind2): #mixes traits by averaging traits of the two individuals
    print("avgmixing traits...")
    log.write("avgmixing traits...")
    log.write("\n")
    index1=0
    for i in ind1: #cycles through population
        ind1[index1]=(ind1[index1]+ind2[index1])/2 #averages values
        index1+=1
def evolve(pop,mutrate,killpercent,sammin,sammax):#evolves population
    print("evolving population...")
    log.write("evolving population...")
    log.write("\n")
    pop=sort(pop)#sorts population
    f.write(str(str(pop[0][2])+'\n'))#writing the max fitness to the file
    startmutlen=(len(pop)-(killpercent*len(pop)))#finds the value where it will start mutating instead of breeding
    mutrateind=mutrate*len(pop[0][0])# how many values will it mutate 
    for ig in pop:
        index1=pop.index(ig)
        if index1<startmutlen:#mutates values if it's in the required range
            for g in range(int(mutrateind)):                                                                                           
                pop[index1][1][randint(0,len(pop[0][0])-1)]=changeInt(randint(0,3))
                pop[index1][0][randint(0,len(pop[0][0])-1)]=random.uniform(sammin,sammax)
                print("individual #",index1,"is good and switching vals")
                log.write(("individual #"+str(index1)+"is good and switching vals"))
                log.write("\n")
        else:  #if it's one of the worst ones, it breeds the good ones and makes a child.
            if(index1<len(pop)-1):
                mixtraitscross(pop[(len(pop)-1)-index1][1],pop[(len(pop)-1)-(index1+1)][1])
                mixtraitsavg(pop[(len(pop)-1)-index1][0],pop[(len(pop)-1)-(index1+1)][0])
                print("individual #",index1,"is bad and switching vals")
                log.write(("individual #"+str(index1)+"is bad and switching vals"))
                log.write("\n")
    return(pop)
wsh.SendKeys(" ")
nickclinegenerationCap=4
populationSize=30
moveLimit=10000
waitMin=0
waitMax=.05
deathRate=.40
mutationRate=.15
population=createPopulation(populationSize,moveLimit,waitMin,waitMax)#creates population of size 30, each individual has 30 moves with a wait time between 0 and 2 seconds.
for integer in range(nickclinegenerationCap):#runs through 4 generations
    cyclePop(population)#runs population
    if(integer==0):
        for indiv in range(len(population)):
            population[indiv][1]=correctDir(population[indiv][1])
    population=evolve(population,mutationRate,deathRate,waitMin,waitMax)#mutates the top 82% with a mutation rate of 5%, and breeds the bottom 18%.
for indiv in population:
    save.write(str(indiv)+"|"+"\n")


save.close()
e.close()
f.close()
log.close()
