import pygame,sys
from pygame.locals import *
pygame.init() 

normal_images = {'control': 'settings/buttons/normal/control.png',
                 'instructions' : 'settings/buttons/normal/instruction.png',
                 'exit': 'settings/buttons/normal/exit.png'} #normal buttons image locations
hover_images = {'control': 'settings/buttons/hover/control.png',
                'instructions' : 'settings/buttons/hover/instruction.png',
                'exit': 'settings/buttons/hover/exit.png'} #hovered buttons image locations

settings_base_img = pygame.image.load('settings/base.png') #loads the setings base image
panel = {'control': 'settings/control_panel.png', 'instructions':'settings/instruction_panel.png'} #panel image locations
pygame.mixer.pre_init(44100, -16, 2, 512) #initialises music in the game
click = pygame.mixer.Sound('menu/click.wav') #generates the click audio
hover = pygame.mixer.Sound('open.wav') #generates the hovered button audio
hover.set_volume(0.2) #sets the volume
click.set_volume(0.2) #sets the volume

class Button: #Button class where all buttons are made and where their attributes are retained
    def __init__(self,button: str,loc: list,dimension:list) -> None: #initialises the buttons
        self.type = button #which button it is, start, settings or exit (in this case end as exit is another feature in python)
        self.normal_img = pygame.image.load(normal_images[button]) #its original image that it has when not hovered over 
        self.hover_img = pygame.image.load(hover_images[button]) #generates another image that is displayed when the mosue is hovering over the button
        self.open = False #whether their panel should be open or closed
        self.dimensions = dimension #the buttons dimensions on the screen used for drawing the button later
        self.image = pygame.transform.smoothscale(
            self.normal_img,
            self.dimensions
            ) #creates the image, size: self.dimensions, surface: the image of button_load of the type stated by the button input
        self.loc = loc #location dictated when the button is created by the loc input

    def hover(self,mouse_pos: list,play_hover)-> None: #triggered every frame
        point = pygame.Rect(self.loc[0],
                            self.loc[1],
                            self.dimensions[0],
                            self.dimensions[1]) #creates a rect where the tile is located to test for any collisions
        if point.collidepoint(mouse_pos) and self.type != 'sound':  #checsk if the mouse position is within the created rect of the button
            self.image = pygame.transform.smoothscale(self.hover_img,
                                                      (self.dimensions[0],
                                                       self.dimensions[1])) #changes the image to a different version of the original when this happens.
            play_hover = True #sets hover to true to indicate the mouse is hovered over the button
        elif self.type != 'sound': #when the button is not the sound button
            self.image = pygame.transform.smoothscale(self.normal_img,self.dimensions) #changes the image to its original as mouse isnt hovered over it
            play_hover = False # sets hover to false to indicate the mouse is not hovered over the button

    def end(self,mouse_pos: list): #triggered when mouse button is clicked
        point = pygame.Rect(self.loc[0],
                            self.loc[1],
                            self.dimensions[0],
                            self.dimensions[1]) #creates a rect where the tile is located to test for any collisions
        
        if point.collidepoint(mouse_pos) and self.type == 'exit': #checsk if the mouse has collided with the button and whether it is the start button
            return False #returns the value False
        else:
            return True #returns the value True

    def click(self, mouse_pos: list): #function used when the button is clicked on and mouse is pressed down, retrives the current mouse position
        point = pygame.Rect(self.loc[0],
                            self.loc[1],
                            self.dimensions[0],
                            self.dimensions[1]) #creates a rect where the tile is located to test for any collisions
        if point.collidepoint(mouse_pos) and self.type != 'instruction':  #checsk if the mouse position is within the created rect of the button
            self.open = not self.open #togles the self.open variable 
            
        elif point.collidepoint(mouse_pos) and self.type != 'control':  #checsk if the mouse position is within the created rect of the button
            self.open = not self.open #toggles the self.open variable



