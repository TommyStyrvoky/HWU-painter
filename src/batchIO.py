from HWUpainter  import *
import os
import sys
import configparser

config = configparser.ConfigParser()
config.sections()

def main():
    if len(sys.argv[1]) <2:
        print('No parameters file passed!')
        return
    config.read(sys.argv[1])
    p = config['parameters']
    fn = config['function']['type']
    if fn == 'renderJson':
       f = p['file']
       renderJson(
           f,
           [float(p['positionX']),
            float(p['positionY'])],
            float(p['scaleFactor']),
            p['view'],
            float(p['rotation'])
            )
    elif fn == 'renderText':
        renderText(
            p['text'],
            p['view'],
            [float(p['positionX']),float(p['positionY'])],
            float(p['rotation']),
            [float(p['sizeX']),float(p['sizeY'])],
            int(p['font']),
            [int(p['colorR']),int(p['colorG']),int(p['colorB'])]
            )
    elif fn == 'renderGrid':
        color1 = [int(p['color1R']),int(p['color1G']),int(p['color1B'])]
        color2 = [int(p['color2R']),int(p['color2G']),int(p['color2B'])]
        renderGrid(
             [int(p['shapePage']),int(p['shapeRow']),int(p['shapeCol'])],
             p['view'],
             [float(p['positionX']),float(p['positionY'])],
             float(p['rotation']),
             [float(p['sizeX']),float(p['sizeY'])],
             [int(p['countX']),int(p['countY'])],
             [float(p['spacingX']),float(p['spacingY'])],
             [color1,color2],
             bool(p['cLerpAt45']),
             [float(p['transparency1']),float(p['transparency2'])],
             bool(p['tLerpAt45']),
             bool(p['tLerpAt45']),
             bool(p['rowSum']),
             float(p['shapeAngle'])
             )
    elif fn == 'renderPattern':
        color1 = [int(p['color1R']),int(p['color1G']),int(p['color1B'])]
        color2 = [int(p['color2R']),int(p['color2G']),int(p['color2B'])]
        renderPattern(
             [int(p['shapePage']),int(p['shapeRow']),int(p['shapeCol'])],
             p['view'],
             [float(p['positionX']),float(p['positionY'])],
             float(p['rotation']),
             [float(p['sizeX']),float(p['sizeY'])],
             int(p['count']),
             float(p['spacing']),
             [color1,color2],
             [float(p['transparency1']),float(p['transparency2'])],
             float(p['shapeAngle'])
             )
    elif fn == 'deleteLayerRange':
        deleteLayerRange(int(p['start']),int(p['end']))
main()