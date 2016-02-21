from const import *
import const as CON
from gamemap import map as Gmap
from AI.ai_config import *
import Event
import queue
import random
import copy
# from Auth.skill_auth import skillAuth

class Helper:
    def __init__( self , env , index , name ):
        self.env = env
        self.index = index
        self.name = name

    def checkMeDead( self ):
        return self.env[ "player" ][ self.index ].dead

    def verifySkillUsage( self , skill_name ):
        player = self.env[ "player" ][ self.index ]
        if skill_name not in player.ai.skill:
            return False
        '''
        for sig in player.ai.skill[ skill_name ]:
            if skillAuth.verify( sig ):
                return True
        '''
        player.ai.skill.remove( skill_name )
        return True

    def getSkillCoolTime( self ):
        return self.env["skill_cool_time"]

    def SkillBonus( self ):
        if self.verifySkillUsage( 'bonus' ):
            self.env["gamec"].add_event(
                Event.skill_event.EventSkillBonus(
                    self.env, self.env["gamec"].tick + self.env["skill_cool_time"] * 1000, self.index
                )
            )
            self.env["skill_cool_time"] += 10

    def SkillConfuse( self ):
        if self.verifySkillUsage( 'confuse' ):
            self.env["gamec"].add_event(
                Event.skill_event.EventSkillConfuse(
                    self.env, self.env["gamec"].tick + self.env["skill_cool_time"] * 1000, self.index
                )
            )
            self.env["skill_cool_time"] += 10

    def SkillDizzy( self ):
        if self.verifySkillUsage( 'dizzy' ):
            self.env["gamec"].add_event(
                Event.skill_event.EventSkillDizzy(
                    self.env, self.env["gamec"].tick + self.env["skill_cool_time"] * 1000, self.index
                )
            )
            self.env["skill_cool_time"] += 10

    def SkillEatNear( self ):
        if self.verifySkillUsage( 'eatnear' ):
            self.env["gamec"].add_event(
                Event.skill_event.EventSkillEatNear(
                    self.env, self.env["gamec"].tick + self.env["skill_cool_time"] * 1000, self.index
                )
            )
            self.env["skill_cool_time"] += 10

    def SkillShoot( self ):
        if self.verifySkillUsage( 'shoot' ):
            self.env["gamec"].add_event(
                Event.skill_event.EventSkillShootYou(
                    self.env, self.env["gamec"].tick + self.env["skill_cool_time"] * 1000, self.index
                )
            )
            self.env["skill_cool_time"] += 10

    def getEatScore( self , opponent_index ):
        if self.env["player"][self.index].score < self.env["player"][opponent_index].score: 
            if self.env["player"][opponent_index].score < 10:
                return self.env["player"][opponent_index].score
            else:
                return 10
        elif self.env["player"][self.index].score > self.env["player"][opponent_index].score: 
            if self.env["player"][self.index].score < 10:
                return self.env["player"][self.index].score * ( -1 )
            else:
                return -10
        else:
            return 0

    def getNearPlayer( self ):
        distance = []
        for i in range(4):
            if i == self.index:
                continue
            pathLen = len( self.getShortestPath( self.env["player"][self.index].pos , self.env["player"][i].pos , self.env["player"][self.index].dir ) )
            distance.append( ( i , pathLen ) )

        distance.sort( key = lambda x: x[1] )
        nearPlayer = []

        for playerDistance in distance:
            if playerDistance[1] == 0:
                continue
            nearPlayer.append( playerDistance[0] )
        return nearPlayer

    def getTopPlayer( self ):
        res = []
        for i in range( 4 ):
            if i == self.index:
                continue
            res.append( i )
        res = sorted( res , key = lambda x : -self.getPlayerScore( x ) )
        return res

    def getDeadPlayer( self ):
        res = []
        for i in range( 4 ):
            if i == self.index or not self.checkPlayerDead( i ):
                continue
            res.append( i )
        return res

    def getLivePlayer( self ):
        res = []
        for i in range( 4 ):
            if i == self.index or self.checkPlayerDead( i ):
                continue
            res.append( i )
        return res
    
    def checkIntersection( self , pos ):
        up = ( 0 , -1 )
        down = ( 0 , 1 )
        left = ( -1 , 0 )
        right = ( 1 , 0 )
        dir_list = [up, down, left, right]
        
        ( x , y ) = pos
        count = 0
        for delta in dir_list:
            ( dx , dy ) = delta
            if Gmap[ x + dx ][ y + dy ]:
                count += 1        
        if count == 2:
            return False
        else:
            return True

    def getHowManyIntersection( self , now_pos , path ):
        count = 0
        for now_dir in path:
            ( dx , dy ) = now_dir
            ( px , py ) = now_pos
            now_pos = ( px + dx , py + dy )
            if self.checkIntersection( now_pos ):
                count += 1
        return count
    
    def getMeMustBe( self , now_dir ): 
        up = ( 0 , -1 )
        down = ( 0 , 1 )
        left = ( -1 , 0 )
        right = ( 1 , 0 )
        dir_list = [up, down, left, right]

        # now_dir = self.env["player"][index].dir 
        ( px , py ) = self.env["player"][self.index].pos
        ( dx , dy ) = now_dir
        now_pos = ( px + dx , py + dy )
        if now_dir == ( 0 , 0 ):
            return None
        
        while not self.checkIntersection( now_pos ):
            for delta in dir_list:
                ( x , y ) = now_pos
                ( dx , dy ) = delta
                counter_delta = ( dx * (-1) , dy * (-1) )
                if ( Gmap[ x + dx ][ y + dy ] ) and counter_delta != now_dir:
                    now_dir = delta
                    break
            ( dir_x , dir_y ) = now_dir
            ( x , y ) = now_pos
            now_pos = ( dir_x + x , dir_y + y )
        return ( now_pos , now_dir )
    
    def getPlayerMustBe( self , index ): 
        up = ( 0 , -1 )
        down = ( 0 , 1 )
        left = ( -1 , 0 )
        right = ( 1 , 0 )
        dir_list = [up, down, left, right]

        now_dir = self.env["player"][index].dir 
        now_pos = self.env["player"][index].pos 

        if self.checkIntersection( now_pos ) or now_dir == ( 0 , 0 ):
            return ( ( 0 , 0 ) , ( 0 , -1 ) )
        
        while not self.checkIntersection( now_pos ):
            for delta in dir_list:
                ( x , y ) = now_pos
                ( dx , dy ) = delta
                counter_delta = ( dx * (-1) , dy * (-1) )
                if ( Gmap[ x + dx ][ y + dy ] ) and counter_delta != now_dir:
                    now_dir = delta
                    break
            ( dir_x , dir_y ) = now_dir
            ( x , y ) = now_pos
            now_pos = ( dir_x + x , dir_y + y )
        return ( now_pos , now_dir )

    def getFacingPlayer( self , now_dir , now_pos = ( -1 , -1 ) ):
        if now_pos == ( -1 , -1 ):
            now_pos = self.env["player"][self.index].pos
        
        ( dir_x , dir_y ) = now_dir
        ( x , y ) = now_pos
        # if walk this way
        now_pos = ( x + dir_x , y + dir_y )
        # if this way is illegal
        if not Gmap[x + dir_x][y + dir_y]:
            print( "this direction is illegal" )
            return []

        up = ( 0 , -1 )
        down = ( 0 , 1 )
        left = ( -1 , 0 )
        right = ( 1 , 0 )
        dir_list = [up, down, left, right]

        facingPlayer = []
        if now_dir == ( 0 , 0 ):
            return facingPlayer

        while self.checkIntersection( now_pos ) == False:
            # find the next direction
            for delta in dir_list:
                ( x , y ) = now_pos
                ( dx , dy ) = delta
                counter_delta = ( dx * (-1) , dy * (-1) )
                if ( Gmap[ x + dx ][ y + dy ] ) and counter_delta != now_dir:
                    now_dir = delta
                    break
            # check player
            for player_index in range(4):
                if self.getPlayerPosition( player_index ) == now_pos:
                    facingPlayer.append( player_index )
            # next
            ( dir_x , dir_y ) = now_dir
            ( x , y ) = now_pos
            now_pos = ( dir_x + x , dir_y + y )

        return facingPlayer

    def checkDirection( self , check_dir ):
        #print( check_dir )
        ( qdx , qdy ) = check_dir
        ( ndx , ndy ) = self.env["player"][self.index].dir
        ( npx , npy ) = self.env["player"][self.index].pos
        counter_dir = ( ndx * (-1) , ndy * (-1) )

        if ( check_dir != counter_dir )  and  ( Gmap[ npx + qdx ][ npy + qdy ] ):
            return True
        else:
            return False
    
    def getAllowedDirection( self ):
        up = (0, -1)
        down = (0, 1)
        left = (-1, 0)
        right = (1, 0)
        dir_list = [up, down, left, right]
        allowedDirection = []
        for i in dir_list:
            if self.checkDirection( i ):
                allowedDirection.append(i)
        return allowedDirection
    

    def getKNearestFood( self, pos, k ):
        # consts
        up = (0, -1)
        down = (0, 1)
        left = (-1, 0)
        right = (1, 0)
        dir_list = [up, down, left, right]

        foodN = 0
        firstnextposlist = []

        traverseMap = [ [False for j in range(11)] for i in range(19) ]
        traverseMap[pos[0]][pos[1]] = True

        Q = queue.Queue()
        Q.put(pos)
        foodPosList = []

        while not Q.empty():
            flag = False
            c = Q.get()
            for neighbor in self.getNearby( c ):
                # if not traversed
                if not traverseMap[ neighbor[0] ][ neighbor[1] ]:
                    Q.put( neighbor )
                    traverseMap[ neighbor[0] ][ neighbor[1] ] = True

                    if neighbor in self.env["food"]:
                        foodN += 1
                        foodPosList.append(neighbor)

                    if foodN == k:
                        flag = True 
                        break
            if flag:
                break

        return foodPosList

    def getNearby( self , pos ):
        # consts
        up = (0, -1)
        down = (0, 1)
        left = (-1, 0)
        right = (1, 0)

        dir_list = [up, down, left, right]

        anslist = []
        for d in dir_list:
            if Gmap[ d[0] + pos[0] ][ d[1] + pos[1] ] == True:
                anslist.append((d[0]+pos[0], d[1]+pos[1]))
        return anslist


    def getShortestPath( self , startpos , endpos , dir_start = (1,0) ):
        copyMap = [ [ Gmap[i][j] and True for j in range(11) ] for i in range(19) ]

        upper = [ (8,4) , (8,5) , (9,5) ]
        lower = [ (9,5) , (10,5) , (10,6) ]
        if startpos in upper:
            for ( i , j ) in upper:
                copyMap[ i ][ j ] = True
        if startpos in lower:
            for ( i , j ) in lower:
                copyMap[ i ][ j ] = True

        dir = [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]
        q = queue.Queue()
        visited = {}
        anc = {}
        S = ( startpos , dir.index( dir_start ) )
        q.put( ( startpos , dir.index( dir_start ) ) )
        visited[ S ] = True
        anc[ S ] = S

        final_stat = None
        while not q.empty():
            now_stat =  q.get()
            ( ( px , py ) , d ) = now_stat
            if px == endpos[ 0 ] and py == endpos[ 1 ]:
                final_stat = now_stat
                break
            for k in range( 4 ):
                if ( d ^ 1 ) == k: # go backward is invalid
                    continue
                ( tx , ty ) = ( px + dir[ k ][ 0 ] , py + dir[ k ][ 1 ] )
                nxt_stat = ( ( tx , ty ) , k )

                if not copyMap[ tx ][ ty ]:
                    continue
                if nxt_stat in visited:
                    continue

                visited[ nxt_stat ] = True
                anc[ nxt_stat ] = now_stat
                q.put( nxt_stat )

        if not final_stat:
            return []
        
        res = []
        
        while anc[ final_stat ] != final_stat:
            res.append( dir[ final_stat[ 1 ] ] )
            final_stat = anc[ final_stat ]
        return res[::-1]


    def calcFoodOnPath( self , startpos , dirlist ):
        foods = 0
        ( px , py ) = startpos[:]
        for p in dirlist:
            px += p[0]
            py += p[1]
            if (px,py) in self.env[ "food" ]:
                foods += 1
        return foods

