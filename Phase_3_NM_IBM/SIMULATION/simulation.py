import random as possible
import time
import threading
import pygame as grapics
import sys

Dallright = {0:10, 1:10, 2:10, 3:10}
Ddanger = 150
Dstarter = 5

sig = []
noOfsig = 4
callright = 0
usedallright = (callright+1)%noOfsig
cstarter = 0 
speed = {'car':2, 'bus':1.3, 'truck':1.3, 'bike':1.8,'ambu':3.5,'police':2.3}

x_plane = {'rite':[0,0,0], 'dwn':[755,727,697], 'lft':[1400,1400,1400],'top':[602,627,657]}    
y = {'rite':[348,370,398],'dwn':[0,0,0],'lft':[498,466,436], 'top':[800,800,800] }

objects = {'rite': {0:[], 1:[], 2:[], 'away':0}, 'dwn': {0:[], 1:[], 2:[], 'away':0}, 'lft': {0:[], 1:[], 2:[], 'away':0}, 'top': {0:[], 1:[], 2:[], 'away':0}}
objTypes = {0:'bus', 1:'car', 2:'bike', 3:'truck',4:'police',5:'ambu'}
trun_num = {0:'rite', 1:'dwn', 2:'lft', 3:'top'}

waveValue = [(530,230),(810,230),(810,570),(530,570)]
waveTimerValue = [(530,210),(810,210),(810,550),(530,550)]

pauseLines = {'rite': 590, 'dwn': 330, 'lft': 800, 'top': 535}
Dpause = {'rite': 580, 'dwn': 320, 'lft': 810, 'top': 545}

pausepingGap = 25
movGap = 25

workingobjTypes = { 'bus': True,'police':True, 'truck': True, 'bike': True, 'ambu':True,'car': True}
workingobjTypesList = []
objectsRotate = {'rite': {1:[], 2:[]}, 'dwn': {1:[], 2:[]}, 'lft': {1:[], 2:[]}, 'top': {1:[], 2:[]}}
objectsNotRotate = {'rite': {1:[], 2:[]}, 'dwn': {1:[], 2:[]}, 'lft': {1:[], 2:[]}, 'top': {1:[], 2:[]}}
rotationAngle = 3
middle = {'rite': {'x_plane':705, 'y':445}, 'dwn': {'x_plane':695, 'y':450}, 'lft': {'x_plane':695, 'y':425}, 'top': {'x_plane':695, 'y':400}}

possibleallrightwaveTimer = True
 
possibleallrightwaveTimerRange = [10,20]

grapics.init()
simulation = grapics.sprite.Group()

class Trafficwave:
    def __init__(self, danger, starter, allright):
        self.danger = danger
        self.starter = starter
        self.allright = allright
        self.waveTex_planet = ""
        
