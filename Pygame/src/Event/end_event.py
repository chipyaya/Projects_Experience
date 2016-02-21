import random
import pygame
import sys

from Event.base_event import BaseEvent
import Event.game_event
import const as CON

class EventGameOver(BaseEvent):
    class SplashResource:
        def __init__(self):
            # init colors
            self.color_black = pygame.Color(0, 0, 0)
            self.color_white = pygame.Color(255, 255, 255)
            # init images
            self.img_splash = CON.IMG_GAMEOVER
            self.IMG =  [
                    pygame.transform.scale( pygame.image.load( "./Image/tuzki.png" ), (int(CON.UNIT * 4), int(CON.UNIT * 4)) ),
                    pygame.transform.scale( pygame.image.load( "./Image/superman.png" ), (int(CON.UNIT * 4), int(CON.UNIT * 4)) ),
                    pygame.transform.scale( pygame.image.load( "./Image/cactus.png" ), (int(CON.UNIT * 3.5), int(CON.UNIT * 3.5)) ),
                    pygame.transform.scale( pygame.image.load( "./Image/pusheen.png" ), (int(CON.UNIT * 4.5), int(CON.UNIT * 4.5)) ),
            ]
            self.pos = [(380, 300), (575, 350), (190, 370), (725, 460)]
            self.beep = pygame.mixer.Sound("./Sound/game_over.wav")
            self.ed = pygame.mixer.Sound("./Sound/ed.wav")
    def __init__(self, env, priority):
        self.env = env
        self.priority = priority
        self.screen = self.env["screen"]
        self.res = EventGameOver.SplashResource()
        self.players = sorted(self.env["player"], key = lambda player : player.score)[::-1]
        self.beep = pygame.mixer.Sound("./Sound/game_over.wav")
        
    def do_action(self):
        screen = self.screen
        res = self.res
        font = pygame.font.SysFont("segoeui", 60)
        scr_width = 1150
        scr_height = 750
        tick_cnt = 0 # tick counter
        run_splash = True # tell if continue splash loop
        mask = pygame.Surface((scr_width, scr_height)) # mask surface
        mask.fill(res.color_black)
        self.env["uic"].pause()
        self.env["gamec"].pause()
        self.env["bgm"].stop()
        self.players = sorted(self.env["player"], key = lambda player : player.score)[::-1]
        cnt = 0
        for p in self.players:
            print( " rank " , cnt , " : " , p.ai.helper.name )
            cnt += 1
        res.beep.play()
        pygame.time.wait(2000)
        res.beep.stop()
        res.ed.play()
        # game loop for splash screen
        while run_splash:
            # handle events
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT: # quit event
                    pygame.quit()
                    self.env["uic"].stop()
                    self.env["gamec"].stop()
                    sys.exit()
                elif event.type == pygame.locals.KEYDOWN: # key events
                    if event.key == pygame.locals.K_ESCAPE:
                         pygame.quit()
                         sys.exit()
            # update screen
            if tick_cnt <= 20:
                screen.fill(res.color_black)

            elif tick_cnt < 30:
                screen.fill(res.color_white)
                screen.blit(res.img_splash, (0, 0))
                mask.set_alpha( -tick_cnt * 255 / 10 + 767)
                screen.blit(mask, (0, 0))

            elif tick_cnt == 90:
                screen.fill(res.color_white)
                screen.blit(res.img_splash, (0, 0))
                (x, y) = res.pos[3]
                screen.blit(res.IMG[ self.players[3].index ], res.pos[3])
                screen.blit( font.render(str(self.players[3].score), True, res.color_black), (x + 70, y - 80))
                
            elif tick_cnt == 150:
                (x, y) = res.pos[2]
                screen.blit(res.IMG[ self.players[2].index ], res.pos[2])
                screen.blit( font.render(str(self.players[2].score), True, res.color_black), (x + 70, y - 80))

            elif tick_cnt == 210:
                (x, y) = res.pos[1]
                screen.blit(res.IMG[ self.players[1].index ], res.pos[1])
                screen.blit( font.render(str(self.players[1].score), True, res.color_black), (x + 70, y - 80))

            elif tick_cnt == 270:
                (x, y) = res.pos[0]
                screen.blit(res.IMG[ self.players[0].index ], res.pos[0])
                screen.blit( font.render(str(self.players[0].score), True, res.color_black), (x + 70, y - 80))
            '''
            elif 620 < tick_cnt <= 650:
                screen.fill(res.color_white)
                screen.blit(res.img_splash, (0, 0))
                mask.set_alpha( tick_cnt * 255 / 20 - 1275)
                screen.blit(mask, (0, 0))
            
            elif tick_cnt > 650:
                break
            '''
            if tick_cnt <= 650:
                tick_cnt += 1
            pygame.display.update()
            pygame.time.wait(30)
        res.ed.stop()
        self.env["pyQUIT"] = True
        self.env["gamec"].stop()
        self.env["uic"].stop()
