import pygame,sys,random #imported modules
from pygame.locals import *
from start_game import start_game #this is done so the game class from another file in my area can be called when its button is pressed
from settings import settings #this is done so the game class from another file in my area can be called when its button is pressed
pygame.init() #initialises pygame

option = str(random.randint(1,3)) #picks a random number between 1 to 3, this is used to determain the image background used

background_image = pygame.image.load('menu/option_'+option+'/menu_background.png') #loads the background image
button_loc = 'menu/'+'option_'+option+'/button/' # button loc location to make it easier when loading all the buttons images

normal_images = {
    'start': button_loc+'/normal/start.png',
    'settings': button_loc+'/normal/settings.png',
    'end': button_loc+'/normal/exit.png',
    'sound': button_loc+'/normal/sound.png'
    } #loads all the buttons default images from their areas
hover_images = {
    'start': button_loc+'hover/start.png',
    'settings': button_loc+'hover/settings.png',
    'end': button_loc+'hover/exit.png',
    'sound': button_loc+'hover/mute.png'
    } #loads all the buttons action images from their areas



pygame.mixer.pre_init(44100, -16, 2, 512) #initialises the mixer and ensures there is no delay and is the correct buffer
pygame.mixer.music.load('music.mp3') #loads the background music    
pygame.mixer.music.play(-1) #plays the background music
click = pygame.mixer.Sound('menu/click.wav') #creates a click sound effect that can be called apon
click.set_volume(0.2)
pygame.mixer.music.set_volume(0.2) #adjusts the volume of the music

class Button: #how the buttons are created
    def __init__(self,button: str,loc: list,dimension:list) -> None:
        self.type = button #which button it is, start, settings or exit (in this case end as exit is another feature in python)
        self.normal_img = pygame.image.load(normal_images[button]) #loads the buttons default image from the dictionary normal_images
        self.hover_img = pygame.image.load(hover_images[button]) #loads the buttons action image from the dictionary hover_images

        self.dimensions = dimension #sets the dimensions of the button
        self.image = pygame.transform.smoothscale(
            self.normal_img,
            self.dimensions
            ) #creates the image, size: self.dimensions, surface: the image of button_load of the type stated by the button input
        self.loc = loc #sets the locaiton of the button
        self.sound = True #variable used to figure out whether sound should be playing
        
    def hover(self,mouse_pos: list)-> None: #triggered every frame
        point = pygame.Rect(
            self.loc[0],
            self.loc[1],
            self.dimensions[0],
            self.dimensions[1]
            ) #creates a rect where the button is located and of the same size as the button to test for any collisions
        
        if point.collidepoint(mouse_pos) and self.type != 'sound':  #checks if the mouse position is within the created rect of the button
            self.image = pygame.transform.smoothscale(
                self.hover_img,
                (self.dimensions[0],self.dimensions[1])
                ) #changes the image to its second version of the original when this happens.
            
        elif self.type != 'sound': #checks that the button hovered over is not the sound button as this one should simpy be toggled
            self.image = pygame.transform.smoothscale(self.normal_img,self.dimensions) #reverts its image back to original

    def mute(self): 
        if self.type == 'sound': #checks button type is the mute button
            self.sound = not self.sound #toggles music on/off
            if self.sound: #if sound should be on
                self.image = pygame.transform.smoothscale(pygame.image.load(normal_images[self.type]),self.dimensions) #image is its default
                pygame.mixer.music.play(-1) #plays the music 
            else:
                self.image = pygame.transform.smoothscale(self.hover_img,self.dimensions) #image is its second version
                pygame.mixer.music.fadeout(0) #stops the music
        

    def click(self,mouse_pos: list): #triggered when mouse button is clicked
        point = pygame.Rect(self.loc[0],
                            self.loc[1],
                            self.dimensions[0],
                            self.dimensions[1]
                            ) #creates a rect where the tile is located to test for any collisions
        
        if point.collidepoint(mouse_pos) and self.type == 'start': #checks if the mouse has collided with the the start button
            return 1 #return 1 if this is the case
        elif point.collidepoint(mouse_pos) and self.type == 'settings': #checks if the mouse has collided with the settings button
            return 2 #return 2 if this is the case
        elif point.collidepoint(mouse_pos) and self.type == 'end': #checks if the mouse has collided with the exit button
            return 3 #return 3 if this is the case
        elif point.collidepoint(mouse_pos) and self.type == 'sound': #checks if the mouse has collided with the exit button
            self.sound = not self.sound #toggles the sound
            if self.sound:
                self.image = pygame.transform.smoothscale(pygame.image.load(normal_images[self.type]),self.dimensions)
                pygame.mixer.music.play(-1) #plays the music 
            else:
                self.image = pygame.transform.smoothscale(self.hover_img,self.dimensions)
                pygame.mixer.music.stop() #stops the music
            return 4

    def is_mute(self): 
        return self.sound #returns the current value held in self.sound

    
    
