import pygame
from pygame.locals import*
from pygame import mixer


pygame.init()



# loading in background image
backgroundClassic_image=pygame.image.load('image/WallPaper.png')
backgroundAncient_image=pygame.image.load('image/WallPaper2.png')

# loading in player image
player_imageClassic=pygame.image.load('image/player.png')
player_imageAncient=pygame.image.load('image/player2.png')
player_imageClassicR=pygame.image.load('image/playerR.png')
player_imageAncientR=pygame.image.load('image/player2R.png')


#loading sound for bullet
BulletSound=mixer.Sound('sound/bullet.wav')

#Loading sound for collision with enemy:
CollidewithEnemy=mixer.Sound('sound/Collide.wav')

#Loading sound for opening of game:
Opening_Sound=mixer.Sound('sound/opening.wav')
Mouse_Sound=mixer.Sound('sound/mouseclick.wav')
Selection_Sound=mixer.Sound('sound/selection.wav')

#loading sound for end of game:
End_GameSound=mixer.Sound('sound/gameover.wav')

#loading sound for win game:
Win_GameSound=mixer.Sound('sound/wingame.wav')
Door_GameSound=mixer.Sound('sound/doorappear.wav')

#Loading in image for opening animation:
Opening_Image= [pygame.image.load('image/opening.png'),pygame.image.load('image/opening.png'),
pygame.image.load('image/opening.png'),pygame.image.load('image/opening.png'),
pygame.image.load('image/opening.png'),pygame.image.load('image/opening.png'),
pygame.image.load('image/opening.png'),pygame.image.load('image/opening.png'),
pygame.image.load('image/opening.png'),pygame.image.load('image/opening.png'),
pygame.image.load('image/opening.png'),pygame.image.load('image/opening.png'),
pygame.image.load('image/opening.png'),pygame.image.load('image/opening.png'),
pygame.image.load('image/opening.png'),pygame.image.load('image/opening.png'),
pygame.image.load('image/opening.png'),pygame.image.load('image/opening1.png'),
pygame.image.load('image/opening1.png'),pygame.image.load('image/opening1.png'),
pygame.image.load('image/opening.png')]

#loading in image for opening game mode selection:
OpeningSelect_BG=pygame.image.load('image/ModeSelection.png')
ClassicMode_image=pygame.image.load('image/ClassicMode.png')
AncientMode_image=pygame.image.load('image/AncientMode.png')
Glow_image=pygame.image.load('image/glow.png')
#Loading image for win game:
Won_Light=pygame.image.load('image/light.png')
Won_Door=pygame.image.load('image/door.png')

#Loading win game page:
Escape_image=pygame.image.load('image/Wingame.png')

#loading in image:
direction_key=pygame.image.load('image/direction1.png')
direction_arrow=pygame.image.load('image/direction2.png')

#loading in endgame page:
End_image=pygame.image.load('image/gameover.png')

# load in image of platform
platformClassic_img= pygame.image.load('image/icicle.png')
platformAncient_img=pygame.image.load('image/brickwall.png')

#Game map for two different game modes:
Classic_map = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0],
[1,1,1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,1,1,0,0,0,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0],
[0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

Ancient_map=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[1,1,0,0,1,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,1,1,0,0,0],
[1,1,0,0,1,1,1,0,0,1,1,0,0,1,0,0,0,0,0,0,0,1,1,0,0,0,1,0,0,1,1,1,0,1,0,0,1,0,0,0,0,1,1,1,1,0,0,0],
[1,1,0,0,1,1,1,0,0,1,1,0,0,1,0,0,1,0,0,0,0,1,1,0,1,0,1,0,0,1,1,1,0,1,0,0,1,0,0,0,0,1,1,0,0,0,0,0],
[1,1,0,0,1,1,1,0,0,1,1,0,0,1,0,0,1,0,0,0,0,1,1,0,1,0,1,0,0,1,1,1,0,1,0,0,1,0,1,0,0,1,1,0,0,0,0,0],
[1,1,0,0,1,1,1,0,0,1,1,0,0,1,0,0,1,0,0,0,0,1,1,0,1,0,1,0,0,1,1,1,0,1,0,0,1,0,1,0,0,1,1,0,0,0,0,0]]

#Upload font type:

fontd1= pygame.font.Font('font/Pieces.ttf',32)
fontd2= pygame.font.Font('font/OldeEnglish.ttf',18)
fontdO= pygame.font.Font('font/Opening.ttf',28) # Font (Opening)
fontdS= pygame.font.Font('font/Pieces.ttf',30) # Font (For Game Mode Selection)
