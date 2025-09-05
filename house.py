import pygame
import sys
from pygame.locals import *
from classes import Text

pygame.init()

SCREEN_WIDTH = 1920  # sets screen width
SCREEN_HEIGHT = 1080  # sets screen height

class Furniture:
    def __init__(self,furniture,loc,size):
        self.furniture = furniture
        self.loc = loc
        self.size = size
        self.image = pygame.transform.smoothscale(pygame.image.load('house/%s.png'%furniture),self.size)

    def collide(self,pos):
        rect = pygame.Rect(self.loc[0],self.loc[1], self.size[0],self.size[1]) #creates a rect where the tile is located to test for any collisions
        if rect.collidepoint(pos):  #checsk if the mouse position is within the created rect of the button
            return True
        else:
            return False



        
def House(SCREEN, DISPLAY, farm_name, CONTROLS, money, HOTBAR, INVENTORY, inventory_animation,
          selected, inventory_button, p, value, clock, held_item, animation_base, TEXT, coin, date, UI_base, season):
    
    running = False
    inventory_opened = False
    frame = 0
    inventory_click = False
    previous_inventory_click = False
    animation_occured = 0
    animation_frame = 0
    p.loc = [504,376]
    p.speed = 4
    house = pygame.transform.smoothscale(pygame.image.load('house/house_base.png'),(448,448))
    FURNITURE = [Furniture('bookshelf',(480,40),(100,150)),
                 Furniture('bed',(180,50),(200,250)),
                 Furniture('sofa',(180,250),(100,180)),
                 Furniture('lamp',(380,50),(75,150)),
                 Furniture('carpet',(480,335),(100,100))]   #create all of the furniture
    
    press_exit = False
    next_to_bed = False
    day_moved_to_next = False
    sleeping = False
    screen = 0
    sprite_sheet = pygame.image.load('house/sleeping__cat.png')
    sleeping_cat = [sprite_sheet.subsurface((0,0), (128,128)),
                    sprite_sheet.subsurface((128,0), (128,128)),
                    sprite_sheet.subsurface((0,128), (128,128)),
                    sprite_sheet.subsurface((128,128), (128,128))] #all the cat animation images
    season_change = False
    
    while not running:
        mouse_pos = pygame.mouse.get_pos() #get the mouse position
        possible_move = p.possible_move()
        for event in pygame.event.get():  #if event is...
            if event.type == pygame.QUIT:  #checks if user is closing the window
                pygame.quit() #close the window
                sys.exit()
                
            if event.type == MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[2] and not sleeping: #when the player has right clicked
                    press_exit = True
                    if next_to_bed:
                        date += 1
                        if date > 30: #if the date has exceeding 30 days
                            if season == 'autumn': #and the current season is autumn
                                date = 1 #reset the date
                                season = 'spring' #switch the season
                                season_change = True #state there has been a season change
                            else:
                                date = 1 #reset the date
                                season = 'autumn' #switch the season
                                season_change = True #state there has been a season change
                                
                        sleeping = True
                        day_moved_to_next = True
                    else:
                        inventory_opened = not inventory_opened #the inventory is toggled

                if pygame.mouse.get_pressed()[0] and not sleeping: #when the player has left clicked
                    for item in HOTBAR:# loops through all the hotbar slots
                        if item.is_clicked(mouse_pos) and not inventory_opened: #checks if mouse clicked hotbar button
                            for slot in HOTBAR: #loops through the hotbar
                                if slot.is_clicked(mouse_pos):#checks if mouse clicked hotbar button
                                    slot.selected = True #sets the slot as selected
                                    p.item = slot.item #sets player item to be this item
                                else:
                                    slot.selected = False #slot is not selected
                    if inventory_opened:     
                        if inventory_button.click(mouse_pos): #if the button has been clicked on
                            inventory_opened = not inventory_opened #the inventory is closed
                        inventory_click = True


            if event.type == MOUSEBUTTONUP:
                if not pygame.mouse.get_pressed()[0]: 
                    inventory_click = False #a click has no longer occured
                        
                        
            if event.type == KEYDOWN: #checks if a key is pressed down
                if event.key == K_f: #checks if key is f
                    pygame.display.toggle_fullscreen() #fullscreens the screen

                if event.key == K_ESCAPE and not inventory_opened:  # checks if the game screen should be exited out
                    press_exit = True #sets the running variable to false so the while loop is no longer run
                    
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
                    next_to_bed = False
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
        p.update(frame)

        if (p.loc[0] >= 532 or p.loc[0] <= 244) or (p.loc[1] < 116 or p.loc[1] > 378): #if player collides with house walls
            p.end_move(p.direction)
            p.retract_move(p.direction) #stops player movement



            
        if inventory_opened: #if the inventory is opened
            for slot in HOTBAR:
                slot.in_inventory() #the slots size and location are moved and updated
            
            if not previous_inventory_click and inventory_click:  #if the player has just clicked
                for slot in HOTBAR: 
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
                       
        else:
            for slot in HOTBAR:
                slot.not_in_inventory() #otherwise hotbar slots are moved and updated back to how they originally are

        for furniture in FURNITURE: 
            if furniture.collide([p.loc[0]+32,p.loc[1]+64]) and furniture.furniture != 'carpet': #check if player collides with furniture
                p.retract_move(p.direction)
                p.end_move(p.direction) #stop player movement
                if furniture.furniture == 'bed':
                    next_to_bed = True #if collided with bed next to bed is true

            if furniture.collide([p.loc[0]+32,p.loc[1]+64]) and furniture.furniture == 'carpet':
                if press_exit: #if they have indicated they want to exit
                    running = True #running is true
                else:
                    running = False
            
                        
                        
            
        previous_inventory_click = inventory_click #sets the variable equal to inventory_click
        press_exit = False

        
        SCREEN.fill((0,0,0))
        if sleeping and screen < 96: #if the player has slept and the animation hasnt reached 96 frames
            screen += 1
            if screen <= 96 / 4:
                image = 0
            elif screen <= 96 / 2:
                image = 1
            elif screen <= (96/4)*3:
                image = 2
            else:
                image = 3
            SCREEN.blit(sleeping_cat[image],(600,400)) #draw the image
            text = Text('rolam', 64, 'Loading . . . ', True, (92,78,146), None, (300,200),'Loading') #create the text loading...
            SCREEN.blit(text.text, text.loc)  #draw it onto the screen
            DISPLAY.blit(SCREEN, (0, 0))
            pygame.display.update()
            clock.tick(60)            

        else:
            sleeping = False
            screen = 0
            SCREEN.blit(house, (160,8)) #draw the house
        
            for furniture in FURNITURE:
                SCREEN.blit(furniture.image, furniture.loc)
                
            if inventory_opened: 
                inventory_button.hover(pygame.mouse.get_pos()) #check if the exit button is hovered in inventory screen
                SCREEN.blit(pygame.transform.smoothscale(pygame.image.load('game/inventory_base_image.png'),(704,448)),(32,32)) #draw the panel
                SCREEN.blit(pygame.transform.smoothscale((inventory_button.image),(inventory_button.size)),(inventory_button.loc)) #draw the exit button




            hotbar_items = []
            for slot in HOTBAR: #loops throught all the hotbar slots
                hotbar_items.append(slot.item) #adds all the hotbar items to a list

                slot.update(value[slot.item]) #updates the value number text next to the slot
                SCREEN.blit(slot.image,slot.loc) #draws the hotbar slot

                if slot.selected and not inventory_opened:
                    SCREEN.blit(selected, slot.loc)
                if slot.item != 'empty': #if the hotbar has an item
                    SCREEN.blit(slot.item_image,slot.loc) #draws the item
                    if inventory_opened:
                        number = Text('rolam', 24, str(slot.value) , True, (92, 64, 51), None, (slot.loc),'slot_value') 
                        SCREEN.blit(number.text, number.loc) #draws the small number text next to the slot
                        
            
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
                
            else:
                SCREEN.blit(p.image,p.loc) #draw player
                SCREEN.blit(UI_base, (640,0)) #draw the ui base
                SCREEN.blit(coin, (644, 84)) #draw the coin image
                for text in TEXT:
                    if text.type == 'money':
                        SCREEN.blit(text.text,(676,88)) #draw the money text
                if date % 7 == 1: #check what day of the week it is
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
                SCREEN.blit(date_text.text,date_text.loc) #draw the date text

            
            DISPLAY.blit(SCREEN, (0, 0))
            pygame.display.update()
            clock.tick(60)
    return date, day_moved_to_next, season, season_change #return these variables back to game loop
