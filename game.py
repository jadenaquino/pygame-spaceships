from turtle import right
import pygame
import os
pygame.init()
pygame.mixer.init()

# the dimension sizes of my game
WIDTH, HEIGHT, = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Attack on planet namek!")

#The background color
GREEN = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (255, 255, 0)
# size of the border
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("space pictures","bang.mp3" ))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("space pictures","laser7.mp3"))

HEALTH_FONT = pygame.font.SysFont('times new roman', 40, GREEN)
WINNER_FONT = pygame.font.SysFont('hangyaku', 40, GREEN)

#The frames that you will play
FPS = 60
VEL = 5
BULLET_VEL = 8
MAX_BULLETS = 3
#The size of both spaceships
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 100, 100

RED_HIT = pygame.USEREVENT + 1
BLUE_HIT = pygame.USEREVENT + 2

#loading in the spaceships and rotating until there facing each other
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('space pictures', 'red spaceship.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 360)
BLUE_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('space pictures', 'blue spaceship.png'))
BLUE_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    BLUE_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 360)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('space pictures', 'namek.png')), (WIDTH, HEIGHT))


def draw_window(red_bullets, blue_bullets, red, blue, red_health, blue_health ):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    #The current positions of where the spaceships are
    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, GREEN)
    blue_health_text = HEALTH_FONT.render(
        "Health: " + str(blue_health), 1, GREEN)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(blue_health_text, (10, 10))

    WIN.blit(RED_SPACESHIP, (red.x , red.y))
    WIN.blit(BLUE_SPACESHIP, (blue.x, blue.y))



    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in blue_bullets:
        pygame.draw.rect(WIN, BLUE, bullet)
    
    pygame.display.update()



#Controls for the red spaceship
def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_a] and red.x - VEL > 0: #LEFT
            red.x -= VEL
    if keys_pressed[pygame.K_d] and red.x + VEL + red.width < BORDER.x: #RIGHT
            red.x += VEL
    if keys_pressed[pygame.K_w] and red.y - VEL > 0: #UP
            red.y -= VEL
    if keys_pressed[pygame.K_s] and red.y + VEL + red.height < HEIGHT - 1: #DOWN
            red.y += VEL

#controls for the blue spaceship
def blue_handle_movement(keys_pressed, blue):
    if keys_pressed[pygame.K_LEFT] and blue.x - VEL > BORDER.x + BORDER.width: #LEFT
            blue.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and blue.x + VEL + blue.width < WIDTH: #RIGHT
            blue.x += VEL
    if keys_pressed[pygame.K_UP] and blue.y - VEL > 0: #UP
            blue.y -= VEL
    if keys_pressed[pygame.K_DOWN] and blue.y + VEL + blue.height < HEIGHT - 1: #DOWN
            blue.y += VEL

bulletLandBlue, bulletLandRed = 0, 0

def handle_bullets(red, blue, red_bullets, blue_bullets):
    global bulletLandBlue
    global bulletLandRed
    for bullet in red_bullets:
        bullet.x += BULLET_VEL
        if blue.colliderect(bullet):
            print("b")
            pygame.event.post(pygame.event.Event(RED_HIT))
            bulletLandRed = bulletLandRed +1
            red_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)
            bulletLandRed = bulletLandRed -1
    
    
    for bullet in blue_bullets:
        bullet.x -= BULLET_VEL
        if red.colliderect(bullet):
            bulletLandBlue = bulletLandBlue+1
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            blue_bullets.remove(bullet)
        elif bullet.x < 0:
            blue_bullets.remove(bullet)
            bulletLandBlue = bulletLandBlue -1

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, GREEN)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    blue = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    global bulletLandBlue
    global bulletLandRed
    leftDebounce, rightDebounce = True, True

    red_bullets = []
    blue_bullets = []

    red_health = 10
    blue_health = 10

    clock = pygame.time.Clock()
    run = True
    cacheTimer = 0
    
    while run:
        clock.tick(45)
        cacheTimer =cacheTimer +1
        if (cacheTimer >= 22):
            cacheTimer =0
            leftDebounce, rightDebounce = True, True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT and len(red_bullets) < MAX_BULLETS and leftDebounce == True:
                
                leftDebounce = False
                bullet = pygame.Rect(
                    red.x + red.width, red.y + red.height//2 - 2, 10, 5)
                red_bullets.append(bullet)
                BULLET_FIRE_SOUND.play()
            if event.key == pygame.K_RSHIFT and len(blue_bullets) < MAX_BULLETS and rightDebounce == True:
                leftDebounce = False
                bullet = pygame.Rect(
                    blue.x-10, blue.y + blue.height//2 - 2, 10, 5)
                blue_bullets.append(bullet)
                BULLET_FIRE_SOUND.play()
        
        if bulletLandBlue >= 1:
            bulletLandBlue = bulletLandBlue-1
            blue_health = blue_health - 1
            BULLET_HIT_SOUND.play()

        if bulletLandRed >= 1:
            bulletLandRed = bulletLandRed-1
            red_health =red_health  -1
            BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "the spartans have won"

        if blue_health <= 0:
            winner_text = "the alien covanent has won!"
        
        if winner_text != "":
            draw_winner(winner_text)
            break

        
        keys_pressed = pygame.key.get_pressed()
        red_handle_movement(keys_pressed, red)
        blue_handle_movement(keys_pressed, blue)
        
        handle_bullets(red, blue, red_bullets, blue_bullets)
        
        draw_window(red_bullets, blue_bullets, red, blue, red_health, blue_health)

    main()
            

if __name__ == "__main__":
    main()