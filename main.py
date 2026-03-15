import pygame, random, sys
from pygame.locals import *
from pathlib import Path
"""
The Final Version of the Dodger Game
"""

# dodger라는 폴더, parent folder
# assets folder
# load player image from a folder called assets, pull out player.png from it
# load baddie image from folder called assets pull out baddie.png from it
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

# terminate: to end the game if something happens(In this case when it touches the baddie)

def terminate():
    pygame.quit()
    sys.exit()

# to show on the screen
def draw_text(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
# waiting for the player to press any key so that they can start the game. If the player press esc the game quits
def wait_for_player_to_press_key():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return
# when the player hits the baddies, when hit, return true
def player_has_hit_baddies(player_rect, baddies):
    for b in baddies:
        if player_rect.colliderect(b['rect']):
            return True
    return False


# Set up pygame, the window, and the mouse cursor.
pygame.init()
main_clock = pygame.time.Clock()
window_surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)

font = pygame.font.SysFont(None, 48)
# get the gameover sound from assets, and get the background sound from assets
game_over_sound = pygame.mixer.Sound(str(ASSETS_DIR / "gameover.wav"))
pygame.mixer.music.load(str(ASSETS_DIR / "background.mid"))

player_rect = player_image.get_rect()

window_surface.fill(BACKGROUNDCOLOR)
draw_text('Dodger', font, window_surface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
draw_text('Press a key to start.', font, window_surface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
# start displaying 위에서 했던 설정들 on the screene
pygame.display.update()

# wait for the player to press the key
wait_for_player_to_press_key()

player_rect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
move_left = move_right = move_up = move_down = False

baddies = []
baddie_add_counter = 0

top_score = 0

while True:
    baddies = []
    score = 0
    player_rect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    move_left = move_right = move_up = move_down = False
    baddie_add_counter = 0
# player the music from the background
    pygame.mixer.music.play(-1,0.0)

    while True:
        # score += every time it returns true
        score += 1
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                # these are all the codes for the left, right, up and down keys + when to stop after releasing 
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
            # detecting key release + when esc pressed quit(terminate) game they  have False in it because, move only once when u click one of these
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
                # The player moves  left right top bottom, if the player moves left the moverate is -1 so they go to the left side, when the moverte is 1 it moves to the right since it s a positive number, if the move rate is 0,-1 it goes down, if the moverate is just 0 it goes up
        if move_left and player_rect.left > 0:
            player_rect.move_ip(-1 * PLAYERMOVERATE, 0)
        if move_right and player_rect.right < WINDOWWIDTH:
            player_rect.move_ip(PLAYERMOVERATE, 0)
        if move_up and player_rect.top > 0:
            player_rect.move_ip(0, -1 * PLAYERMOVERATE)
        if move_down and player_rect.bottom < WINDOWHEIGHT:
            player_rect.move_ip(0, PLAYERMOVERATE)

        baddie_add_counter += 1
        # add a baddie adds up every time baddie add counter = 6(while looped 6 times
        if baddie_add_counter == ADDNEWBADDIERATE:
            baddie_add_counter = 0
            baddie_size = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            new_baddie = {
                'rect': pygame.Rect(
                    random.randint(0, WINDOWWIDTH - baddie_size),
                    0 - baddie_size,
                    baddie_size,
                    baddie_size
                ),
                # control baddie speed
                'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                'surface': pygame.transform.scale(baddie_image, (baddie_size, baddie_size))
            }
            baddies.append(new_baddie)
        
        # x = 0 stay there, only the y changes and goes down by the amount of speed
        for b in baddies:
            b['rect'].move_ip(0, b['speed'])
# get rid of baddies if they are not showing on the screen anymore, if they are all stakced under the screen it may cause lags.
        for b in baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)
        window_surface.fill(BACKGROUNDCOLOR)
        draw_text(f"Score: {score}", font, window_surface, 10, 0)
        draw_text(f"Top Score:{top_score}", font, window_surface, 10, 40)
        window_surface.blit(player_image, player_rect)

        for b in baddies:
            window_surface.blit(b['surface'], b['rect'])
        pygame.display.update()
# when the player hits the baddies show the top score(the score right before the player died), after that show game over sign and press key to play again
        if player_has_hit_baddies(player_rect, baddies):
            if score > top_score:
                top_score = score
            break
        main_clock.tick(FPS)
    pygame.mixer.music.stop()
    game_over_sound.play()

    draw_text('GAME OVER', font, window_surface, (WINDOWWIDTH /3), (WINDOWHEIGHT/3))
    draw_text('Press a key to play again', font, window_surface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)

    pygame.display.update()
    wait_for_player_to_press_key()
    main_clock.tick(FPS)
