import pygame
from sys import exit
from random import randint
import math
import os

SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

start_time = 0
player_life = 3

def lives():

   if player_life == 1:
       screen.blit(heart1_surface,heart1)
   elif player_life == 2:
       screen.blit(heart2_surface,heart2)
   elif player_life == 3:
       screen.blit(heart3_surface,heart3)
   



def display_score():
    current_time = int(pygame.time.get_ticks()/1000)-start_time #gets time in miliseconds > 1000 - seconds

    text_surface = font.render(f"Score: {current_time}", False, "#4a4a4a")  #1: text, 2: smoothing letters, 3: color
    text_rectangle = text_surface.get_rect(topright = (750,20))

    pygame.draw.rect(screen, "#00bfff", text_rectangle)
    pygame.draw.rect(screen, "#00bfff", text_rectangle, 6)

    screen.blit(text_surface, text_rectangle)

def save_high_score(score):
    high_score = load_high_score()
    if score > high_score:
        with open(os.path.join(SCRIPT_DIRECTORY, "high_score.txt"),"w") as file:    
            file.write(str(score))
    

def load_high_score():
    with open(os.path.join(SCRIPT_DIRECTORY, "high_score.txt")) as file:
        high_score = int(file.read())
       
    return high_score

def display_high_score():
    high_score = load_high_score()

    hs_surface = font.render(f"Highscore: {high_score}", False, "#4a4a4a")  #1: text, 2: smoothing letters, 3: color
    hs_rectangle = hs_surface.get_rect(topright = (500,20))
    screen.blit(hs_surface, hs_rectangle)

def enemy_movement(enemy_list):
    if enemy_list:
        for enemy_rect in enemy_list:
            enemy_rect.x -= 5 
            if enemy_rect.bottom >= 300 and enemy_rect.bottom <= 350:
                screen.blit(shoe1_surface,enemy_rect)
            elif enemy_rect.bottom >= 80 and enemy_rect.bottom <= 190:
                screen.blit(shoe3_surface,enemy_rect)
            elif enemy_rect.bottom >= 360 and enemy_rect.bottom <=500:
                screen.blit(shoe2_surface, enemy_rect) 
        enemy_list = [enemy for enemy in enemy_list if enemy.x > -100]
        return enemy_list
    else:
        return[]

def cracker_movement(cracker_list):
    if cracker_list:
        for crack_rect in cracker_list:
            crack_rect.x -= 5
            if crack_rect.bottom >= 100 and crack_rect.bottom <=800:
                screen.blit(cracker_surface, crack_rect)
        cracker_list = [fish for fish in cracker_list if fish.x > -100]
        return cracker_list
    else:
        return[]    


def collisions(player, enemy):
    global player_life
    current_time = int(pygame.time.get_ticks()/1000)-start_time
    if enemy:
        for enemy_rect in enemy:
            if player.colliderect(enemy_rect):
                player_life -= 1
                enemy.remove(enemy_rect)
                if player_life > 0:
                    return True
                elif player_life == 0:
                    save_high_score(current_time)
                    return False

    return True

def cracker_collisions(player,fish):
    global player_life
    current_time = int(pygame.time.get_ticks()/1000)-start_time
    if fish:
        for crack_rect in fish:
            if player.colliderect(crack_rect):
                if player_life < 3:
                    player_life += 1
                    fish.remove(crack_rect)
                elif player_life == 0:
                    save_high_score(current_time)
                    return False
    return True


def player_animation():
    
    global player_surface, player_index
    
    #display the jump surface when player is not on floor
    if player_rectangle.bottom < 390:
        #jump
        player_surface = player_jump
    #play walking animation if the player is on floor
    elif player_rectangle.bottom + player_Y_change >= 440:
        player_surface = player_down
    elif player_rectangle.bottom == 390:
        #walk
        player_index += 0.1
        if player_index >= len(player_walk): 
            player_index = 0
        player_surface = player_walk[int(player_index)]

pygame.init()

#screen setup
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Loki the Cat")

