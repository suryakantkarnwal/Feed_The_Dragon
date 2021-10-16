import pygame,random

#Initialize Pygame
pygame.init()

 #Set display surface
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 500
display_surface = pygame.display.set_mode(( WINDOW_WIDTH , WINDOW_HEIGHT))
pygame.display.set_caption('Feed The Dragon')

#FPS and clock
FPS = 60
clock = pygame.time.Clock()


#Set game values
PLAYER_STARTING_LIVES = 5
PLAYER_VELOCITY = 10
COIN_STARTING_VELOCITY = 10
COIN_ACCELERATION = .5
BUFFER_DISTANCE = -100


score = 0
player_lives = PLAYER_STARTING_LIVES
coint_velocity = COIN_STARTING_VELOCITY


#Set colors
GREEN = (0,255,0)
DARK_GREEN = (10,50,10)
WHITE = (255,255,255)
BLACK = (0,0,0)

#Set fonts
font = pygame.font.Font('AttackGraffiti.ttf',32)

#Set text
score_text = font.render("Score: "+str(score),True , GREEN , DARK_GREEN)
score_rect =  score_text.get_rect()
score_rect.topleft = (10, 10)

title_text = font.render("Feed The Dragon",True , GREEN , BLACK)
title_rect = title_text.get_rect()
title_rect.centerx = WINDOW_WIDTH//2
title_rect.y = 10

lives_text = font.render("Lives: "+ str(player_lives),True , GREEN, DARK_GREEN)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH - 10 , 10)

game_over_text = font.render("GAME OVER",True, GREEN ,DARK_GREEN)
game_over_rect =  game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH//2 , WINDOW_HEIGHT//2)

continue_text = font.render("Press any key to start again",True , GREEN , BLACK)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 30)

#Set sound and music
coin_sound = pygame.mixer.Sound('coin_sound.wav')
miss_sound = pygame.mixer.Sound('miss_sound.wav')
miss_sound.set_volume(.1)
pygame.mixer.music.load('ftd_background_music.wav')

#Set Image
dragon_image = pygame.image.load('dragon_right.png')
dragon_rect = dragon_image.get_rect()
dragon_rect.left = 8
dragon_rect.centery = WINDOW_HEIGHT//2

coin_image = pygame.image.load('coin.png')
coin_rect = coin_image.get_rect()
coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)


#Game Loop
pygame.mixer.music.play(-1,0.0)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #Dragon movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and dragon_rect.top > 64 :
        dragon_rect.y -= PLAYER_VELOCITY
    if keys[pygame.K_DOWN] and dragon_rect.bottom < WINDOW_HEIGHT:
        dragon_rect.y += PLAYER_VELOCITY

    #Coin movement
    if coin_rect.x < 0:
        player_lives -= 1
        miss_sound.play()
        coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)
    else:
        coin_rect.x -= coint_velocity

    #Collsion event
    if dragon_rect.colliderect(coin_rect):
        score +=1
        coin_sound.play()
        coint_velocity += COIN_ACCELERATION
        coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)
    
    #Update score and lives after collision
    score_text = font.render("Score: "+str(score),True , GREEN , DARK_GREEN)
    lives_text = font.render("Lives: "+ str(player_lives),True , GREEN, DARK_GREEN)

    if player_lives == 0:
        display_surface.blit(game_over_text,game_over_rect)
        display_surface.blit(continue_text,continue_rect)
        pygame.display.update()

        #Pasue the game until player decide what to do next
        pygame.mixer.music.stop()
        is_pause = True
        while is_pause:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    score = 0
                    player_lives = PLAYER_STARTING_LIVES
                    dragon_rect.y = WINDOW_HEIGHT //2
                    coint_velocity = COIN_STARTING_VELOCITY
                    pygame.mixer.music.play(-1,0.0)
                    is_pause = False
                
                if event.type == pygame.QUIT:
                    is_pause = False
                    running = False
                    

    #Fill the display
    display_surface.fill((BLACK))

    #Bitt the live coverage of the game
    display_surface.blit(score_text,score_rect)
    display_surface.blit(title_text, title_rect)
    display_surface.blit(lives_text,lives_rect)
    pygame.draw.line(display_surface, WHITE , (0,64) ,(WINDOW_WIDTH,64),2)

    #Blit Dragon and coin
    display_surface.blit(dragon_image,dragon_rect)
    display_surface.blit(coin_image, coin_rect)

    #Updating the display
    pygame.display.update()
    clock.tick(FPS)

#END Of GAME
pygame.quit()
