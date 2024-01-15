import pygame
import pygame_menu as pm
from game_func import main

pygame.init()
size = width, height = 1200, 800
screen = pygame.display.set_mode(size)

RED = (255, 0, 0) 
GREEN = (0, 255, 0) 
WHITE = (255, 255, 255) 
BLACK = (0, 0, 0)
mainMenu = pm.Menu(title="ZOMBI VS PLANTS", 
                    width=500, 
                    height=500, 
                    theme=pm.themes.THEME_DARK) 
mainMenu.add.button("ИГРАТЬ",  main, font_color=BLACK, 
                    background_color=GREEN) 
mainMenu.add.label(title="") 
mainMenu.add.button(title="ВЫЙТИ", font_color=BLACK,
                    action=pm.events.EXIT, background_color=RED)
mainMenu.mainloop(screen)
pygame.quit()