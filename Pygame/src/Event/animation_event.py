import pygame

from Event.base_event import BaseEvent
import const as CON
import math

IMG_ANIME = CON.IMG_AINMATION_UP
IMG_DOWN = {
    "Confuse" : CON.IMG_CONFUSE_DOWN,
    "Dizzy" : CON.IMG_DIZZY_DOWN,
    "Bonus" : CON.IMG_BONUS_DOWN,
    "Near" : CON.IMG_NEAR_DOWN,
    "Shoot" : CON.IMG_SHOOT_DOWN,
}

IMG_PLAYER =  [
    pygame.transform.scale( pygame.image.load( "./Image/tuzki.png" ), (int(CON.UNIT * 4), int(CON.UNIT * 4)) ),
    pygame.transform.scale( pygame.image.load( "./Image/superman.png" ), (int(CON.UNIT * 4), int(CON.UNIT * 4)) ),
    pygame.transform.scale( pygame.image.load( "./Image/cactus.png" ), (int(CON.UNIT * 3.5), int(CON.UNIT * 3.5)) ),
    pygame.transform.scale( pygame.image.load( "./Image/pusheen.png" ), (int(CON.UNIT * 4.5), int(CON.UNIT * 4.5)) ),
]

class EventDrawSkillAnime( BaseEvent ):
    class Frame( pygame.sprite.Sprite ):
        def __init__( self, image , pos ):
            pygame.sprite.Sprite.__init__( self )
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.topleft = pos

    def __init__( self , env , priority , skill_name, player_id ):
        self.env = env
        self.priority = priority
        self.skill_name = skill_name
        self.surf = env[ "screen" ]
        self.upper = IMG_ANIME
        self.lower = IMG_DOWN[ skill_name ]
        self.img = IMG_PLAYER[ player_id ]
        self.anime_group = pygame.sprite.Group()
        self.sound_in = pygame.mixer.Sound("./Sound/skill_in.wav")
        self.sound_out = pygame.mixer.Sound("./Sound/skill_out.wav")

    def do_action( self ):
        self.env[ "gamec" ].pause()
        self.env[ "uic" ].pause()

        for i in range( CON.FPS ):
            if i == CON.FPS // 6:
                self.sound_in.play()
            if i == CON.FPS // 6 * 4:
                self.sound_out.play()
            self.env[ "player_painter" ].update()
            self.env[ "food_painter" ].update()
            self.env[ "score_painter" ].update()
            dx = ( i * 2 - CON.FPS ) ** 3 + CON.FPS
            dx = dx // 30
            self.anime_group.empty()
            self.anime_group.add( self.Frame( self.upper , ( 0 + dx , int( 4.8 * CON.UNIT ) ) ) )
            self.anime_group.add( self.Frame( self.img , ( 0 + dx + 200 , int( 6.2 * CON.UNIT ) ) ) )
            self.anime_group.add( self.Frame( self.lower , ( 5 * CON.UNIT - dx , int( 5.2 * CON.UNIT ) ) ) )

            self.env[ "player_painter" ].clear()
            self.env[ "food_painter" ].clear()
            self.env[ "score_painter" ].clear()
            self.anime_group.clear( self.surf , CON.IMG_BG )

            self.env[ "player_painter" ].draw()
            self.env[ "food_painter" ].draw()
            self.env[ "score_painter" ].draw()
            self.anime_group.draw( self.surf )

            pygame.display.update()
            pygame.time.wait( CON.TICKS_PER_TURN )

        self.anime_group.empty()
        self.anime_group.clear( self.surf , CON.IMG_BG )

        self.env[ "gamec" ].resume()
        self.env[ "uic" ].resume()

