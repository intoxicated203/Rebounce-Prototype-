import pygame
from pygame.constants import *
import framework
import sys
import time

pygame.init()
pygame.font.init()

WHITE = pygame.Color(255, 255, 255)
MENU_SHADE = pygame.Color(26, 26, 26)

font = pygame.font.SysFont('arial', 40)

def draw_bg(window, screenshot, shade):
    window.blit(screenshot, (0, 0))
    window.blit(shade, (0, 0))

def menu(window, menu, screenshot):
    shade = pygame.Surface((window.get_width(), window.get_height()))
    shade.set_alpha(200)
    shade.fill(MENU_SHADE)

    last_time = time.time()

    while True:

        delta_time, last_time = framework.get_delta_time(last_time)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return not menu, delta_time

        draw_bg(window, screenshot, shade)
        window.blit(font.render('menu', True, WHITE), (0, 0))
        pygame.display.update()
