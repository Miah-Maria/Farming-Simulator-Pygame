import pygame
import sys
from pygame.locals import *

SCREEN_WIDTH = 1920  # sets screen width
SCREEN_HEIGHT = 1080  # sets screen height

TILE_SIZE = 64 #Sets the tile size for all tiles in the game
RENDER_DISTANCE = 13*TILE_SIZE #sets the render distance as 13 tiles in each direction
#holds the game map size of the full map

class Text:
    def __init__(self, font, size, text, antialias, colour, background, loc,type):
        self.font = font #font of the text
        self.type = type
        self.size = size #size of the text
        self.text = text #what is said
        self.antialias = antialias 
        self.colour = colour #colour of the text
        self.background = background #is there a background
        texts = pygame.font.SysFont(self.font, self.size) #makes the text
        self.text = texts.render(self.text, self.antialias, self.colour, self.background) #render the text
        self.loc = loc #location of the text
        
        self.shop_size = 36-2*(len(text))
        shop_texts = pygame.font.SysFont(self.font, self.shop_size)
        self.shop_text = shop_texts.render(text, self.antialias, self.colour, self.background)
        
    def update(self,text):
        self.text = text
        self.size = 48-2*(len(text))
        self.shop_size = 36-2*(len(text))
        texts = pygame.font.SysFont(self.font, self.size) #makes the text
        shop_texts = pygame.font.SysFont(self.font, self.shop_size) 
        self.text = texts.render(self.text+'g', self.antialias, self.colour, self.background) #render the text
        self.shop_text = shop_texts.render(text+'g', self.antialias, self.colour, self.background)
        
        
       