#time controlling frame rate
clock = pygame.time.Clock()
FPS = 60

#font settings
font = pygame.font.Font(os.path.join(SCRIPT_DIRECTORY, "font.ttf"), 25)
font_over = pygame.font.Font(os.path.join(SCRIPT_DIRECTORY, "font.ttf"), 80)


#background
sky_surface = pygame.image.load(os.path.join(SCRIPT_DIRECTORY, "sky.jpg"))
ground_surface = pygame.image.load(os.path.join(SCRIPT_DIRECTORY, "ground.png"))

bg_width = sky_surface.get_width()

#draw scrolling background
scroll = 0
tiles = math.ceil(800 / bg_width) +1



#game active/over
game_active = False

game_over = font_over.render("Game over", False, "#4a4a4a")  #1: text, 2: smoothing letters, 3: color
game_over_rectangle = game_over.get_rect(center = (400,100))

#welcome screen

font_name = pygame.font.Font(os.path.join(SCRIPT_DIRECTORY, "font.ttf"), 50)
font_name = font_name.render("Loki the Cat", False, "#4a4a4a")
font_name_rect = font_name.get_rect(center = (400, 80))

font_start = pygame.font.Font(os.path.join(SCRIPT_DIRECTORY, "font.ttf"), 40)
font_start = font_start.render("press space to start", False, "#4a4a4a")
font_start_rect = font_start.get_rect(center = (400, 150))


#enemies
shoe1_surface = pygame.image.load(os.path.join(SCRIPT_DIRECTORY, "shoe.jpg")).convert_alpha()
shoe1_rectangle = shoe1_surface.get_rect(midright = (600, 350))

shoe2_surface = pygame.image.load(os.path.join(SCRIPT_DIRECTORY, "shoe2.png")).convert_alpha()
shoe2_rectangle = shoe2_surface.get_rect(bottomright = (300, 150))

shoe3_surface = pygame.image.load(os.path.join(SCRIPT_DIRECTORY, "shoe3.png")).convert_alpha()
shoe3_rectangle = shoe3_surface.get_rect(bottomright = (300, 150))

#player
player_walk1 = pygame.image.load(os.path.join(SCRIPT_DIRECTORY, "cat1.png")).convert_alpha()
player_walk2 = pygame.image.load(os.path.join(SCRIPT_DIRECTORY, "cat2.png")).convert_alpha()
player_walk = [player_walk1, player_walk2]
player_index = 0
player_surface = player_walk[player_index]

player_jump = pygame.image.load(os.path.join(SCRIPT_DIRECTORY, "cat3.png")).convert_alpha()
player_down = pygame.image.load(os.path.join(SCRIPT_DIRECTORY, "cat4.png")).convert_alpha()
player_rectangle = player_walk1.get_rect(midbottom = (70,390)) #takes surfaces and draws rectangle around it

#player lives
heart1_surface = pygame.image.load(os.path.join(SCRIPT_DIRECTORY, "heart1.png")).convert_alpha()
heart1 = heart1_surface.get_rect(topright = (100,20))

heart2_surface = pygame.image.load(os.path.join(SCRIPT_DIRECTORY, "heart2.png")).convert_alpha()
heart2 = heart2_surface.get_rect(topright = (100,20))

heart3_surface = pygame.image.load(os.path.join(SCRIPT_DIRECTORY, "heart3.png")).convert_alpha()
heart3 = heart3_surface.get_rect(topright = (100,20))

#heal
cracker_surface = pygame.image.load(os.path.join(SCRIPT_DIRECTORY, "heal.png")).convert_alpha()
cracker_rect = cracker_surface.get_rect(bottomright = (300,150))

cracker_timer = pygame.USEREVENT +1
pygame.time.set_timer(cracker_timer, 10000)
cracker_rect_list = []

#player moving
player_gravity = 0 #jump

player_X_change = 0
player_Y_change = 0


#intro screen
player_stand = pygame.image.load(os.path.join(SCRIPT_DIRECTORY, "loki.jpg")).convert_alpha()
player_st_rectangle = player_stand.get_rect(center = (400,300))

