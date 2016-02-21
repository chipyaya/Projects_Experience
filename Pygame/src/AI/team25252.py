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
        

    def decide( self ):
        """
        print("*****************")
        print("mypos ", self.helper.getMyPosition())
        print("playerpos ", self.helper.getPlayerPosition(3))
        print("mydir", self.helper.getMyDirection())
        print("playerDir", self.helper.getPlayerDirection(3))
        print("myscore", self.helper.getMyScore())
        print("playerscore", self.helper.getPlayerScore(3))
        print("medead", self.helper.checkMeDead())
        print("playerDead", self.helper.checkPlayerIsDead(3))
        print("meStopped", self.helper.checkMeStopped())
        print("playerStopped", self.helper.checkPlayerStopped(3))
        print("*****************")

        skill_rand = random.randrange( 10 )
        if skill_rand == 6:
            self.helper.SkillBonus()
        if skill_rand == 4:
            self.helper.SkillDizzy()
        if skill_rand == 5:
            self.helper.SkillConfuse()
        """

        res = self.dirs[ random.randrange( 4 ) ]
        if self.helper.checkMeDead():
            return res
        while not self.helper.checkDirection( res ):
            res = self.dirs[ random.randrange( 4 ) ]
        return res