class Player:
    TILE_SIZE = 64
    def __init__(self, size, loc, item):                
        self.size = size #sets the size of the player
        self.loc = loc #sets the starting location of the player
        self.player_movement = {'RIGHT':False, 'LEFT': False, 'UP':False, 'DOWN':False} #the dictionary that is used when the player is moving
        self.speed = 10 #sets the speed that the player walks across the screen
        self.idle = {'UP':(pygame.image.load('game/character/idle/up1.png'),
                                pygame.image.load('game/character/idle/up2.png')),
                     'DOWN':(pygame.image.load('game/character/idle/down1.png'),
                                pygame.image.load('game/character/idle/down2.png')),
                     'RIGHT':(pygame.image.load('game/character/idle/right1.png'),
                                pygame.image.load('game/character/idle/right2.png')),
                     'LEFT':(pygame.image.load('game/character/idle/left1.png'), #holds and loads all the idle images for animation
                                pygame.image.load('game/character/idle/left2.png'))}
        self.move = {'UP':(pygame.image.load('game/character/move/up1.png'),
                                pygame.image.load('game/character/move/up2.png')),
                     'DOWN':(pygame.image.load('game/character/move/down1.png'),
                                pygame.image.load('game/character/move/down2.png')),
                     'RIGHT':(pygame.image.load('game/character/move/right1.png'),
                                pygame.image.load('game/character/move/right2.png')),
                     'LEFT':(pygame.image.load('game/character/move/left1.png'),
                                pygame.image.load('game/character/move/left2.png'))} #holds and loads all the moving images for animation

        self.current_1 = self.idle['DOWN'][0] #holds the first current image
        self.current_2 = self.idle['DOWN'][1] #holds the second current image
        self.image = pygame.transform.smoothscale(self.current_1, self.size) #transforms the image to the correct size
        self.item = item #the item the player is currently using
        self.possible_loc = [self.loc[0],self.loc[1]+TILE_SIZE]
        self.rect = pygame.Rect(self.loc, (self.size)) #creates a rect of the player so the camera can know its centre
        self.direction = 'DOWN'
        self.image_loc = self.loc
        self.water_bucket = 20

    def update(self, frame):
        if self.player_movement['RIGHT']: #if the player is pressing right control
            self.loc[0] += self.speed
            self.direction = 'RIGHT'
        elif self.player_movement['LEFT']: #if the player is pressing left control
            self.loc[0] -= self.speed
            self.direction = 'LEFT'
        elif self.player_movement['UP']: #if the player is pressing up control
            self.loc[1] -= self.speed
            self.direction = 'UP' 
        elif self.player_movement['DOWN']: #if the player is pressing down control
            self.loc[1] += self.speed
            self.direction = 'DOWN'  

        if frame < 12:  # checks that the frame counter is less than 12
            self.image = pygame.transform.smoothscale(
                self.current_1,
                self.size)  # sets image to correct current image
        elif frame > 12:  # checks that the frame counter is more than 12
            self.image = pygame.transform.smoothscale(
                self.current_2,
                self.size)  # sets image to correct current image

        if self.loc[0] < -50: #if the player is too far left
            self.loc[0] += self.speed #cancels any further movement
        elif self.loc[0] > 1925: #if the player is too far right
            self.loc[0] -= self.speed #cancels any further movement
        elif self.loc[1] < -50: #if the player is too far up
            self.loc[1] += self.speed #cancels any further movement
        elif self.loc[1] > 1925: #if the player is too far down
            self.loc[1] -= self.speed #cancels any further movement
        
        self.rect = pygame.Rect(self.loc, (self.size)) #updates the rect to the new location
        self.image_loc = self.loc

            
    def begin_move(self,move): #called when buttons are being pressed
        self.player_movement[move]= True #sets that value to true
        self.current_1 = self.move[move][0] #changes current image to correct direction image
        self.current_2 = self.move[move][1] #changes current image to correct direction image

        
    def end_move(self,move):  #called when buttons aren't being pressed
        if self.player_movement[move]:
            self.player_movement[move]= False #sets that value to false 
            self.current_1 = self.idle[move][0] #changes current image to correct direction image
            self.current_2 = self.idle[move][1] #changes current image to correct direction image
         
    def possible_move(self):
        self.possible_loc = self.loc.copy() 
        if self.direction == 'RIGHT':
            self.possible_loc[0] = self.loc[0] + 64 #location a tile to the right of the player
        if self.direction == 'LEFT':
            self.possible_loc[0] = self.loc[0] - 64 #location a tile to the left of the player
        if self.direction == 'DOWN':
            self.possible_loc[1] = self.loc[1] + 64 #location a tile below the player
        if self.direction == 'UP': 
            self.possible_loc[1] = self.loc[1] - 64 #location a tile above the player

        return self.possible_loc

    def retract_move(self,direction):
        if self.direction == 'RIGHT':
            self.loc[0] -= self.speed
        if self.direction == 'LEFT':
            self.loc[0] += self.speed
        if self.direction == 'DOWN':
            self.loc[1] -= self.speed
        if self.direction == 'UP':
            self.loc[1] += self.speed

    def update_water(self, fill):
        if fill: #if the player is refilling their bucket
            self.water_bucket = 20 #set the value to the max
        else:
            self.water_bucket -= 1 #decrese the value

    def animation_image(self, animation):
        self.image = pygame.transform.smoothscale(animation,(192,192)) #sets the image to the correct animation image
        self.image_loc = self.loc[0]-64,self.loc[1]-64 #sets the location of the image to the correct centre location
        


class Camera:
    def __init__(self, pos: tuple[int, int]):
        self.rect = pygame.Rect(pos, (TILE_SIZE*12, TILE_SIZE*8)) #creates the rect of how many tiles and how wide the camera should be
    def update(self, player: Player):
        self.rect.center = player.rect.center #centres the camera to the player's centre
        self.rect = self.rect.clamp((0,0),(1920, 1920)) #clamps the rect location of the camera to not go out the bounds of (0,0) and the game map size
        
    def to_camera_view(self, other_pos: tuple[int, int]) -> tuple[int, int]:
        return (other_pos[0] - self.rect.x, other_pos[1] - self.rect.y) #returns the location of the tile in relation to the camera's viewpoint