class obj(grapics.sprite.Sprite):
    def __init__(self, lane, objClass, direction_number, direction, will_turn):
        grapics.sprite.Sprite.__init__(self)
        self.lane = lane
        self.objClass = objClass
        self.speed = speed[objClass]
        self.direction_number = direction_number
        self.direction = direction
        self.x_plane = x_plane[direction][lane]
        self.y = y[direction][lane]
        self.away = 0
        self.willTurn = will_turn
        self.Rotate = 0
        self.rotateAngle = 0
        objects[direction][lane].append(self)
        self.index_plane = len(objects[direction][lane]) - 1
        self.awayIndex_plane = 0
        way = "images/" + direction + "/" + objClass + ".png"
        self.originalImage = grapics.image.load(way)
        self.image = grapics.image.load(way)

        if(len(objects[direction][lane])>1 and objects[direction][lane][self.index_plane-1].away==0):   
            if(direction=='rite'):
                self.pause = objects[direction][lane][self.index_plane-1].pause 
                - objects[direction][lane][self.index_plane-1].image.get_rect().width 
                - pausepingGap         
            elif(direction=='lft'):
                self.pause = objects[direction][lane][self.index_plane-1].pause 
                + objects[direction][lane][self.index_plane-1].image.get_rect().width 
                + pausepingGap
            elif(direction=='dwn'):
                self.pause = objects[direction][lane][self.index_plane-1].pause 
                - objects[direction][lane][self.index_plane-1].image.get_rect().height 
                - pausepingGap
            elif(direction=='top'):
                self.pause = objects[direction][lane][self.index_plane-1].pause 
                + objects[direction][lane][self.index_plane-1].image.get_rect().height 
                + pausepingGap
        else:
            self.pause = Dpause[direction]
            
        if(direction=='rite'):
            temp = self.image.get_rect().width + pausepingGap    
            x_plane[direction][lane] -= temp
        elif(direction=='lft'):
            temp = self.image.get_rect().width + pausepingGap
            x_plane[direction][lane] += temp
        elif(direction=='dwn'):
            temp = self.image.get_rect().height + pausepingGap
            y[direction][lane] -= temp
        elif(direction=='top'):
            temp = self.image.get_rect().height + pausepingGap
            y[direction][lane] += temp
        simulation.add(self)

    def output(self, screen):
        screen.blit(self.image, (self.x_plane, self.y))

    def move(self):
        if(self.direction=='rite'):
            if(self.away==0 and self.x_plane+self.image.get_rect().width>pauseLines[self.direction]):
                self.away = 1
                objects[self.direction]['away'] += 1
                if(self.willTurn==0):
                    objectsNotRotate[self.direction][self.lane].append(self)
                    self.awayIndex_plane = len(objectsNotRotate[self.direction][self.lane]) - 1
            if(self.willTurn==1):
                if(self.lane == 1):
                    if(self.away==0 or self.x_plane+self.image.get_rect().width<pauseLines[self.direction]+40):
                        if((self.x_plane+self.image.get_rect().width<=self.pause or (callright==0 and cstarter==0) or self.away==1) and (self.index_plane==0 or self.x_plane+self.image.get_rect().width<(objects[self.direction][self.lane][self.index_plane-1].x_plane - movGap) or objects[self.direction][self.lane][self.index_plane-1].Rotate==1)):               
                            self.x_plane += self.speed
                    else:
                        if(self.Rotate==0):
                            self.rotateAngle += rotationAngle
                            self.image = grapics.transform.rotate(self.originalImage, self.rotateAngle)
                            self.x_plane += 2.4
                            self.y -= 2.8
                            if(self.rotateAngle==90):
                                self.Rotate = 1
                                objectsRotate[self.direction][self.lane].append(self)
                                self.awayIndex_plane = len(objectsRotate[self.direction][self.lane]) - 1
                        else:
                            if(self.awayIndex_plane==0 or (self.y>(objectsRotate[self.direction][self.lane][self.awayIndex_plane-1].y + objectsRotate[self.direction][self.lane][self.awayIndex_plane-1].image.get_rect().height + movGap))):
                                self.y -= self.speed
                elif(self.lane == 2):
                    if(self.away==0 or self.x_plane+self.image.get_rect().width<middle[self.direction]['x_plane']):
                        if((self.x_plane+self.image.get_rect().width<=self.pause or (callright==0 and cstarter==0) or self.away==1) and (self.index_plane==0 or self.x_plane+self.image.get_rect().width<(objects[self.direction][self.lane][self.index_plane-1].x_plane - movGap) or objects[self.direction][self.lane][self.index_plane-1].Rotate==1)):                 
                            self.x_plane += self.speed
                    else:
                        if(self.Rotate==0):
                            self.rotateAngle += rotationAngle
                            self.image = grapics.transform.rotate(self.originalImage, -self.rotateAngle)
                            self.x_plane += 2
                            self.y += 1.8
                            if(self.rotateAngle==90):
                                self.Rotate = 1
                                objectsRotate[self.direction][self.lane].append(self)
                                self.awayIndex_plane = len(objectsRotate[self.direction][self.lane]) - 1
                        else:
                            if(self.awayIndex_plane==0 or ((self.y+self.image.get_rect().height)<(objectsRotate[self.direction][self.lane][self.awayIndex_plane-1].y - movGap))):
                                self.y += self.speed
            else: 
                if(self.away == 0):
                    if((self.x_plane+self.image.get_rect().width<=self.pause or (callright==0 and cstarter==0)) and (self.index_plane==0 or self.x_plane+self.image.get_rect().width<(objects[self.direction][self.lane][self.index_plane-1].x_plane - movGap))):                
                        self.x_plane += self.speed
                else:
                    if((self.awayIndex_plane==0) or (self.x_plane+self.image.get_rect().width<(objectsNotRotate[self.direction][self.lane][self.awayIndex_plane-1].x_plane - movGap))):                 
                        self.x_plane += self.speed
        elif(self.direction=='dwn'):
            if(self.away==0 and self.y+self.image.get_rect().height>pauseLines[self.direction]):
                self.away = 1
                objects[self.direction]['away'] += 1
                if(self.willTurn==0):
                    objectsNotRotate[self.direction][self.lane].append(self)
                    self.awayIndex_plane = len(objectsNotRotate[self.direction][self.lane]) - 1
            if(self.willTurn==1):
                if(self.lane == 1):
                    if(self.away==0 or self.y+self.image.get_rect().height<pauseLines[self.direction]+50):
                        if((self.y+self.image.get_rect().height<=self.pause or (callright==1 and cstarter==0) or self.away==1) and (self.index_plane==0 or self.y+self.image.get_rect().height<(objects[self.direction][self.lane][self.index_plane-1].y - movGap) or objects[self.direction][self.lane][self.index_plane-1].Rotate==1)):                
                            self.y += self.speed
                    else:   
                        if(self.Rotate==0):
                            self.rotateAngle += rotationAngle
                            self.image = grapics.transform.rotate(self.originalImage, self.rotateAngle)
                            self.x_plane += 1.2
                            self.y += 1.8
                            if(self.rotateAngle==90):
                                self.Rotate = 1
                                objectsRotate[self.direction][self.lane].append(self)
                                self.awayIndex_plane = len(objectsRotate[self.direction][self.lane]) - 1
                        else:
                            if(self.awayIndex_plane==0 or ((self.x_plane + self.image.get_rect().width) < (objectsRotate[self.direction][self.lane][self.awayIndex_plane-1].x_plane - movGap))):
                                self.x_plane += self.speed
                elif(self.lane == 2):
                    if(self.away==0 or self.y+self.image.get_rect().height<middle[self.direction]['y']):
                        if((self.y+self.image.get_rect().height<=self.pause or (callright==1 and cstarter==0) or self.away==1) and (self.index_plane==0 or self.y+self.image.get_rect().height<(objects[self.direction][self.lane][self.index_plane-1].y - movGap) or objects[self.direction][self.lane][self.index_plane-1].Rotate==1)):                
                            self.y += self.speed
                    else:   
                        if(self.Rotate==0):
                            self.rotateAngle += rotationAngle
                            self.image = grapics.transform.rotate(self.originalImage, -self.rotateAngle)
                            self.x_plane -= 2.5
                            self.y += 2
                            if(self.rotateAngle==90):
                                self.Rotate = 1
                                objectsRotate[self.direction][self.lane].append(self)
                                self.awayIndex_plane = len(objectsRotate[self.direction][self.lane]) - 1
                        else:
                            if(self.awayIndex_plane==0 or (self.x_plane>(objectsRotate[self.direction][self.lane][self.awayIndex_plane-1].x_plane + objectsRotate[self.direction][self.lane][self.awayIndex_plane-1].image.get_rect().width + movGap))): 
                                self.x_plane -= self.speed
            else: 
                if(self.away == 0):
                    if((self.y+self.image.get_rect().height<=self.pause or (callright==1 and cstarter==0)) and (self.index_plane==0 or self.y+self.image.get_rect().height<(objects[self.direction][self.lane][self.index_plane-1].y - movGap))):                
                        self.y += self.speed
                else:
                    if((self.awayIndex_plane==0) or (self.y+self.image.get_rect().height<(objectsNotRotate[self.direction][self.lane][self.awayIndex_plane-1].y - movGap))):                
                        self.y += self.speed
        elif(self.direction=='lft'):
            if(self.away==0 and self.x_plane<pauseLines[self.direction]):
                self.away = 1
                objects[self.direction]['away'] += 1
                if(self.willTurn==0):
                    objectsNotRotate[self.direction][self.lane].append(self)
                    self.awayIndex_plane = len(objectsNotRotate[self.direction][self.lane]) - 1
            if(self.willTurn==1):
                if(self.lane == 1):
                    if(self.away==0 or self.x_plane>pauseLines[self.direction]-70):
                        if((self.x_plane>=self.pause or (callright==2 and cstarter==0) or self.away==1) and (self.index_plane==0 or self.x_plane>(objects[self.direction][self.lane][self.index_plane-1].x_plane + objects[self.direction][self.lane][self.index_plane-1].image.get_rect().width + movGap) or objects[self.direction][self.lane][self.index_plane-1].Rotate==1)):                
                            self.x_plane -= self.speed
                    else: 
                        if(self.Rotate==0):
                            self.rotateAngle += rotationAngle
                            self.image = grapics.transform.rotate(self.originalImage, self.rotateAngle)
                            self.x_plane -= 1
                            self.y += 1.2
                            if(self.rotateAngle==90):
                                self.Rotate = 1
                                objectsRotate[self.direction][self.lane].append(self)
                                self.awayIndex_plane = len(objectsRotate[self.direction][self.lane]) - 1
                        else:
                            if(self.awayIndex_plane==0 or ((self.y + self.image.get_rect().height) <(objectsRotate[self.direction][self.lane][self.awayIndex_plane-1].y  -  movGap))):
                                self.y += self.speed
                elif(self.lane == 2):
                    if(self.away==0 or self.x_plane>middle[self.direction]['x_plane']):
                        if((self.x_plane>=self.pause or (callright==2 and cstarter==0) or self.away==1) and (self.index_plane==0 or self.x_plane>(objects[self.direction][self.lane][self.index_plane-1].x_plane + objects[self.direction][self.lane][self.index_plane-1].image.get_rect().width + movGap) or objects[self.direction][self.lane][self.index_plane-1].Rotate==1)):                
                            self.x_plane -= self.speed
                    else:
                        if(self.Rotate==0):
                            self.rotateAngle += rotationAngle
                            self.image = grapics.transform.rotate(self.originalImage, -self.rotateAngle)
                            self.x_plane -= 1.8
                            self.y -= 2.5
                            if(self.rotateAngle==90):
                                self.Rotate = 1
                                objectsRotate[self.direction][self.lane].append(self)
                                self.awayIndex_plane = len(objectsRotate[self.direction][self.lane]) - 1
                        else:
                            if(self.awayIndex_plane==0 or (self.y>(objectsRotate[self.direction][self.lane][self.awayIndex_plane-1].y + objectsRotate[self.direction][self.lane][self.awayIndex_plane-1].image.get_rect().height +  movGap))):
                                self.y -= self.speed
            else: 
                if(self.away == 0):
                    if((self.x_plane>=self.pause or (callright==2 and cstarter==0)) and (self.index_plane==0 or self.x_plane>(objects[self.direction][self.lane][self.index_plane-1].x_plane + objects[self.direction][self.lane][self.index_plane-1].image.get_rect().width + movGap))):                
                        self.x_plane -= self.speed
                else:
                    if((self.awayIndex_plane==0) or (self.x_plane>(objectsNotRotate[self.direction][self.lane][self.awayIndex_plane-1].x_plane + objectsNotRotate[self.direction][self.lane][self.awayIndex_plane-1].image.get_rect().width + movGap))):                
                        self.x_plane -= self.speed
        elif(self.direction=='top'):
            if(self.away==0 and self.y<pauseLines[self.direction]):
                self.away = 1
                objects[self.direction]['away'] += 1
                if(self.willTurn==0):
                    objectsNotRotate[self.direction][self.lane].append(self)
                    self.awayIndex_plane = len(objectsNotRotate[self.direction][self.lane]) - 1
            if(self.willTurn==1):
                if(self.lane == 1):
                    if(self.away==0 or self.y>pauseLines[self.direction]-60):
                        if((self.y>=self.pause or (callright==3 and cstarter==0) or self.away == 1) and (self.index_plane==0 or self.y>(objects[self.direction][self.lane][self.index_plane-1].y + objects[self.direction][self.lane][self.index_plane-1].image.get_rect().height +  movGap) or objects[self.direction][self.lane][self.index_plane-1].Rotate==1)):
                            self.y -= self.speed
                    else:   
                        if(self.Rotate==0):
                            self.rotateAngle += rotationAngle
                            self.image = grapics.transform.rotate(self.originalImage, self.rotateAngle)
                            self.x_plane -= 2
                            self.y -= 1.2
                            if(self.rotateAngle==90):
                                self.Rotate = 1
                                objectsRotate[self.direction][self.lane].append(self)
                                self.awayIndex_plane = len(objectsRotate[self.direction][self.lane]) - 1
                        else:
                            if(self.awayIndex_plane==0 or (self.x_plane>(objectsRotate[self.direction][self.lane][self.awayIndex_plane-1].x_plane + objectsRotate[self.direction][self.lane][self.awayIndex_plane-1].image.get_rect().width + movGap))):
                                self.x_plane -= self.speed
                elif(self.lane == 2):
                    if(self.away==0 or self.y>middle[self.direction]['y']):
                        if((self.y>=self.pause or (callright==3 and cstarter==0) or self.away == 1) and (self.index_plane==0 or self.y>(objects[self.direction][self.lane][self.index_plane-1].y + objects[self.direction][self.lane][self.index_plane-1].image.get_rect().height +  movGap) or objects[self.direction][self.lane][self.index_plane-1].Rotate==1)):
                            self.y -= self.speed
                    else:   
                        if(self.Rotate==0):
                            self.rotateAngle += rotationAngle
                            self.image = grapics.transform.rotate(self.originalImage, -self.rotateAngle)
                            self.x_plane += 1
                            self.y -= 1
                            if(self.rotateAngle==90):
                                self.Rotate = 1
                                objectsRotate[self.direction][self.lane].append(self)
                                self.awayIndex_plane = len(objectsRotate[self.direction][self.lane]) - 1
                        else:
                            if(self.awayIndex_plane==0 or (self.x_plane<(objectsRotate[self.direction][self.lane][self.awayIndex_plane-1].x_plane - objectsRotate[self.direction][self.lane][self.awayIndex_plane-1].image.get_rect().width - movGap))):
                                self.x_plane += self.speed
            else: 
                if(self.away == 0):
                    if((self.y>=self.pause or (callright==3 and cstarter==0)) and (self.index_plane==0 or self.y>(objects[self.direction][self.lane][self.index_plane-1].y + objects[self.direction][self.lane][self.index_plane-1].image.get_rect().height + movGap))):                
                        self.y -= self.speed
                else:
                    if((self.awayIndex_plane==0) or (self.y>(objectsNotRotate[self.direction][self.lane][self.awayIndex_plane-1].y + objectsNotRotate[self.direction][self.lane][self.awayIndex_plane-1].image.get_rect().height + movGap))):                
                        self.y -= self.speed 

