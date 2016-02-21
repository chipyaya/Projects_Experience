import pygame
import images
import math
import const as CON
import itertools
from const import *
from Event.base_event import *
from collections import OrderedDict
from Event.scoreboard_event import *

class EventDrawInit( BaseEvent ):
    def __init__( self , env , priority ):
        self.env = env
        self.priority = priority

    def do_action( self ):
        self.env["screen"].blit( CON.IMG_BG, (0, 0) )
        self.env[ "food_painter" ] = FoodPainter( self.env )
        self.env[ "player_painter" ] = PlayerPainter( IMG_BG , self.env[ "screen" ] , self.env[ "player" ] , self.env['crash'] )
        self.env[ "score_painter" ] = ScorePainter( IMG_BG , self.env[ "screen" ] , self.env[ "player" ] , self.env )
        self.env[ "uic" ].add_event( EventDrawItem( self.env , self.priority + TICKS_PER_TURN ) )

class EventDrawItem( BaseEvent ):
    def __init__( self , env , priority ):
        self.env = env
        self.priority = priority

    def do_action( self ):
        self.env[ "player_painter" ].update()
        self.env[ "food_painter" ].update()
        self.env[ "score_painter" ].update()

        self.env[ "player_painter" ].clear()
        self.env[ "food_painter" ].clear()
        self.env[ "score_painter" ].clear()

        self.env[ "player_painter" ].draw()
        self.env[ "food_painter" ].draw()
        self.env[ "score_painter" ].draw()

        pygame.display.update()
        self.env[ "uic" ].add_event( EventDrawItem( self.env , self.priority + CON.TICKS_PER_TURN ) )

        
class EventCloseWindow(BaseEvent):
    def __init__(self, env, pp):
        BaseEvent.__init__(self)
        self.env = env
        self.priority = pp
    def do_action(self):
        #pygame.event.pump()
        if self.env["pyQUIT"] or self.env["pyESC"]:
            self.env[ "gamec" ].add_event(
              Event.game_event.EventEndGame( self.env , self.priority + EVENT_CON.TICKS_PER_TURN )
            )
        self.env["uic"].add_event(
          Event.ui_event.EventCloseWindow(self.env, self.priority + EVENT_CON.TICKS_PER_TURN)
        )


