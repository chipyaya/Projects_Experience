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
        return self.dirs[ random.randrange( 4 ) ]

