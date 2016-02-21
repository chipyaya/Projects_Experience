from AI.base_ai import BaseAI
from AI.ai_config import *
import random

class TeamAI( BaseAI ):
    def __init__( self , helper ):
        BaseAI.__init__( self , helper )

    def decide( self ):
        helper = self.helper
        my_pos = helper.getMyPosition()
        my_dir = helper.getMyDirection()
        res = helper.askGodDirection( "FoodGod" )

        if helper.checkMeDead():
            return res

        nearest_food = helper.getKNearestFood( my_pos , 1 )
        if len( nearest_food ) > 0:
            path_to_food = helper.getShortestPath( my_pos , nearest_food[0] , helper.getMyDirection() )
            if len( path_to_food ) > 0:
                res = path_to_food[0]
        
        while not helper.checkDirection( res ):
            res = helper.askGodDirection( "FoodGod" )

        return res
