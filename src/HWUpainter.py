from operationsFn import *
import json

def generateLayer(parameters):
    updateGamepad()
    global gamepad
    global minPressTime
    
    createLayer()
    setView(parameters['view'])
    selectShape(*parameters['shape'])
    setColor(parameters['color'])
    setPosition(parameters['position'][0],parameters['position'][1])
    setRotation(parameters['rotation'])
    setScale(parameters['size'][0],parameters['size'][1])
    setTransparency(parameters['transparency'])
    pressKey(a_button,minPressTime)
    time.sleep(debounceTime)
    pressKey(b_button,minPressTime)
    time.sleep(debounceTime)
    
def deleteLayerRange(startLayer,endLayer):
    global minPressTime,debounceTime
    for i in range(0,startLayer+4):#get to layer:
        pressKey(dpad_down,minPressTime)
        time.sleep(debounceTime) 
    for layer in range(0,endLayer-startLayer):
        rTrigger(255)
        time.sleep(minPressTime)
        rTrigger(0)
        time.sleep(debounceTime)   
        pressKey(dpad_right,minPressTime)
        time.sleep(debounceTime)   
        pressKey(a_button,minPressTime)
        time.sleep(debounceTime)   
        pressKey(dpad_down,minPressTime) #go down one layer
        time.sleep(debounceTime)
    for i in range(0,startLayer+4):#return to start
        pressKey(dpad_up,minPressTime)
        time.sleep(debounceTime)
        
def renderJson(file,startPos,scaleFact,view,rotation):
    f = open(file)
    data = json.load(f)
    f.close()
    layerSize=[0,0]
    print('Total layers:'+str(len(data['shapes'])))
    for i,layer in enumerate(data['shapes']):
        print('Layer: '+str(i+1))
        if i>0:
            shape = circle
            if type(layer['type'])==list: #load custom shape
                 shape = layer['type']
            elif type(shape)==int:
                shape = mapShapes[shape]
            xPos = ((layer['data'][0])*scaleFact-layerSize[0]/2*scaleFact)#+startPos[0]
            yPos = ((-layer['data'][1])*scaleFact+layerSize[1]/2*scaleFact)#+startPos[1]
            position = [xPos,yPos]
            position = rotateAboutPosition(startPos,position,rotation)
            angle =layer['data'][4]#+90
            size = [layer['data'][2]*scaleToUnits*scaleFact,layer['data'][3]*scaleToUnits*scaleFact]
            color = [layer['color'][0],layer['color'][1],layer['color'][2]]
            
            newLayer =dict(view=view,shape=shape,color=color,position =position,rotation=rotation+angle,size=size,transparency=0)
            generateLayer(newLayer)
        else:
            layerSize = [layer['data'][2],layer['data'][3]]
    print("done!")
    
def renderText(text,view,startPos,rotation,size,font,color):
    #font parameters
    fonts=[14,16,18,20,22,24,26,28,30]
    hasNumerics=[False,True,False,False,False,False,False,False,False]
    hasComma =[True,False,False,True,True,True,True,True,True]
    hasSemiColon =[True,False,True,True,True,True,True,True,True]
    fontPadding=[10,20,8.5,8,12,12,12,14,16]
    fontHeight=[20,20,20,20,20,20,20,20,20]
    thinCharMult = [0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8]
    wideCharMult = [1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25,1.25]
    
    #font tables
    charmap =[
        ['a','b','c','d','e','f','g','h','i'],
        ['j','k','l','m','n','o','p','q','r'],
        ['s','t','u','v','w','x','y','z','1'],
        ['2','3','4','5','6','7','8','9','0'],
        ['?','!','"',r':',';',',','@']]
    
    thinChars =['i','j','k','l','1','!',r':',';',',']
    wideChars =['M','W']
    
    curPos = 0
    currentRow = 0
    for line in text.splitlines():
        for i in range(0, len(line)):
            character = line[i]
            print(character)
            col,row =  findIndex2D(character.lower(),charmap)
            page =fonts[font]
            if character.islower() or character in charmap[4] or character.isnumeric():
                page += 1
            charMult = 1

            if character in thinChars:
                charMult = thinCharMult[font]
            if character in wideChars:
                charMult = wideCharMult[font]

            textHeight = fontHeight[font]*charMult*size[1]/100
            textPadding = fontPadding[font]*charMult*size[0]/100
            
            if (character ==',' and not hasComma[font]) or (character ==';' and not hasSemiColon[font]) or (character.isnumeric() and character.isupper() and not hasNumerics[font]):
                chararacter=' '
            if (hasComma[font] or hasSemiColon[font]) and row ==4 and col ==9:
                if not hasSemiColon[font] and not hasComma[font]:
                    col -= 2
                else:
                    col -= 1

            charIndex =[page,row,col]
            if character == ' ':
                curPos+=textPadding
            else:
                position = rotateAboutPosition(startPos,[curPos,currentRow],rotation)
                print(curPos)
                print(currentRow)
                print(position)
                newLayer = dict(view=view,shape=charIndex,color=color,position = position,rotation=rotation,size=size,transparency=0)
                generateLayer(newLayer)
            curPos+=textPadding
        curPos = 0
        currentRow += textHeight
        
        
def renderGrid(shape,view,startPos,rotation,size,count,spacing,color,colorDiag,transparency,transpDiag,rowShift,rowSum,shapeAngle):
    for y in range(0,count[0]):
        for x in range(0,count[1]):
            offset = 0
            if y%2 !=0:
                offset = rowShift
            if rowSum:
                offset=y*rowShift
            position = rotateAboutPosition(startPos,[(spacing[0]*(x+offset)*(size[0]/100)),-(spacing[1]*(y)*size[1]/100)],rotation)
            
            if transpDiag:
                transparencyLerped = lerp(transparency[0],(x+y)/(count[0]+count[1]-2))
            else:
                transparencyLerped = lerp(transparency[0],transparency[1],x/(count[1]-1))
                
            if colorDiag:
                 colorLerped = lerp(color[0],color[1],(x+y)/(count[0]+count[1]-2))
            else:
                colorLerped = lerp(color[0],color[1],x/(count[1]-1))
            newLayer =dict(view=view,shape=shape,color=colorLerped,position =position,rotation=rotation+shapeAngle,size=size,transparency=transparencyLerped)
            generateLayer(newLayer)
