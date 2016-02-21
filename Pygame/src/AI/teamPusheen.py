from AI.ai_config import *
from AI.base_ai import *
from helper import *

class TeamAI( BaseAI ):
    def __init__( self , helper ):
        self.skill = []
        self.helper = helper
        self.stoponce = False;

    # max of dict: 
    #    max( myMap , key = myMap.get )


    def decide( self ):
        api      =  self.helper
        score    =  api.getMyScore()
        pos      =  api.getMyPosition()
        direc    =  api.getMyDirection()
        time     =  api.getTimeLeft()
        pScore   =  api.getTopPlayer()
        # score list
        for n in range(3):
            if score >= api.getPlayerScore( pScore[n] ):
                pScore.insert( n , api.index )
                break
        if len( pScore ) < 4:
            pScore.insert( 3 , api.index )
        pNear    =  api.getNearPlayer()
        print( pNear )
        rank     =  n
       
        
        # action to do
        normal = 0
        chase = 1
        hide = 2

        # accepted pos list
        dirlist = { (1,0):(0,0) , (0,1):(0,0) , (-1,0):(0,0) , (0,-1):(0,0) }
        oklist = {}

        # Mode 0: Eating!!
        if len( api.getShortestPath( pos , api.getPlayerPosition( pNear[0] ) , direc ) ) > 5:
            foodlist = api.getKNearestFood( pos , 1 )
            if len( foodlist ) > 0:
                foodpath = api.getShortestPath( pos , foodlist[0] , direc )
                if len( foodpath ) > 0:
                    return foodpath[0]

        # Mode 1: 1st place
        if rank == 0:
            for i in range( 1 , 4 ):
                playerpos = api.getPlayerMustBe( pScore[i] )
                if playerpos[0][0] == 0 and playerpos[0][1] == 0:
                    playerpos = api.getPlayerPosition( pScore[i] )
                firstpath = api.getShortestPath( pos , playerpos , direc )
                if len( firstpath ) == 0:
                    continue
                else:
                    firstpos = firstpath[0]
                dirlist.pop( firstpos )
                dirlist[ firstpos ] = ( hide , pScore[i] )
            for i in dirlist:
                if dirlist[ i ][0] == normal and api.checkDirection( i ): 
                    oklist[i] = api.calcFoodOnPath( pos , api.getShortestPath( pos, api.getPlayerPosition( dirlist[i][1] ) , direc ) )
            if len( oklist ) > 0:
                return max( oklist , key=oklist.get )
        
        # Mode 2: 2,3,4 place
        else:
            # for those higher than me
            for i in range( 0 , rank ):
                playerpos = api.getPlayerMustBe( pScore[i] )
                if playerpos[0][0] == 0 and playerpos[0][1] == 0:
                    playerpos = api.getPlayerPosition( pScore[i] )
                firstpath = api.getShortestPath( pos , playerpos , direc )
                if len( firstpath ) == 0:
                    continue
                else:
                    firstpos = firstpath[0]
                if ( dirlist[ firstpos ][0] == chase and pNear.index( dirlist[ firstpos ][1] ) > pNear.index( pScore[i] ) ) or dirlist[ firstpos ][0] != chase:
                    dirlist.pop( firstpos )
                    dirlist[ firstpos ] = ( chase , pScore[i] )

            # for those lower than me
            for i in range( rank+1 , 4 ):
                playerpos = api.getPlayerMustBe( pScore[i] )
                if playerpos[0][0] == 0 and playerpos[0][1] == 0:
                    playerpos = api.getPlayerPosition( pScore[i] )
                firstpath = api.getShortestPath( pos , playerpos , direc )
                if len( firstpath ) == 0:
                    continue
                else:
                    firstpos = firstpath[0]
                dirlist.pop( firstpos )
                dirlist[ firstpos ] = ( hide , pScore[i] )
        
            # chase but not hide , then more food.
            for k in dirlist:
                if dirlist[k][0] == chase:
                    oklist[k] = api.calcFoodOnPath( pos , api.getShortestPath( pos, api.getPlayerPosition( dirlist[k][1] ) , direc ) )
            if len( oklist ) != 0:
                return max( oklist , key=oklist.get )
            else:
                for k in dirlist:
                    if dirlist[k][0] == normal and api.checkDirection( k ):
                        return k
        
        # still no answer
        direction = api.askGodDirection( "HTLin" )
        while not api.checkDirection( direction ) and not api.checkMeDead():
            direction = api.askGodDirection( "Li Chen XDD" )
        
        return direction
        
                