def initialize():
    minTime = possibleallrightwaveTimerRange[0]
    max_planeTime = possibleallrightwaveTimerRange[1]
    if(possibleallrightwaveTimer):
        ts1 = Trafficwave(0, Dstarter, possible.randint(minTime,max_planeTime))
        sig.append(ts1)
        ts2 = Trafficwave(ts1.danger+ts1.starter+ts1.allright, Dstarter, possible.randint(minTime,max_planeTime))
        sig.append(ts2)
        ts3 = Trafficwave(Ddanger, Dstarter, possible.randint(minTime,max_planeTime))
        sig.append(ts3)
        ts4 = Trafficwave(Ddanger, Dstarter, possible.randint(minTime,max_planeTime))
        sig.append(ts4)
    else:
        ts1 = Trafficwave(0, Dstarter, Dallright[0])
        sig.append(ts1)
        ts2 = Trafficwave(ts1.starter+ts1.allright, Dstarter, Dallright[1])
        sig.append(ts2)
        ts3 = Trafficwave(Ddanger, Dstarter, Dallright[2])
        sig.append(ts3)
        ts4 = Trafficwave(Ddanger, Dstarter, Dallright[3])
        sig.append(ts4)
    repeat()

def repeat():
    global callright, cstarter, usedallright
    while(sig[callright].allright>0):
        topdateValueues()
        time.sleep(1)
    cstarter = 1

    for i in range(0,3):
        for obj in objects[trun_num[callright]][i]:
            obj.pause = Dpause[trun_num[callright]]
    while(sig[callright].starter>0): 
        topdateValueues()
        time.sleep(1)
    cstarter = 0 
    if(possibleallrightwaveTimer):
        sig[callright].allright = possible.randint(possibleallrightwaveTimerRange[0],possibleallrightwaveTimerRange[1])
    else:
        sig[callright].allright = Dallright[callright]
    sig[callright].starter = Dstarter
    sig[callright].danger = Ddanger
       
    callright = usedallright 
    usedallright = (callright+1)%noOfsig    
    sig[usedallright].danger = sig[callright].starter+sig[callright].allright
    repeat()

