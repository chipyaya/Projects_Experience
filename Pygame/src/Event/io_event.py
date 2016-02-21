import pygame
import pygame.locals

from Event.base_event import BaseEvent
import Event.game_event
import Event.skill_event
import const as CON

move_keys = {
    pygame.locals.K_LEFT : ( -1 , 0 ),
    pygame.locals.K_RIGHT : ( 1 , 0 ),
    pygame.locals.K_UP : ( 0 , -1 ),
    pygame.locals.K_DOWN : ( 0 , 1 ),
    pygame.locals.K_a : ( -1 , 0 ),
    pygame.locals.K_d : ( 1 , 0 ),
    pygame.locals.K_w : ( 0 , -1 ),
    pygame.locals.K_s : ( 0 , 1 ),
    pygame.locals.K_f : ( -1 , 0 ),
    pygame.locals.K_h : ( 1 , 0 ),
    pygame.locals.K_t : ( 0 , -1 ),
    pygame.locals.K_g : ( 0 , 1 ),
    pygame.locals.K_j : ( -1 , 0 ),
    pygame.locals.K_l : ( 1 , 0 ),
    pygame.locals.K_i : ( 0 , -1 ),
    pygame.locals.K_k : ( 0 , 1 ),
}

# player1: index = 0, key = (w, a, s, d)
# player2: index = 1, key = (t, f, g, h)
# player3: index = 2, key = (i, j, k, l)
# player4: index = 3, key = (up, left, down, right)

keys_to_player = {
    pygame.locals.K_LEFT : 3,    pygame.locals.K_RIGHT : 3,    pygame.locals.K_UP : 3,    pygame.locals.K_DOWN : 3,
    pygame.locals.K_a : 0,    pygame.locals.K_d : 0,    pygame.locals.K_w : 0,    pygame.locals.K_s : 0,
    pygame.locals.K_f : 1,    pygame.locals.K_h : 1,    pygame.locals.K_t : 1,    pygame.locals.K_g : 1,
    pygame.locals.K_j : 2,    pygame.locals.K_l : 2,    pygame.locals.K_k : 2,    pygame.locals.K_i : 2,
}

class EventPyEvent(BaseEvent):
    def __init__(self, env, priority):
        self.priority = priority
        self.env = env

    def do_action(self):
        for e in pygame.event.get():
            if e.type == pygame.locals.QUIT:
                self.env[ "gamec" ].add_event( Event.game_event.EventEndGame( self.env , self.priority) )
            elif e.type == pygame.locals.KEYDOWN:
                if e.key == pygame.locals.K_p:
                    if self.env["gamec"].is_pause:
                        self.env["gamec"].resume()
                    else:
                        self.env["gamec"].pause()
                '''
                if e.key == pygame.locals.K_z:
                    self.env["gamec"].add_event( Event.skill_event.EventSkillDizzy(self.env, self.priority, 3) )
                if e.key == pygame.locals.K_x:
                    self.env["gamec"].add_event( Event.skill_event.EventSkillConfuse(self.env, self.priority, 3) )
                if e.key == pygame.locals.K_c:
                    self.env["gamec"].add_event( Event.skill_event.EventSkillBonus(self.env, self.priority, 3) )
                if e.key == pygame.locals.K_v:
                    self.env["gamec"].add_event( Event.skill_event.EventSkillEatNear(self.env, self.priority, 3) )
                if e.key == pygame.locals.K_b:
                    self.env["gamec"].add_event( Event.skill_event.EventSkillShootYou(self.env, self.priority, 3) )
                '''
                if e.key not in move_keys:
                    continue
                player_index = keys_to_player[ e.key ]
                if not self.env[ "player" ][ player_index ].ai:
                    self.env["player"][player_index].dir_buf = move_keys[ e.key ]
        self.env["uic"].add_event(EventPyEvent(self.env, self.priority + CON.TICKS_PER_TURN))