class ControlButton: #Control button class where all buttons are made and where their attributes are retained
    def __init__(self, key, loc:list, button:str): #initialises the buttons
        self.type = button #which control button it is
        self.dimension = (175,40) #what size the button should be
        self.image_loc = 'settings/buttons/control/button_'+button+'.png' #the location of the buttons image in my files
        self.image = pygame.transform.smoothscale(pygame.image.load(self.image_loc),
                                                  self.dimension) #loads the image so it only needs to be loaded once

        self.loc = loc #the location of where the button is blitted
        self.key = key #they key assigned to the button
        self.key_dimension = (75,40) #the dimension of the key image
        self.key_image = pygame.transform.smoothscale(pygame.image.load('settings/buttons/control/key/button_'+str(key)+'.png'),
                                                      self.key_dimension) #loads the image so it only needs to be loaded once
        self.key_loc = (loc[0] + 100, loc[1]) #the location of where the image should be blitted
        
        self.key_draw = True #a varaible that states whether the key image should be drawn or not
        self.is_clicked = False #a variable that states whether a button has been clicked on
        
    def click(self, mouse_pos): #function used when the mouse is pressed down and a click is registered
        point = point = pygame.Rect(self.loc[0],self.loc[1],self.dimension[0],self.dimension[1]) #creates a rect at the point where the mouse is
        if point.collidepoint(mouse_pos): #checks for any collision between this point and the button's rect
            self.is_clicked = not self.is_clicked #toggles the variable is_clicked 
        if self.is_clicked: #when is_clicked is true
            self.image = pygame.transform.smoothscale(pygame.image.load('settings/buttons/clicked.png'),
                                                      self.dimension) #image is changed to waiting for new control image
            self.key_draw = False #key image is not drawn

        return self.is_clicked #returns the variable
    
    def change(self, key, CONTROLS): #function used when a key has been pressed down, takes in what key has been pressed and the CONTROLS dictionary
        self.key = key #changes the self assigned key to this key
        self.key_image = pygame.transform.smoothscale(pygame.image.load('settings/buttons/control/key/button_'+str(key)+'.png'),
                                                      self.key_dimension) #draws the new key image
        self.image = self.image = pygame.transform.smoothscale(pygame.image.load(self.image_loc),
                                                               self.dimension) #draws its original image 
        self.is_clicked = False #reverts the variable back to false
        self.key_draw = True #reverts the variable back to true
        CONTROLS[self.type] = key #changes the value for that action in the dictionary to the new assigned key
        return CONTROLS #returns the dictionary
        

basic_CONTROLS = [K_q,K_w,K_e,K_r,K_t,K_y,K_u,K_i,K_o,K_p,K_a,K_s,K_d,K_g,K_h,K_j,K_k,K_l,K_z,K_x,K_c,K_v,K_b,K_n,K_m,
                  K_1,K_2,K_3,K_4,K_5,K_6,K_7,K_8,K_9,K_0,
                  K_BACKSPACE,K_TAB,K_RETURN,K_SPACE,K_MINUS,K_EQUALS,K_QUOTE,K_CAPSLOCK,K_RSHIFT,K_LSHIFT,
                  K_LEFTBRACKET,K_RIGHTBRACKET,K_SEMICOLON,K_HASH,K_COMMA,K_PERIOD,K_SLASH,K_BACKSLASH] #list of all the keys that can be used        


