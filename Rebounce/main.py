import pygame
from pygame.locals import *
import framework
import menus
import os
import time
import random

pygame.init()
pygame.font.init()

# VARIABLES----------------------------------------------------------------------------------------
# RGB & Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (40, 40, 40)
TEXT_GRAY = (64, 64, 64)

# Monitor
WIDTH = 1200 
HEIGHT = 675
MONITOR_SIZE = (pygame.display.Info().current_w, pygame.display.Info().current_h)
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('rebounce.')
FPS = 120

# Fonts
FPS_FONT = pygame.font.Font(os.path.join('assets', 'fonts', 'times new roman.ttf'), 40)
HEALTH_FONT = pygame.font.Font(os.path.join('assets', 'fonts', 'GothamMedium_1.ttf'), 75)
SCORE_FONT = pygame.font.Font(os.path.join('assets', 'fonts', 'GothamMedium_1.ttf'), 200)

# USEREVENTS
SPAWN_BALL = USEREVENT + 0
FPS_REFRESH = USEREVENT + 1

# Settings
PONG_SPEED = 10 # in 60 fps
PONG_WIDTH = 25
PONG_HEIGHT = 100
BALL_SIZE = 18
BALLY_OFFSET = 18
MAX_BOUNCE_TIME = 6
PONG_HEALTH = 5
DASH_MULTIPLIER = 2
MAX_DASH_TIME = 25
DASH_RESET_TIME = -10
MAX_DASH_FRAMES = 10
MAX_DASH_FRAME_DURATION = 500
FIRST_DASH_RGB = 128
PONG_FADE_RATE = 5

