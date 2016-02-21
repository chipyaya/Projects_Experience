from AI.base_ai import BaseAI
from AI.ai_config import *
import random

class TeamAI( BaseAI ):
    def __init__( self , helper ):
        BaseAI.__init__( self , helper )
        self.dirs = [
          AI_DIR_UP,
          AI_DIR_DOWN,
          AI_DIR_RIGHT,
          AI_DIR_LEFT
        ]

    def decide( self ):
        # print( "Eat 0 gets:" , self.helper.getEatScore( 0 ) )
        # print( "Nearest player:" , self.helper.getNearPlayer() )
        # print( "Player 0 must be:" , self.helper.getPlayerMustBe( 0 ) )
        # print( "Player" , self.helper.getFacingPlayer() , "facing" )
        print( jizz )
        pathlist = self.helper.getShortestPath( self.helper.getMyPosition() , 
            self.helper.getPlayerPosition( 0 ) , self.helper.getMyDirection() )
        #print( "path to tuzki:" ,  pathlist )
        # print( "3 nearest food:" , self.helper.getKNearestFood( self.helper.getMyPosition() , 3 ) )
        # dirlist = [ (1,0),(0,1),(0,1) ]
        #print( self.helper.calcFoodOnPath( self.helper.getMyPosition() , pathlist ) , "on path" )
        """
        self.helper.getEatScore( 0 )
        self.helper.getNearPlayer()
        self.helper.getPlayerMustBe( 0 )
        self.helper.getFacingPlayer()
        self.helper.getKNearestFood( self.helper.getMyPosition() , 3 )
        self.helper.calcFoodOnPath( self.helper.getMyPosition() , dirlist )
        """
