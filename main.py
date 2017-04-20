import pygame, sys, random
from pygame.locals import *

WINDOWWIDTH = 1000
WINDOWHEIGHT = 680
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)
FPS = 40
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 80
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 6
PLAYERMOVERATE = 5

def terminate():
    pygame.quit()
    sys.exit()
    
def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return
                
def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
    
# set up pygame, the window, and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("dodger v1.9.6")
pygame.mouse.set_visible(False)

# set up font
font = pygame.font.SysFont(None, 70)
font1 = pygame.font.SysFont(None, 40)

# set up sounds
gameOverSound = pygame.mixer.Sound('resources\\gameOver.wav')
pygame.mixer.music.load('resources\\background.wav')

# set up images
playerImage = pygame.transform.scale(pygame.image.load('resources\\player.png'), (80, 85))
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('resources\\baddie.png')

# show the "Start" screen
drawText('Dodger', font, windowSurface, WINDOWWIDTH / 3 + 100, WINDOWHEIGHT / 3)
drawText('Press any key to start the game', font1, windowSurface, WINDOWWIDTH / 3 - 30, WINDOWHEIGHT / 2 + 50)
pygame.display.update()
waitForPlayerToPressKey()

topScore = 0
while True:
    # set up the start of the game
    baddies = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH - 2, WINDOWHEIGHT - 50)
    moveLeft = moveUp = moveRight = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)
    
    while True:  # The game loop runs while the game part is playing
        score += 1  # Increase score
        
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    reviseCheat = True
                if event.key == ord('x'):
                    slowCheat = True
                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = True
                    moveRight = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = True
                    moveLeft = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = True
                    moveDown = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = True
                    moveUp = False

            if event.type == KEYUP:
                if event.key == ord('z'):
                    reviseCheat = False
                    score = 0
                if event.key == ord('x'):
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                    terminate()

                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False

            if event.type == MOUSEMOTION:
                # If the mouse moves, move the player to where the cursor is.
                playerRect.move_ip(event.pos[0] - playerRect.centerx, event.pos[1] - playerRect.centery)

        # Add new baddies at the top of the screen, if needed.
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            newBaddie = {'rect':pygame.Rect(random.randint(0, WINDOWWIDTH - baddieSize), 0 - baddieSize, baddieSize, baddieSize),
                         'speed':random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                         'surface':pygame.transform.scale(baddieImage, (baddieSize, baddieSize))
                        }

            baddies.append(newBaddie)

        # move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.left < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        # move the mouse cursor to match the player
        pygame.mouse.set_pos(playerRect.centerx, playerRect.centery)
        
        # move the baddies down
        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

        # delete baddie that have fallen past the bottom
        for b in baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)

        # Draw the game world on the window
        windowSurface.fill(BACKGROUNDCOLOR)

        # Draw the score and the score
        drawText('score: %s' %(score), font1, windowSurface, 10, 10)
        drawText('top scrore: %s' %(topScore), font1, windowSurface, 10, 40)

        # Draw the player's rectanger
        windowSurface.blit(playerImage, playerRect)

        # Draw each baddie
        for b in baddies[:]:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        # check if any of the baddies have hit the player.
        if playerHasHitBaddie(playerRect, baddies):
            if score > topScore:
                topScore = score
            break

        mainClock.tick(FPS)

    # stop the game and show the 'Game over' screen.
    pygame.mixer.music.play(-1, 0.0)
    gameOverSound.play()

    drawText('Game over', font, windowSurface, (WINDOWWIDTH / 3) + 30, (WINDOWHEIGHT / 3))
    drawText('Press a key to play again!', font1, windowSurface, (WINDOWHEIGHT / 3) + 100, (WINDOWHEIGHT / 3) + 70)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()
