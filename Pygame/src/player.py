class Player():
    def __init__(self):
        self.score = 0
        self.dead = False
        self.index = 0
        self.dir = (0, 0)
        self.dir_buf = (0, 0)
        self.pos_pre = (0, 0)
        self.pos_draw = (0, 0)
        self.pos = (0, 0)
        self.limit_time = 0  # can't move
        self.food_animation = 0 # used for animation
        self.ai = None
        self.is_dizzy = False
        self.score_rate = 1
