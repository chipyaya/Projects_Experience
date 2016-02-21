import random
import pygame
import imp
import sys
import traceback

from Event.base_event import BaseEvent
import Event.ui_event
import Event.io_event
import Event.end_event
import Event.animation_event
from player import Player
from helper import Helper
from gamemap import Map
import const as CON

class EventBeforePause:
    def __init__(self, bgm):
        self.bgm = bgm

    def do_action(self):
        self.bgm.pause()

class EventAfterPause:
    def __init__(self, bgm):
        self.bgm = bgm

    def do_action(self):
        self.bgm.unpause()

class EventStartGame(BaseEvent):
    def __init__(self, env, ailist, rnd_seed, priority):
        self.priority = priority
        self.env = env
        self.ailist = [ x for x in map( str , ailist ) ]
        self.random_seed = rnd_seed

    def getAi( self , ailist , player ):
        if len( ailist ) <= player.index:
            return
        i = player.index
        if ailist[ i ] == '_':
          return
        loadtmp = imp.load_source('', './AI/team' + self.ailist[i] + '.py')
        print("Load team" + str(self.ailist[i]) + ".py")
        try:
            player.ai = loadtmp.TeamAI( Helper( self.env , i , self.ailist[i] ) )
            # player.ai.skill = ["bonus", "dizzy", "confuse", "bonus", "eatnear", "shoot"]
        except:
            print( "  player " , i , "'s AI __init__ is crashed'" )
            traceback.print_exc()

    def do_action(self):
        # random.seed(self.random_seed)
        self.env["player"] = []
        self.env["map"] = Map()
        self.env["food"] = []
        self.env["timer"] = 0
        self.env["skill_cool_time"] = 0
        self.env['bgm'] = pygame.mixer.Channel(0)
        self.env['bgm'].play(pygame.mixer.Sound('Sound/bgm.wav'))
        self.env['gamec'].set_pause_event(EventBeforePause(self.env['bgm']), EventAfterPause(self.env['bgm']))
        self.env["crash"] = []

        # setup charater
        start_pos = [ ( 1 , 1 ) , ( 1 , 9 ) , ( 17 , 1 ) , ( 17 , 9 ) ]
        for i in range( 4 ):
            p = Player()
            p.index = i
            ( tx , ty ) = start_pos[ i ]
            p.pos = (tx, ty)
            p.pos_draw = (tx, ty)
            self.getAi( self.ailist , p )
            self.env["player"].append(p)

        self.env["pyQUIT"] = False
        self.env["uic"].add_event( Event.io_event.EventPyEvent(self.env, self.priority) )
        self.env["gamec"].add_event( EventTimer(self.env, self.priority) )
        self.env["uic"].add_event( Event.ui_event.EventDrawInit(self.env, self.priority + 1) )
        self.env["gamec"].add_event( EventMove(self.env, self.priority + 2) )
        self.env["gamec"].add_event( EventCheckCrash(self.env, self.priority + 3) )
        self.env["gamec"].add_event( EventCheckSamePlace(self.env, self.priority + 4) )
        self.env["gamec"].add_event( EventEatFood(self.env, self.priority + 5) )
        self.env["gamec"].add_event( EventAddFood(self.env, self.priority + 6) )
        self.env["gamec"].add_event( EventDecide(self.env, self.priority + 7) )


class EventEndGame(BaseEvent):
    def __init__(self, env, priority):
        self.env = env
        self.priority = priority


    def do_action(self):
        self.env["pyQUIT"] = True
        self.env["gamec"].stop()
        self.env["uic"].stop()

class EventTimer(BaseEvent):
    def __init__(self, env, priority):
        self.env = env
        self.priority = priority

    def do_action(self):
        #print( self.env[ 'timer' ] )
        if self.env["timer"] == CON.TOTAL_TIME:
            self.env["uic"].add_event( Event.end_event.EventGameOver(self.env, -1) )
        else:
            self.env["timer"] += 1
            if self.env["skill_cool_time"] > 0:
                self.env["skill_cool_time"] -= 1
            self.env["gamec"].add_event( EventTimer(self.env, self.priority + 1000) )

