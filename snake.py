# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 10:23:46 2016

@author: lab301-user28
"""

import selenium, os, urllib
from selenium import webdriver
import win32com.client as comctl
from random import randint
import time
import random
import lxml
import math
from lxml import html
from urllib import request

from bs4 import BeautifulSoup

chromedriver="C:/Python34/Scripts/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver

wsh = comctl.Dispatch("WScript.Shell")
wsh.AppActivate("http://www.me.umn.edu/~dockt036/snake.html")


driver = webdriver.Chrome(executable_path='C:/Python34/Scripts/chromedriver')
driver.get('http://www.me.umn.edu/~dockt036/snake.html')
hidden_element = driver.find_element_by_id('sbTryAgain0')
element=driver.find_element_by_class_name('snake-panel-component').find_element_by_class_name('snake-panel-component') #gets the element of the length
def createIndividual(length,mintim, maxtim): # creates array of arrays (individual = [[wait time(ex. float 0.3), wait time, etc][direction (ex. int 1, 1 corresponds to right), directon,][fitness of individual]])
    return [[random.uniform(mintim,maxtim) for x in range(length)],[randint(0,3) for x in range(length)],[]]
    
def changeInt(int1):#converts integer from array to corresponding direction that can be sent as a key
    if(int1==0):
        return '{UP}'
    if(int1==1):
        return '{RIGHT}'
    if(int1==2):
        return '{DOWN}'
    if(int1==3):
        return '{LEFT}'

def run(ind):#runs through the movement code (2 arrays, one for wait time, one for direction of snake)
    for x in range(len(ind[0])):
        if hidden_element.is_displayed():#if the snake dies, start next individual
            break
            wsh.SendKeys(" ")
        time.sleep(ind[0][x])
        wsh.SendKeys(changeInt(ind[1][x]))
        print(changeInt(ind[1][x]))#prints what keys are being pressed
    
def indfit(time): #finds individual's fitness
    points=int(element.text[7:]) #not sure if this will work
    print(points)
    #points=int(input("how many points did the individual get: "))#right now this code above is supposed to get the value in the bottom left hand corner for length. The school's firewall blocks the website, so it returns nothing.
    
    for i in points:
        if(points[i-1]==" " and points[i-2]==":"):
            pts=points[8:]
            return math.pow(time,pts)
            break
    
    #pts=1 #temporary
    #return (pts/time)
    #return math.pow(time,pts)#if the snake gets a point, the fitness goes up exponentially so it can favor code that can get the most amount of points

def createPopulation(size, length, mintim, maxtim): #creates a population of individuals (array of array of arrays)
    population=[]
    for x in range(size):
        population.append(createIndividual(length, mintim, maxtim))
    return population

def cyclePop(pop): #runs the code
    index1=0
    for x in pop:
        start_time=time.time()
        pop1=pop[index1]
        run(pop1)
        pop[index1][2]=indfit(time.time()-start_time)
        print("Fitness of individual ",(index1+1),": ",pop[index1][2])
        wsh.SendKeys(" ")
        index1+=1
    print("Population Fitness: ",popFitScore(pop))
    with open('popFit.txt', 'w') as f:
        f.write(str(str(popFitScore(pop))+'\n'))
def popFitScore(pop): # finds the fitness score of the population (this will return every time to show evolution in progress)
    sum1=0
    for x in pop:
        sum1+=x[2]
    return sum1/len(pop)
def bubble_sort(items):
        """bubble sort"""
        for i in range(len(items)):
                for j in range(len(items)-1-i):
                        if items[j][2] > items[j+1][2]:
                                items[j], items[j+1] = items[j+1], items[j]
def mixtraitscross(ind1,ind2): #mixes traits by swapping the traits of two individuals
    index1=0
    for i in ind1: #cycles through population
        if index1%2==1: #every other value
            ind1[index1]=ind2[index1] #sets value
        index1+=1
def mixtraitsavg(ind1,ind2): #mixes traits by averaging traits of the two individuals
    index1=0
    for i in ind1: #cycles through population
        ind1[index1]=(ind1[index1]+ind2[index1])/2 #averages values
        index1+=1
def evolve(pop,mutrate,killpercent,sammin,sammax):#evolves population
    bubble_sort(pop)#sorts population
    with open('maxFit.txt', 'w') as f:
        f.write(str(str(pop[0][2])+'\n'))#writing the max fitness to the file
    startmutlen=(len(pop)-(killpercent*len(pop)))#finds the value where it will start mutating instead of breeding
    mutrateind=mutrate*len(pop[0][0])# how many values will it mutate
    for ig in pop:
        index1=pop.index(ig)
        if index1<startmutlen:#mutates values if it's in the required range
            for g in range(int(mutrateind)):
                ig[0][randint(0,len(pop[0][0])-1)]=randint(0,3)
                ig[1][randint(0,len(pop[0][0])-1)]=random.uniform(sammin,sammax)
        else:
            if((index1+1)!=len(pop)):  #if it's one of the worst ones, it breeds the good ones and makes a child.                                                    
                mixtraitscross(pop[len(pop[0])-index1][0],pop[len(pop[0])-(index1+1)][0])
                mixtraitsavg(pop[len(pop[0])-index1][1],pop[len(pop[0])-(index1+1)][1])

index8=0
with open('page.txt', 'w') as f:
        f.write(element.text) #writes element to a .txt file
while(index8<=50):#runs through 50 generations
    x=createPopulation(30,30,0,2)#creates population of size 30, each individual has 30 moves with a wait time between 0 and 2 seconds.
    cyclePop(x)#runs population
    evolve(x,.05,.35,0,2)#mutates the top 75% with a mutation rate of 5%, and breeds the bottom 35%.
    index8+=1#increment population.
