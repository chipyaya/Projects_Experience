import sys
import pygame

class SplashScreen:
    class SplashResource:
        def __init__(self):
            # init colors
            self.color_white = pygame.Color(255, 255, 255)
            self.color_black = pygame.Color(0, 0, 0)
            # init images
            self.img_splash = [pygame.image.load('Image/splash_screen_1.png'), pygame.image.load('Image/splash_screen_2.png'), pygame.image.load('Image/splash_screen_3.png'),]
            self.img_breath = pygame.image.load('Image/breath.png')
            self.breath_pos = (400,430)
            
    # init function
    def __init__(self, env):
        assert env != None
        # init objects
        self.env = env
        self.screen = self.env["screen"]
        self.res = SplashScreen.SplashResource()
        
    # run splash screen
    def start(self):
        screen = self.screen
        sound = pygame.mixer.Sound('Sound/logo.wav')
        res = self.res
        scr_width = 1150
        scr_height = 750
        tick_cnt = 0 # tick counter
        run_splash = True # tell if continue splash loop
        mask = pygame.Surface((scr_width, scr_height)) # mask surface
        mask.fill(res.color_black)
        # game loop for splash screen
        while run_splash:
            # handle events
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT: # quit event
                    pygame.quit()
                    sys.exit()
              
                elif event.type == pygame.locals.KEYDOWN: # key events
                    # quit game if key ESC is pressed
                     if event.key == pygame.locals.K_ESCAPE:
                         pygame.quit()
                         sys.exit()
                     # skip splash screen
                     else:
                         run_splash = False
            # update screen
            if tick_cnt <= 20:
                if tick_cnt == 20:
                    sound.play()
                screen.fill(res.color_black)

            elif tick_cnt <= 30:
                screen.fill(res.color_white)
                screen.blit(res.img_splash[0], (0, 0))
                mask.set_alpha( -tick_cnt * 255 / 10 + 767)
                screen.blit(mask, (0, 0))

            elif tick_cnt <= 90:
                screen.fill(res.color_white)
                screen.blit(res.img_splash[1], (0, 0))
                (x, y) = res.breath_pos
                screen.blit(res.img_breath, (x - tick_cnt * 2 // 3, y + tick_cnt // 2))
                
            elif tick_cnt <= 120:
                screen.fill(res.color_white)
                screen.blit(res.img_splash[2], (0, 0))
                mask.set_alpha( tick_cnt * 255 / 20 - 1275)
                screen.blit(mask, (0, 0))

            else:
                break

            tick_cnt += 1
            pygame.display.update()
            pygame.time.wait(30)

        sound.stop()
