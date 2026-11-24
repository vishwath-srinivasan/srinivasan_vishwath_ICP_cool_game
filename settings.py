import pygame as pg

WIDTH = 1024
HEIGHT = 768
TILESIZE = 32
TITLE = "Best game evah!!!"
FPS = 30

#Colors in rgb format
BGCOLOR = (255, 100, 100)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

#player settings
PLAYER_SPEED = 30
PLAYER_ACC = 2
PLAYER_GRAV = 4
PLAYER_FRIC = -0.12
PLAYER_HIT_RECT = pg.Rect(0, 0, TILESIZE-5, TILESIZE-5)
PLAYER_FRIC = -0.1
PLAYER_JUMP = 50

#hoop settings
HOOP_SCALE = 0.75 
HOOP_WIDTH = int(200 * HOOP_SCALE)
HOOP_HEIGHT = int(600 * HOOP_SCALE)
HOOP_BACKBOARD = (44, 17, 20, 58)
HOOP_RIM = (76, 76)

#player controls
RED_CONTROLS = {"left": pg.K_a, "right": pg.K_d, "jump": pg.K_w, "shoot": pg.K_f} #dictionary for player red controls
BLUE_CONTROLS = {"left": pg.K_LEFT, "right": pg.K_RIGHT, "jump": pg.K_UP, "shoot": pg.K_l} #dictionary for player blue controls
PLAYER_FEET_GAP = 5 #removes 5 pixels between shoes and floor

#ball settings
BALL_SIZE = 27
BALL_GRAV = 3
BALL_BOUNCE = 0.7
BALL_SHOT = (22,-36) #speed of ball in (x,y) when shot
BALL_MAX_SPEED = 55
BALL_PICKUP_DELAY = 500 #500 ms delay before picking up ball to make it fairer
BALL_ANCHORS = [(39, 55), (41, 60), (42, 63), (41, 60), (42, 63), (40, 54), (37, 9), (39, 39)] #positions of ball to anchor onto player when someone has possession

#backboard settings
BACKBOARD_BOUNCE = 0.65 #how much speed ball keeps after bouncing off
BACKBOARD_GRIP = 0.9 #speed kept when ball is sliding off of backboard

#scoring settings
HOOP_SCORE_HALF = 8 #pixels distance of how far ball has to be from rim to score
THREE_POINT_DISTANCE = 300 #pixel distance from hoop from 3 point line