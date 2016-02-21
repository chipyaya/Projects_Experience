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
    
    # do this mode when
    # *** YOU ARE NOT IN CHASE MODE ***
    # (1) there is no food or you are dead
    # (2) someone whose score is less than yours is on the path to the food you want
    
    def safe_random_mode( self ):
        res = self.dirs[ random.randrange( 4 ) ]
        allowed_direction = self.helper.getAllowedDirection()
        face_who = []
        candidate_direction = []
        
        # get safe directions, and save them in candidate_direction
        for direction in allowed_direction:
            is_candidate = True
            facing_player = self.helper.getFacingPlayer( direction )
            for player in facing_player:
                if self.helper.getPlayerScore( player ) <= self.helper.getMyScore():
                    is_candidate = False
                    face_who.append(player)
            
            next_intersection = self.helper.getMeMustBe( direction )[0]
            my_len_to_next_intersection = len( self.helper.getShortestPath( self.helper.getMyPosition() , next_intersection , direction ) )
            if is_candidate:
                for player in range(4):
                    if player == self.helper.index:
                        continue
                    if self.helper.getPlayerScore( player ) <= self.helper.getMyScore():
                        if self.helper.getPlayerDirection( player ) != ( 0 , 0 ):
                            other_len_to_next_intersection = len( self.helper.getShortestPath( self.helper.getPlayerPosition( player ) , next_intersection , self.helper.getPlayerDirection( player ) ) )
                            if other_len_to_next_intersection <= my_len_to_next_intersection:
                                print( "random escape ", player )
                                print( "direction is ", direction )
                                is_candidate = False
                                face_who.append(player)

            if is_candidate:
                candidate_direction.append( direction )
        
        res = self.dirs[ random.randrange( 4 ) ]
        if self.helper.checkMeDead():
            return res
        if len(candidate_direction) == 0:
            # choose the one that the score of the facing player is the lowest
            if len(allowed_direction) == 1:
                res = allowed_direction[0]
            elif len(allowed_direction) == 2:
                if self.helper.getPlayerScore( face_who[0] ) < self.helper.getPlayerScore( face_who[1] ):
                    res = allowed_direction[0]
                else:
                    res = allowed_direction[1]
            elif len(allowed_direction) == 3:
                if self.helper.getPlayerScore( face_who[0] ) < self.helper.getPlayerScore( face_who[1] ) and self.helper.getPlayerScore( face_who[0] ) < self.helper.getPlayerScore( face_who[2] ):
                    res = allowed_direction[0]
                if self.helper.getPlayerScore( face_who[1] ) < self.helper.getPlayerScore( face_who[2] ):
                    res = allowed_direction[1]
                else:
                    res = allowed_direction[2]
        else:
            while res not in candidate_direction:
                res = self.dirs[ random.randrange( 4 ) ]

        print( "res = ", res )
        return res
    

    def check_eat_food_mode( self , path_to_food , path_len ):
        # check whether someone whose score is less than yours is on the path to the food
        eat_food_mode = True
        ( px , py ) = self.helper.getMyPosition()
        for i in range(path_len):
            ( dx , dy ) = path_to_food[i]
            ( px , py ) = ( px + dx , py + dy )
            for player in range(4):
                if ( px , py ) == self.helper.getPlayerPosition( player ):
                    if self.helper.getPlayerScore( player ) < self.helper.getMyScore():
                        eat_food_mode = False

        # after the path but before the next intersection
        if path_len >= 2:
            # come from the last step
            # if path_len == 1 , you would probably walk into wall
            ( last_x , last_y ) = path_to_food[path_len - 2]
            last_pos = ( px - last_x , py - last_y )
            facing_player = self.helper.getFacingPlayer( path_to_food[path_len - 2] , last_pos )
            for player in facing_player:
                if self.helper.getPlayerScore( player ) <= self.helper.getMyScore():
                    eat_food_mode = False
        if path_len == 1:
            # just walk the last step directly
            facing_player = self.helper.getFacingPlayer( path_to_food[path_len - 1] )
            for player in facing_player:
                if self.helper.getPlayerScore( player ) <= self.helper.getMyScore():
                    eat_food_mode = False

        # when you are at the last intersection before you get the food
        # if someone's distance to the food is shorter than you and his score is also less than you
        if self.helper.getHowManyIntersection( self.helper.getMyPosition() , path_to_food ) == 0:
            next_intersection = self.helper.getMeMustBe( path_to_food[0] )[0]
            my_len_to_next_intersection = len( self.helper.getShortestPath( self.helper.getMyPosition() , next_intersection , path_to_food[0] ) )
            for player in range(4):
                if player == self.helper.index:
                    continue
                if self.helper.getPlayerScore( player ) <= self.helper.getMyScore():
                    if self.helper.getPlayerDirection( player ) != ( 0 , 0 ):
                        other_len_to_next_intersection = len( self.helper.getShortestPath( self.helper.getPlayerPosition( player ) , next_intersection , self.helper.getPlayerDirection( player ) ) )
                        if other_len_to_next_intersection <= my_len_to_next_intersection:
                            print( "escape ", player )
                            eat_food_mode = False
        
        #if eat_food_mode:
            #print( "the food I search for: ", px , " " , py )
        return eat_food_mode
    
    def chase_mode( self ):
        #print( "chase_mode" )
        # To those whose score is higher than you
        # check whether you can get to his must_be before he can, if so , chase him 
        for player in range(4):
            if player == self.helper.index:
                continue
            if self.helper.getPlayerScore( player ) > self.helper.getMyScore():
                must_be = self.helper.getPlayerMustBe( player )[0]
                must_dir = self.helper.getPlayerMustBe( player )[1]
                if must_be == ( 0 , 0 ):
                    continue
                other_len = len( self.helper.getShortestPath( self.helper.getPlayerPosition( player ) , must_be , self.helper.getPlayerDirection( player ) ) )            
                my_path_to_must_be = self.helper.getShortestPath( self.helper.getMyPosition() , must_be , self.helper.getMyDirection() )
                my_len = len( my_path_to_must_be )
                if my_len <= other_len:
                    print( "chase " , player )
                    if my_len == 0:
                        ( mx , my ) = must_dir
                        counter_dir = ( mx * (-1) , my * (-1) )
                        return ( True , counter_dir )
                    return ( True , my_path_to_must_be[0] )
                
        return ( False , ( 0 , 0 ) )


    def decide( self ):
        # if you are not in 1st place , do chase mode
        rank = 0
        for player in range(4):
            if self.helper.getPlayerScore( player ) > self.helper.getMyScore():
                rank += 1
        if rank >= 1:
            # chase_mode = ( True/False , direction )
            chase_mode = self.chase_mode()
            if chase_mode[0] == True:
                return chase_mode[1]
        
        # try the best 3 choice of eating food
        nearest_food = self.helper.getKNearestFood( self.helper.getMyPosition() , 3 )
        eat_food_mode = False
        safe_dir = [ True , True , True , True ]
        k = 0
        while (not eat_food_mode) and k <= 2:
            if len( nearest_food ) <= k or self.helper.checkMeDead() or self.helper.getMyDirection() == ( 0 , 0 ):
                return self.safe_random_mode()
            
            path_to_food = self.helper.getShortestPath( self.helper.getMyPosition() , nearest_food[k] , self.helper.getMyDirection() )
            path_len = len( path_to_food ) 
            eat_food_mode = self.check_eat_food_mode( path_to_food , path_len )
            if not eat_food_mode:
                i = 0
                for direction in self.dirs:
                    if direction == path_to_food[0]:
                        safe_dir[i] = False
                    i += 1
            else:
                i = 0
                for direction in self.dirs:
                    if direction == path_to_food[0]:
                        if not safe_dir[i]:
                            eat_food_mode = False
                    i += 1
            k += 1

        if eat_food_mode: 
            return path_to_food[0]
        else:
            return self.safe_random_mode()
