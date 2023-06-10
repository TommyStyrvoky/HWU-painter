#shape primitive mapping (page,row,col)
square =[2,0,0]
circle=[2,1,0]
hexagon = [2,1,2]

#operation speeds in units/s
rotStep = 57.7605
moveStep = 17.5
scaleStep = 25
transparencyStep = 11.75

#convert movement to scale
scaleToUnits = 68/20*2

mapViews ={'right side':0,'left side':1,'front':2,'rear':3,'above':4}

#remaps forza painter shape type values
mapShapes ={1:square,16:circle}