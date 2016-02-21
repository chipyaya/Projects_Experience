from AI.base_ai import BaseAI
from AI.ai_config import *
import random

class TeamAI( BaseAI ):
    def __init__( self , helper ):
        BaseAI.__init__( self , helper )
        self.skill = [ "bonus" , "bonus" , "bonus" , "confuse" , "dizzy" , "shoot" , "eatnear"]

    def decide( self ):
        self.helper.SkillConfuse()
        self.helper.SkillDizzy()
        self.helper.SkillShoot()
        self.helper.SkillEatNear()
        self.helper.SkillBonus()

        res = self.helper.askGodDirection( "RandomGod" )

        if self.helper.checkMeDead():
            return res

        while not self.helper.checkDirection( res ):
            res = self.helper.askGodDirection( "RandomGod" )

        return res
