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
    
    def noFoodMode():
        print('noFoodMode')
        ai = self.helper
        rankList = ai.getTopPlayer()
        for i in range(4):
            if rankList[i] == ai.index:
                break
        if i >= 3:
            pathLen = []
            for i in range(3, len(rankList)):
                pathLen.append( ai.getShortestPath(ai.getMyPosition, ai.getPlayerPosition(j), ai.getMyDirection) )
        
            aim = 0
            if pathLen[0] > pathLen[1]:
                aim = 2
            else:
                aim = 3
            return ai.getShortestPath(ai.getMyPosition, ai.getPlayerPosition(aim), ai.getMyDirection)[0] 
        #rank 1, 2
        else:
            #too far--hide(not finished)
            print('rank 1 2')
            if len( ai.getShortestPath(ai.getMyPosition, ai.getPlayerPosition(aim), ai.getMyDirection) ) > 5:
                return self.random()

            #eat!!
            else:
                print('eat')
                return ai.getShortestPath(ai.getMyPosition, ai.getPlayerPosition(aim), ai.getMyDirection)[0] 

                


    
    def personToward(self):
        ai = self.helper
        if ai.checkMeDead():
            return False
        my_pos = ai.getMyDirection()
        print(my_pos)
        facingP = ai.getFacingPlayer(my_pos)

        print(facingP)
        for i in facingP:
            if ai.getPlayerDirection(i) == (-1 * ai.getMyDirection()[0], -1 * ai.getMyDirection(i)[1]):
                return True
        return False        
    
    def random( self ):
        ai = self.helper
        if not ai.checkMeDead():
            ai = self.helper
            res = ai.askGodDirection('der3318')
            while not ai.checkDirection(res):
                res = ai.askGodDirection('der3318')
            return res
        return (1, 0)
    
    def willHavePerson( self, path ):
        ai = self.helper
        for i in range(4):
            if i == ai.index:
                continue
            aimPos = ai.getMyPosition()
            for j in path:
                aimPos = (aimPos[0] + j[0], aimPos[1] + j[1])
                if aimPos == ai.getPlayerPosition( i ):
                    print(i, aimPos)
                    print('haveP')
                    return True
        print('noP')
        return False


    def decide( self ):
        ai = self.helper
        my_pos = ai.getMyPosition()
        my_dir = ai.getMyDirection()
        time = ai.getTimeLeft()
        
        if not ai.checkMeDead():
            foodPosList = ai.getKNearestFood(my_pos, 10)
            for i in range(1, len(foodPosList)):
                isFood = 1
                path = ai.getShortestPath(my_pos, foodPosList[i], my_dir)
                if self.willHavePerson(path):
                    continue
                else:
                    return path[0]
            if isFood and self.personToward():
                return self.random()
            if not isFood:
                self.noFoodMode()
                
        else:
            print("dead")

        print('God')
        return ai.askGodDirection('der3318')