# CLASSES------------------------------------------------------------------------------------------
class Ball:
    def __init__(self, center_cord, side, x_speed, y_speed):
        self.pos = list(center_cord)
        self.rect = pygame.Rect(center_cord[0] - BALL_SIZE//2, center_cord[1] - BALL_SIZE//2, BALL_SIZE*2, BALL_SIZE*2)
        self.side = side # 0 is left, 1 is right
        self.life = random.randint(3, 5)
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.inscreen = False
        self.color = WHITE
        self.fade_rate = 0

    def bounce(self, direction, life_decrease=False):
        if direction == 'x':    self.x_speed *= -1
        if direction == 'y':    self.y_speed *= -1
        if life_decrease:       self.life -= 1

    def move(self, delta_time, pong):
        #self.pos[0] += self.x_speed * delta_time
        self.rect.x += self.x_speed * delta_time
        
        if self.rect.colliderect(pong): #or (self.side == 1 and self.rect.x <= 0) or (
            #self.side == 0 and self.rect.bottomright[0] >= window_dimension[0]):
            self.bounce('x')
            if self.x_speed < 0:    self.rect.right = pong.left
            else:                   self.rect.left = pong.right

        #self.pos[1] += self.y_speed * delta_time
        self.rect.y += self.y_speed * delta_time

        if self.rect.colliderect(pong): # or (self.side == 1 and self.rect.y <= 0) or (
            #self.side == 0, self.rect.bottomright[1] >= window_dimension[1]):
            self.bounce('y')
            #if self.y_speed > 0 :   self.rect.top = pong.bottom
            #else:                   self.rect.bottom = pong.top
            
    def handle_wall_collision(self):
        width = window.get_width()
        height = window.get_height()

        # Left~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if self.side == 0:
            if not self.inscreen:   x_bound_1 = BALL_SIZE * 2
            else:               x_bound_1 = -BALL_SIZE

            if x_bound_1 <= self.rect.x <= width // 2 - BALL_SIZE * 2:
                self.inscreen = True
                if self.rect.x <= 0:                    self.bounce('x', True)
                if self.rect.y <= 0:                    self.bounce('y', True)
                if self.rect.bottomright[1] >= height:  self.bounce('y', True)


            # Right~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if self.side == 1:
            if not self.inscreen:   x_bound_2 = width - BALL_SIZE * 2
            else:                   x_bound_2 = width + BALL_SIZE
            
            if width // 2 <= self.rect.x <= x_bound_2:
                self.inscreen = True
                if self.rect.bottomright[0] >= width:   self.bounce('x', True)
                if self.rect.y <= 0:                    self.bounce('y', True)
                if self.rect.bottomright[1] >= height:  self.bounce('y', True)

    def draw(self):
        #pygame.draw.circle(window, BLACK, self.pos, BALL_SIZE + 7)
        self.color = tuple([rgb - self.fade_rate for rgb in self.color])
        if self.color[0] >= DARK_GRAY[0]:
            pygame.draw.circle(window, pygame.Color(*self.color, self.color[0]), (self.rect.centerx, self.rect.centery), BALL_SIZE)
        #pygame.draw.rect(window, BLACK, self.rect)

# FUNCTIONS----------------------------------------------------------------------------------------
# Draw~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def draw_window():
    window.fill(DARK_GRAY)

def draw_pong(pong):
    pygame.draw.line(window, WHITE,
     (window.get_width() // 2, 0), (window.get_width() // 2, window.get_height()))
    #pygame.draw.rect(window, BLACK, pong.inflate(20, 20))
    pygame.draw.rect(window, WHITE, pong)

def draw_pong_fades(pong_fade_list):
    for pong_fade in pong_fade_list:
        #if current_frame - pong_pos[1] > MAX_DASH_FRAMES * 2:
        #    last_pong_pos.remove(pong_pos)
        #if current_frame - pong_pos[1] <= MAX_DASH_FRAME_DURATION:
        #rgb = 255
        if pong_fade[1] >= DARK_GRAY[0] + DARK_GRAY[0] % PONG_FADE_RATE:
            pygame.draw.rect(window, (pong_fade[1], pong_fade[1], pong_fade[1]), pong_fade[0])#pygame.Color(80, 80, 80, pong_fade[2]), pong_fade[0])
            pong_fade[1] -= PONG_FADE_RATE #pong_fade[2] -= 25
        else:
            pong_fade_list.remove(pong_fade)

def draw_balls(balls):
    for ball in balls:
        ball.draw()

def draw_fps(fps_overlay, fps_toggle):
    if fps_toggle and fps_overlay:
        window.blit(fps_overlay, (0, 0))

def draw_score(score_text, score_pos):
    window.blit(score_text, score_pos)

def draw_health(health_text, health_pos):
    window.blit(health_text, health_pos)

# System~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def switch_screen_mode(fullscreen):
    new_fullscreen = not fullscreen
    if new_fullscreen:
            new_window = pygame.display.set_mode(MONITOR_SIZE, FULLSCREEN)
    else:
            pygame.display.quit() 
            pygame.display.init()
            new_window = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption('pongz')
    return new_window, new_fullscreen

def render_score(score):
    score_text = SCORE_FONT.render(str(score), True, TEXT_GRAY)

    score_width, score_height = SCORE_FONT.size(str(score))
    score_x = window.get_width()//2 - score_width//2
    score_y = window.get_height()//2 - score_height//2

    return score_text, (score_x, score_y, score_width, score_height)

def render_health(health, score_pos):
    health_text = HEALTH_FONT.render(str(health), True, TEXT_GRAY)

    health_height = HEALTH_FONT.size(str(health))[1]
    health_x = score_pos[0] + score_pos[2]
    health_y = score_pos[1] - health_height

    return health_text, (health_x, health_y)

# Logic~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def spawn_ball(balls, delta_time):
    width = window.get_width()
    height = window.get_height()

    ballx = random.choice([[-30, 0], [width + 30, 1]])
    bally = random.randint(height // 2 - BALLY_OFFSET, height // 2 + BALLY_OFFSET)
    if ballx[1] == 0:
        x_speed = random.randint(8, 10)
    elif ballx[1] == 1:
        x_speed = -random.randint(8, 10)
    y_speed = random.choice([-1, 1]) * random.randint(5, 7)
    balls.append(Ball(center_cord=(ballx[0], bally), side=ballx[1],
    x_speed=x_speed * delta_time, y_speed=y_speed * delta_time))

def delete_ball(balls, health, score):
    for ball in balls:
        if ((ball.inscreen) and ((ball.rect.x <= -BALL_SIZE * 2) or (ball.rect.y <= -BALL_SIZE * 2) or (
        ball.rect.x >= window.get_width()) or (ball.rect.y >= window.get_width()))):
            if health >= 1:
                health -= 1
            balls.remove(ball)

        if health == 0:
            balls.clear()

        if ball.color[0] < DARK_GRAY[0]:
            balls.remove(ball)

        if ball.life == 0:
            score += 1
            ball.x_speed = 0
            ball.y_speed = 0
            ball.fade_rate = 5

    return health, score

def handle_movement(pong, mod, speed, last_pong_pos, dash_timer, direction):
    if direction == 0: 
        speed *= -1  # Going up
        cond = (direction == 0) and (pong.y + speed * DASH_MULTIPLIER >= 0)
    else:
        cond = (direction == 1) and (pong.y + speed * DASH_MULTIPLIER <= window.get_height())

    if mod & KMOD_LSHIFT and cond and DASH_RESET_TIME <= dash_timer <= MAX_DASH_TIME:
            pong.y += speed * DASH_MULTIPLIER
            dash_timer += 1
            #if dash_timer % 1 == 0:
            last_pong_pos.append([pong.copy(), FIRST_DASH_RGB])
    else:
        pong.y += speed
    #if dash_timer % 5 == 0:
    #    last_pong_pos.append([pong.copy(), current_frame, FIRST_DASH_RGB])


    return pong, dash_timer

# MAIN---------------------------------------------------------------------------------------------
def main():
    global window
    #global current_frame

    pong = pygame.Rect(window.get_width() // 2 - PONG_WIDTH // 2,
                       window.get_height() // 2 - PONG_HEIGHT // 2, PONG_WIDTH, PONG_HEIGHT)
    balls = []

    pygame.time.set_timer(SPAWN_BALL, 3000)
    pygame.time.set_timer(FPS_REFRESH, 500, 1)
    fps_overlay = None
    fps_toggle = False
    health = PONG_HEALTH
    score = 0
    last_pong_pos = []
    dash_timers = [0, 0]

    fullscreen = False
    menu = False

    run = True
    clock = pygame.time.Clock()
    last_time = time.time()
    #current_frame = 0

    while run:
        # width & height aliases~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        width = window.get_width()
        height = window.get_height()
        screenshot = window.subsurface(pygame.Rect(0, 0, width, height)).copy()

        # Delta time~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        delta_time, last_time = framework.get_delta_time(last_time)
        speed = PONG_SPEED * delta_time

        #current_frame += 1
        clock.tick(FPS)

        # Events-----------------------------------------------------------------------------------
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                run = False
                break
            
            # Keyboard inputs (not hold-able)~~~~~~~~~~~~~~~~~~~~~~~~
            if event.type == KEYDOWN:
                if event.key == K_f:
                    #if event.mod & KMOD_LCTRL:
                        window, fullscreen = switch_screen_mode(fullscreen)
                        width = window.get_width()
                        height = window.get_height()
                        pong.x = width // 2 - 25 // 2
                        if pong.bottomleft[1] >= height:
                            pong.y = height - pong.height

                if event.key == K_q:
                    fps_toggle = not fps_toggle
                    if fps_toggle:
                        fps_overlay = None
                        pygame.time.set_timer(FPS_REFRESH, 20, 1)

                if event.key == K_ESCAPE:
                    #if not menu:
                    #    for ball in balls:
                    #        ball.x_speed /= delta_time
                    #        ball.y_speed /= delta_time
                    menu, delta_time = menus.menu(window, not menu, screenshot)
                    #if not menu:
                    #    for ball in balls:
                    #        ball.x_speed *= delta_time
                    #        ball.y_speed *= delta_time
                    #speed = PONG_SPEED * delta_time
                    while menu:
                        pygame.time.wait(1000)


            # USEREVENTS checks~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            if event.type == SPAWN_BALL:
                if health >= 1:
                    spawn_ball(balls, delta_time)

            if event.type == FPS_REFRESH:
                if fps_toggle and delta_time != 0:
                    fps_overlay = FPS_FONT.render(
                        str(int(clock.get_fps())), True, WHITE)
                    pygame.time.set_timer(FPS_REFRESH, 1500)

            # Keyboard inputs (hold-able)~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            keydowns = pygame.key.get_pressed()
            mod = pygame.key.get_mods()

        if not run: break

        # Logic------------------------------------------------------------------------------------
        # Handle movement~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if (keydowns[K_w] or keydowns[K_UP]) and (pong.y - speed > 0):
            pong, dash_timers[0] = handle_movement(pong, mod, speed,last_pong_pos, dash_timers[0], direction=0)
        elif not keydowns[K_w] and not keydowns[K_UP]:
            dash_timers[0] = DASH_RESET_TIME

        if (keydowns[K_s] or keydowns[K_DOWN]) and (pong.bottomleft[1] + speed < height):
            pong, dash_timers[1] = handle_movement(pong, mod, speed, last_pong_pos, dash_timers[1], direction=1)
        elif not keydowns[K_s] and not keydowns[K_DOWN]:
            dash_timers[1] = DASH_RESET_TIME

        # Handle balls~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        for ball in balls:
            if not menu:
                ball.move(delta_time, pong)    
            ball.handle_wall_collision()
        
        # Handle health & delete balls~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        health, score = delete_ball(balls, health, score)
        score_text, score_pos = render_score(score)
        health_text, health_pos = render_health(health, score_pos)

        # Display----------------------------------------------------------------------------------
        draw_window()
        draw_score(score_text, score_pos)
        draw_health(health_text, health_pos)
        draw_pong_fades(last_pong_pos)
        draw_pong(pong)
        #pygame.draw.circle(window, WHITE, (50, 50), 18)
        draw_balls(balls)
        draw_fps(fps_overlay, fps_toggle)
        pygame.display.update()

if __name__ == "__main__":
    main()
