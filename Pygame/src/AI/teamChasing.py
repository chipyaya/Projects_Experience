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
        my_score = helper.getMyScore()
        res = helper.askGodDirection( "RoadGod" )

        if helper.checkMeDead():
            return res

        for player_index in range(4):
            if player_index == self.helper.index:
                continue
            if helper.getPlayerScore( player_index ) > my_score:
                target_place = helper.getPlayerMustBe( player_index )[0]
                
                if target_place == ( 0 , 0 ):
                    continue
                
                target_dir =  helper.getPlayerMustBe( player_index )[1]
                player_pos = helper.getPlayerPosition( player_index )
                player_dir = helper.getPlayerDirection( player_index )
                path_to_target_place = helper.getShortestPath( my_pos , target_place , my_dir )
                steps_of_player = len( helper.getShortestPath( player_pos , target_place , player_dir ) )
                steps_of_me = len( path_to_target_place )
                
                if steps_of_player >= steps_of_me:
                    if steps_of_me == 0:
                        ( dx , dy ) = target_dir
                        res = ( -dx , -dy )
                    else:
                        res = path_to_target_place[0]
        
        while not helper.checkDirection( res ):
            res = helper.askGodDirection( "RoadGod" )

        return res
