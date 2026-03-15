import pygame, random, sys
from pygame.locals import *
from pathlib import Path
"""
step03 - 플레이어 : 이미지 등장 + 키보드 움직이기
"""

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / 'assets'
player_image = pygame.image.load(str(ASSETS_DIR / "player.png"))
baddie_image = pygame.image.load(str(ASSETS_DIR / "baddie.png"))

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (255, 255, 255)
FPS = 60
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 6
PLAYERMOVERATE = 5

def terminate():
    pygame.quit()
    sys.exit()

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def wait_for_player_to_press_key():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return



# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)

font = pygame.font.SysFont(None, 48)
player_rect = player_image.get_rect()

windowSurface.fill(BACKGROUNDCOLOR)
drawText('Dodger', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()

wait_for_player_to_press_key()

player_rect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
move_left = move_right = move_up = move_down = False

baddies = []
baddie_add_counter = 0

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        if event.type == KEYDOWN:
            if event.key == K_LEFT or event.key == K_a:
                move_right = False
                move_left = True
            if event.key == K_RIGHT or event.key == K_d:
                move_right = True
                move_left = False
            if event.key == K_UP or event.key == K_w:
                move_up = True
                move_down = False
            if event.key == K_DOWN or event.key == K_s:
                move_up = False
                move_down = True
        if event.type == KEYUP:
            if event.key ==  K_LEFT or event.key == K_a:
                move_left = False
            if event.key ==  K_RIGHT or event.key == K_d:
                move_right = False
            if event.key ==  K_UP or event.key == K_w:
                move_up = False
            if event.key ==  K_DOWN or event.key == K_s:
                move_down = False
            if event.key == K_ESCAPE:
                terminate()
    if move_left and player_rect.left > 0:
        player_rect.move_ip(-1 * PLAYERMOVERATE, 0)
    if move_right and player_rect.right < WINDOWWIDTH:
        player_rect.move_ip(PLAYERMOVERATE, 0)
    if move_up and player_rect.top > 0:
        player_rect.move_ip(0, -1 * PLAYERMOVERATE)
    if move_down and player_rect.bottom < WINDOWHEIGHT:
        player_rect.move_ip(0, PLAYERMOVERATE)

    baddie_add_counter += 1
    if baddie_add_counter == ADDNEWBADDIERATE:
        badie_add_counter = 0
        baddie_size = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
        new_baddie = {
            'rect': pygame.Rect(
                random.randint(0, WINDOWWIDTH - baddie_size),
                0 - baddie_size,
                baddie_size,
                baddie_size
            ),
            'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
            'surface': pygame.transform.scale(baddie_image, (baddie_size, baddie_size))

        }
        baddies.append(new_baddie)
    for b in baddies:
        b['rect'].move_ip(0, b['speed'])

    for b in baddies[:]:
        if b['rect'].top > WINDOWHEIGHT:
            baddies.remove(b)
    windowSurface.fill(BACKGROUNDCOLOR)
    windowSurface.blit(player_image, player_rect)

    for b in baddies:
        windowSurface.blit(b['surface'], b['rect'])

    pygame.display.update()
    mainClock.tick(FPS)
