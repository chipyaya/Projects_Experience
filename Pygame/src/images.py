import pygame
from const import *

IMG_PLAYER = {}
FIGHTS = []
names = ['tuzki', 'superman', 'cactus', 'pusheen']
dirs = [((0, 1), 'd'), ((0, -1), 'u'), ((1, 0), 'r'), ((-1, 0), 'l')]

for name in names:
    arrows = {}
    for dir in dirs:
        img = []
        for frame in range(1,5):
            img.append(pygame.transform.scale(
                pygame.image.load( './Image/%s_%c_%d.png'%(name, dir[1], frame) ), (int(UNIT * 2), int(UNIT * 2)) 
            ))
        arrows[dir[0]] = img
    arrows[ ( 0 , 0 ) ] = [
      pygame.transform.scale( pygame.image.load( "./Image/%s.png"%(name) ), (int(UNIT * 2), int(UNIT * 2)) )
      for i in range( 4 )
    ] 
    IMG_PLAYER[name] = arrows
    
for i in range(1, 5):
    FIGHTS.append(pygame.transform.scale( pygame.image.load( './Image/fight_%d.png'%(i,) ), (int(UNIT * 3), int(UNIT * 3)) ))

CENTER_PLAYERS = {
    'tuzki': (0.5, 0.7),
    'superman': (0.5, 0.7),
    'cactus': (0.5, 0.9),
    'pusheen': (0.5, 0.5),
}