## TESTING-------------------
    def getMyPosition( self ):
        return self.env["player"][self.index].pos
    def getPlayerPosition( self , index ):
        return self.env["player"][index].pos

    def getMyDirection( self ):
        return self.env["player"][self.index].dir
    def getPlayerDirection( self , index ):
        return self.env["player"][index].dir

    def getMyScore( self ):
        return self.env["player"][self.index].score
    def getPlayerScore( self, index ):
        return self.env["player"][index].score

    def checkMeDead( self ):
        return self.env["player"][self.index].dead
    def checkPlayerDead( self , index ):
        return self.env["player"][index].dead

    def checkMeStopped( self ):
        return (self.env["player"][self.index].pos_pre == self.env["player"][self.index].pos)
    def checkPlayerStopped( self, index ):
        return (self.env["player"][index].pos_pre == self.env["player"][index].pos)

    # godName is unused
    def askGodDirection( self , godName ):
        up = (0, -1)
        down = (0, 1)
        left = (-1, 0)
        right = (1, 0)
        dir_list = [up, down, left, right]
        return dir_list[random.randrange(4)]
    # godName is unused
    def askGodPosition( self , godName ):
        ( rand_x , rand_y ) = ( random.randrange(19) , random.randrange(11) )
        while not Gmap[rand_x][rand_y]:
            ( rand_x , rand_y ) = ( random.randrange(19) , random.randrange(11) )
        return ( rand_x, rand_y )
    def getTimeLeft( self ):
        return (CON.TOTAL_TIME - self.env["timer"])

    def getMapInfo( self ):
        BLOCK = "BLOCK"
        EMPTY_ROAD = "ROAD"
        FOOD = "FOOD"
        OTHER_PLAYER = "PLAYER"
        MYSELF = "ME"

        # mark block and empty_road
        mapInfo = copy.deepcopy(Gmap)
        
        #mark block and road
        for y in range(11):
            for x in range(19):
                if mapInfo[x][y] is True:
                    mapInfo[x][y] = EMPTY_ROAD
                else:
                    mapInfo[x][y] = BLOCK

        # mark myself
        ( my_x, my_y ) = self.env["player"][self.index].pos
        mapInfo[my_x][my_y] = MYSELF

        # mark other player
        for i in range(4):
            if i == self.index:
                continue
            ( px, py ) = self.env["player"][i].pos
            mapInfo[px][py] = OTHER_PLAYER

        # mark food
        for ( food_x, food_y ) in self.env["food"]:
            mapInfo[food_x][food_y] = FOOD

        return mapInfo
