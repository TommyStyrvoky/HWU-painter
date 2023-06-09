import *controllerFn.py
import *configParams.py
import colorsys
import math

def findIndex2D(item,array):
    for row,i in enumerate(array):
        for col,j in enumerate(i):
            if j == item:
                return col,row
    return 0,0

def lerp(start,end,alpha):
    if type(start) == list and type(end) == list:
        if len(start)==len(end):
            lerpedVal = []
            for i,value in enumerate(start):
                newVal = start[i] + (end[i]-start[i])*alpha
                lerpedVal.append(newVal)
            return lerpedVal
        else:
            return start
    else:
        return start + (end-start)*alpha
def convertColor(colorValue):#convert RGB to required controller input steps
    hsv = list(colorsys.rgb_to_hsv(colorValue[0]/255,colorValue[1]/255,colorValue[2]/255))
    steps =[36,20,20]
    colorSnapped =[]
    for i,value in enumerate(hsv):
        if value ==0:
            colorSnapped.append(0)
        else:
            colorSnapped.append(int(steps[i]/(1/value)))
    return colorSnapped

def setColor(color):
    global debounceTime,minPressTime,gamepad
    pressKey(y_button ,minPressTime)
    time.sleep(debounceTime)
    resetColor()
    colorInputs = convertColor(color)
    for count,value in enumerate(colorInputs):
        for i in range(0,value):
            pressKey(dpad_right,minPressTime)
            time.sleep(debounceTime)
        if count+1 != len(colorInputs):
            pressKey(dpad_down,minPressTime)
            time.sleep(debounceTime)
    pressKey(a_button ,minPressTime)
    time.sleep(debounceTime)
    return colorInputs

def resetColor():
    global debounceTime,minPressTime
    steps =[0,0,20]
    for value in steps:
        for i in range(0,value):
            pressKey(dpad_left,minPressTime)
            time.sleep(debounceTime)
        pressKey(dpad_down,minPressTime)
        time.sleep(debounceTime)
    for i in range(0,3):#reset
        pressKey(dpad_up,minPressTime)
        time.sleep(debounceTime)

def selectShape(page,row,col):
    global debounceTime,minPressTime
    for p in range(0,page): 
        pressKey(rb_button,minPressTime*2)
        time.sleep(debounceTime)
    for c in range(0,col):
        pressKey(dpad_right,minPressTime)
        time.sleep(debounceTime)
    for r in range(0,row): 
        pressKey(dpad_down,minPressTime)
        time.sleep(debounceTime)
    pressKey(a_button,minPressTime)
    time.sleep(debounceTime)
    
def setPosition(x,y):
    global debounceTime,minPressTime,moveStep
    moveLimit =250
    xTime = abs(min(x,moveLimit)/moveStep)
    yTime = abs(min(y,moveLimit)/moveStep)
    
    minTime = min(xTime,yTime)
    maxTime = max(xTime,yTime)-minTime
    
    xDir = int(math.copysign(1, x)*32767)
    yDir = int(math.copysign(1, y)*32767)
    if x ==0:
        xDir = 0
    if y == 0:
        yDir = 0
        
    if xTime == minTime:
        lThumbStick(xDir,yDir)
        time.sleep(xTime)
        lThumbStick(0,0)
        lThumbStick(0,yDir)
        time.sleep(maxTime)
        lThumbStick(0,0)
    else:
        lThumbStick(xDir,yDir)
        time.sleep(yTime)
        lThumbStick(0,0)
        lThumbStick(xDir,0)
        time.sleep(maxTime)
        lThumbStick(0,0)
    
def setRotation(angle):
    global debounceTime,minPressTime,rotStep
    normalizedAngle = angle%360
    if normalizedAngle>360:
        rotTime = (abs(normalizedAngle-360))/rotStep #bug here
        lTrigger(128)
        time.sleep(rotTime)
        lTrigger(0)
    else:
        rotTime = abs(normalizedAngle)/rotStep
        rTrigger(128)
        time.sleep(rotTime)
        rTrigger(0)

def setTransparency(transparency):
    global debounceTime,minPressTime,transparencyStep
    if transparency != 0:
        transpTime = min(transparency,100)/transparencyStep
        gamepad.press_button(lb_button)
        gamepad.update()
        lTrigger(128)
        time.sleep(transpTime)
        lTrigger(0)
        gamepad.release_button(lb_button)
        gamepad.update()

def rotateAboutPosition(origin,offset,rotation):
    x = origin[0]+math.cos(math.radians(rotation))*offset[0]+math.sin(math.radians(rotation))*offset[1]
    y = origin[1]+math.sin(math.radians(rotation))*offset[0]+math.cos(math.radians(rotation))*offset[1]
    return [x,y]

def setScale(scaleX,scaleY):
    global debounceTime,minPressTime,scaleStep
    baseScale = 83 #default size
    rThumbStick(32767,0)
    time.sleep((100-baseScale)/scaleStep)
    rThumbStick(0,0)
    scaleLimit = 1000
    xTime = abs(min(scaleX,scaleLimit)-100)/scaleStep
    yTime = abs(min(scaleY,scaleLimit)-100)/scaleStep
    
    minTime = min(xTime,yTime)
    maxTime = max(xTime,yTime)-minTime
    
    xDir = int(math.copysign(1, scaleX-100)*32767)
    yDir = int(math.copysign(1, scaleY-100)*32767)
    
    if scaleX ==0:
        xDir = 0
    if scaleY == 0:
        yDir = 0
    
    if scaleX!=scaleY:
        gamepad.press_button(lb_button)
        gamepad.update()
        if xTime == minTime:
            rThumbStick(xDir,yDir)
            time.sleep(xTime)
            rThumbStick(0,0)
            rThumbStick(0,yDir)
            time.sleep(maxTime)
            rThumbStick(0,0)
        else:
            rThumbStick(xDir,yDir)
            time.sleep(yTime)
            rThumbStick(0,0)
            rThumbStick(xDir,0)
            time.sleep(maxTime)
            rThumbStick(0,0)
        gamepad.release_button(lb_button)
        gamepad.update()
    else:
        rThumbStick(xDir,0)
        time.sleep(xTime)
        rThumbStick(0,0)


def setView(view):
    global debounceTime,minPressTime,mapViews
    count = mapViews[view]
    for i in range(0,count):
        pressKey(rb_button,debounceTime)
        time.sleep(debounceTime)
    pressKey(a_button,minPressTime)
    time.sleep(debounceTime)
        
    
def createLayer():
    for i in range(0,3):#reset
        pressKey(dpad_down,minPressTime)
        time.sleep(debounceTime)
    pressKey(a_button,minPressTime)
    time.sleep(debounceTime)