class EventDecide( BaseEvent ):
    def __init__( self , env , priority ):
        self.env = env
        self.priority = priority
        self.players = self.env[ "player" ]

    def do_action( self ):
        for player in self.players:
            if player.ai and not player.is_dizzy:
                try:
                    res = player.ai.decide()
                    if not res:
                        continue
                    ( dx , dy ) = res
                    #print( ( dx, dy ) )
                    if abs( int( dx ) ) + abs( int( dy ) ) != 1:
                        continue
                    player.dir_buf = ( dx , dy )
                except:
                    print( "  player " , player.index , "'s AI decision is crashed'" )
                    traceback.print_exc()

        self.env[ "gamec" ].add_event(
            EventDecide( self.env , self.priority + CON.TURNS_PER_MOVE * CON.TICKS_PER_TURN )
        )


class EventMove(BaseEvent):
    def __init__(self, env, priority):
        self.priority = priority
        self.env = env

    # check if dir_buf can be used or not
    def available_place(self, index, pos):
        (x, y) = pos
        if self.env["player"][index].dead:
            if (x, y) == CON.GATE1 or (x, y) == CON.GATE2:
                return True
        if not 0 <= (x) < CON.ROOM_X:
            return False
        if not 0 <= (y) < CON.ROOM_Y:
            return False
        if (x, y) in self.env["map"].blocks:
            return False
        return True

    def dir_available(self, index):
        (x_now, y_now) = self.env["player"][index].pos
        (x_dir, y_dir) = self.env["player"][index].dir
        return self.available_place(index, (x_now + x_dir, y_now + y_dir))

    def dir_buffer_available(self, index):
        (x_now, y_now) = self.env["player"][index].pos
        (x_dir, y_dir) = self.env["player"][index].dir_buf
        if ( x_now , y_now ) == ( 10 , 5 ):
            return (x_dir, y_dir) == ( 0 , 1 )
        if ( x_now , y_now ) == ( 8 , 5 ):
            return (x_dir, y_dir) == ( 0 , -1 )
        if (x_dir, y_dir) == (0, 0):
            return False
        if (-x_dir, -y_dir) == self.env["player"][index].dir:
            return False
        return self.available_place(index, (x_now + x_dir, y_now + y_dir))

    def do_action(self):
        for i in range(4):

            (x_now, y_now) = self.env["player"][i].pos
            self.env["player"][i].pos_pre = self.env["player"][i].pos   # updata pos_pre
            if self.env["player"][i].dead == True:
                if self.env["player"][i].limit_time > 0 and not self.env["player"][i].is_dizzy:
                    self.env["player"][i].limit_time -= CON.TURNS_PER_MOVE * CON.TICKS_PER_TURN
                if self.env["player"][i].limit_time == 0:
                    if (x_now, y_now) == (9, 5) and not self.dir_buffer_available(i):
                        default_dir = random.randrange(2)
                        if default_dir == 0:
                            self.env["player"][i].dir_buf = (-1, 0)
                        else:
                            self.env["player"][i].dir_buf = (1, 0)
                    if (x_now, y_now) == (8, 5):
                        self.env["player"][i].dir = (0, -1)
                    if (x_now, y_now) == (10, 5):
                        self.env["player"][i].dir = (0, 1)
            if ((x_now, y_now) == (8, 3) or (x_now, y_now) == (10, 7)) and (not self.dir_available(i)) and (not self.dir_buffer_available(i)):
                default_dir = random.randrange(2)
                if default_dir == 0:
                    self.env["player"][i].dir_buf = (-1, 0)
                else:
                    self.env["player"][i].dir_buf = (1, 0)
            if self.env["player"][i].is_dizzy == True and self.env["player"][i].dead == False:
                self.env["player"][i].dir_buf = (0, 0)
            if self.dir_buffer_available(i) and self.env["player"][i].limit_time == 0:
                self.env["player"][i].dir = self.env["player"][i].dir_buf
                self.env["player"][i].dir_buf = (0, 0)
            if self.dir_available(i):
                (x_dir, y_dir) = self.env["player"][i].dir
                pos_future = (x_now + x_dir, y_now + y_dir)
                flag = False
                if pos_future == CON.GATE1 or pos_future == CON.GATE2:
                    for j in range(i):
                        if pos_future == self.env["player"][j].pos:
                            flag = True
                if flag == False:
                    if pos_future == CON.GATE1 or pos_future == CON.GATE2:
                        self.env["player"][i].dead = False
                    self.env["player"][i].pos = pos_future
        self.env["gamec"].add_event( EventMove(self.env, self.priority + CON.TURNS_PER_MOVE * CON.TICKS_PER_TURN) )

