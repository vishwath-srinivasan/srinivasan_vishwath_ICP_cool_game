import pygame as pg #imports pygame with shorthand of pg
from settings import * #imports everything from settings.py
from pygame.sprite import Sprite #imports Sprite class
from os import path #imports path to let us use our system's directory system
from utils import *

from random import randint

vec = pg.math.Vector2

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

def collide_with_walls(sprite, group, dir): #wall collision by checking hitbox of Player vs Wall so it doesn't faze through
    #check for x collision
    if dir == 'x':
        #checking to see if we've collided with hitrects
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits: 
            if hits[0].rect.centerx > sprite.hit_rect.centerx: #checks if we're to the left of the wall/object
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2 #reposition the player (sprite) to left side of wall/object
            if hits[0].rect.centerx < sprite.hit_rect.centerx: #checks if we're to the right of the wall/object
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2 #reposition player (sprite) to right side of wall/object
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery: #checks if we're above wall/object
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2 #reposition player (sprite) to upper side of wall
            if hits[0].rect.centery < sprite.hit_rect.centery: #checks if we're below wall/object
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2 #reposition player (sprite) to lower side of wall
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Player(Sprite): #creates class Player
    def __init__(self, game, x, y, sheet, controls): #method that initializes Sprite, only runs once
        self.groups = game.all_sprites, game.all_players #gets all of the sprite images
        Sprite.__init__(self, self.groups) #initializes Sprite
        self.game = game
        self.controls = controls
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, sheet))
        self.load_images()
        self.image = self.frames_r[0] #first frame for right direction
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT.copy() #copying hitbox for 2nd player
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.pos = vec(x*TILESIZE,y*TILESIZE)
        self.hit_rect.center = (self.pos.x, self.pos.y)
        self.rect.centerx = self.hit_rect.centerx
        self.rect.bottom = self.hit_rect.bottom + PLAYER_FEET_GAP
        self.jumping = False
        self.jump_time = 0
        self.facing_left = False
        self.ball_anchor = BALL_ANCHORS[0]
        self.last_update = 0
        self.current_frame = 0
        self.coins = 0
        self.cofric = -0.1
    def load_images(self): #gets all frames to animate from for sprite
        self.frames_r = [self.spritesheet.get_image(0, 0, 50, 150), #idle
                         self.spritesheet.get_image(50, 0, 50, 150), #run 1
                         self.spritesheet.get_image(100, 0, 50, 150), #run 2
                         self.spritesheet.get_image(150, 0, 50, 150), #run 3
                         self.spritesheet.get_image(200, 0, 50, 150), #run 4
                         self.spritesheet.get_image(250, 0, 50, 150), #jump: takeoff
                         self.spritesheet.get_image(300, 0, 50, 150), #jump: rising
                         self.spritesheet.get_image(350, 0, 50, 150)] #jump: falling
        self.frames_l = [pg.transform.flip(self.frames_r[0], True, False), #mirrored copies for facing left
                         pg.transform.flip(self.frames_r[1], True, False),
                         pg.transform.flip(self.frames_r[2], True, False),
                         pg.transform.flip(self.frames_r[3], True, False),
                         pg.transform.flip(self.frames_r[4], True, False),
                         pg.transform.flip(self.frames_r[5], True, False),
                         pg.transform.flip(self.frames_r[6], True, False),
                         pg.transform.flip(self.frames_r[7], True, False)]
    def get_keys(self): #gets input to move Player
        # self.vel = vec(0,0)
        keys = pg.key.get_pressed()
        if keys[self.controls["left"]]: #checks if left direction key is pressed for either player
            self.acc.x = -PLAYER_ACC #makes player_speed negative on the x axis
            self.facing_left = True
        if keys[self.controls["right"]]: #checks if right direction key is pressed for either player
            self.acc.x = PLAYER_ACC #makes player_speed positive on x_axis
            self.facing_left = False
        if keys[self.controls["jump"]]: #checks if jump key is pressed for either player (up arrow/w key)
            self.jump()
    def on_ground(self): #checks if player is on the ground for jumping
        self.hit_rect.y += 2 #goes down 2 pixels
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False, collide_hit_rect) #checks if there's collision
        self.hit_rect.y -= 2 #goes back up
        return bool(hits) #returns True/False for collision to determine if player is on ground or not
    def jump(self):
        if self.on_ground() and not self.jumping:
            self.jumping = True
            self.jump_time = pg.time.get_ticks() #starts tracking jump time
            self.vel.y = -PLAYER_JUMP #y velocity goes up
    def is_jumping(self):
        if self.vel.y > 0 and self.on_ground(): 
            self.jumping = False #if going back down, Player is not jumping --> jumping = False
    def shoot(self):
        if self.game.ball.owner is self: #if you're shooting, it will check if you have the ball or not
            self.game.ball.shoot() #shoots ball
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 100: #checks if time between last update is greater than 350 ms
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % 4 #updates to next frame then when at last frame for correct player modulus remainder will set it back to 0
        if not self.on_ground(): #if not on the ground
            if self.jumping and now - self.jump_time < 100: #if jumping and time ellapsed is less than 100 ms
                frame = 5
            elif self.vel.y < 0: #if going back down
                frame = 6
            else:
                frame = 7
        elif abs(self.vel.x) > 1: #if on the ground and moving
            frame = 1 + self.current_frame
        else:
            frame = 0
        if self.facing_left: #check if facing left
            frames = self.frames_l
        else:
            frames = self.frames_r
        self.image = frames[frame] #setting new frame
        bx, by = BALL_ANCHORS[frame]
        if self.facing_left:
            self.ball_anchor = (49 - bx, by) #moves ball on the other side (moving across x axis)
        else:
            self.ball_anchor = (bx, by) #sets ball_anchor to the appropriate position based on the player's frame
    def update(self):
        self.animate()
        self.is_jumping()
        self.acc = vec(0,PLAYER_GRAV)
        self.get_keys() #waits for input from games
        self.acc.x += self.vel.x * PLAYER_FRIC
        self.acc.y += self.vel.y * PLAYER_FRIC
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        if abs(self.vel.y) < 0.1:
            self.vel.y = 0
        self.pos += self.vel + 0.5 * self.acc
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')
        self.hit_rect.centery = self.pos.y
        if collide_with_walls(self, self.game.all_walls, 'y'):
            self.jumping = False
        self.rect.centerx = self.hit_rect.centerx
        self.rect.bottom = self.hit_rect.bottom + PLAYER_FEET_GAP #moves player down 5 pixels

