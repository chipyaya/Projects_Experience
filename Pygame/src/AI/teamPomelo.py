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
    

    def safe_random_mode( self ):
        res = self.dirs[ random.randrange( 4 ) ]
        allowed_direction = self.helper.getAllowedDirection()
        candidate_direction = []
        
        # get safe directions
        for direction in allowed_direction:
            is_candidate = True
            facing_player = self.helper.getFacingPlayer( direction )
            for player in facing_player:
                if self.helper.getPlayerScore( player ) <= self.helper.getMyScore():
                    is_candidate = False
            if is_candidate:
                candidate_direction.append( direction )
        
        res = self.dirs[ random.randrange( 4 ) ]
        if self.helper.checkMeDead():
            return res
        if len(candidate_direction) == 0:
            while res not in allowed_direction:
                res = self.dirs[ random.randrange( 4 ) ]
        else:
            while res not in candidate_direction:
                res = self.dirs[ random.randrange( 4 ) ]

        #print( "res = ", res )
        return res

    def decide( self ):
        
        nearest_food = self.helper.getKNearestFood( self.helper.getMyPosition() , 1 )
        if len( nearest_food ) == 0 or self.helper.checkMeDead() or self.helper.getMyDirection() == ( 0 , 0 ):
            return self.safe_random_mode()
        
        path_to_food = self.helper.getShortestPath( self.helper.getMyPosition() , nearest_food[0] , self.helper.getMyDirection() )
        path_len = len( path_to_food )
        ( px , py ) = self.helper.getMyPosition()
        
        go_this_way = True
        for i in range(path_len):
            ( dx , dy ) = path_to_food[i]
            ( px , py ) = ( px + dx , py + dy )
            for player in range(4):
                if ( px , py ) == self.helper.getPlayerPosition( player ):
                    if self.helper.getPlayerScore( player ) < self.helper.getMyScore():
                        go_this_way = False
        
        if path_len >= 2:
            ( last_x , last_y ) = path_to_food[path_len - 2]
            last_pos = ( px - last_x , py - last_y )
            facing_player = self.helper.getFacingPlayer( path_to_food[path_len - 2] , last_pos )
            for player in facing_player:
                if self.helper.getPlayerScore( player ) <= self.helper.getMyScore():
                    go_this_way = False

        if go_this_way:
            #print( "the food I search for: ", px , " " , py )
            #print( "path: ", path_to_food )
            #print( "my postion: ", self.helper.getMyPosition() )
            #print( "pathToFood: ", pathToFood[0] )
            return path_to_food[0]
        else:
            return self.safe_random_mode()