def topdateValueues():
    for i in range(0, noOfsig):
        if(i==callright):
            if(cstarter==0):
                sig[i].allright-=1
            else:
                sig[i].starter-=1
        else:
            sig[i].danger-=1

def generateobjects():
    while(True):
        obj_type = possible.choice(workingobjTypesList)
        lane_number = possible.randint(1,2)
        will_turn = 0
        if(lane_number == 1):
            temp = possible.randint(0,99)
            if(temp<40):
                will_turn = 1
        elif(lane_number == 2):
            temp = possible.randint(0,99)
            if(temp<40):
                will_turn = 1
        temp = possible.randint(0,99)
        direction_number = 0
        dist = [25,50,75,100]
        if(temp<dist[0]):
            direction_number = 0
        elif(temp<dist[1]):
            direction_number = 1
        elif(temp<dist[2]):
            direction_number = 2
        elif(temp<dist[3]):
            direction_number = 3
        obj(lane_number, objTypes[obj_type], direction_number, trun_num[direction_number], will_turn)
        time.sleep(1)

class Main:
    global workingobjTypesList
    i = 0
    for objType in workingobjTypes:
        if(workingobjTypes[objType]):
            workingobjTypesList.append(i)
        i += 1
    thread1 = threading.Thread(name="initialization",target=initialize, args=())    # initialization
    thread1.daemon = True
    thread1.start()

    black = (0, 0, 0)
    white = (255, 255, 255)

    screenWidth = 1400
    screenHeight = 800
    screenSize = (screenWidth, screenHeight)

    background = grapics.image.load('images/intersection.png')

    screen = grapics.display.set_mode(screenSize)
    grapics.display.set_caption("SIMULATION")

    dangerwave = grapics.image.load('images/sig/danger.png')
    starterwave = grapics.image.load('images/sig/starter.png')
    allrightwave = grapics.image.load('images/sig/allright.png')
    font = grapics.font.Font(None, 30)
    thread2 = threading.Thread(name="generateobjects",target=generateobjects, args=()) 
    thread2.daemon = True
    thread2.start()

    while True:
        for event in grapics.event.get():
            if event.type == grapics.QUIT:
                sys.exit()

        screen.blit(background,(0,0))
        for i in range(0,noOfsig):  
            if(i==callright):
                if(cstarter==1):
                    sig[i].waveTex_planet = sig[i].starter
                    screen.blit(starterwave, waveValue[i])
                else:
                    sig[i].waveTex_planet = sig[i].allright
                    screen.blit(allrightwave, waveValue[i])
            else:
                if(sig[i].danger<=10):
                    sig[i].waveTex_planet = sig[i].danger
                else:
                    sig[i].waveTex_planet = "---"
                screen.blit(dangerwave, waveValue[i])
        waveTex_planets = ["","","",""]

        for i in range(0,noOfsig):  
            waveTex_planets[i] = font.render(str(sig[i].waveTex_planet), True, white, black)
            screen.blit(waveTex_planets[i],waveTimerValue[i])

        for obj in simulation:  
            screen.blit(obj.image, [obj.x_plane, obj.y])
            obj.move()
        grapics.display.update()


Main()