class Tile:
    def __init__(self, location: tuple[int, int], autumn_image: pygame.Surface, tile: int, spring_image: pygame.Surface):
        self.loc = location #stores the location of the tile on the map
        self.autumn_image = pygame.transform.smoothscale(autumn_image, (TILE_SIZE, TILE_SIZE)) #stores the image of the tile
        self.spring_image = pygame.transform.smoothscale(spring_image, (TILE_SIZE, TILE_SIZE)) #stores the image of the tile
        self.tile = tile
        self.size = (64,64)
        self.crop = None
        self.watered = False
        self.image = self.autumn_image
        
    def check_collide(self,pos):
        point = pygame.Rect(self.loc[0],self.loc[1], self.size[0],self.size[1]) #creates a rect where the tile is located to test for any collisions
        if point.collidepoint(pos):  #checsk if the mouse position is within the created rect of the button
            return True
        else:
            return False
        
    def update_values(self, tile, image): 
        self.tile = tile #update tile type
        self.image = image #update tile image

    def change_season(self,season):
        if season == 'autumn': #if the season is currently autumn
            self.image = self.autumn_image #set the image to the autemn tile image
        elif season == 'spring':
            self.image = self.spring_image #set the image to the spring tile image
        
        

class Button:
    def __init__(self,loc,button,size):
        self.loc = loc #location of the button
        self.button = button #type of button
        self.size = size #size of the button
        self.unclicked = pygame.image.load('game/button/%s_unpressed.png' % button) #image of button when not hovered over
        self.clicked = pygame.image.load('game/button/%s_pressed.png' % button) #imag eof button when hovered over
        self.image = pygame.transform.smoothscale(self.unclicked,self.size) #image of the button currently

    def click(self,mouse_pos):
        point = pygame.Rect(self.loc[0],self.loc[1], self.size[0],self.size[1]) #creates a rect where the tile is located to test for any collisions
        if point.collidepoint(mouse_pos):  #checsk if the mouse position is within the created rect of the button
            return True
        else:
            return False
        
    def hover(self,mouse_pos):
        point = pygame.Rect(self.loc[0], self.loc[1], self.size[0],self.size[1]) #creates a rect where the tile is located to test for any collisions
        if point.collidepoint(mouse_pos):  #checsk if the mouse position is within the created rect of the button
            self.image = pygame.transform.smoothscale(self.clicked,self.size) #changed image
        else:
            self.image = pygame.transform.smoothscale(self.unclicked,self.size)#changed image

            
            
class Hotbar:
    def __init__(self, loc: tuple,number: int, item: str, amount: int, CONTROLS: dict, hotbar: str, selected: bool):
        self.loc = [loc[0]+(64*number),loc[1]] #location
        self.item = item #held item
        self.size = (64, 64) #size
        self.item_image = pygame.transform.smoothscale(
            pygame.image.load('game/item/%s.png' % self.item), self.size) #item image
        self.value = amount #amount of the item
        self.image = pygame.transform.smoothscale(
            pygame.image.load('game/hotbar_base_image.png'), self.size) #slot image
        self.hotbar = hotbar #hotbar allocation
        self.key = CONTROLS[hotbar] #assigned key
        self.selected = selected #is it selected
        self.stored_loc = loc #stored loc
        self.clicked = False #is it clicked
        self.number = number #what slot number is it
        
    def in_inventory(self):
        self.size = (48,48) #changed size
        self.item_image = pygame.transform.smoothscale(
            pygame.image.load('game/item/%s.png' % self.item), self.size) #remade item image
        self.image = pygame.transform.smoothscale(
            pygame.image.load('game/hotbar_base_image.png'), self.size) #remade slot image
        self.loc = [self.stored_loc[0]+(48*self.number)+144,120] #remade loc

    def not_in_inventory(self):
        self.size = (64,64) #changed size
        self.item_image = pygame.transform.smoothscale(
            pygame.image.load('game/item/%s.png' % self.item), self.size) #remade item image
        self.image = pygame.transform.smoothscale(
            pygame.image.load('game/hotbar_base_image.png'), self.size) #remade slot image
        self.loc = [self.stored_loc[0]+(64*self.number),448] #remade loc
        
    def is_clicked(self,mouse_pos):
        point = pygame.Rect(self.loc[0],self.loc[1],self.size[0],self.size[1]) #create point to check for collision
        if point.collidepoint(mouse_pos):
            return True #returns true if clicked on slot
        else:
            return False #return false if not clicked on slot

    def in_bin(self):
        self.size = (48,48) #changed size
        self.item_image = pygame.transform.smoothscale(
            pygame.image.load('game/item/%s.png' % self.item), self.size) #remade item image
        self.image = pygame.transform.smoothscale(
            pygame.image.load('game/hotbar_base_image.png'), self.size) #remade slot image
        self.loc = [self.stored_loc[0]+(48*self.number)+80,184] #remade loc        

    def update(self, value):
        self.value = value
        if self.value == 0:
            self.item = 'empty'
            self.item_image = pygame.transform.smoothscale(
                pygame.image.load('game/item/%s.png' % self.item), self.size)

    def update_water(self,item):
        self.item = item
        self.item_image = pygame.transform.smoothscale(pygame.image.load('game/item/%s.png' % self.item), self.size)

        
    
