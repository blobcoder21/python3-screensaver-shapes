import pygame
import os
import struct
import time
import math

# Constants
WIDTH, HEIGHT = 800, 480
TIMEOUT_THRESHOLD = 1  # Time threshold to ignore accidental keypresses (in seconds)
CLEAR_TIMES = [5, 3]  # Time intervals to clear the screen (5 seconds initially, then 3)
SHAPE_SIDES = 12  # Number of sides for the dodecagon (12-gon)

# Init Pygame
pygame.init()

# Force resolution to 800x480 (WVGA) to prevent "off-screen" issues
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME | pygame.FULLSCREEN)
pygame.mouse.set_visible(False)

clock = pygame.time.Clock()
running = True
last_input_time = time.time()
clear_time = time.time() + CLEAR_TIMES[0]  # Initial clear time after 5 seconds
clear_interval = CLEAR_TIMES[0]  # First interval is 5 seconds

def rand_byte(n=1):
    return os.urandom(n)

def rand_int(min_val, max_val):
    r = struct.unpack("I", rand_byte(4))[0]
    return min_val + (r % (max_val - min_val + 1))

def rand_color():
    return tuple(rand_int(0, 255) for _ in range(3))

def draw_random_shape():
    shape = rand_int(0, 3)  # 0 for circle, 1 for rect, 2 for line, 3 for polygon (12-gon)
    color = rand_color()
    x = rand_int(0, WIDTH)
    y = rand_int(0, HEIGHT)
    size = rand_int(20, 120)

    if shape == 0:  # circle
        pygame.draw.circle(screen, color, (x, y), size // 2)
    elif shape == 1:  # rect
        pygame.draw.rect(screen, color, pygame.Rect(x, y, size, size))
    elif shape == 2:  # line
        x2 = rand_int(0, WIDTH)
        y2 = rand_int(0, HEIGHT)
        pygame.draw.line(screen, color, (x, y), (x2, y2), rand_int(1, 5))
    elif shape == 3:  # polygon (12-gon)
        points = []
        angle_step = 2 * math.pi / SHAPE_SIDES
        for i in range(SHAPE_SIDES):
            angle = i * angle_step
            px = x + size * math.cos(angle)
            py = y + size * math.sin(angle)
            points.append((px, py))
        pygame.draw.polygon(screen, color, points)

# Main loop
while running:
    # Periodically clear the screen
    if time.time() > clear_time:
        screen.fill((0, 0, 0))  # Fill screen with black
        pygame.display.flip()
        clear_time = time.time() + clear_interval  # Set the next clear time

        # After the first clear, set interval to 3 seconds
        if clear_interval == CLEAR_TIMES[0]:
            clear_interval = CLEAR_TIMES[1]

    # Draw random shape
    draw_random_shape()
    pygame.display.flip()
    clock.tick(30)

    for event in pygame.event.get():
        # Ignore accidental inputs that are too fast (within TIMEOUT_THRESHOLD)
        if time.time() - last_input_time < TIMEOUT_THRESHOLD:
            continue

        if event.type in [pygame.KEYDOWN, pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.QUIT]:
            running = False
            break
        last_input_time = time.time()  # Update the time of the last input
