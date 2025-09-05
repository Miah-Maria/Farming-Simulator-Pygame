import pygame
import sys
from pygame.locals import *
pygame.init()
from classes import Structure, Text, Player, Camera, Tile, Button, Hotbar, Inventory, Crop
from house import House
SCREEN_WIDTH = 1920  # sets screen width
SCREEN_HEIGHT = 1080  # sets screen height

TILE_SIZE = 64 #Sets the tile size for all tiles in the game
RENDER_DISTANCE = 13*TILE_SIZE #sets the render distance as 13 tiles in each direction
GAME_MAP_SIZE = (50*TILE_SIZE, 30*TILE_SIZE) #holds the game map size of the full map


        
def load_map():
    global GAME_MAP_SIZE
    import json

    autumn_sprite_sheet = pygame.image.load("game/data/spritesheet/autumn_tile_types.png") #holds the image of all the tiles
    spring_sprite_sheet = pygame.image.load("game/data/spritesheet/spring_tile_types.png")

    tiles = [] #create empty tiles list where the tiles will be stored

    with open("game/data/map.ldtk", "r") as f: #opens the LDtk file
        map_data: dict = json.load(f) #name the file map_data
    tile_info: list[dict] = map_data["levels"][0]["layerInstances"][0] #access the tile_info within the dictionaries within the LDtk file
    grid_size: int = tile_info["__gridSize"] #get the grid size from the tile info dictionary
    spring_tiles_loaded : dict[int, pygame.Surface] = {} #empty list of all the tiles loaded
    autumn_tiles_loaded: dict[int, pygame.Surface] = {} #empty list of all the tiles loaded
    GAME_MAP_SIZE = tile_info["__cWid"]*TILE_SIZE, tile_info["__cWid"]*TILE_SIZE #set GAME_MAP_SIZE to equal the size of the map
    
    for tile in tile_info["gridTiles"]: #go through each tile within the game_map
        position = tile["px"] #set the position to equal the value under the key 'px'
        position = (position[0]/grid_size*TILE_SIZE, position[1]/grid_size*TILE_SIZE) #position on the screen is this value scaled by grid/tile size 
        autumn_image = autumn_tiles_loaded.get(tile["t"]) #set the image to equal the value under the key 't' in the tiles loaded list
        spring_image = spring_tiles_loaded.get(tile["t"]) #set the image to equal the value under the key 't' in the tiles loaded list        
        type_of_tile = tile["t"]
        if autumn_image is None: #if there is no image here
            source = tile["src"] #get the source of the image within the tilesheet
            autumn_image = autumn_sprite_sheet.subsurface(source, (grid_size, grid_size)) #get that specific tile image within the whole image
            autumn_tiles_loaded[tile["t"]] = autumn_image #set the value under this key equal to this image
            
        if spring_image is None:
            source = tile["src"] #get the source of the image within the tilesheet
            spring_image = spring_sprite_sheet.subsurface(source, (grid_size, grid_size)) #get that specific tile image within the whole image
            spring_tiles_loaded[tile["t"]] = spring_image #set the value under this key equal to this image            
            
        
        tiles.append(Tile(position, autumn_image.copy(), type_of_tile, spring_image.copy())) #add this tile to the tiles list
        
    return tiles, autumn_tiles_loaded, spring_tiles_loaded

def euclid_distance(pos1, pos2):
    return max(abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1])) #gives the distance between the two points given


def create_Hotbar(CONTROLS, HOTBAR, items, value):
    for x, item in enumerate(items):
        HOTBAR.append(Hotbar((96, 448),x, item, value[item], CONTROLS, 'Hotbar_'+str(x+1), False))
    return HOTBAR

def create_Inventory(INVENTORY, inventory_items, value):
    for y, item in enumerate(inventory_items):
        for x, slot in enumerate(item):
            INVENTORY.append(Inventory((96+(48*x)+144, 240+(48*y)), slot, value[slot]))
    return INVENTORY


def load_animation(animation,amount):
    sprite_sheet = pygame.image.load('game/sprite_animation/%s.png'%animation)
    sprite_image = []
    for y in range(amount[1]):
        for x in range(amount[0]):
            sprite_image.append(sprite_sheet.subsurface((x*128,y*128), (128,128)))
    return sprite_image


def play_animation(animation, count, p):
    if count < 6:
        if p.direction == 'UP': #when player faced up
            p.animation_image(animation[2])
        elif p.direction == 'DOWN': #when player faced down
            p.animation_image(animation[0])
        elif p.direction == 'RIGHT': #when player faced right
            p.animation_image(animation[6])
        elif p.direction == 'LEFT': #when player faced left
            p.animation_image(animation[4])
        count += 1
        done = False
        
    elif count < 12:
        if p.direction == 'UP': #when player faced up
            p.animation_image(animation[3])
        elif p.direction == 'DOWN': #when player faced down
            p.animation_image(animation[1])
        elif p.direction == 'RIGHT': #when player faced right
            p.animation_image(animation[7])
        elif p.direction == 'LEFT': #when player faced left
            p.animation_image(animation[5])
        count += 1
        done = False

    else:
        count = 0
        done = True
    return count, done 
    
    
