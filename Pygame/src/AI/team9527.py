from AI.base_ai import BaseAI
from AI.ai_config import *
import random
from helper import *

class TeamAI( BaseAI ):
    def __init__( self , helper ):
        BaseAI.__init__( self , helper )
        self.dirs = [
          AI_DIR_UP,
          AI_DIR_DOWN,
          AI_DIR_RIGHT,
          AI_DIR_LEFT
        ]

        self.status = "flee"
        self.path = []
        # chase
        self.chase_dir = (0, 0)
        self.chase_player = 0
        self.must_pos = (0,0)
        # tail
        self.tail_player = 0
    
    def random_dir(self):
        res = self.dirs[ random.randrange( 4 ) ]
        if self.helper.checkMeDead():
            return res
        while not self.helper.checkDirection( res ):
            res = self.dirs[ random.randrange( 4 ) ]
        return res

    def is_approaching(self, enemy, try_dir):
        api = self.helper
        my_pos = api.getMyPosition()
        (x, y) = my_pos
        (dx, dy) = try_dir
        my_next_pos  = (x + dx, y + dy)
        enemy_pos = api.getPlayerPosition(enemy)
        enemy_dir = api.getPlayerDirection(enemy)

        me_to_enemy = []
        me_to_enemy.append(try_dir)
        me_to_enemy += api.getShortestPath(my_next_pos, enemy_pos, try_dir)

        enemy_to_me = api.getShortestPath(enemy_pos, my_pos, enemy_dir)
        me_to_enemy_len = len(me_to_enemy)
        enemy_to_me_len = len(enemy_to_me)

        #if me_to_enemy_len < 7 and enemy_to_me_len < 7:
            #print("***** i to him len", me_to_enemy_len)
            #print(me_to_enemy)
            #print("***** he to i len", enemy_to_me_len)
            #print(enemy_to_me)
        if me_to_enemy_len == enemy_to_me_len and me_to_enemy_len < 7:
            return True
        else:
            return False
        
    def decide( self ):
        api = self.helper
        my_pos = api.getMyPosition()
        my_dir = api.getMyDirection()

        # if dead, init the status
        if api.checkMeDead():
            #print("dead")
            self.status = "flee"
            return self.random_dir()

        # can I chase others ?
        if self.status == "flee":
            for i in range(4):
                if i == api.index or api.getEatScore(i) <= 0:
                    continue
                (must_pos, facing_dir) = api.getPlayerMustBe(i)
                if must_pos == (0, 0):
                    continue
                self.must_pos = must_pos
                (p_pos, p_dir) = (api.getPlayerPosition(i), api.getPlayerDirection(i))
                if len(api.getShortestPath(p_pos, must_pos, p_dir)) < len(api.getShortestPath(my_pos, must_pos, my_dir)):
                    continue
                self.status = "chase"
                self.chase_player = i
                self.path = api.getShortestPath(my_pos, must_pos, my_dir)
                (facing_x , facing_y) = facing_dir
                self.chase_dir = (facing_x * (-1), facing_y * (-1))
                break

        # chase mode
        if self.status == "chase":
            #print("chase player" , self.chase_player)
            #print("pos" , self.must_pos)
            if api.checkPlayerDead(self.chase_player) or api.getEatScore(self.chase_player) < 0:
                self.status = "flee"
            elif len(self.path) == 0:
                if api.checkDirection(self.chase_dir):
                    self.status = "flee"
                    return self.chase_dir
                elif api.checkDirection(my_dir):
                    self.status = "flee"
                else:
                    self.status = "wait_for_catch"
                    return my_dir
            else:
                return self.path.pop(0)

        # wait for catching him
        if self.status == "wait_for_catch":
            #print("wait_for_catch")
            #print("wait for player " , self.chase_player)
            if api.checkPlayerDead(self.chase_player) or api.getEatScore(self.chase_player) < 0:
                self.status = "flee"
            else:
                if api.checkDirection(my_dir):
                    self.status = "flee"
                else:
                    return my_dir

        # flee the player
        if self.status == "flee":
            (max_len, max_dir) = (0, (1, 0))
            nearest_players = []

            for player in api.getNearPlayer():
                if api.getEatScore(player) < 0:
                    nearest_players.append(player)

            if len(nearest_players) != 0:
                dir_available = []
                for player in nearest_players:
                    for try_dir in api.getAllowedDirection():
                        p_pos = api.getPlayerPosition(player)
                        shortest_path = api.getShortestPath(my_pos, p_pos, try_dir)
                        nearest_len = len(shortest_path)
                        if nearest_len <= 3 and not self.is_approaching(player, try_dir):
                            self.status = "tail"
                            self.tail_player = player
                            self.path = shortest_path
                            return self.path.pop(0)
                        elif self.is_approaching(player, try_dir):
                            #print(player, " is approaching")
                            if try_dir in dir_available:
                                dir_available.remove(try_dir)
                            continue
                        else:
                            dir_available.append(try_dir)
                if len(dir_available) != 0:
                    return dir_available[random.randrange(len(dir_available))]

        # tailing the low score player
        if self.status == "tail":
            self.path.append(api.getPlayerDirection(self.tail_player))
            next_dir = self.path.pop(0)
            #print("tail player " , self.tail_player)
            if api.checkPlayerDead(self.tail_player) or api.getEatScore(self.tail_player) >= 0:
                self.status = "flee"
            else:
                shortest_path = api.getShortestPath(my_pos, api.getPlayerPosition(self.tail_player), next_dir)
                if len(shortest_path) > 2 or self.is_approaching(self.tail_player, next_dir):
                    self.status = "flee"
                else:
                    return next_dir

        # if don't know what to do, random!
        #print("at a loss!!!")
        return self.random_dir()
        
