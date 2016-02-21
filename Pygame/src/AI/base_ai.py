from AI.ai_config import *

class BaseAI:
    def __init__( self , helper ):
        self.skill = []
        self.helper = helper

    def decide( self ):
        pass