def create_button(BUTTONS:list,DISPLAY)->list: #takes in the list of buttons
    BUTTONS = [] #empties that list
    #creates all the buttons again with the correct dimensions
    BUTTONS.append(Button('start',((DISPLAY.get_width()*0.1),(DISPLAY.get_height()//4)),(DISPLAY.get_width()//3,DISPLAY.get_height()//10)))
    BUTTONS.append(Button('settings',((DISPLAY.get_width()*0.1),(DISPLAY.get_height()//8)*3),(DISPLAY.get_width()//4.5,DISPLAY.get_height()//15)))
    BUTTONS.append(Button('end',(78,240),(DISPLAY.get_width()//12,DISPLAY.get_height()//18)))                  
    BUTTONS.append(Button('sound',((DISPLAY.get_width()*0.9), DISPLAY.get_height()//20),(DISPLAY.get_width()//12,DISPLAY.get_width()//12)))
    return BUTTONS #returns this list

class Cloud: #class that creates and moves the clouds
    def __init__(self,cloud:str,loc,dimensions): #initialises each individual cloud
        self.cloud = cloud #the pathway for where the image of the cloud is stored
        self.loc_x,self.loc_y = loc #stores cloud original location
        self.loc = self.loc_x,self.loc_y
        self.dimensions = dimensions #stores clouds dimensions
        self.image_loc = pygame.image.load('menu/option_'+option+'/cloud/'+self.cloud+'.png') #creates the image of the cloud
        self.image = pygame.transform.smoothscale(
            self.image_loc,
            self.dimensions
            ) #smoothscale transforms the image to its correct dimensions

    def resize(self,dimension): #resize function called when the window has been resized
        self.dimensions = dimension #recreate the dimensions
        self.image = pygame.transform.smoothscale(
            self.image_loc,
            self.dimensions
            ) #smoothscale transforms the image to its correct dimensions

    def update(self,DISPLAY): #function that occurs every frame
        self.loc_x +=0.5 #increases the clouds x value by 0.5 every frame
        
        if self.loc_x > DISPLAY.get_width()+10: #checks if the cloud is off the screen (+a buffer worth of space so it doesnt teleport) 
            self.loc_x = -DISPLAY.get_width()//5 #moves the cloud to the beginning of the screen (+a buffer worth of space so it doesnt teleport) 
        self.loc = self.loc_x,self.loc_y #stores the new location of the cloud
        
def create_cloud(CLOUDS:list,DISPLAY)->list: # a function to create a cloud everytime the window size has been adjusted
    CLOUDS = [] #empties out the cloud list
    #creates the clouds with their correct, type, location and dimension
    CLOUDS.append(Cloud('1',(50,20),(270,110)))
    CLOUDS.append(Cloud('2',(400,20),(270,90)))
    CLOUDS.append(Cloud('3',(700,40),(150,60)))
    return CLOUDS #returns these new clouds


        

class Jumino: #class the creates and moves a small sprite across the screen dependent on the players inputs
    def __init__(self,loc:list,dimensions:list)->None: #initialises the jumino

        self.dimensions = dimensions #stores the juminos dimensions
        self.movement = {'right':False,'left':False,'idle':True} #a dictionary that contains the possible states the jumino could be in

        #load all these images before hand to save storage
        self.idle = [pygame.image.load('menu/option_'+option+'/jumino/idle/j1.png'),pygame.image.load('menu/option_'+option+'/jumino/idle/j2.png')]
        self.right = [pygame.image.load('menu/option_'+option+'/jumino/move/r1.png'),pygame.image.load('menu/option_'+option+'/jumino/move/r2.png')]
        self.left = [pygame.image.load('menu/option_'+option+'/jumino/move/l1.png'),pygame.image.load('menu/option_'+option+'/jumino/move/l2.png')]

        self.current_1 = self.idle[0] #set the current image to its idle
        self.current_2 = self.idle[1] #set the counterpart image to its second idle
        
        self.image = pygame.transform.smoothscale(
            self.current_1,
            self.dimensions
            ) #smoothly scales the image to the correct dimensions
        self.loc_x = loc[0]
        self.loc_y = loc[1]
        self.loc = self.loc_x,self.loc_y #stores the location of the sprite

    def update(self,frame,DISPLAY): #function that occurs every frame
        if self.movement['idle']: #checks if sprite is in idle
            self.current_1 = self.idle[0] #sets the current images to their correct images
            self.current_2 = self.idle[1]

        elif self.movement['right']: #checks if sprite is in right
            self.current_1 = self.right[0] #sets the current images to their correct images
            self.current_2 = self.right[1]
            self.loc_x +=1

        elif self.movement['left']:  #checks if sprite is in left
            self.current_1 = self.left[0] #sets the current images to their correct images
            self.current_2 = self.left[1]
            self.loc_x -=1
    
        if self.loc_x >= DISPLAY.get_width()-DISPLAY.get_width()//50: #checks if the sprite is off the screen (+ a buffer)
            self.loc_x = DISPLAY.get_width() -DISPLAY.get_width()//50 #adjusts the sprites x value so it stays on the screen
        if self.loc_x <= 0: #checks if the sprite is off the screen 
            self.loc_x = 1 #adjusts the sprites x value so it stays on the screen
        if frame < 12: #checks that the frame counter is less than 12
            self.image = pygame.transform.smoothscale(
                self.current_1,
                self.dimensions
                ) #sets image to correct current image

        elif frame > 12: #checks that the frame counter is more than 12
            self.image = pygame.transform.smoothscale(
                self.current_2,
                self.dimensions
                ) #sets image to correct current image
        self.loc = self.loc_x,self.loc_y
            
    def begin_move(self,move): #called when buttons are being pressed
        self.movement[move]= True #sets that value to true
    
    def end_move(self,move):  #called when buttons aren't being pressed
        self.movement[move]= False #sets that value to false        

def create_jumino(DISPLAY)->list: #function that can be called to recreate the jumino when screen is resized
    return  Jumino((220,305),(60,70))


def main_menu(monitor_size:list,SCREEN,DISPLAY,clock,SCREEN_SIZE): #the function that is run when the program is run from the 'main.py' file
    fullscreen = False #indicates whether fullscreen should be toggled
    
    switch_screen_1 = False #indicates whether screen 1 should be opened
    switch_screen_2 = False #indicates whether screen 2 should be opened
    BUTTONS = [] #empty list that stores the buttons
    CLOUDS = [] #empty list that stores the clouds
    # ^ initialising the windows information
    sound = True #variable to check if sound should be running throughout the program
    BUTTONS = create_button(BUTTONS,DISPLAY) #creates the buttons
    CLOUDS = create_cloud(CLOUDS,DISPLAY) #creates the clouds
    j= create_jumino(DISPLAY) #creates the jumino
    #creating all the buttons/clouds/jumino and appending them to the empty buttons list
    CONTROLS = {'Forward': 119,'Left': 97,'Down': 115,'Right': 100,
                'Hotbar_1': 49,'Hotbar_2': 50,'Hotbar_3': 51,'Hotbar_4': 52,'Hotbar_5': 53,'Hotbar_6': 54,'Hotbar_7': 55,'Hotbar_8': 56,'Hotbar_9': 57,
                'Action_1': 'L_mouse','Action_2': 'R_mouse','Sound': 109}
    frame = 0 #frame counter

    while True:
        for event in pygame.event.get(): #checks for event
            if event.type == pygame.QUIT: #checks if the cross is pressed
                pygame.quit() #exits out of the whole program if this is the case
                sys.exit()

            if event.type == KEYDOWN: #checks for any keys being pressed down
                if event.key == K_f: #if key F is pressed
                    pygame.display.toggle_fullscreen()
                    
                if event.key == CONTROLS['Sound']: #when the key assigned to sound action is pressed 
                    sound = not sound #toggles the sound
                    for b in BUTTONS: #loops through all the buttons in the list
                        b.mute() #uses the sound fucntion from the button class
                    
                if event.key == CONTROLS['Left']: #checks if the key assigned to moving left is pressed down
                    j.end_move('idle') #ends idle move
                    j.begin_move('left') #begins moving left

                if event.key == CONTROLS['Right']: #checks if the key assigned to moving right is pressed down
                    j.end_move('idle') #ends idle move
                    j.begin_move('right') #begins moving right

            if event.type == KEYUP: #checks if any keys have stopped being pressed
                if event.key == CONTROLS['Left']: #if this key is the key assigned to moving left
                    j.end_move ('left') #ends moving left
                    j.begin_move('idle') #begins idle move
                    
                if event.key == CONTROLS['Right']: #if this key is the key assigned to moving right
                    j.end_move ('right') #ends moving right
                    j.begin_move('idle') #begins idle move 
                        
            if event.type == MOUSEBUTTONDOWN: #checks if a mosue button is pressed down
                if pygame.mouse.get_pressed()[0]:
                    mouse_pos = pygame.mouse.get_pos() #gets the position of the mouse curser
                    for b in BUTTONS: #loops through the buttons in the list BUTTONS
                        screen = b.click(mouse_pos) #returns a number based on what button it clicked
                        #switches to the screen or exits the program based on the number returned
                        if screen == 1:
                            switch_screen_1 = True
                        elif screen == 2:
                            switch_screen_2 = True
                        elif screen == 3:
                            pygame.quit()
                            sys.exit()
                        elif screen == 4: #if the return is 4, it means the mute button has been pressed
                            sound = not sound #therefore it toggles sound to the opposite of what it was
                        if sound: #if sound is true 
                            click.play() #the click sound is played

                    

                    
##############################UPDATES
        

            
        if switch_screen_1: #checks if the screen should switch
            start_game(fullscreen,monitor_size,SCREEN,DISPLAY,clock,CONTROLS,background_image) #opens the game function from my game.py python file
            switch_screen_1 = False #toggle switch screen
            
        if switch_screen_2:
            CONTROLS = settings(fullscreen,monitor_size,SCREEN,DISPLAY,clock,background_image,sound, CONTROLS) #opens the settings function from my settings.py python file
            switch_screen_2 = False #toggle switch screen

        background = pygame.transform.smoothscale( #background image creation
            background_image,
            (pygame.display.Info().current_w,pygame.display.Info().current_h)
            )

        
        for b in BUTTONS: #loops through the list with the buttons contained within
            b.hover(pygame.mouse.get_pos()) #checks if the mouse is hovering over a button
        for c in CLOUDS: #loops through all the clouds in the list
            c.update(DISPLAY) #performs the update function in the cloud class
            
        if frame > 24: #checks that frame has not exceeded 24
            frame = 0 #sets it back to zero if this has occured
        frame +=1 #increments frame by one each frame
        j.update(frame,DISPLAY) #passes this into jumino so that its animation can be figured out
     
        

##############################DRAWING
    
        SCREEN.blit(background,(0,0)) #blits the background to the screen
        
        for cloud in CLOUDS: #goes through each cloud in the CLOUDS list
            SCREEN.blit(cloud.image,cloud.loc) #blits this to its correct location
        SCREEN.blit(j.image,j.loc) #blits the jumino to its correct location
        for button in BUTTONS: #loops through the list with the buttons contained within
            SCREEN.blit(button.image,button.loc) #draws each button at its location and correct image
            
        DISPLAY.blit(SCREEN,(0,0)) #blits the screen onto the display
        pygame.display.update() #updates the display
        clock.tick(60) #framerate
