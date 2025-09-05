import pygame
import sys
from pygame.locals import *
from game import game
from game import Button
pygame.init()

SCREEN_WIDTH = 1920  # sets screen width
SCREEN_HEIGHT = 1080  # sets screen height
basic_CONTROLS = [K_q,K_w,K_e,K_r,K_t,K_y,K_u,K_i,K_o,K_p,K_a,K_s,K_d,K_f,K_g,K_h,K_j,K_k,K_l,K_z,K_x,K_c,K_v,K_b,K_n,K_m,
                  K_1,K_2,K_3,K_4,K_5,K_6,K_7,K_8,K_9,K_0] #list of the controls allowed to be typed

class Text:
    def __init__(self, font, size, text, antialias, colour, background, loc):
        self.font = font #font of the text
        self.size = size #size of the text
        self.text = text #what is said
        self.antialias = antialias 
        self.colour = colour #colour of the text
        self.background = background #is there a background
        texts = pygame.font.SysFont(self.font, self.size) #makes the text
        self.text = texts.render(self.text, self.antialias, self.colour, self.background) #render the text
        self.loc = loc #location of the text

        

def start_game(fullscreen, monitor_size, SCREEN, DISPLAY, clock, CONTROLS, background_image):
    running = True 
    switch_screen = False
    draw = True #whether anything should be drawn
    LETTER = '-> ' #the beginning of the text for the farm name
    BUTTONS = [Button((200,300),'cancel',(64,64)),Button((500,300),'confirm',(64,64))] #the cancel and confirm buttons
    while running:
        mouse_pos = pygame.mouse.get_pos() #gets the current mouse position
        for event in pygame.event.get():  #if event is...
            if event.type == pygame.QUIT:  #checks if user is closing the window
                pygame.quit() #close the window
                sys.exit()
            if event.type == KEYDOWN: 
                if event.key == K_ESCAPE: #when escape is pressed
                    running = False #stop running the program

                for key in basic_CONTROLS: #loops through all the control
                    if event.key == key: #if the key is pressed
                        if len(LETTER) != 15:  #if the farm name is not longer than 12 characters
                            LETTER = LETTER + event.unicode #puts the character into the list to be drawn on the screen
                
                if event.key == K_SPACE: #if the space bar is pressed
                    if len(LETTER) != 15: #if the farm name is not longer than 12 characters
                        LETTER = LETTER + ' ' #adds a space in the list

                if event.key == K_BACKSPACE: #if the backspace button is pressed
                    if len(LETTER) >= 4: #if the user has entered any characters
                        LETTER = LETTER[:-1] #remove the last character

            if event.type == MOUSEBUTTONDOWN: #if the mouse is pressed down
                if pygame.mouse.get_pressed()[0]: #if there has been a left click
                    for button in BUTTONS:
                        clicked = button.click(mouse_pos) #go through the clicked function of the button
                        if clicked: #if that button has been clicked
                            if button.button == 'cancel': #and if that button was the cancel button
                                LETTER = '-> ' #return the list to its original 
                            elif button.button == 'confirm': #if that button was confirm
                                switch_screen = True #switch the screen
                                draw = False #dont draw
  
        TEXT = []
        
        TEXT.append(Text('rolam', 80-(len(LETTER)), LETTER.lower(), True, (170,139,102), None, (150,128))) #appends this text to the list
        TEXT.append(Text('rolam', 48, 'Type In Your Farm Name', True, (170,139,102), None, (192,32) )) #appends this text to the list
        TEXT.append(Text('rolam', 24, ' - Name cant be greater than 12 characters -', True, (170,139,102), None, (210,80))) #appends this text to the list


        for button in BUTTONS:
            button.hover(mouse_pos) #checks if the mouse is hovering over the button
        if switch_screen:
            game(fullscreen,monitor_size,SCREEN,DISPLAY,clock,CONTROLS,LETTER.strip('-> ')) #opens the game screen
            running = False

        if draw:
            background = pygame.transform.smoothscale(background_image,(pygame.display.Info().current_w,pygame.display.Info().current_h)) #draw background
            SCREEN.blit(background,(0,0)) #blits the background to the screen
            SCREEN.blit(pygame.transform.scale(pygame.image.load('game/base.png'),(512,544)),(128,-16)) #draw panel
            for text in TEXT:
                SCREEN.blit(text.text,text.loc) #draw text
            for button in BUTTONS:
                SCREEN.blit(button.image,button.loc) #draw button
            DISPLAY.blit(SCREEN, (0, 0)) 
            pygame.display.update()
            clock.tick(60)