class Inventory:
    def __init__(self, loc, item, amount):
        self.loc = loc #location
        self.stored_loc = loc
        self.item = item #item at the slot
        self.size = (48, 48) #size
        self.item_image = pygame.transform.smoothscale(
            pygame.image.load('game/item/%s.png' % self.item), self.size) #item image
        self.value = amount #amount of the item
        self.image = pygame.transform.smoothscale(
            pygame.image.load('game/hotbar_base_image.png'), self.size) #slot image
        self.clicked = False #is it clicked

    def is_clicked(self,mouse_pos):
        point = pygame.Rect(self.loc[0],self.loc[1],self.size[0],self.size[1]) #create point to check for collision
        if point.collidepoint(mouse_pos):
            return True #returns true if clicked on slot
        else:
            return False #return false if not clicked on slot
        
    def update(self, value):
        self.value = value
        if self.value == 0:
            self.item = 'empty'
            self.item_image = pygame.transform.smoothscale(
                pygame.image.load('game/item/%s.png' % self.item), self.size)

    def not_in_bin(self):
        self.size = (48,48) #changed size
        self.item_image = pygame.transform.smoothscale(
            pygame.image.load('game/item/%s.png' % self.item), self.size) #remade item image
        self.image = pygame.transform.smoothscale(
            pygame.image.load('game/hotbar_base_image.png'), self.size) #remade slot image
        self.loc = self.stored_loc #remade loc

    def in_bin(self):
        self.size = (48,48) #changed size
        self.item_image = pygame.transform.smoothscale(
            pygame.image.load('game/item/%s.png' % self.item), self.size) #remade item image
        self.image = pygame.transform.smoothscale(
            pygame.image.load('game/hotbar_base_image.png'), self.size) #remade slot image
        self.loc = [self.stored_loc[0]-64,self.stored_loc[1]+32] #remade loc  

class Structure:
    def __init__(self,loc,type,size):
        self.type = type
        self.loc = loc
        self.size = size
        self.image = pygame.transform.scale(pygame.image.load('game/structure/%s.png'%self.type),self.size)


class Crop:
    def __init__(self,loc,crop,date):
        self.loc = loc #location of the crop
        self.crop = crop #type of crop
        self.size = (64, 64) #size of the crop
        self.growth = 0 #growth stage 
        self.growth_speed = 6 #growth speed
        self.date = date
        self.image_sheet = pygame.image.load('game/crop/%s.png'%self.crop) #crop spritesheet
        self.dead_sheet = pygame.image.load('game/crop/dead_%s.png'%self.crop)
        self.animation_image = [] #animation list
        self.dead_animation = []
        for y in range(3):
            for x in range(2):
                self.animation_image.append(pygame.transform.smoothscale(self.image_sheet.subsurface((x*128,y*128),(128,128)),(64,64))) #loaded animation
                self.dead_animation.append(pygame.transform.smoothscale(self.dead_sheet.subsurface((x*128,y*128),(128,128)),(64,64)))
        self.image = self.animation_image[0] #crop image
        self.item = crop[:-5] #crop
        self.alive = True


    def update(self,date, watered):
        if date and watered and self.alive and self.image != self.animation_image[5]:
            self.growth += 1 #increment the crop growth by 1
            self.image = self.animation_image[self.growth] #change the image to the correct growth image

                    
    def check_collide(self,pos):
        point = pygame.Rect(self.loc[0],self.loc[1], self.size[0],self.size[1]) #creates a rect where the tile is located to test for any collisions
        if point.collidepoint(pos):  #checsk if the mouse position is within the created rect of the button
            return True
        else:
            return False

    def season_change(self):
        self.alive = False #state the crop should no longer be alive
        self.image = pygame.transform.smoothscale(self.dead_animation[self.growth],(64,64)) #change the image of the crop to the correct dead image