class FoodPainter:
    def __init__(self,env):
        self.tick = 0
        self.tick_per_pic = 10
        self.env = env
        self.fgroup = pygame.sprite.OrderedUpdates()
        self.fdict = OrderedDict()
        # record tick for each food
        self.glob_tick = 0
    def Foods(self, pos, img):
        fsprite = pygame.sprite.Sprite()
        fsprite.image = img
        fsprite.rect = fsprite.image.get_rect()
        # images of the foods are 1.5x, so it's necessary to set the topleft to a proper position
        (x, y) = pos
        fsprite.rect.topleft = (x*CON.UNIT - int(CON.UNIT * 0.5), y*CON.UNIT - int(CON.UNIT * 0.5))
        return fsprite
    def reassign_tick(self):
        return -1
    def update(self):
        self.fgroup.empty()
        for k in self.env["food"]:
            if k not in self.fdict:
                self.fdict[k] = self.reassign_tick()
        tmp = OrderedDict()
        for k in self.fdict:
            if k in self.env["food"]:
                tmp[k] = self.fdict[k]
        self.fdict = tmp
        self.glob_tick -= 1
        if self.glob_tick <= self.tick_per_pic*-4:
            self.glob_tick = self.reassign_tick()
        for k in self.fdict :
            #update tick per turn
            if self.glob_tick < 0:
                self.fgroup.add(self.Foods(k, CON.IMG_FOOD[self.glob_tick//self.tick_per_pic*-1-1]))
            else:
                self.fgroup.add(self.Foods(k, CON.IMG_FOOD[0]))
        #for k in self.fdict :
        #    #update tick per turn
        #    self.fdict[k] -= 1
        #    if self.fdict[k] <= self.tick_per_pic*-4:
        #        self.fdict[k] = self.reassign_tick()
        #    if self.fdict[k] < 0:
        #        self.fgroup.add(self.Foods(k, CON.IMG_FOOD[self.fdict[k]//self.tick_per_pic*-1-1]))
        #    else:
        #        self.fgroup.add(self.Foods(k, CON.IMG_FOOD[0]))
    def clear(self):
        self.fgroup.clear(self.env["screen"], CON.IMG_BG)

    def draw(self):
        self.fgroup.draw(self.env["screen"])

class PlayerPainter:
    class MySprite( pygame.sprite.Sprite ):
        def __init__(self, image, pos_screen):
            pygame.sprite.Sprite.__init__( self )
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.topleft = pos_screen
    class Boom(pygame.sprite.Sprite):
        def __init__(self, pos):
            pygame.sprite.Sprite.__init__(self)
            self.frame = 0
            self.pos = pos
            self.image = images.FIGHTS[0]
            self.rect = self.image.get_rect()
            self.rect.topleft = (UNIT*pos[0] - UNIT*1.2, UNIT*pos[1] - UNIT*1.2)
            
        def update(self):
            self.frame = (self.frame + 1) % 4
            self.image = images.FIGHTS[self.frame]

    def __init__(self, background, screen, players, crash):
        self.background = background
        self.screen = screen
        self.players = players
        self.crash = crash
        self.player_group = pygame.sprite.OrderedUpdates()
        self.poses = [ list(x.pos) for x in self.players]
        self.text_group = pygame.sprite.OrderedUpdates()
        self.fight_group = pygame.sprite.OrderedUpdates()
        self.frame = [0 for _ in self.players]
        self.frame_skill = [0 for _ in self.players]
        self.dead_pre = [False for _ in self.players]
        #self.font = pygame.font.SysFont(pygame.font.get_default_font(), 24, bold=False, italic=False)
        self.font = pygame.font.Font("Prototype.ttf", 24, bold=False, italic=False)

    def update(self):
        crash = self.crash
        self.player_group.empty()
        self.text_group.empty()
        
        covered = set()
        
        for pos, people in crash:
            if len(people)>=2:
                covered.add(pos)
        
        for sprite in self.fight_group.sprites():
            if sprite.pos in covered:
                sprite.update()
                covered.remove(sprite.pos)
            else:
                sprite.kill()
                
        for pos in covered:
            self.fight_group.add(self.Boom(pos))
        
        for ind, player in enumerate(self.players):
            dir = player.dir
            ( x , y ) = self.poses[ind]

            self.player_group.add(PlayerPainter.MySprite(
                images.IMG_PLAYER[images.names[player.index]][player.dir][int(self.frame[ind])%4],
                ( UNIT*x - UNIT*images.CENTER_PLAYERS[images.names[player.index]][0] ,
                  UNIT*y - UNIT*images.CENTER_PLAYERS[images.names[player.index]][1] )
            ))

            if player.is_dizzy:
                self.player_group.add(PlayerPainter.MySprite(
                IMG_CONFUSING[ int(self.frame_skill[ind] % 4) ],
                ( UNIT*x - UNIT*images.CENTER_PLAYERS[images.names[player.index]][0] ,
                  UNIT*y - UNIT*images.CENTER_PLAYERS[images.names[player.index]][1] - UNIT // 2)
                ))

            self.text_group.add(PlayerPainter.MySprite(
                self.font.render(str(player.score), True, pygame.Color("black")),
                ( UNIT*x - UNIT*0.5 + UNIT * 1 - 5, UNIT*y - UNIT*0.5 - 10)
            ))
            
            x, y = tuple(self.poses[ind])
            if player.dead and not self.dead_pre[ind]:
                self.poses[ind] = list(player.pos)
            else:
                if (player.pos[0] - self.poses[ind][0])**2 + (player.pos[1] - self.poses[ind][1])**2 <= 0.03:
                    self.poses[ind] = list(player.pos)
                else:
                    self.poses[ind][0] += (player.pos[0] - self.poses[ind][0]) * 0.1 * ((player.pos[0] - self.poses[ind][0])**2 + (player.pos[1] - self.poses[ind][1])**2)**-0.5
                    self.poses[ind][1] += (player.pos[1] - self.poses[ind][1]) * 0.1 * ((player.pos[0] - self.poses[ind][0])**2 + (player.pos[1] - self.poses[ind][1])**2)**-0.5

            self.dead_pre[ind] = player.dead
            if x != self.poses[ind][0] or y != self.poses[ind][1]:
                self.frame[ind] += 0.25
            self.frame_skill[ind] += 0.25

    def clear(self):
        self.player_group.clear(self.screen, self.background)
        self.text_group.clear(self.screen, self.background)
        self.fight_group.clear(self.screen, self.background)

    def draw(self):
        self.player_group.draw(self.screen)
        self.text_group.draw(self.screen)
        self.fight_group.draw(self.screen)
