import random
import queue
import pygame.time

import const as CON

class Controller:
    def __init__(self, before_pause=None, after_pause=None):
        #random.seed(random_seed)
        self.active = False
        self.is_pause = False
        self.clock = pygame.time.Clock()
        self.tick = 0
        self.event_queue = queue.PriorityQueue()
        self.before_pause = before_pause
        self.after_pause = after_pause

    def main(self):
        self.active = True
        while self.active == True:
            while self.active == True and self.event_queue.empty() == False:
                get_event = self.event_queue.get_nowait()
                if (get_event.priority <= self.tick):
                    get_event.do_action()
                else:
                    self.event_queue.put(get_event)
                    break
                while self.is_pause and self.active:
                    pygame.time.wait(200)
            self.tick += CON.TICKS_PER_TURN
            self.clock.tick(CON.FPS)

    def set_pause_event(self, before, after):
        self.before_pause = before
        self.after_pause = after

    def stop(self):
        self.active = False

    def pause(self):
        if self.before_pause:
            self.before_pause.do_action()
        self.is_pause = True

    def resume(self):
        self.is_pause = False
        if self.after_pause:
            self.after_pause.do_action()

    def add_event(self, new_event):
        self.event_queue.put(new_event, True, new_event.priority)

    def get_current_turn(self):
        return self.tick / game_config.TICKS_PER_TURN
