import pygame
import const as CON
from Event.base_event import *

# get a picture by [0-9]
number_to_image = {
    0 : CON.IMG_NUM0, 1 : CON.IMG_NUM1, 2 : CON.IMG_NUM2, 3 : CON.IMG_NUM3, 4 : CON.IMG_NUM4,
    5 : CON.IMG_NUM5, 6 : CON.IMG_NUM6, 7 : CON.IMG_NUM7, 8 : CON.IMG_NUM8, 9 : CON.IMG_NUM9,
}

class ScorePainter:
    class MySprite( pygame.sprite.Sprite ):
        def __init__(self, image, pos):
            pygame.sprite.Sprite.__init__( self )
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.topleft = pos

    def __init__(self, background, screen, players, env):
        self.background = background
        self.screen = screen
        self.players = players
        self.env = env
        self.score_group = pygame.sprite.Group()
        self.text_group = pygame.sprite.Group()
        self.time_group = pygame.sprite.Group()
        self.tick = 0
        self.score_pre = [0, 0, 0, 0]
        self.score_diff = [0, 0, 0, 0]
        self.score_time = [0, 0, 0, 0]
    def update(self):
        self.score_group.empty()
        self.text_group.empty()
        self.time_group.empty()
        font = pygame.font.SysFont("segoeui", 30)
        font_num = pygame.font.SysFont("comicsansms", 50)
        black = (0, 0, 0)
        red = (220, 0, 0)
        blue = (0, 0, 220)
        pos = [(280,  CON.ROOM_Y * CON.UNIT + 40), (280,  CON.ROOM_Y * CON.UNIT + 120), (740,  CON.ROOM_Y * CON.UNIT + 40), (740,  CON.ROOM_Y * CON.UNIT + 120)]
        name = ["Tuzki", "Superman", "Cactus", "Pusheen",]
        for i in range(4):
            if self.players[i].ai:
                name[i] = self.players[i].ai.helper.name
        ant_pos = [(0 ,70), (-5, 90), (0, 140), (10, 165), (10, 205), (0, 220), (-10, 235), (0, 280), (5, 300), (0, 330), (-5, 340), (0, 360), (5, 400), (10, 425), (5, 470), (5, 520), (-5, 560), (-10, 590), (0, 600)]
        for player in self.players:
            (x, y) = pos[player.index]
            if player.limit_time > 0:
                self.score_group.add( ScorePainter.MySprite(CON.IMG_DEATH[player.limit_time // 1000], (x - 250, y - CON.UNIT // 2)) )
            elif player.is_dizzy and player.dir == (0, 0):
                self.score_group.add( ScorePainter.MySprite(CON.IMG_DIZZY, (x - 250, y - CON.UNIT // 2)) )
            elif player.is_dizzy and player.dir != (0, 0):
                self.score_group.add( ScorePainter.MySprite(CON.IMG_CONFUSE, (x - 250, y - CON.UNIT // 2)) )
            elif player.score_rate == 2:
                self.score_group.add( ScorePainter.MySprite(CON.IMG_BONUS, (x - 250, y - CON.UNIT // 2)) )
            self.text_group.add( ScorePainter.MySprite(font.render(name[player.index], True, black), (x - 170, y)) )
            self.score_group.add( ScorePainter.MySprite(number_to_image[ player.score // 100 ], (x, y)) )
            self.score_group.add( ScorePainter.MySprite(number_to_image[ player.score % 100 // 10 ], (x + CON.FONT_SIZE // 2, y)) )
            self.score_group.add( ScorePainter.MySprite(number_to_image[ player.score % 10 ], (x + CON.FONT_SIZE, y)) )
            self.time_group.add( ScorePainter.MySprite(CON.IMG_PATH[ self.env["timer"] // (CON.TOTAL_TIME // 18) ], (CON.ROOM_X * CON.UNIT, CON.UNIT * 2)) )
            (x_ant, y_ant) = ant_pos[ self.env["timer"] // (CON.TOTAL_TIME // 18) ]
            self.time_group.add( ScorePainter.MySprite(CON.IMG_ANT[ int(self.tick) % 4 ], (CON.ROOM_X * CON.UNIT + x_ant, y_ant)) )
            if player.score != self.score_pre[ player.index ]:
                self.score_time[player.index] = 40
                self.score_diff[player.index] = player.score - self.score_pre[ player.index ]
                self.score_pre[player.index] = player.score
            if self.score_time[player.index] > 0:
                if self.score_diff[player.index] > 0:
                   self.text_group.add( ScorePainter.MySprite(font_num.render("+" + str(self.score_diff[player.index]), True, red), (x + int(1.5 * CON.FONT_SIZE), y - (40 - self.score_time[player.index]))) ) 
                else:
                    self.text_group.add( ScorePainter.MySprite(font_num.render("-" + str(-self.score_diff[player.index]), True, blue), (x + int(1.5 * CON.FONT_SIZE), y - (40 - self.score_time[player.index]))) ) 
                self.score_time[player.index] -= 1
        self.tick += 0.1
    def clear(self):
        self.score_group.clear(self.screen, self.background)
        self.text_group.clear(self.screen, self.background)
        self.time_group.clear(self.screen, self.background)
    def draw(self):
        self.text_group.draw(self.screen)
        self.score_group.draw(self.screen)        
        self.time_group.draw(self.screen)