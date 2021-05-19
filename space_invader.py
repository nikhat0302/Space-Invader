import pygame
from pygame.locals import*
import random
import math
from pygame import mixer

pygame.init()
screen=pygame.display.set_mode((800,600))
logo=pygame.image.load("gallery/space_logo.png")
pygame.display.set_icon(logo)
pygame.display.set_caption("Space Invader")
background=pygame.image.load("gallery/space_background.png")


#-----------------------player variables---------------------
playerimg=pygame.image.load("gallery/space_player.png")
playerX=365
playerY=500
playerX_change=0

def player(x,y):
    screen.blit(playerimg, (x,y))

#-----------------------enemy variables---------------------
enemyimg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
no_of_enemies=6

for x in range(no_of_enemies):
    enemyimg.append(pygame.image.load("gallery/space_enemy.png"))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(0,100))
    enemyX_change.append(4)
    enemyY_change.append(40)

def enemy(x,y,i):
        screen.blit(enemyimg[i], (x,y))

#-----------------------bullet variables---------------------
bulletimg=pygame.image.load("gallery/bullet.png")
bulletX=367
bulletY=510
bulletY_change=0

def bullet(x,y):
    screen.blit(bulletimg, (x+16,y))

def isCollide(bulletX,bulletY,enemyX,enemyY):
    distance=math.sqrt(math.pow(enemyX-bulletX, 2) + (math.pow(enemyY-bulletY, 2)))
    if distance<20:
        return True
    else:
        return False


#-----------------------score variables-------------------
score=0
font=pygame.font.Font('freesansbold.ttf', 32)
textX=10
textY=10

def show_score(x,y):
    score_val=font.render("Score: " + str(score), True, (255,255,255))
    screen.blit(score_val, (x,y))

#------------------------game over-------------------
font=pygame.font.Font('freesansbold.ttf', 52)
gameX=300
gameY=200

def game_over(x,y):
    game=font.render("Game Over", True, (255,255,255))
    screen.blit(game, (x,y))

def isCollision(playerX,playerY,enemyX,enemyY):
    distance_over=math.sqrt(math.pow(enemyX-playerX, 2) + (math.pow(enemyY-playerY, 2)))
    if distance_over<55:
        return True
    else:
        return False

if __name__ == "__main__":

    running=True
    while running:
        screen.fill((0,0,0))
        screen.blit(background, (0,0))
        mixer.music.load("gallery/background.mp3")
        mixer.music.play(-1)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                running=False

            elif event.type==KEYDOWN:
                if event.key==K_LEFT:
                    playerX_change=-5
                elif event.key==K_RIGHT:
                    playerX_change=5

                elif event.key==K_SPACE:
                    overSound=mixer.Sound("gallery/game_over.wav")
                    overSound.play()
                    bulletY_change=-10
                    bulletX=playerX
                    if bulletY<0:
                        bulletY=510

            if event.type==KEYUP:
                if event.key==K_LEFT or event.key==K_RIGHT:
                    playerX_change=0

        bulletY+=bulletY_change
        bullet(bulletX, bulletY)

        playerX+=playerX_change
        if playerX<=0:
            playerX=0
        elif playerX>=736:
            playerX=736
        player(playerX,playerY)

        for x in range(no_of_enemies):
            enemyX[x]+=enemyX_change[x]

            if enemyX[x]<=0:
                enemyX_change[x]=4
                enemyY[x]+=enemyY_change[x]
            elif enemyX[x]>=736:
                enemyX_change[x]=-4
                enemyY[x]+=enemyY_change[x]

            collide=isCollide(bulletX,bulletY,enemyX[x],enemyY[x])
            if collide:
                score+=1
                enemyX[x]=random.randint(0,736)
                enemyY[x]=random.randint(0,100)
                explosionSound=mixer.Sound("gallery/explosion.wav")
                explosionSound.play()

            collision=isCollision(playerX,playerY,enemyX[x],enemyY[x])
            if collision:
                screen.blit(background, (0,0))
                game_over(gameX,gameY)
                running=False
                
            enemy(enemyX[x],enemyY[x],x)
    
        show_score(textX,textY)

        pygame.display.update()