#timer
enemy_timer = pygame.USEREVENT + 1 
pygame.time.set_timer(enemy_timer, 3000)
enemy_rectangle_list = []

while True:
    #game quitting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit() #from the sys module, stopping while loop
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: #jump on space down
                    if player_rectangle.bottom >= 390:
                        player_gravity = -29
                if event.key == pygame.K_d:
                    player_X_change += 1
                    scroll -= 2
                if event.key == pygame.K_a:
                    player_X_change -= 1
                    scroll += 2
                if event.key == pygame.K_s:
                    player_Y_change = 50
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d or event.key == pygame.K_a:
                    player_X_change = 0
                if event.key == pygame.K_s:
                    player_Y_change = 0

        if game_active:
            if event.type == pygame.KEYDOWN:
                game_active = True
                
        else: 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                shoe1_rectangle.left = 800
                shoe2_rectangle.left = 1500
                shoe3_rectangle.left = 900
                cracker_rect.left = 1100
                start_time = int(pygame.time.get_ticks()/1000)
                player_life = 3

        if event.type == enemy_timer and game_active: #random enemy spawn
            enemy_type = randint(1,4) #pics numbers 1-4
          
            if enemy_type == 1: 
                enemy_rectangle_list.append(shoe1_surface.get_rect(bottomright = (randint(900,1100), randint(300, 350))))
            elif enemy_type == 2:
                enemy_rectangle_list.append(shoe3_surface.get_rect(bottomright = (randint(900,1100), randint(80,190))))
            elif enemy_type == 3:
                enemy_rectangle_list.append(shoe2_surface.get_rect(bottomright = (randint(900,1100), randint(360,500))))

        if event.type == cracker_timer and game_active: #cracker collision
            cracker_rect_list.append(cracker_surface.get_rect(bottomright = (randint(900,1100), randint(100,800))))
                
            
  

    if game_active:
        #draw scrolling background
        for i in range(0,tiles):
            screen.blit(sky_surface, (i*800 + scroll,0))
            scroll -= 3
        #reset scroll
        if abs(scroll) > 800:
            scroll = 0

        #draw all the screen elements
        screen.blit(ground_surface, (-30,290))
        display_score()
        lives()
        
        #draw elements with positions
        screen.blit(shoe1_surface, shoe1_rectangle)
        screen.blit(shoe2_surface, shoe2_rectangle)

        screen.blit(cracker_surface,cracker_rect)
 

        #player, player gravity
        player_gravity += 1
        player_rectangle.y += player_gravity


        if player_rectangle.bottom >= 390: #floor collision
            player_rectangle.bottom = 390

        player_animation()

          
        #screen boundaries
        if player_rectangle.x <= 0:
            player_rectangle.x = 0
        elif player_rectangle.x >= 700:
            player_rectangle.x = 700


        # update the position of the player_rectangle
        player_rectangle.x += player_X_change
        player_rectangle.y += player_Y_change

        # draw the rectangle (or your sprite) at the new position
        screen.blit(player_surface, (player_rectangle))
        
        #enemy movement
        enemy_rectangle_list = enemy_movement(enemy_rectangle_list) 

        #cracker movement
        cracker_rect_list = cracker_movement(cracker_rect_list)


        #collisions
        game_active = collisions(player_rectangle, enemy_rectangle_list)

        game_active = cracker_collisions(player_rectangle, cracker_rect_list)

        #game over
        if player_life <= 0:
            game_active = False

            
    else:
        #welcome screen
        screen.fill("#a6a6a4")
        screen.blit(font_name, font_name_rect)
        screen.blit(font_start, font_start_rect)
        screen.blit(player_stand, player_st_rectangle)
        player_rectangle.midbottom = (80,300)
        player_gravity = 0
        enemy_rectangle_list.clear()
        cracker_rect_list.clear()
        display_high_score()

    pygame.display.update()
    clock.tick(FPS) #running not faster than 6*/sec