class EventDrawEatNearAnime( BaseEvent ):
    class Frame( pygame.sprite.Sprite ):
        def __init__( self, image , pos ):
            pygame.sprite.Sprite.__init__( self )
            self.image = image
            self.rect = self.image.get_rect()
            ( x , y ) = pos
            self.rect.topleft = ( x - CON.UNIT // 2 , y - CON.UNIT // 2 )

    def __init__( self , env , priority , player_id , eaten_foods ):
        self.env = env
        self.priority = priority
        self.pid = player_id
        self.eaten_foods = eaten_foods# [ ( CON.UNIT * x , CON.UNIT * y ) for ( x , y ) in eaten_foods ]
        self.player = self.env[ "player" ][ self.pid ]
        self.surf = env[ "screen" ]
        self.food_img = CON.IMG_FOOD[ 0 ]
        self.anime_group = pygame.sprite.Group()

    def do_action( self ):
        if len( self.eaten_foods ) == 0:
            return
        self.env[ "gamec" ].pause()
        self.env[ "uic" ].pause()

        ( px , py ) = self.env[ "player" ][ self.pid ].pos
        ( px , py ) = ( CON.UNIT * px , CON.UNIT * py )


        for pos in self.eaten_foods:
            if pos in self.env[ "food" ]:
                self.env[ "food" ].remove( pos )
                self.player.score += 5 * self.player.score_rate

        total_frame = CON.FPS // 4
        for i in range( total_frame ):
            self.env[ "player_painter" ].update()
            self.env[ "food_painter" ].update()
            self.env[ "score_painter" ].update()
            self.anime_group.empty()
            for ( x , y ) in self.eaten_foods:
                ratio = ( i / total_frame ) ** 2
                ( x , y ) = ( CON.UNIT * x , CON.UNIT * y )
                ( tx , ty ) = (
                    x + ( px - x ) * ratio ,
                    y + ( py - y ) * ratio
                )
                #print( "  now eaten foods at " , ( tx , ty ) )
                self.anime_group.add( self.Frame( self.food_img , ( tx , ty ) ) )

            self.env[ "player_painter" ].clear()
            self.env[ "food_painter" ].clear()
            self.env[ "score_painter" ].clear()
            self.anime_group.clear( self.surf , CON.IMG_BG )

            self.env[ "player_painter" ].draw()
            self.env[ "food_painter" ].draw()
            self.env[ "score_painter" ].draw()
            self.anime_group.draw( self.surf )

            pygame.display.update()
            pygame.time.wait( CON.TICKS_PER_TURN )

        self.anime_group.empty()
        self.anime_group.clear( self.surf , CON.IMG_BG )

        self.env[ "gamec" ].resume()
        self.env[ "uic" ].resume()

class EventDrawShoot(BaseEvent):
    class Frame(pygame.sprite.Sprite):
        def __init__(self, image, pos):
            pygame.sprite.Sprite.__init__(self)
            self.image = image
            self.rect = self.image.get_rect()
            (x, y) = pos
            self.rect.topleft = (x - CON.UNIT, y - CON.UNIT)
    def __init__(self, env, priority, player_id, target_id):
        self.env = env
        self.priority = priority
        self.pid = player_id
        self.tid = target_id
        self.player = self.env["player"]
        self.surf = env["screen"]
        self.rocket_img = CON.IMG_ROCKET
        self.explode_img = CON.IMG_EXPLODE
        self.anime_group = pygame.sprite.Group()
    def killing(self, i, j):
        self.player[i].score -= 5
        self.player[j].score += 5
        if self.player[i].score < 0:
            self.player[j].score += self.player[i].score
            self.player[i].score = 0
        self.player[i].pos = (9, 5)
        self.player[i].pos_pre = (9, 5)
        self.player[i].pos_draw = (9, 5)
        self.player[i].dir = (0, 0)
        self.player[i].dir_buf = (0, 0)
        self.player[i].dead = True
        self.player[i].limit_time = 9 * CON.TURNS_PER_MOVE * CON.TICKS_PER_TURN  # unable to move for about 3 sec(s)
    def do_action(self):
        (px, py) = self.env["player"][self.pid].pos
        (tx, ty) = self.env["player"][self.tid].pos
        self.env["gamec"].pause()
        self.env["uic"].pause()

        total_frame = CON.FPS // 4
        (vx, vy) = (tx - px, ty - py)
        (dx, dy) = (vx / total_frame, vy / total_frame)
        (rx, ry) = (px, py)
        sita = math.atan2(-vy, vx)
        rocket = pygame.transform.rotate(self.rocket_img , sita * 180 / math.pi)
        for i in range(total_frame):
            self.env["player_painter"].update()
            self.env["food_painter"].update()
            self.env["score_painter"].update()
            self.anime_group.empty()

            self.anime_group.add(self.Frame(rocket,
                (int(rx * CON.UNIT), int(ry * CON.UNIT)))
            )
            rx += dx
            ry += dy

            if i == total_frame - 1:
                self.anime_group.add( self.Frame( self.explode_img, (tx * CON.UNIT, ty * CON.UNIT) ) )

            self.env["player_painter"].clear()
            self.env["food_painter"].clear()
            self.env["score_painter"].clear()
            self.anime_group.clear(self.surf, CON.IMG_BG)

            self.env["player_painter"].draw()
            self.env["food_painter"].draw()
            self.env["score_painter"].draw()
            self.anime_group.draw(self.surf)

            pygame.display.update()
            pygame.time.wait(CON.TICKS_PER_TURN)

        pygame.time.wait(CON.TICKS_PER_TURN * 10)
        self.anime_group.empty()
        self.anime_group.clear( self.surf , CON.IMG_BG )

        self.killing(self.tid, self.pid)
        self.env[ "gamec" ].resume()
        self.env[ "uic" ].resume()