class EventAddFood(BaseEvent):
    def __init__(self, env, priority):
        self.priority = priority
        self.env = env

    def food_ok( self , new_food ):
        if len( self.env[ "food" ] ) > CON.MAX_FOOD:
            return False

        if new_food in self.env["map"].blocks:
            return False
        if new_food in self.env["food"]:
            return False
        for player in self.env[ "player" ]:
            if new_food == player.pos or new_food == player.pos_pre:
                return False
        (x1, y1) = CON.GATE1
        (x2, y2) = CON.GATE2
        (x, y) = new_food
        if x1 <= x <= x2 and y1 <= y <= y2:
            return False
        return True

    def do_action(self):
        new_food = (random.randrange(CON.ROOM_X), random.randrange(CON.ROOM_Y))

        if self.food_ok( new_food ):
            self.env["food"].append(new_food)
        self.env["gamec"].add_event(
          EventAddFood(self.env, self.priority + CON.ADD_FOOD_TIME * CON.TURNS_PER_MOVE * CON.TICKS_PER_TURN)
        )

class EventEatFood(BaseEvent):
    def __init__(self, env, priority):
        self.priority = priority
        self.env = env

    def do_action(self):
        for i in range(4):
            for pos_food in self.env["food"]:
                if pos_food == self.env["player"][i].pos:
                    self.env["player"][i].food_animation = 20 # enable the animation of eating food
                    self.env["food"].remove(pos_food)
                    self.env["player"][i].score += 5 * self.env["player"][i].score_rate
        self.env["gamec"].add_event( EventEatFood(self.env, self.priority + CON.TURNS_PER_MOVE * CON.TICKS_PER_TURN) )

class EventCheckSamePlace(BaseEvent):
    def __init__(self, env, priority):
        self.priority = priority
        self.env = env

    def is_crashed(self, i, j):
        if self.env["player"][i].pos ==  self.env["player"][j].pos:
            return True
        if self.env["player"][i].pos_pre == self.env["player"][j].pos and self.env["player"][i].pos == self.env["player"][j].pos_pre:
            return True
        return False

    def do_action(self):
        dir_list = []

        up = (0, (-1))
        down = (0, 1)
        left = ((-1), 0)
        right = (1, 0)

        dir_list = [up, down, left, right]
        is_used = [False, False, False, False]

        for i in range(4):
            if is_used[i]:
                continue

            if not self.env["player"][i].dead:
                score_total = 0
                n = 0
                for j in range(4):
                    if self.is_crashed(i, j):
                        is_used[j] = True
                        score_total += self.env["player"][j].score
                        n += 1
                if n <= 1:
                    continue

                dir_available = []

                (px, py) = self.env["player"][i].pos
                for delta in dir_list:
                    (dx, dy) = delta
                    if (px + dx, py + dy) not in self.env["map"].blocks:
                        dir_available.append(delta)

                random.shuffle(dir_list)

                if len(dir_available) < n:
                    for dir in dir_list:
                        if dir not in dir_available:
                            dir_available.append(dir)
                            break

                random.shuffle(dir_available)

                # average the score of the players at the same place, since they were all the minimum before crashing
                # assign dir to the  first player
                for j in range(4):
                    if self.is_crashed(i, j):
                        self.env["player"][j].score = int(score_total / n)
                        newDir = dir_available.pop()
                        self.env["player"][j].dir_buf  = newDir
                        self.env["player"][j].dir  = newDir


                if self.env["player"][i].pos in self.env["food"]:
                        self.env["food"].remove( self.env["player"][i].pos )

        self.env["gamec"].add_event( EventCheckSamePlace(self.env, self.priority + CON.TURNS_PER_MOVE * CON.TICKS_PER_TURN) )

