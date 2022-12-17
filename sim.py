#2::50, https://www.youtube.com/watch?v=AY9MnQ4x3zk
import pygame
import random
from sys import exit
pygame.init() #starts game
width,height = 800,400
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Yippee")
clock = pygame.time.Clock()
#other stuff
sky = pygame.image.load('graphics/Sky.png').convert()
ground = pygame.image.load('graphics/ground.png').convert()
#text
score = 0
test_font = pygame.font.Font('fonts/Pixeltype.ttf',50)
text_surfece = test_font.render("Score: " + str(score),False,(255,0,0))
text_rect = text_surfece.get_rect(midbottom = (400,70))
#snail emeny
#snail = pygame.image.load('graphics/snail.png').convert_alpha()#Makes transparency
#snail.rect = snail.get_rect(midbottom = (900,300))
#player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('graphics/player_walk_1.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = (80,300))
class Snail(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load('graphics/snail.png').convert_alpha()
            self.rect = self.image.get_rect(midbottom = (900,300))
snails = []
snails.append(Snail())
player = Player()
#player = pygame.image.load('graphics/player_stand.png').convert_alpha()
#player_rect = player.get_rect(midbottom = (80,300))
#entire game within here



#variables that are to change within the game
pressedspace = False
speedup = 0
inair = False
alive = True
legcrossed = True
crossdelay = 3
#code
music = pygame.mixer.Sound('audio/music.wav')
music.play(loops = -1)
while True:
    if alive:
        #handles events
        for event in pygame.event.get():
            #closes game
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        #checks key press
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] == 1 and not pressedspace and not inair:
            print("jump")
            pressedspace,inair = True,True
            player.image = pygame.image.load('graphics/player_stand.png').convert_alpha()
            player.rect = player.image.get_rect(midbottom = (80,300))
            speedup = 37
            jump_sound = pygame.mixer.Sound('audio/audio_jump.mp3')
            jump_sound.play()
        elif keys[pygame.K_SPACE] == 0 and pressedspace:
            pressedspace = False
        #moves up and down
        if inair:
            player.rect.top -= speedup
            speedup -= 3
            if player.rect.bottom >= 300 and speedup < 0:
                inair = False
                speedup = 0
                player.rect.bottom = 300
                print("l")
                player.image = pygame.image.load('graphics/player_walk_1.png').convert_alpha()
                player.rect = player.image.get_rect(midbottom = (80,300))
        #makes guy walk
        if legcrossed and (not inair) and crossdelay == 0:
            player.image = pygame.image.load('graphics/player_walk_1.png').convert_alpha()
            player.rect = player.image.get_rect(midbottom = player.rect.midbottom)
            legcrossed = False
            crossdelay = 4
        elif not legcrossed and (not inair) and crossdelay == 0:
            player.image = pygame.image.load('graphics/player_walk_2.png').convert_alpha()
            player.rect = player.image.get_rect(midbottom = player.rect.midbottom)
            legcrossed = True
            crossdelay = 4
        if not inair:
            crossdelay -= 1
        #moves snail
        for snail in snails:
            if snail.rect.left > -100:
                snail.rect.left -= 8
            else:
                snails.remove(snail)
                if alive:
                    score += 1
            if player.rect.colliderect(snail.rect) == 1:
                alive = False
        mouse_pos = pygame.mouse.get_pos()
        if player.rect.collidepoint(mouse_pos) == 1:
            print("COLLDE")
        #makes new snails
        if len(snails) == 0:
            snails.append(Snail())
        elif random.randint(1,int(99 * .99**score)+1) == 100:
            for snail in snails:
                if snail.rect.left > 600:
                    break
            else:
                snails.append(Snail())

        #Displays final window
        screen.blit(sky,(0,0))#LEFTMOST CORNER IS POSITION
        screen.blit(ground,(0,300))#put ground above sky
        #text
        text_surfece = test_font.render("Score: " + str(score),False,(255,0,0))
        text_rect = text_surfece.get_rect(midbottom = (400,70))
        pygame.draw.rect(screen,'gray',text_rect.inflate(5,5))
        pygame.draw.rect(screen,'black',text_rect.inflate(25,25),width=10)
        screen.blit(text_surfece,text_rect.move(2.5,2.5))
        #snail/player
        for snail in snails:
            screen.blit(snail.image,snail.rect)
        screen.blit(player.image,player.rect)
        pygame.display.update()
        clock.tick(60)
    else:
        #print(alive)
        #prints end screen
        test_font = pygame.font.Font('fonts/Pixeltype.ttf',75)
        text_surfece = test_font.render("GAME OVER! FINAL SCORE: " + str(score),False,(255,0,0))
        text_rect = text_surfece.get_rect(midbottom = (400,100))
        #Displays final window
        screen.blit(sky,(0,0))#LEFTMOST CORNER IS POSITION
        screen.blit(ground,(0,300))#put ground above sky
        #reset button
        reset = pygame.image.load("graphics/Replay.png").convert_alpha()
        reset_rect = reset.get_rect(center = (400,250))
        screen.blit(reset,reset_rect)
        for event in pygame.event.get():
            if pygame.mouse.get_pressed()[0] and reset_rect.collidepoint(pygame.mouse.get_pos()):
                alive = True
                score = 0
                snails = []
                snails.append(Snail())
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        #text
        pygame.draw.rect(screen,'gray',text_rect.inflate(5,5))
        pygame.draw.rect(screen,'black',text_rect.inflate(25,25),width=10)
        screen.blit(text_surfece,text_rect.move(2.5,2.5))
        pygame.display.update()
        clock.tick(60)