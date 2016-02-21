import const as CON

class Map():
  def __init__(self):
    self.blocks = [
      (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10),
      (1, 0), (1, 10),
      (2, 0), (2, 2), (2, 3), (2, 4), (2, 6), (2, 7), (2, 8), (2, 10),
      (3, 0), (3, 2), (3, 8), (3, 10),
      (4, 0), (4, 4), (4, 6), (4, 10),
      (5, 0), (5, 1), (5, 2), (5, 4), (5, 6), (5, 8), (5, 9), (5, 10),
      (6, 0), (6, 10),
      (7, 0), (7, 2), (7, 4), (7, 5), (7, 6), (7, 8), (7, 10),
      (8, 0), (8, 2), (8, 6), (8, 8), (8, 10), ( 8 , 4 ),
      (9, 0), (9, 2), (9, 4), (9, 6), (9, 8), (9, 10),
      (10, 0), (10, 2), (10, 4), (10, 8), (10, 10), ( 10 , 6 ),
      (11, 0), (11, 2), (11, 4), (11, 5), (11, 6), (11, 8), (11, 10),
      (12, 0), (12, 10),
      (13, 0), (13, 1), (13, 2), (13, 4), (13, 6), (13, 8), (13, 9), (13, 10),
      (14, 0), (14, 4), (14, 6), (14, 10),
      (15, 0), (15, 2), (15, 8), (15, 10),
      (16, 0), (16, 2), (16, 3), (16, 4), (16, 6), (16, 7), (16, 8), (16, 10),
      (17, 0), (17, 10),
      (18, 0), (18, 1), (18, 2), (18, 3), (18, 4), (18, 5), (18, 6), (18, 7), (18, 8), (18, 9), (18, 10),
    ]    

mapInv = [
  [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
  [False,  True,  True,  True,  True, False,  True,  True,  True,  True,  True,  True,  True, False,  True,  True,  True,  True, False],
  [False,  True, False, False,  True, False,  True, False, False, False, False, False,  True, False,  True, False, False,  True, False],
  [False,  True, False,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True, False,  True, False],
  [False,  True, False,  True, False, False,  True, False, False, False, False, False,  True, False, False,  True, False,  True, False],
  [False,  True,  True,  True,  True,  True,  True, False,  True,  True,  True, False,  True,  True,  True,  True,  True,  True, False],
  [False,  True, False,  True, False, False,  True, False, False, False, False, False,  True, False, False,  True, False,  True, False],
  [False,  True, False,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True,  True, False,  True, False],
  [False,  True, False, False,  True, False,  True, False, False, False, False, False,  True, False,  True, False, False,  True, False],
  [False,  True,  True,  True,  True, False,  True,  True,  True,  True,  True,  True,  True, False,  True,  True,  True,  True, False],
  [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
]
map = [
  [False, False, False, False, False, False, False, False, False, False, False],
  [False,  True,  True,  True,  True,  True,  True,  True,  True,  True, False],
  [False,  True, False, False, False,  True, False, False, False,  True, False],
  [False,  True, False,  True,  True,  True,  True,  True, False,  True, False],
  [False,  True,  True,  True, False,  True, False,  True,  True,  True, False],
  [False, False, False,  True, False,  True, False,  True, False, False, False],
  [False,  True,  True,  True,  True,  True,  True,  True,  True,  True, False],
  [False,  True, False,  True, False, False, False,  True, False,  True, False],
  [False,  True, False,  True, False, False, False,  True, False,  True, False],
  [False,  True, False,  True, False, False, False,  True, False,  True, False],
  [False,  True, False,  True, False, False, False,  True, False,  True, False],
  [False,  True, False,  True, False, False, False,  True, False,  True, False],
  [False,  True,  True,  True,  True,  True,  True,  True,  True,  True, False],
  [False, False, False,  True, False,  True, False,  True, False, False, False],
  [False,  True,  True,  True, False,  True, False,  True,  True,  True, False],
  [False,  True, False,  True,  True,  True,  True,  True, False,  True, False],
  [False,  True, False, False, False,  True, False, False, False,  True, False],
  [False,  True,  True,  True,  True,  True,  True,  True,  True,  True, False],
  [False, False, False, False, False, False, False, False, False, False, False]
]