def game(fullscreen, monitor_size, SCREEN, DISPLAY, clock, CONTROLS,farm_name):
    running = True #states whether the program should be running
    HOTBAR = [] #empty hotbar list
    INVENTORY = [] #empty inventory list
    sprite_sheet = pygame.image.load("game/data/spritesheet/autumn_tile_types.png") #holds the image of all the tile    
    hotbar_items = ['filled_water_bucket', 'hoe', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty'] #list of all the hotbar items
    value = {'hoe': 1, 'water_bucket': 1, 'filled_water_bucket': 1, 'strawberry_seed': 5,'empty': 0} #dictionary of how many of each item the user has
    inventory_items = [['empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty'],
                       ['empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty'],
                       ['empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty']] #list of all the inventory items

    HOTBAR = create_Hotbar(CONTROLS, HOTBAR, hotbar_items, value) #runs the create_hotbar function that creates all the hotbar slots
    INVENTORY = create_Inventory(INVENTORY, inventory_items, value) #runs the create_inventory function that creates all the inventory slots
    p = Player((64, 64), [50, 200], 'empty') #create the instance of the player and passes in its location, size and current item
    inventory_button = Button((688,16),'exit',(64,64)) #create the exit button in the inventory
    shipping_bin_exit_button = Button((688,16),'exit',(64,64)) #create the exit button in the inventory
    
    AUTUMN_SHOP_BUTTONS = [Button((688,16),'exit',(64,64)),
               Button((304,208),'pumpkin_seed',(256,64)),
               Button((304,288),'wheat_seed',(256,64)),
               Button((304,368),'corn_seed',(256,64))]
    SHOP_BUTTONS = AUTUMN_SHOP_BUTTONS
    
    SPRING_SHOP_BUTTONS = [Button((688,16),'exit',(64,64)),
               Button((304,208),'beetroot_seed',(256,64)),
               Button((304,288),'strawberry_seed',(256,64)),
               Button((304,368),'carrot_seed',(256,64))]
    
    BIN_BUTTONS = [Button((688,16),'exit',(64,64)),
               Button((368,80),'cancel',(64,64)),
               Button((538,80),'confirm',(64,64))]

    frame = 0 #sets the frame variable to 0
    
    selected = pygame.transform.smoothscale(pygame.image.load('game/hotbar_select.png'), (64, 64)) #loads and transforms the image for select in inventory
    inventory_opened = False #states whether the inventory is currently open
    shop_opened = False
    shipping_bin_opened = False
    autumn_shop_base = pygame.image.load('game/shop_base.png')
    spring_shop_base = pygame.image.load('game/spring_shop_base.png')
    shipping_bin_base = pygame.image.load('game/shipping_bin_base.png')
    inventory_click = False #states whether the inventory has been clicked
    previous_inventory_click = False #holds the previous inventory_click state
    
    held_item = 'empty' #holds the currently held item
    bin_item = 'empty'
    bin_value = 0
    bin_base = pygame.transform.smoothscale(pygame.image.load('game/bin_base.png'), (80,80))
    
    
    TILES, autumn_tiles_loaded, spring_tiles_loaded = load_map() #runs the load map function to create all the tiles of the mpa
    CAMERA = Camera((0, 0)) #create the camera instance at the position 0,0
    STRUCTURES = []
    STRUCTURES.append(Structure((768,64),'house',(384,384)))
    STRUCTURES.append(Structure((1280,288),'shipping_bin',(128,96)))
    STRUCTURES.append(Structure((384,160),'shop',(192,256)))

    animation_base = pygame.transform.smoothscale(pygame.image.load('game/animation_base.png'),(128,128)) #animation base image
    inventory_animation = load_animation('inventory',[3,4]) #loads all the animation images
    shop_animation = load_animation('shop', [2,3])
    bin_animation = load_animation('bin',[1,2])
    watering = load_animation('filled_water_bucket', [2,4])
    empty_watering = load_animation('water_bucket', [2,4])
    tilling = load_animation('hoe', [2,4])
    
    idle = True
    angry = False
    happy = False
    occured = 0
    animation_occured = 0 #how many times an animation has occured
    animation_frame = 0 #what animation the sprite should be at
    animation_count = 0
    animation = False
    
    SEEDS = ['pumpkin_seed','corn_seed','wheat_seed']
    allowed_crops = ['pumpkin_seed','corn_seed','wheat_seed']
    CROPS = []
    tools = ['water_bucket', 'filled_water_bucket', 'hoe']

    season = 'autumn'    
    money = 1000 #the amount of money the character has
    cost = {'pumpkin_seed': 100,'wheat_seed': 50, 'corn_seed': 75,'strawberry_seed': 100,'beetroot_seed': 50, 'carrot_seed': 75}
    sell_cost = {'pumpkin_seed': 100,'wheat_seed': 50, 'corn_seed': 75,'pumpkin': 150,'wheat': 100, 'corn': 125,
                 'strawberry_seed': 100,'beetroot_seed': 50, 'carrot_seed': 75,'strawberry': 150,'beetroot': 100, 'carrot': 125}
    TEXT = []
    TEXT.append(Text('rolam', 48-2*(len(farm_name)), farm_name, True, (170,139,102), None, (64,288),'farm_name')) #farm name text
    money_text = Text('rolam', 48-2*(len(str(money))),str(money)+ 'g', True, (170,139,102), None, (64,336), 'money')#money text
    TEXT.append(money_text)
    coin = pygame.transform.smoothscale(pygame.image.load('game/coin.png'),(32,32)) #draws the coin
    date = 1
    UI_base = pygame.transform.smoothscale(pygame.image.load('game/UI_base.png'),(128,128))
    inventory_items = []
    day_moved_to_next = False
    season_change = False
    
    for slot in INVENTORY:
        inventory_items.append(slot.item) #adds all the inventory items to a list
        slot.update(value[slot.item])

    while running:
        mouse_pos = pygame.mouse.get_pos() #get the mouse position
        possible_move = p.possible_move()
        for event in pygame.event.get():  #if event is...
            if event.type == pygame.QUIT:  #checks if user is closing the window
                pygame.quit() #close the window
                sys.exit()
                
            if event.type == MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[2]: #when the player has right clicked
                    if (p.loc[0] >= 340 and p.loc[0] <= 560) and p.loc[1] == 370 and p.direction == 'UP': #when the player is next to the shop
                        shop_opened = not shop_opened
                    elif (p.loc[0] >= 950 and p.loc[0] <= 980 ) and p.loc[1] == 330 and p.direction == 'UP': #when the player is next to the house
                        date,day_moved_to_next,season, season_change = House(SCREEN, DISPLAY, farm_name, CONTROLS, money,
                              HOTBAR, INVENTORY, inventory_animation, selected,
                              inventory_button, p, value, clock, held_item, animation_base, TEXT,coin, date, UI_base, season)
                        p.loc = [960,330]
                        p.speed = 10
                    elif (p.loc[0] >= 1240 and p.loc[0] <= 1370) and p.loc[1] == 330 and p.direction == 'UP': #when the player is next to the shipping bin
                        shipping_bin_opened = True
                    
                        
                    else:
                        inventory_opened = not inventory_opened #the inventory is toggled

                if pygame.mouse.get_pressed()[0]: #when the player has left clicked
                    for item in HOTBAR:# loops through all the hotbar slots
                        if item.is_clicked(mouse_pos) and not inventory_opened and not shop_opened: #checks if mouse clicked hotbar button
                            for slot in HOTBAR: #loops through the hotbar
                                if slot.is_clicked(mouse_pos):#checks if mouse clicked hotbar button
                                    slot.selected = True #sets the slot as selected
                                    p.item = slot.item #sets player item to be this item
                                else:
                                    slot.selected = False #slot is not selected
                                    
                    if inventory_opened:     
                        if inventory_button.click(mouse_pos): #if the button has been clicked on
                            inventory_opened = not inventory_opened #the inventory is closed
                            
                    if shop_opened: #when the shop is opened
                        
                        for button in SHOP_BUTTONS:
                            if button.click(mouse_pos): #check if any of the buttons have been clicked
                                
                                if button.button == 'exit': #if its the exit button
                                    shop_opened = not shop_opened #close out of the shop screen
                                else:
                                    temp_money = money - cost[button.button] #temporary money is what the money would be if the transaction is succesful
                                    if temp_money >= 0: #if temp money is bigger or equal to zero
                                        angry = False 
                                        idle = False
                                        happy = True #set animation to happy
                                        money = money - cost[button.button] #decrease money by value of the seed
                                        money_text.update(str(money))
                                        if button.button in hotbar_items: #check if the crop is already in the hotbar
                                            value[button.button] += 1 #adds one to the amount of the crop they have

                                        elif button.button in inventory_items: #check if the crop is already in the inventory
                                            value[button.button] += 1 #adds one to the amount of the crop they have
                                            
                                        else:
                                            found = False
                                            for slot in HOTBAR:
                                                if not found:
                                                    if slot.item == 'empty': #if the slot is empty
                                                        slot.item = button.button #sets the slot to be the crop
                                                        value.update({button.button: 1 }) #adds the crop to the dictionary and adds 1 to value
                                                        found = True
                                                        
                                            if not found:
                                                for slot in INVENTORY:
                                                    if not found:
                                                        if slot.item == 'empty': #if the slot is empty
                                                            slot.item = button.button #sets the slot to be the crop
                                                            value.update({button.button: 1 }) #adds the crop to the dictionary and adds 1 to value                                        
                                                            found = True
                                    else:
                                        happy = False
                                        idle = False
                                        angry = True #set animation to angry
                                                         
                    if shipping_bin_opened:
                        for button in BIN_BUTTONS:
                            if button.click(mouse_pos): #check if any of the buttons have been clicked
                                if button.button == 'exit': #if its the exit button
                                    shipping_bin_opened = not shipping_bin_opened #close out of the shop screen
                                    
                                elif button.button == 'cancel':
                                    if bin_item in hotbar_items: #check if the crop is already in the hotbar
                                        value[bin_item] += bin_value #adds one to the amount of the crop they have
                                        bin_item = 'empty'
                                        
                                    elif bin_item in inventory_items: #check if the crop is already in the inventory
                                        value[bin_item] += bin_value #adds one to the amount of the crop they have
                                        bin_item = 'empty'
                                    else:
                                        found = False
                                        for slot in HOTBAR:
                                            if not found:
                                                if slot.item == 'empty': #if the slot is empty
                                                    slot.item = bin_item #sets the slot to be the crop
                                                    value.update({bin_item: bin_value }) #adds the crop to the dictionary and adds 1 to value
                                                    found = True
                                                    bin_item = 'empty'
                                                    
                                        if not found:
                                            for slot in INVENTORY:
                                                if not found:
                                                    if slot.item == 'empty': #if the slot is empty
                                                        slot.item = bin_item #sets the slot to be the crop
                                                        value.update({bin_item: bin_value }) #adds the crop to the dictionary and adds 1 to value                                        
                                                        found = True
                                                        bin_item = 'empty'

                                elif button.button == 'confirm':
                                    money += sell_cost[bin_item]*bin_value
                                    money_text.update(str(money))
                                    bin_item = 'empty'
                                    
                                    
                    inventory_click = True #a click has occured
                    
                    if p.item == 'hoe' and not inventory_opened and not shop_opened and not animation: #checks if the player has the hoe selected
                        done = False
                        for tile in TILES:
                            if not done:
                                if (tile.check_collide(
                                    [possible_move[0]+32,possible_move[1]+64])or tile.check_collide(
                                        (p.loc[0]+32,p.loc[1]+64))) and tile.tile == 14: #checks if next to a dirt tile
                                    tile.update_values(0,pygame.transform.smoothscale(autumn_tiles_loaded[0],(TILE_SIZE,TILE_SIZE)))
                                    #changes the tile, image and type
                                    animation = True
                                    animation_type = tilling
                                    done = True
                                    
                                elif (tile.check_collide(
                                    [possible_move[0]+32,possible_move[1]+64])or tile.check_collide(
                                        (p.loc[0]+32,p.loc[1]+64))) and tile.tile == 0: #checks if next to a tilled dirt tile
                                    not_possible = False
                                    for crop in CROPS:
                                        if crop.loc == tile.loc:
                                            not_possible = True
                                        else:
                                            if not not_possible:
                                                not_possible = False

                                    if not not_possible:
                                        tile.update_values(14,pygame.transform.smoothscale(autumn_tiles_loaded[14],(TILE_SIZE,TILE_SIZE)))
                                    animation = True
                                    animation_type = tilling
                                    done = True
                                    #changes the tile, image and type
                                
                    if p.item == 'filled_water_bucket' and not inventory_opened and not animation:  #checks if the player has the filled water bucket selected
                        done = False
                        for tile in TILES:
                            if not done:
                                if (tile.check_collide(
                                    [possible_move[0]+32,possible_move[1]+64])or tile.check_collide(
                                        (p.loc[0]+32,p.loc[1]+64))) and tile.tile == 0: #checks if next to a tilled tile
                                    if p.water_bucket > 0: #if water bucket isnt empty
                                        tile.update_values(
                                            0,pygame.transform.smoothscale(sprite_sheet.subsurface((0,640), (128,128)),(TILE_SIZE,TILE_SIZE)))
                                        tile.watered = True
                                        p.update_water(False) #update water bucket value
                                        if p.water_bucket <= 0: #if the water bucket is empty
                                            for slot in HOTBAR:
                                                if slot.item == p.item:
                                                    slot.update_water('water_bucket') #update the water bucket
                                                    p.item = 'water_bucket'

                                        animation = True #animation is ocuring
                                        animation_type = watering #animation type
                                        done = True     
                                        #changes the tile, image and type

                    if p.item == 'water_bucket' and not inventory_opened and not animation:
                        for tile in TILES:
                            if tile.check_collide(
                                [possible_move[0]+32,possible_move[1]+64]) and  tile.tile in [
                                    15,16,17,18,19,20,21,22,23,24]: #checks if next to a water tile                        
                                p.update_water(True) #fills the water bucket up
                                for slot in HOTBAR:
                                    if slot.item == p.item:
                                        slot.update_water('filled_water_bucket') #updates the water bucket
                                        p.item = 'filled_water_bucket'
                                        
                                        animation = True #animation is occuring
                                        animation_type = empty_watering #animation type
                                        
                    if p.item in allowed_crops and not inventory_opened and not shop_opened and not animation: #checks if the player has a seed selected
                        done = False
                        for tile in TILES:
                            if not done:
                                if (tile.check_collide(
                                    [possible_move[0]+32,possible_move[1]+64])or tile.check_collide((p.loc[0]+32,p.loc[1]+64))) and (
                                    tile.tile == 0 or tile.tile == 25): #check if next to tilled dirt or watered tilled dirt
                                    has_crop = False
                                    for crop in CROPS:
                                        if crop.loc == tile.loc: #if a crop shares a location with the tile
                                            has_crop = True    #this tile already has a crop
                                    if not has_crop: #if the tile doesnt have a crop
                                        CROPS.append(Crop(tile.loc,p.item,date)) #adds the crop to the CROPS variable
                                        for slot in HOTBAR: 
                                            if slot.selected: 
                                                slot.value -= 1 #takes one from the amount of that item the player has
                                                value[p.item] = slot.value #sets the value dictionary equal to this value
                                                if slot.value == 0: #if the value has reached 0
                                                    slot.item = 'empty' 
                                                    p.item = 'empty' #both slot and player items become empty
                                        done = True
                                            
                    if p.item == 'empty' and not inventory_opened and not shop_opened and not animation: #checks if the player has nothing selected
                        done = False
                        for crop in CROPS:
                            if not done:
                                if (crop.check_collide([possible_move[0]+32,possible_move[1]+64]) or crop.check_collide(
                                    (p.loc[0]+32,p.loc[1]+64))):
                                    if crop.alive and crop.image == crop.animation_image[5]:
                                    #checks if next to a crop that is at its final stage of growth
                                        if crop.item in hotbar_items: #check if the crop is already in the hotbar
                                            value[crop.item] += 1 #adds one to the amount of the crop they have
                                            CROPS.remove(crop) #removes the crop from the list so its no longer drawn on the screen
                                            done = True

                                        elif crop.item in inventory_items: #check if the crop is already in the inventory
                                            value[crop.item] += 1 #adds one to the amount of the crop they have
                                            CROPS.remove(crop) #removes the crop from the list so its no longer drawn on the screen
                                            done = True
                                            
                                        else:
                                            found = False
                                            for slot in HOTBAR:
                                                if not found:
                                                    if slot.item == 'empty': #if the slot is empty
                                                        slot.item = crop.item #sets the slot to be the crop
                                                        value.update({crop.item: 1 }) #adds the crop to the dictionary and adds 1 to value
                                                        CROPS.remove(crop) #removes the crop from the list so its no longer drawn on the screen
                                                        if slot.selected: #if the slot is selected
                                                            p.item = slot.item #sets that item to be the player item
                                                        found = True
                                                        done = True

                                            if not found:
                                                for slot in INVENTORY:
                                                    if not found:
                                                        if slot.item == 'empty': #if the slot is empty
                                                            slot.item = crop.item #sets the slot to be the crop
                                                            value.update({crop.item: 1 }) #adds the crop to the dictionary and adds 1 to value
                                                            CROPS.remove(crop) #removes the crop from the list so its no longer drawn on the screen                                           
                                                            found = True
                                                            done = True
                                    elif not crop.alive:
                                        CROPS.remove(crop) #removes the crop from the list so its no longer drawn on the screen
                                    
                                                            
            if event.type == MOUSEBUTTONUP:
                if not pygame.mouse.get_pressed()[0]: 
                    inventory_click = False #a click has no longer occured
                        
                        
            if event.type == KEYDOWN: #checks if a key is pressed down
                if event.key == K_f: #checks if key is f
                    pygame.display.toggle_fullscreen() #fullscreens the screen

                if event.key == K_ESCAPE and not inventory_opened and not shop_opened and not shipping_bin_opened:  # checks if the game screen should be exited out
                    running = False #sets the running variable to false so the while loop is no longer run
                    
                if event.key == CONTROLS['Left']: #checks if key is left control key
                    p.end_move('RIGHT') #ends all the other direction moves
                    p.end_move('UP')
                    p.end_move('DOWN') 
                    p.begin_move('LEFT') #begins left move

                elif event.key == CONTROLS['Right']: #checks if key is right control key
                    p.end_move('LEFT') #ends all the other direction moves
                    p.end_move('DOWN')
                    p.end_move('UP')
                    p.begin_move('RIGHT') #begins right move
                elif event.key == CONTROLS['Down']: #checks if key is down control key
                    p.end_move('LEFT') #ends all the other direction moves
                    p.end_move('RIGHT')
                    p.end_move('UP')
                    p.begin_move('DOWN') #begins down move
                elif event.key == CONTROLS['Forward']: #checks if key is up control key
                    p.end_move('LEFT') #ends all the other direction moves
                    p.end_move('DOWN')
                    p.end_move('RIGHT')
                    p.begin_move('UP') #begins up move
                    
                for item in HOTBAR: # loops through all the hotbar slots
                    if event.key == CONTROLS[item.hotbar]: #checks if the key pressed is a hotbar button
                        for slot in HOTBAR: #loops through the hotbar
                            if event.key == CONTROLS[slot.hotbar]: #checks if the key pressed is a hotbar button
                                slot.selected = True #sets the slot as selected
                                p.item = slot.item #sets player item to be this item
                            else:
                                slot.selected = False #slot is not selected

            if event.type == KEYUP: #when a key is left up
                if event.key == CONTROLS['Left']: #checks if that key is left key
                    p.end_move('LEFT') #ends left move
                elif event.key == CONTROLS['Right']:#checks if that key is right key
                    p.end_move('RIGHT')#ends right move
                elif event.key == CONTROLS['Down']:#checks if that key is down key
                    p.end_move('DOWN') #ends down move
                elif event.key == CONTROLS['Forward']:#checks if that key is up key
                    p.end_move('UP') #ends up move


        frame += 1 #increments the frame variable
        if frame > 24: 
            frame = 0 #resets the frame variable

        if animation:
            animation_count, animation_done = play_animation(animation_type, animation_count, p)
            if animation_done:
                animation = False
            
        if occured > 96:
            occured = 0
            angry = False
            happy = False
            idle = True

        if inventory_opened: #if the inventory is opened
            for slot in HOTBAR:
                slot.in_inventory() #the slots size and location are moved and updated
                
                if not previous_inventory_click and inventory_click:  #if the player has just clicked
                    if held_item == 'empty': #if there is no currently held item
                        if slot.is_clicked(mouse_pos): #if a slot has been clicked
                            if held_item == 'empty': 
                                held_item = slot.item #that item becomes the new held item
                                held_item_img = slot.item_image #and image
                                slot.item = 'empty' #and the slot item is taken away
                                if slot.selected:
                                    p.item = slot.item

                            

                    elif held_item != 'empty' and slot.item == 'empty':
                        if slot.is_clicked(mouse_pos):
                            slot.item = held_item #the held item is placed into this slot
                            slot.item_image = held_item_img #and the image
                            held_item = 'empty' #and held item is turned back to empty state
                        if slot.selected:
                            p.item = slot.item
                            
            if not previous_inventory_click and inventory_click:  #if the player has just clicked
                for slot in INVENTORY:
                    if held_item == 'empty': #if there is no currently held item
                        if slot.is_clicked(mouse_pos): #if a slot has been clicked
                            if held_item == 'empty': 
                                held_item = slot.item #that item becomes the new held item
                                held_item_img = slot.item_image #and image
                                slot.item = 'empty' #and the slot item is taken away

                    elif held_item != 'empty' and slot.item == 'empty':
                        if slot.is_clicked(mouse_pos):
                            slot.item = held_item #the held item is placed into this slot
                            slot.item_image = held_item_img #and the image
                            held_item = 'empty' #and held item is turned back to empty state
                
                            

        if shipping_bin_opened:
            done = False
            for slot in HOTBAR:
                slot.in_bin()
                if not previous_inventory_click and inventory_click:
                    if bin_item == 'empty' and slot.item not in tools: #if there is no currently held item
                        if slot.is_clicked(mouse_pos): #if a slot has been clicked
                            if bin_item == 'empty': 
                                bin_item = slot.item #that item becomes the new held item
                                bin_item_img = slot.item_image #and image
                                bin_value = 1                                
                                slot.update(slot.value-1)
                                value[slot.item] = slot.value
                                if slot.value == 0:
                                    value[slot.item] = slot.value
                                    slot.item == 'empty' #and the slot item is taken away  
                                if slot.selected:
                                    p.item = slot.item
                                done = True
                                    
                    elif bin_item == slot.item:
                        if slot.is_clicked(mouse_pos): #if a slot has been clicked
                            bin_value += 1
                            slot.update(slot.value-1)
                            value[slot.item] = slot.value
                            if slot.value == 0:
                                value[slot.item] = slot.value
                                slot.item == 'empty'
                            if slot.selected:
                                p.item = slot.item
                            done = True

            if not done:   
                for slot in INVENTORY:
                    slot.in_bin()
                    if not previous_inventory_click and inventory_click:
                        if bin_item == 'empty' and slot.item not in tools: #if there is no currently held item
                            if slot.is_clicked(mouse_pos): #if a slot has been clicked
                                if bin_item == 'empty': 
                                    bin_item = slot.item #that item becomes the new held item
                                    bin_item_img = slot.item_image #and image
                                    bin_value = 1                                
                                    slot.update(slot.value-1)
                                    value[slot.item] = slot.value
                                    if slot.value == 0:
                                        value[slot.item] = slot.value
                                        slot.item == 'empty' #and the slot item is taken away
                                        
                        elif bin_item == slot.item:
                            if slot.is_clicked(mouse_pos): #if a slot has been clicked
                                bin_value += 1
                                slot.update(slot.value-1)
                                value[slot.item] = slot.value
                                if slot.value == 0:
                                    value[slot.item] = slot.value
                                    slot.item == 'empty'
                                                 
                            
                            
        elif not inventory_opened:
            for slot in HOTBAR:
                slot.not_in_inventory()
            for slot in INVENTORY:
                slot.not_in_bin()


        if season_change:
            if season == 'autumn': #if the season is autumn
                for tile in TILES:
                    tile.change_season('autumn') #change all the tiles to their autumn variants
                    allowed_crops = ['pumpkin_seed','corn_seed','wheat_seed'] #set the allowed crops that can be planted to the autumn crops
                SHOP_BUTTONS = AUTUMN_SHOP_BUTTONS #set the shop buttons to the autumn variant
            else:
                for tile in TILES:
                    tile.change_season('spring') #change all the tiles to their spring variants
                    allowed_crops = ['strawberry_seed','beetroot_seed','carrot_seed'] #set the allowed crops that can be planted to the spring crops
                SHOP_BUTTONS = SPRING_SHOP_BUTTONS #set the shop buttons to the spring variant
                    
            for crop in CROPS:
                crop.season_change() #kill all the crops that are planted
            season_change = False #reset the season_change variable
            
        if not animation:
            p.update(frame) #updates the player location and image
            
        if ((p.loc[0] > 340 and p.loc[1] > 290) and (p.loc[0] < 560 and p.loc[1] < 370)) or (
            (p.loc[0] > 1240 and p.loc[1] > 280) and (p.loc[0] < 1390 and p.loc[1] < 330)) or (
                (p.loc[0] > 730 and p.loc[1] > 340) and (p.loc[0] < 930 and p.loc[1] < 400)) or (
                    (p.loc[0] > 1020 and p.loc[1] > 340) and (p.loc[0] < 1130 and p.loc[1] < 400)) or (
                        (p.loc[0] > 730 and p.loc[1] > 290) and (p.loc[0] < 760 and p.loc[1] < 370)) or (
                            (p.loc[0] > 1070 and p.loc[1] > 290) and (p.loc[0] < 1130 and p.loc[1] < 370)) or (
                                (p.loc[0] > 730 and p.loc[1] == 320) and (p.loc[0] < 1130 and p.loc[1] == 320)): #all the collideable walls
                p.retract_move(p.direction) #takes back the movement
                p.end_move(p.direction) #stops movement

      
        CAMERA.update(p) #updates the camera location based on the player rect centre
        SCREEN.fill((255, 255, 255)) #fills the screen in white
        
        for tile in TILES:
            if tile.check_collide([p.rect.center[0],p.rect.center[1]+16]) and tile.tile in [15,16,17,18,19,20,21,22,23,24]: #if player collide with water
                p.retract_move(p.direction) #takes away the movement
                p.end_move(p.direction) #stops the movement
            for crop in CROPS:
                if crop.loc == tile.loc:
                    crop.update(day_moved_to_next,tile.watered)

            if day_moved_to_next and tile.watered:
                tile.watered = False
                tile.update_values(0,pygame.transform.smoothscale(sprite_sheet.subsurface((0,0), (128,128)),(TILE_SIZE,TILE_SIZE)))
       
            if euclid_distance(p.loc, tile.loc) < RENDER_DISTANCE: #checks if the distance between the player and the tile is less then the render distance
                SCREEN.blit(tile.image, CAMERA.to_camera_view(tile.loc)) #draw the tile that is in relation to the camera location                          

        day_moved_to_next = False
        previous_inventory_click = inventory_click #sets the variable equal to inventory_click   


        for crop in CROPS:
            if euclid_distance(p.loc, crop.loc) < RENDER_DISTANCE: #checks if the distance between the player and the crop is less then the render distance
                SCREEN.blit(crop.image, CAMERA.to_camera_view(crop.loc)) #draw the crop that is in relation to the camera location

        if p.loc[1] <= 290: #if the y of the player is less than 290
            if not inventory_opened and not shop_opened:  #player is drawn behind the structure
                SCREEN.blit(p.image, CAMERA.to_camera_view(p.image_loc))            
            for structure in STRUCTURES:
                if euclid_distance(p.loc, structure.loc) < RENDER_DISTANCE:
                    SCREEN.blit(structure.image, CAMERA.to_camera_view(structure.loc))
        else: #player is drawn above the structure
            for structure in STRUCTURES:
                if euclid_distance(p.loc, structure.loc) < RENDER_DISTANCE:
                    SCREEN.blit(structure.image, CAMERA.to_camera_view(structure.loc))   
            if not inventory_opened and not shop_opened: 
                SCREEN.blit(p.image, CAMERA.to_camera_view(p.image_loc))
                
        if inventory_opened: 
            inventory_button.hover(pygame.mouse.get_pos()) #check if the exit button is hovered in inventory screen
            SCREEN.blit(pygame.transform.smoothscale(pygame.image.load('game/inventory_base_image.png'),(704,448)),(32,32)) #draw the panel
            SCREEN.blit(pygame.transform.smoothscale((inventory_button.image),(inventory_button.size)),(inventory_button.loc)) #draw the exit button
            
        else:
            SCREEN.blit(UI_base, (640,0)) #draws the ui base
            SCREEN.blit(coin, (644, 84)) #draw the coin image
            for text in TEXT:
                if text.type == 'money':
                    SCREEN.blit(text.text,(676,88)) #display the money text
            if date % 7 == 1: #decide what day of the week it is
                day = 'Mon'
            elif date % 7 == 2:
                day = 'Tue'
            elif date % 7 == 3:
                day = 'Wed'            
            elif date % 7 == 4:
                day = 'Thu'                  
            elif date % 7 == 5:
                day = 'Fri'
            elif date % 7 == 6:
                day = 'Sat'
            elif date % 7 == 0:
                day = 'Sun'
            date_text = Text('rolam', 32, day + '. '+ str(date), True, (170,139,102), None, (672,18),'farm_name') #create the date text
            SCREEN.blit(date_text.text,date_text.loc) #draw the text

        if shipping_bin_opened and not inventory_opened:
            SCREEN.blit(pygame.transform.smoothscale(shipping_bin_base,(704,448)),(32,32))
            for button in BIN_BUTTONS:
                button.hover(pygame.mouse.get_pos()) #update the button to check if mouse hovered over it               
                SCREEN.blit(pygame.transform.smoothscale((button.image),(button.size)),(button.loc)) #draw the buttons
                
            inventory_items = []
            for slot in INVENTORY:
                inventory_items.append(slot.item) #adds all the inventory items to a list
                slot.update(value[slot.item])
                SCREEN.blit(slot.image, slot.loc) #draw the slot
                if slot.item != 'empty':
                    SCREEN.blit(slot.item_image, slot.loc) #draw the inventory item
                    number = Text('rolam', 24, str(slot.value) , True, (92, 64, 51), None, slot.loc ,'slot_value')
                    SCREEN.blit(number.text, number.loc) #draws the small number text next to the slot
                    
            SCREEN.blit(bin_base, (444, 72))
            if bin_item != 'empty':
                SCREEN.blit(bin_item_img, (460,88))
                number = Text('rolam', 24, str(bin_value) , True, (92, 64, 51), None, (460,88),'bin_value') 
                SCREEN.blit(number.text, number.loc) #draws the small number text next to the slot                

                amount = Text('rolam', 24, str(sell_cost[bin_item]*bin_value) + 'g', True, (170,139,102), None, (640,96),'cost')
                SCREEN.blit(amount.text, amount.loc) #draws the small number text next to the slot 
                    
            if frame <= 12:
                SCREEN.blit(pygame.transform.smoothscale(bin_animation[0],(40,40)),(96,96))
            else:
                SCREEN.blit(pygame.transform.smoothscale(bin_animation[1],(40,40)),(96,96))
                
        hotbar_items = []
        for slot in HOTBAR: #loops throught all the hotbar slots
            hotbar_items.append(slot.item) #adds all the hotbar items to a list

            slot.update(value[slot.item]) #updates the value number text next to the slot
            SCREEN.blit(slot.image,slot.loc) #draws the hotbar slot

            if slot.selected and not inventory_opened and not shipping_bin_opened:
                SCREEN.blit(selected, slot.loc)
            if slot.item != 'empty': #if the hotbar has an item
                SCREEN.blit(slot.item_image,slot.loc) #draws the item
                if slot.item != 1:
                    number = Text('rolam', 24, str(slot.value) , True, (92, 64, 51), None, (slot.loc),'slot_value') 
                    SCREEN.blit(number.text, number.loc) #draws the small number text next to the slot


        if shop_opened and not inventory_opened: #when the shop is opened
            if season == 'autumn':
                SCREEN.blit(pygame.transform.smoothscale(autumn_shop_base,(704,448)),(32,32)) #draw the shop background
                for button in AUTUMN_SHOP_BUTTONS:
                    button.hover(pygame.mouse.get_pos()) #update the button to check if mouse hovered over it               
                    SCREEN.blit(pygame.transform.smoothscale((button.image),(button.size)),(button.loc)) #draw the buttons
            else:
                SCREEN.blit(pygame.transform.smoothscale(spring_shop_base,(704,448)),(32,32)) #draw the shop background
                for button in SPRING_SHOP_BUTTONS:
                    button.hover(pygame.mouse.get_pos()) #update the button to check if mouse hovered over it               
                    SCREEN.blit(pygame.transform.smoothscale((button.image),(button.size)),(button.loc)) #draw the buttons
                    
            SCREEN.blit(money_text.shop_text,(616,120))
            
            if frame > 12: #when the frame is above 24
                if idle:
                    SCREEN.blit(pygame.transform.scale(shop_animation[2],(64,64)), (224,106)) #draw that frame animation
                elif angry:
                    SCREEN.blit(pygame.transform.scale(shop_animation[4],(64,64)), (224,106)) #draw that frame animation
                    occured += 1
                elif happy:
                    SCREEN.blit(pygame.transform.scale(shop_animation[0],(64,64)), (224,106)) #draw that frame animation
                    occured += 1
            else:
                if idle:
                    SCREEN.blit(pygame.transform.scale(shop_animation[3],(64,64)), (224,106)) #draw that frame animation
                elif angry:
                    SCREEN.blit(pygame.transform.scale(shop_animation[5],(64,64)), (224,106)) #draw that frame animation
                    occured += 1
                elif happy:
                    SCREEN.blit(pygame.transform.scale(shop_animation[1],(64,64)), (224,106)) #draw that frame animation
                    occured +=1
                

            
            
        if inventory_opened:
            inventory_items = []
            for slot in INVENTORY:
                inventory_items.append(slot.item) #adds all the inventory items to a list
                slot.update(value[slot.item])
                SCREEN.blit(slot.image, slot.loc) #draw the slot
                if slot.item != 'empty':
                    SCREEN.blit(slot.item_image,slot.loc) #draw the inventory item
                    number = Text('rolam', 24, str(slot.value) , True, (92, 64, 51), None, (slot.loc),'slot_value')
                    SCREEN.blit(number.text, number.loc) #draws the small number text next to the slot
                    
            if held_item != 'empty':
                SCREEN.blit(held_item_img,[mouse_pos[0]-24,mouse_pos[1]-24]) #draw the held item at the mouse posititon
            SCREEN.blit(animation_base, (80,112))

            
            if frame > 12: #when the frame is above 24
                if animation_occured < 3: #and if the animation has occured less than 3 times
                    SCREEN.blit(pygame.transform.scale(inventory_animation[animation_frame],(64,64)), (112,154)) #draw that frame animation
                    animation_occured += 1 #increase the amount that animation has occured
                else:
                    animation_occured = 0 #reset the amount the animation has occured
                    animation_frame += 1 #increase the frame
                    if animation_frame > len(inventory_animation)-1: #if reach the end of the animation list
                        animation_frame = 0 #reset the animation frame
                    SCREEN.blit(pygame.transform.scale(inventory_animation[animation_frame],(64,64)), (112,154)) #draw that frame animation
                    
            else:
                SCREEN.blit(pygame.transform.scale(inventory_animation[0],(64,64)), (112,154)) #draw the normal idle animation

            for text in TEXT: 
                SCREEN.blit(text.text,text.loc) #draw the text
            SCREEN.blit(coin,(192,336)) #draw the coin        

        DISPLAY.blit(SCREEN, (0, 0))
        pygame.display.update()
        clock.tick(60)