class Ball(Sprite):
    def __init__(self, game, owner):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)  
        self.game = game
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "ball.png"))
        self.image = self.spritesheet.get_image(0, 0, 13, 13)
        self.rect = self.image.get_rect()
        self.pos = vec(0,0)
        self.vel = vec(0,0) 
        self.owner = owner
        self.release_time = 0
        self.follow_owner()
    def follow_owner(self): #ball stays attached to player
        bx, by = self.owner.ball_anchor
        self.rect.center = (self.owner.rect.left + bx, self.owner.rect.top + by)
        self.pos = vec(self.rect.center)
    def shoot(self):
        if self.owner.facing_left:
            direction = -1
        else:
            direction = 1
        self.vel = vec(direction * BALL_SHOT[0], BALL_SHOT[1])
        self.owner = None
        self.release_time = pg.time.get_ticks()
    def update(self):
        if self.owner: #if it's anchored
            self.follow_owner()
            return
        self.vel.y = min(self.vel.y + BALL_GRAV, BALL_MAX_SPEED)
        self.vel.x *= 0.99
        self.pos.x += self.vel.x
        self.rect.centerx = self.pos.x
        hit = pg.sprite.spritecollideany(self, self.game.all_walls)
        if hit:
            if self.vel.x > 0:
                self.rect.right = hit.rect.left
            else:
                self.rect.left = hit.rect.right
            self.pos.x = self.rect.centerx
            self.vel.x *= -BALL_BOUNCE
        self.pos.y += self.vel.y
        self.rect.centery = self.pos.y
        hit = pg.sprite.spritecollideany(self, self.game.all_walls)
        if hit:
            if self.vel.y > 0:
                self.rect.bottom = hit.rect.top
            else:
                self.rect.top = hit.rect.bottom
            self.pos.y = self.rect.centery
            self.vel.y *= -BALL_BOUNCE
            if abs(self.vel.y) < 6: #if y velocity is too small to bounce, it will stop bouncing
                self.vel.y = 0
                self.vel.x *= 0.8
        if pg.time.get_ticks() - self.release_time > BALL_PICKUP_DELAY: #player can pick up loose ball if pickup delay has passed
            for player in self.game.all_players:
                if player.rect.inflate(-14, 0).colliderect(self.rect):
                    self.owner = player
                    self.vel = vec(0,0)
                    break

class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y

class Particle(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_particles
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE/8, TILESIZE/8))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.vel = vec(randint(-180,180), randint(-180,180)) #sets velocity to any random direction
        self.pos = vec(x,y) #position is the current (x,y) coordinate
        self.speed = 5 #sets speed
        self.countdown = Cooldown()
        self.countdown.event_time = floor(pg.time.get_ticks()/1000)
    def update(self):
        self.countdown.ticking()
        self.pos += self.vel * self.speed * self.game.dt
        if self.countdown.delta > 1:
            self.kill()
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

class Hoop(Sprite):
    def __init__(self, game, x, y): #method that initializes Sprite, only runs once
        self.groups = game.all_sprites, game.all_hoops #gets all of the sprite images
        Sprite.__init__(self, self.groups) #initializes Sprite
        self.game = game
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "hoop_spritesheet.png")) #loads image for Hoop
        self.image = self.spritesheet.get_image(0, 0, 200, 600)
        self.image = pg.transform.scale(self.image, (100, 300)) #scales the image, so it will fit in the game window
        if x >= len(game.map.data[0]) / 2: #checks if hoop will be placed on the right side, so it can mirror the hoop
            self.image = pg.transform.flip(self.image, True, False) #flips image across the vertical axis
        self.rect = self.image.get_rect() #creates the rectangle based on the size of the final image
        self.pos = vec(x*TILESIZE, y*TILESIZE)
        self.rect.midbottom = (x*TILESIZE + TILESIZE/2, y*TILESIZE) #places hoop on top of "H" tile in level1.txt