class EventCheckCrash(BaseEvent):
    def __init__(self, env, priority):
        self.priority = priority
        self.env = env

    def is_crashed(self, i, j):
        if self.player[i].pos ==  self.player[j].pos:
            # is empty
            if len(self.env["crash"]) == 0:
                crashPos = self.player[i].pos
                self.env["crash"].append( (crashPos, [i, j]) )
            else:
                crashPos = self.player[i].pos
                for k in self.env["crash"]:
                    if k[0] == crashPos:
                        if i not in k[1]:
                            k[1].append(i)
                        if j not in k[1]:
                            k[1].append(j)
                    else:
                        self.env["crash"].append( (crashPos, [i, j]) )
            return True
        if self.player[i].pos_pre == self.player[j].pos and self.player[i].pos == self.player[j].pos_pre:
            (pre_x, pre_y) = self.player[i].pos_pre
            (now_x, now_y) = self.player[i].pos
            mid = ( (pre_x + now_x) / 2 , (pre_y + now_y) / 2)
            # is empty
            if len(self.env["crash"]) == 0:
                crashPos = mid
                self.env["crash"].append( (crashPos, [i, j]) )
            else:
                crashPos = mid
                for k in self.env["crash"]:
                    if k[0] == crashPos:
                        if i not in k[1]:
                            k[1].append(i)
                        if j not in k[1]:
                            k[1].append(j)
                    else:
                        self.env["crash"].append( (crashPos, [i, j]) )
            return True
        return False
    def do_action(self):
        # sort the players by score, making sure that the player with minumin score would eat all the players with higher score
        self.player = sorted(self.env["player"], key = lambda player : player.score)
        #self.env["crash"] = []
        del self.env["crash"][ : ]
        for i in range(4):
            for j in range(4):
                if i >= j or self.player[i].dead or self.player[j].dead:
                    continue
                if self.is_crashed(i, j):
                    if self.player[i].score > self.player[j].score:
                        self.player[i].score -= 10
                        self.player[j].score += 10
                        if self.player[i].score < 0:
                            self.player[j].score += self.player[i].score
                            self.player[i].score = 0
                        self.player[i].pos = (9, 5)
                        self.player[i].pos_pre = (9, 5)
                        self.player[i].pos_draw = (9, 5)
                        self.player[i].dir = (0, 0)
                        self.player[i].dir_buf = (0, 0)
                        self.player[i].dead = True
                        self.player[i].limit_time = 9 * CON.TURNS_PER_MOVE * CON.TICKS_PER_TURN  # unable to move for about 3 sec(s)
                    elif self.player[i].score < self.player[j].score:
                        self.player[i].score += 10
                        self.player[j].score -= 10
                        if self.player[j].score < 0:
                            self.player[i].score += self.player[j].score
                            self.player[j].score = 0
                        self.player[j].pos = (9, 5)
                        self.player[j].pos_pre = (9, 5)
                        self.player[j].pos_draw = (9, 5)
                        self.player[j].dir = (0, 0)
                        self.player[j].dir_buf = (0, 0)
                        self.player[j].dead = True
                        self.player[j].limit_time = 9 * CON.TURNS_PER_MOVE * CON.TICKS_PER_TURN  # unable to move for about 3 sec(s)
        #print("crash", self.env["crash"])
        self.env["player"] = sorted(self.player, key = lambda player : player.index)
        self.env["gamec"].add_event( EventCheckCrash(self.env, self.priority + CON.TURNS_PER_MOVE * CON.TICKS_PER_TURN) )
