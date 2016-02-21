import pygame

UNIT = 50
FONT_SIZE = 60

IMG_BG = pygame.transform.scale( pygame.image.load( "./Image/bg_map.png" ), (UNIT * 21, UNIT * 15) )

IMG_PLAYER1 = [
                pygame.transform.scale( pygame.image.load( "./Image/tuzki.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/tuzki.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/tuzki.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/tuzki.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
]
IMG_PLAYER1_d = [
                pygame.transform.scale( pygame.image.load( "./Image/tuzki_d_1.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/tuzki_d_2.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/tuzki_d_3.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/tuzki_d_4.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
]
IMG_PLAYER1_r = [
                pygame.transform.scale( pygame.image.load( "./Image/tuzki_r_1.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/tuzki_r_2.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/tuzki_r_3.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/tuzki_r_4.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
]
IMG_PLAYER1_u = [
                pygame.transform.scale( pygame.image.load( "./Image/tuzki_u_1.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/tuzki_u_2.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/tuzki_u_3.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/tuzki_u_4.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
]
IMG_PLAYER1_l = [
                pygame.transform.scale( pygame.image.load( "./Image/tuzki_l_1.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/tuzki_l_2.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/tuzki_l_3.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/tuzki_l_4.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
]

IMG_PLAYER2 = [
                pygame.transform.scale( pygame.image.load( "./Image/superman.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/superman.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/superman.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/superman.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
]
IMG_PLAYER2_d = [
                pygame.transform.scale( pygame.image.load( "./Image/superman_d_1.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/superman_d_2.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/superman_d_3.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/superman_d_4.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
]
IMG_PLAYER2_r = [
                pygame.transform.scale( pygame.image.load( "./Image/superman_r_1.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/superman_r_2.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/superman_r_3.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/superman_r_4.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
]
IMG_PLAYER2_u = [
                pygame.transform.scale( pygame.image.load( "./Image/superman_u_1.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/superman_u_2.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/superman_u_3.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/superman_u_4.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
]
IMG_PLAYER2_l = [
                pygame.transform.scale( pygame.image.load( "./Image/superman_l_1.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/superman_l_2.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/superman_l_3.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/superman_l_4.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
]

IMG_PLAYER3 = [
                pygame.transform.scale( pygame.image.load( "./Image/cactus.png" ), (int(UNIT * 1.8), int(UNIT * 1.8)) ),
                pygame.transform.scale( pygame.image.load( "./Image/cactus.png" ), (int(UNIT * 1.8), int(UNIT * 1.8)) ),
                pygame.transform.scale( pygame.image.load( "./Image/cactus.png" ), (int(UNIT * 1.8), int(UNIT * 1.8)) ),
                pygame.transform.scale( pygame.image.load( "./Image/cactus.png" ), (int(UNIT * 1.8), int(UNIT * 1.8)) ),
]
IMG_PLAYER3_d = [
                pygame.transform.scale( pygame.image.load( "./Image/cactus_d_1.png" ), (int(UNIT * 1.8), int(UNIT * 1.8)) ),
                pygame.transform.scale( pygame.image.load( "./Image/cactus_d_2.png" ), (int(UNIT * 1.8), int(UNIT * 1.8)) ),
                pygame.transform.scale( pygame.image.load( "./Image/cactus_d_3.png" ), (int(UNIT * 1.8), int(UNIT * 1.8)) ),
                pygame.transform.scale( pygame.image.load( "./Image/cactus_d_4.png" ), (int(UNIT * 1.8), int(UNIT * 1.8)) ),
]
IMG_PLAYER3_r = [
                pygame.transform.scale( pygame.image.load( "./Image/cactus_r_1.png" ), (int(UNIT * 1.8), int(UNIT * 1.8)) ),
                pygame.transform.scale( pygame.image.load( "./Image/cactus_r_2.png" ), (int(UNIT * 1.8), int(UNIT * 1.8)) ),
                pygame.transform.scale( pygame.image.load( "./Image/cactus_r_3.png" ), (int(UNIT * 1.8), int(UNIT * 1.8)) ),
                pygame.transform.scale( pygame.image.load( "./Image/cactus_r_4.png" ), (int(UNIT * 1.8), int(UNIT * 1.8)) ),
]
IMG_PLAYER3_u = [
                pygame.transform.scale( pygame.image.load( "./Image/cactus_u_1.png" ), (int(UNIT * 1.8), int(UNIT * 1.8)) ),
                pygame.transform.scale( pygame.image.load( "./Image/cactus_u_2.png" ), (int(UNIT * 1.8), int(UNIT * 1.8)) ),
                pygame.transform.scale( pygame.image.load( "./Image/cactus_u_3.png" ), (int(UNIT * 1.8), int(UNIT * 1.8)) ),
                pygame.transform.scale( pygame.image.load( "./Image/cactus_u_4.png" ), (int(UNIT * 1.8), int(UNIT * 1.8)) ),
]
IMG_PLAYER3_l = [
                pygame.transform.scale( pygame.image.load( "./Image/cactus_l_1.png" ), (int(UNIT * 1.8), int(UNIT * 1.8)) ),
                pygame.transform.scale( pygame.image.load( "./Image/cactus_l_2.png" ), (int(UNIT * 1.8), int(UNIT * 1.8)) ),
                pygame.transform.scale( pygame.image.load( "./Image/cactus_l_3.png" ), (int(UNIT * 1.8), int(UNIT * 1.8)) ),
                pygame.transform.scale( pygame.image.load( "./Image/cactus_l_4.png" ), (int(UNIT * 1.8), int(UNIT * 1.8)) ),
]

IMG_PLAYER4 = [
                pygame.transform.scale( pygame.image.load( "./Image/pusheen.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/pusheen.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/pusheen.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/pusheen.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
]
IMG_PLAYER4_d = [
                pygame.transform.scale( pygame.image.load( "./Image/pusheen_d_1.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/pusheen_d_2.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/pusheen_d_3.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/pusheen_d_4.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
]
IMG_PLAYER4_r = [
                pygame.transform.scale( pygame.image.load( "./Image/pusheen_r_1.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/pusheen_r_2.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/pusheen_r_3.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/pusheen_r_4.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
]
IMG_PLAYER4_u = [
                pygame.transform.scale( pygame.image.load( "./Image/pusheen_u_1.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/pusheen_u_2.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/pusheen_u_3.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/pusheen_u_4.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
]
IMG_PLAYER4_l = [
                pygame.transform.scale( pygame.image.load( "./Image/pusheen_l_1.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/pusheen_l_2.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/pusheen_l_3.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/pusheen_l_4.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
]

IMG_FOOD = [
           pygame.transform.scale( pygame.image.load( "./Image/food.png" ), (int(UNIT * 1.5), int(UNIT * 1.5)) ),
           pygame.transform.scale( pygame.image.load( "./Image/food.png" ), (int(UNIT * 1.5), int(UNIT * 1.5)) ),
           pygame.transform.scale( pygame.image.load( "./Image/food.png" ), (int(UNIT * 1.5), int(UNIT * 1.5)) ),
           pygame.transform.scale( pygame.image.load( "./Image/food.png" ), (int(UNIT * 1.5), int(UNIT * 1.5)) ),
]

IMG_GAMEOVER = pygame.transform.scale( pygame.image.load( "./Image/bg_gameover.png" ), (UNIT * 21, UNIT * 15) )

IMG_NUM0 = pygame.transform.scale( pygame.image.load( "./Image/num_0.png" ), (FONT_SIZE, FONT_SIZE) )
IMG_NUM1 = pygame.transform.scale( pygame.image.load( "./Image/num_1.png" ), (FONT_SIZE, FONT_SIZE) )
IMG_NUM2 = pygame.transform.scale( pygame.image.load( "./Image/num_2.png" ), (FONT_SIZE, FONT_SIZE) )
IMG_NUM3 = pygame.transform.scale( pygame.image.load( "./Image/num_3.png" ), (FONT_SIZE, FONT_SIZE) )
IMG_NUM4 = pygame.transform.scale( pygame.image.load( "./Image/num_4.png" ), (FONT_SIZE, FONT_SIZE) )
IMG_NUM5 = pygame.transform.scale( pygame.image.load( "./Image/num_5.png" ), (FONT_SIZE, FONT_SIZE) )
IMG_NUM6 = pygame.transform.scale( pygame.image.load( "./Image/num_6.png" ), (FONT_SIZE, FONT_SIZE) )
IMG_NUM7 = pygame.transform.scale( pygame.image.load( "./Image/num_7.png" ), (FONT_SIZE, FONT_SIZE) )
IMG_NUM8 = pygame.transform.scale( pygame.image.load( "./Image/num_8.png" ), (FONT_SIZE, FONT_SIZE) )
IMG_NUM9 = pygame.transform.scale( pygame.image.load( "./Image/num_9.png" ), (FONT_SIZE, FONT_SIZE) )

IMG_DEATH = [
                pygame.transform.scale( pygame.image.load( "./Image/death_1.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/death_2.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/death_3.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
]

IMG_PATH = [
            pygame.transform.scale( pygame.image.load( "./Image/path_1.png" ), (int(UNIT * 2), int(UNIT * 12)) ),
            pygame.transform.scale( pygame.image.load( "./Image/path_2.png" ), (int(UNIT * 2), int(UNIT * 12)) ),
            pygame.transform.scale( pygame.image.load( "./Image/path_3.png" ), (int(UNIT * 2), int(UNIT * 12)) ),
            pygame.transform.scale( pygame.image.load( "./Image/path_4.png" ), (int(UNIT * 2), int(UNIT * 12)) ),
            pygame.transform.scale( pygame.image.load( "./Image/path_5.png" ), (int(UNIT * 2), int(UNIT * 12)) ),
            pygame.transform.scale( pygame.image.load( "./Image/path_6.png" ), (int(UNIT * 2), int(UNIT * 12)) ),
            pygame.transform.scale( pygame.image.load( "./Image/path_7.png" ), (int(UNIT * 2), int(UNIT * 12)) ),
            pygame.transform.scale( pygame.image.load( "./Image/path_8.png" ), (int(UNIT * 2), int(UNIT * 12)) ),
            pygame.transform.scale( pygame.image.load( "./Image/path_9.png" ), (int(UNIT * 2), int(UNIT * 12)) ),
            pygame.transform.scale( pygame.image.load( "./Image/path_10.png" ), (int(UNIT * 2), int(UNIT * 12)) ),
            pygame.transform.scale( pygame.image.load( "./Image/path_11.png" ), (int(UNIT * 2), int(UNIT * 12)) ),
            pygame.transform.scale( pygame.image.load( "./Image/path_12.png" ), (int(UNIT * 2), int(UNIT * 12)) ),
            pygame.transform.scale( pygame.image.load( "./Image/path_13.png" ), (int(UNIT * 2), int(UNIT * 12)) ),
            pygame.transform.scale( pygame.image.load( "./Image/path_14.png" ), (int(UNIT * 2), int(UNIT * 12)) ),
            pygame.transform.scale( pygame.image.load( "./Image/path_15.png" ), (int(UNIT * 2), int(UNIT * 12)) ),
            pygame.transform.scale( pygame.image.load( "./Image/path_16.png" ), (int(UNIT * 2), int(UNIT * 12)) ),
            pygame.transform.scale( pygame.image.load( "./Image/path_17.png" ), (int(UNIT * 2), int(UNIT * 12)) ),
            pygame.transform.scale( pygame.image.load( "./Image/path_18.png" ), (int(UNIT * 2), int(UNIT * 12)) ),
            pygame.transform.scale( pygame.image.load( "./Image/path_18.png" ), (int(UNIT * 2), int(UNIT * 12)) ),
]

IMG_ANT = [
            pygame.transform.scale( pygame.image.load( "./Image/ant_1.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
            pygame.transform.scale( pygame.image.load( "./Image/ant_2.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
            pygame.transform.scale( pygame.image.load( "./Image/ant_3.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
            pygame.transform.scale( pygame.image.load( "./Image/ant_4.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
]

IMG_CONFUSING = [
                pygame.transform.scale( pygame.image.load( "./Image/confuse_1.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/confuse_2.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/confuse_3.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
                pygame.transform.scale( pygame.image.load( "./Image/confuse_4.png" ), (int(UNIT * 2), int(UNIT * 2)) ),
]


IMG_AINMATION_UP = pygame.image.load( "./Image/animation_up.png" )
IMG_CONFUSE_DOWN = pygame.image.load( "./Image/confuse_down.png" )
IMG_BONUS_DOWN = pygame.image.load( "./Image/bonus_down.png" )
IMG_DIZZY_DOWN = pygame.image.load( "./Image/dizzy_down.png" )
IMG_NEAR_DOWN = pygame.image.load( "./Image/near_down.png" )
IMG_SHOOT_DOWN = pygame.image.load( "./Image/shoot_down.png" )
IMG_BONUS = pygame.transform.scale( pygame.image.load( "./Image/bonus.png" ), (int(UNIT * 2), int(UNIT * 2)) )
IMG_DIZZY = pygame.transform.scale( pygame.image.load( "./Image/dizzy.png" ), (int(UNIT * 2), int(UNIT * 2)) )
IMG_CONFUSE = pygame.transform.scale( pygame.image.load( "./Image/confuse_other.png" ), (int(UNIT * 2), int(UNIT * 2)) )
IMG_CONFUSE_ME = pygame.transform.scale( pygame.image.load( "./Image/confuse_me.png" ), (int(UNIT * 2), int(UNIT * 2)) )
IMG_ROCKET = pygame.transform.scale( pygame.image.load( "./Image/rocket.png" ), (int(UNIT * 3), int(UNIT * 3)) )
IMG_EXPLODE = pygame.transform.scale( pygame.image.load( "./Image/explode.png" ), (int(UNIT * 3), int(UNIT * 3)) )

TICKS_PER_TURN = 33
FPS = 36

MAX_FOOD = 10
PICS = 4

ROOM_X = 19
ROOM_Y = 11
SCORE_X = 19
SCORE_Y = 4
ANT_X = 2
ANT_Y = 15
GATE1 = (8, 4)
GATE2 = (10, 6)

TURNS_PER_MOVE = 10
TOTAL_TIME = 180 #(seconds)

CONFUSE_TIME = 3 * 3
DIZZY_TIME = 3 * 3
BONUS_TIME = 3 * 5
ADD_FOOD_TIME = 1
