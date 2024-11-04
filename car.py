import pygame
import sys
import math
import random
from constants import *

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Manual and Automatic Lane Detection with Obstacle")


car_angle = 0 
car_speed = 2 
car_x = WIDTH // 2 + TRACK_RADIUS * math.cos(math.radians(car_angle))
car_y = HEIGHT // 2 + TRACK_RADIUS * math.sin(math.radians(car_angle))


automatic_mode = False
object_exists = True

object_angle = random.randint(0, 359)
object_x = WIDTH // 2 + TRACK_RADIUS * math.cos(math.radians(object_angle))
object_y = HEIGHT // 2 + TRACK_RADIUS * math.sin(math.radians(object_angle))
while(object_x == car_x and object_y==car_y):
    object_angle = random.randint(0, 359)
    object_x = WIDTH // 2 + TRACK_RADIUS * math.cos(math.radians(object_angle))
    object_y = HEIGHT // 2 + TRACK_RADIUS * math.sin(math.radians(object_angle))


button_rect = pygame.Rect(10, 10, 200, 40)
object_erase_button_rect = pygame.Rect(300,10,150,40)


running = True
while running:
    screen.fill(GRAY)  
    
    pygame.draw.circle(screen, BLACK, (WIDTH // 2, HEIGHT // 2), TRACK_RADIUS + LANE_WIDTH // 2)
    pygame.draw.circle(screen, GRAY, (WIDTH // 2, HEIGHT // 2), TRACK_RADIUS - LANE_WIDTH // 2)
    
    mouse_pos = pygame.mouse.get_pos()

    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect)
    else:
        if automatic_mode==True:
            pygame.draw.rect(screen, RED, button_rect)
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
        
    font = pygame.font.SysFont(None, 24)
    button_text = font.render("Toggle Automatic Mode", True, WHITE)
    screen.blit(button_text, (button_rect.x + 10, button_rect.y + 10))

    if object_erase_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen,BUTTON_HOVER_COLOR, object_erase_button_rect)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, object_erase_button_rect)
    
    font = pygame.font.SysFont(None, 24)
    button_text = font.render("Toggle object", True, WHITE)
    screen.blit(button_text, (object_erase_button_rect.x + 10, object_erase_button_rect.y + 10))

    
    if object_exists:
        pygame.draw.circle(screen, OBJECT_COLOR, (int(object_x), int(object_y)), 10)

    
    # lane detection
    dist_of_car_from_center = math.sqrt((car_x - WIDTH // 2) ** 2 + (car_y - HEIGHT // 2) ** 2)
    if INNER_BOUNDARY <= dist_of_car_from_center <= OUTER_BOUNDARY:
        car_color = GREEN
    else:
        car_color = RED  


    car_surface = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(car_surface, car_color, (0, 0, CAR_WIDTH, CAR_HEIGHT))
    rotated_car = pygame.transform.rotate(car_surface, -car_angle)
    car_rect = rotated_car.get_rect(center=(car_x, car_y))
    screen.blit(rotated_car, car_rect.topleft)

    
    # object detection
    distance_to_object = math.sqrt((car_x - object_x) ** 2 + (car_y - object_y) ** 2)

    if object_exists and distance_to_object < STOP_DISTANCE * 3:
        car_speed = max(0.1, CAR_MAX_SPEED * (distance_to_object / (STOP_DISTANCE * 3)))
        if distance_to_object <= STOP_DISTANCE:
            car_speed = 0  
    else:
        car_speed = CAR_MAX_SPEED  



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                automatic_mode = not automatic_mode  
            if object_erase_button_rect.collidepoint(event.pos):
                object_exists = not object_exists
 

    if automatic_mode and car_speed > 0:
        car_angle = (car_angle - car_speed) % 360 
        car_x = WIDTH // 2 + TRACK_RADIUS * math.cos(math.radians(car_angle))
        car_y = HEIGHT // 2 + TRACK_RADIUS * math.sin(math.radians(car_angle))
    else:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:  
            car_x += car_speed * math.cos(math.radians(car_angle))
            car_y += car_speed * math.sin(math.radians(car_angle))
        elif keys[pygame.K_DOWN]:  
            car_x -= car_speed * math.cos(math.radians(car_angle))
            car_y -= car_speed * math.sin(math.radians(car_angle))
        if keys[pygame.K_LEFT]:
            car_angle += 5
        if keys[pygame.K_RIGHT]:
            car_angle -= 5


    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()
sys.exit()