def create_button(BUTTONS:list,DISPLAY,sound)->list:
    BUTTONS = [] #empty list that stores the buttons so that they can be draw later on in the program
    BUTTONS.append(Button('control',(-DISPLAY.get_width()//32,(DISPLAY.get_height()//10*3)),(300,DISPLAY.get_height()//6))) #creates control button
    BUTTONS.append(Button('instructions',(-DISPLAY.get_width()//20,(DISPLAY.get_height()//10)*5),(295,DISPLAY.get_height()//6))) #create instruction button
    BUTTONS.append(Button('exit',(0,(DISPLAY.get_height()//10)*9),(DISPLAY.get_width()//12,DISPLAY.get_height()//12)))#create exit button
    return BUTTONS #returns the list BUTTONS

def create_control_button(CONTROLS):
    CONTROLBUTTONS = []#empty list that stores the buttons so that they can be draw later on in the program
    CONTROLBUTTONS.append(ControlButton(CONTROLS['Forward'], (300,75),'Forward')) #create forward button
    CONTROLBUTTONS.append(ControlButton(CONTROLS['Left'], (300,115), 'Left')) #create left button
    CONTROLBUTTONS.append(ControlButton(CONTROLS['Down'], (300,155), 'Down')) #create down button
    CONTROLBUTTONS.append(ControlButton(CONTROLS['Right'], (300,195), 'Right')) #create right button
    CONTROLBUTTONS.append(ControlButton(CONTROLS['Hotbar_1'], (525,75), 'Hotbar_1')) #create hotbar 1 button
    CONTROLBUTTONS.append(ControlButton(CONTROLS['Hotbar_2'],(525,115),'Hotbar_2'))#create hotbar 2 button
    CONTROLBUTTONS.append(ControlButton(CONTROLS['Hotbar_3'], (525,155), 'Hotbar_3'))#create hotbar 3 button
    CONTROLBUTTONS.append(ControlButton(CONTROLS['Hotbar_4'],(525,195),'Hotbar_4'))#create hotbar 4 button
    CONTROLBUTTONS.append(ControlButton(CONTROLS['Hotbar_5'], (525,235), 'Hotbar_5'))#create hotbar 5 button
    CONTROLBUTTONS.append(ControlButton(CONTROLS['Hotbar_6'], (525,275),'Hotbar_6'))#create hotbar 6 button
    CONTROLBUTTONS.append(ControlButton(CONTROLS['Hotbar_7'],(525,315),'Hotbar_7'))#create hotbar 7 button
    CONTROLBUTTONS.append(ControlButton(CONTROLS['Hotbar_8'], (525,355), 'Hotbar_8'))#create hotbar 8 button
    CONTROLBUTTONS.append(ControlButton(CONTROLS['Hotbar_9'], (525,395), 'Hotbar_9'))#create hotbar 9 button
    CONTROLBUTTONS.append(ControlButton(CONTROLS['Action_1'],(300,255), 'Action_1'))#create action 1 button
    CONTROLBUTTONS.append(ControlButton(CONTROLS['Action_2'],(300,295), 'Action_2'))#create action 2 button
    CONTROLBUTTONS.append(ControlButton(CONTROLS['Sound'],(300,355),'Sound'))#create sound button
    return CONTROLBUTTONS#returns the list BUTTONS
           
def settings(fullscreen,monitor_size,SCREEN,DISPLAY,clock,background,sound, CONTROLS):
    running = True #sets running equal to true to indicate the program should be running
    play_hover = False #sets play_hover to False
    BUTTONS = []
    BUTTONS = create_button(BUTTONS,DISPLAY,sound)#sets BUTTONS equal to the produced list from the create_button function
    CONTROLBUTTONS = create_control_button(CONTROLS)#sets CONTROLBUTTONS equal to the produced list from the create_control_button function
    
    show_control_button = False #states whether the control buttons should be shown on the screen
    show_instruction_panel = False #state whether the instruction panel should be shown on the screen
    clicked_control = False #state whether a control has been clicked on

    while running: #whilst running variable is true
        for event in pygame.event.get(): #checks through events within the code
            if event.type == pygame.QUIT: #checks if the quit event has occured
                pygame.quit() #close out of pygame
                sys.exit() #close out the system
            if event.type == KEYDOWN: #toggles fullscreen
                if event.key == K_f: #checks if f key pressed
                    pygame.display.toggle_fullscreen() #toggles fullscreen
                if event.key == K_ESCAPE: #checks if the game screen should be exited out
                    running = False


                if clicked_control: #when a control has been clicked on
                    keys = pygame.key.get_pressed() #get all the keys that has been pressed currently
                    for x in basic_CONTROLS: #loops through all the possible keys that are allowed
                        if keys[x]: #if that key has been pressed 
                            for control in CONTROLBUTTONS: #loops through all the control buttons
                                if control.is_clicked and (x not in CONTROLS.values()or CONTROLS[control.type] == x) : #if the button is clicked
                                    #and the key is not already assigned to another action
                                    CONTROLS = control.change(x,CONTROLS) #change the CONTROLS dictionary to be the correct key
                                    clicked_control = False #now that the click has been handled clicked_control is changed back to False
                                    
                        
                                    
            if event.type == MOUSEBUTTONDOWN: #checks if the mouse is pressed down
                if pygame.mouse.get_pressed()[0]:
                    mouse_pos = pygame.mouse.get_pos() #get the mouse current position
                    for button in BUTTONS: #loops throught all the buttons in the BUTTON list
                        button.click(mouse_pos) #opens the click function within the button class and passes in the current mouse position
                        running = button.end(mouse_pos) #sets running equal to the value returned from the end function in the button class
                    

                    for control in CONTROLBUTTONS: #loops through all the control buttons
                        if not clicked_control and (control.type != 'Action_1' and control.type != 'Action_2'): #if the button is not action 1 or 2
                            clicked = control.click(mouse_pos) #clicked is set to the value returned from the click funciton
                            if clicked: #only if click is true
                                clicked_control = True #is clicked control turned true
                            
                    if sound: #if the sound variable is true
                        click.play() #play the click sound
                    
        background = pygame.transform.smoothscale( #background image creation
            background,
            (pygame.display.Info().current_w,pygame.display.Info().current_h)
            )
        settings_base = pygame.transform.smoothscale( #background image creation
            settings_base_img,
            (300,530)
            )
        for button in BUTTONS: #loops through all the buttons in the button list
            button.hover(pygame.mouse.get_pos(),#opens the hover function within the button class and passes in the current mouse position 
                         play_hover) #and returns whether the mouse is over the button
            if play_hover: #if this value is true
                hover.play() #the sound is played
                  
        SCREEN.blit(background,(0,0))
        show_control_button = False #sets the variable to false
        show_instruction_panel = False #sets the variable to false
        for b in BUTTONS: #loops through the main buttons
            if b.open and b.type != 'exit': #if the button self made variable open is true and the button is not the exit button
                
                if b.type == 'control':
                    show_control_button = True #shows the control panel
                elif b.type == 'instructions':
                    show_instruction_panel = True #show the instruction panel
                SCREEN.blit(pygame.transform.smoothscale(pygame.image.load(panel[b.type]),(750,400)),(0,50)) #draws the panel
        
            

             
        SCREEN.blit(settings_base, (-5,-5)) #draws the settings_base image at this location

       
        for control in CONTROLBUTTONS: #loops through the control buttons
            if show_control_button and not show_instruction_panel: #if the control button is opened and the instruction panel is not opened
                SCREEN.blit(control.image,control.loc) #draw the control buttons 
                if control.key_draw: #if the keys should be drawn
                    SCREEN.blit(control.key_image,control.key_loc) #draw the keys
                            

        for button in BUTTONS: #loops through all the buttons in the button list
            SCREEN.blit(button.image,button.loc) #gets each buttons image and location and draws them onto the screen
                  
        DISPLAY.blit(SCREEN,(0,0)) #blits the screen onto the display 
        pygame.display.update()
        clock.tick(60)
    return CONTROLS #returns the keys back to menu
