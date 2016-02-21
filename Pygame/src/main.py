#!/usr/bin/env python3
import sys
import random
import threading
import pygame

import controller
import Event.game_event
import const as CON
import splash_screen

def main(argv):
    random_seed = '514'
    # create controllers
    gamec = controller.Controller()
    uic = controller.Controller()

    # INIT OF ENV
    pygame.init()
    env = {"gamec" : gamec , "uic" : uic}
    pygame.display.set_caption("Sticker War")
    env["screen"] = pygame.display.set_mode( (CON.ROOM_X * CON.UNIT + CON.ANT_X * CON.UNIT, CON.ROOM_Y * CON.UNIT + CON.SCORE_Y * CON.UNIT) ,0,32)
    env["gamec"].add_event(Event.game_event.EventStartGame(env, argv[1:], random_seed, 0))

    # create treads
    gamec_thread = threading.Thread(target=gamec.main)
    #uic_thread = threading.Thread(target=uic.main)
    
    opening=splash_screen.SplashScreen(env)
    opening.start()
	# start threads
    gamec_thread.start()
    #uic_thread.start()
    uic.main()

    # wait threads terminate
    gamec_thread.join()
    #uic_thread.join()
    while not env['pyQUIT']:
        for e in pygame.event.get():
            if e.type == pygame.locals.KEYDOWN or e.type == pygame.locals.QUIT:
                env['pyQUIT'] = True

    pygame.quit()

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
