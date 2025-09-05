import pygame #imports the module pygame
from menu import main_menu #imports my main menu function from a separate file named, 'menu'

pygame.init() #initialises pygame
pygame.display.set_caption('Stardew Valley') #sets the caption of the window of my game to 'Stardew Valley'
SCREEN_WIDTH = 1920 #sets screen width
SCREEN_HEIGHT = 1080 #sets screen height
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT) #creates a screen size list that can easily be called apon
#screen are the dimensions used in the code to ensure there is no issue when the player wishes to change their window size

clock = pygame.time.Clock() #clock
monitor_size = [pygame.display.Info().current_w,pygame.display.Info().current_h] #fetches the users monitor size, needs to be done
                                                                                #before the DISPLAY is set as if its done after it
                                                                                 #would return those dimensionss
TILE_SIZE = 64 #tile size
WINDOW_SIZE = (TILE_SIZE*12, TILE_SIZE*8) #window size based on tile size so it is 12 tiles across and 8 in height
DISPLAY = pygame.display.set_mode(WINDOW_SIZE, pygame.SCALED)#create a display that makes use of the pygame.SCALED attribute

SCREEN = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)) #creates the SCREEN

main_menu(monitor_size,SCREEN,DISPLAY,clock,SCREEN_SIZE) #opens the main menu function from the separate file


