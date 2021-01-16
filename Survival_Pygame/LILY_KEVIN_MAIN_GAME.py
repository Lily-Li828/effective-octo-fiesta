#Final project game by Kevin Phung and Lily

#imports:
import sys
import time
import pygame
import random
import math
from pygame.locals import*
from pygame import mixer
from data import *

#Initiate variable checktime:
checktime=0

def main():
    #Initiate Pygame
    pygame.init()

    #set up the clock
    clock=pygame.time.Clock()

    #creates timer in air
    air_timer=0

    #set up window caption and icon
    pygame.display.set_caption('ESCAPING:Mansion of Munglis')
    icon=pygame.image.load('image/Icon.png')
    pygame.display.set_icon(icon)

    #creates window
    WINDOW_SIZE= (400,500)
    screen=pygame.display.set_mode(WINDOW_SIZE,0,32)


    #Initiate values:
    moving_right=False
    moving_left =False
    vertical_momentum =0
    player_location= [50,50]
    player_y_momentum =0

    # Creates a Player Rect
    player_rect=pygame.Rect(150,250,32,32)

    #Initializes bullet class with location, picture and ammo depending on difficulty
    class Bullet():
        def __init__(self,x,y,BulletPic,ammocount):
            self.BulletImg=pygame.image.load(BulletPic)
            self.bulletX = x
            self.bulletY = y
            self.bulletY_change = 14
            self.bullet_state = "ready"
            self.ammo=ammocount

        def getbulletY_change(self):
            return self.bulletY_change

        def getbullet_state(self):
            return self.bullet_state

        def newbullet_state(self,newstate):
            self.bullet_state=newstate

        def getBulletX(self):
            return self.bulletX

        def getBulletY(self):
            return self.bulletY

        def newbulletX(self,newx):
            self.bulletX=newx

        def newbulletY(self,newy):
            self.bulletY=newy

     #Method Defined to fire a bullet
        def fire_bullet(self,x,y):
            # GLOBAL: to use the variables outside of the class
            global bullet_state
            self.bullet_state="fire"
            # to make sure that the bullet fires from the middle and on top a bit of the stuff
            screen.blit(self.BulletImg,(x+16,y+10))

        def checkammo(self):
            return self.ammo

        def useammo(self):
            self.ammo=self.ammo -1


    class scrollbackground():
        def __init__(self,image,x,y):
            self.image = image
            self.x=x
            self.y=y

        def scroll(self,scrollspeed):
            self.x=0
            self.x= self.x-scrollspeed

        def draw(self):
            screen.blit(self.image,(self.x,self.y))





    #score variables:
    score_value=0
    font= pygame.font.Font('font/OldeEnglish.ttf',30)
    font2= pygame.font.Font('font/Pieces.ttf',23)

    textX=10
    textY=10
    textX2=10
    textY2=35



    #Function to show key control directions for a certain time
    def directioncheck(direction_key,direction_arrow):
        global checktime
        if checktime<600:
            screen.blit(direction_key,(15,350))
            screen.blit(direction_arrow,(35,50))
            checktime +=1


    # Function defined to show the score
    def show_score(x,y):
        score=font.render("Score:"+str(score_value)+"/100",True,(255,255,255))
        screen.blit(score,(x,y))

    def show_ammo(x,y):
        ammo=font2.render("Ammo:"+str(Bullet.checkammo()),True,(255,255,255))
        screen.blit(ammo,(x,y))

    # Function defined to draw player:

    def DrawPlayer(image,x,y):
        screen.blit(image,(x,y))

    # Function defined to draw enemy:
    def DrawEnemy(x, y,i):
        screen.blit(EnemyImg[i], (x, y))



    # Function returns true if bullet collides with enemy, false if doesnt.
    def BulletisCollision(enemyX,enemyY,bulletX,bulletY):
        distance= math.sqrt(math.pow(enemyX-bulletX,2)+math.pow(enemyY-bulletY,2))
        if distance< 20:
            return True
        else:
            return False


    #Function to prevent the player from walking out
    #the sides of the screen
    def collision_screen(rect):
        if rect.x<0:
            rect.x=0
        if rect.x>370:
            rect.x=370

    #tile collision define function:
    def collision_test(rect,tiles):
        hit_list=[]
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    # function that moves the player
    #and implements collision
    def move(rect,movement,tiles):
        collision_types={'top':False,'bottom':False,'right':False,'left':False}
        rect.x += movement[0]
        hit_list=collision_test(rect,tiles)
        for tile in hit_list:
            if movement[0]>0:
                rect.right = tile.left
                collision_types['right']= True
            elif movement [0]<0:
                rect.left = tile.right
                collision_types['left']= True

        rect.y +=movement[1]
        hit_list= collision_test(rect,tiles)
        for tile in hit_list:
            if movement[1]<0:
                rect.top= tile.bottom
                collision_types['top']= True
            if movement[1]>0:
                rect.bottom= tile.top
                collision_types['bottom']=True
        return rect.x,rect.y, collision_types


    # Default assigning Game to Classic Mode
    ClassicP=True
    AncientP=False

    #Began playing opening music
    Opening_Word=fontdO.render(("<Click Screen To Begin>"),True,(255,255,255))
    SelectClassic_Word=fontdS.render(("Classic"),True,(255,255,255))
    SelectClassic_Level=font2.render(("(Easy)"),True,(255,255,255))
    SelectAncient_Word=fontdS.render(("Ancient"),True,(255,255,255))
    SelectAncient_Level=font2.render(("(Hard)"),True,(255,255,255))
    Opening_Sound.play()
    Inside_Opening=True
    Opening=True

    #Opening of the game
    while Opening:
        while Inside_Opening:
            for i in Opening_Image:# Creating opening animation
                screen.blit(i,(0,0))
                screen.blit(Opening_Word,(150,390))
                clock.tick(10) # assigning specific time
                pygame.display.update()

                for event in pygame.event.get():# Event Loop
                    if event.type== QUIT:# Check for window quits
                        pygame.quit() # stop pygame
                        sys.exit() #stop script

               #if player clicks on the screen
                    if event.type==pygame.MOUSEBUTTONDOWN:
                        Opening_Sound.stop()
                        Mouse_Sound.play()
                        Inside_Opening=False #Breaks out of the opening screen

        screen.blit(OpeningSelect_BG,(0,0))#blit the selection background
        screen.blit(ClassicMode_image,(50,150)) #blit classic mode
        screen.blit(AncientMode_image,(218,150)) #blit Ancient mode

        #blits the Glow according to player's choice:
        if ClassicP:
            screen.blit(SelectClassic_Word,(70,200))
            screen.blit(SelectClassic_Level,(70,230))
            screen.blit(Glow_image,(30,150))
        if AncientP:
            screen.blit(SelectAncient_Word,(238,200))
            screen.blit(SelectAncient_Level,(238,230))
            screen.blit(Glow_image,(205,150))

        for event in pygame.event.get():# Event Loop
            if event.type== QUIT:# Check for window quits
                pygame.quit() # stop pygame
                sys.exit() #stop script
            if event.type==KEYDOWN:
                 #Left is Classic Mode
                if event.key==K_LEFT:
                    Mouse_Sound.play()
                    ClassicP=True
                    AncientP=False
                #Right is Ancient mode
                if event.key==K_RIGHT:
                    Mouse_Sound.play()
                    ClassicP=False
                    AncientP=True
                #When the player selects a mode
                if event.key == K_SPACE:
                    Selection_Sound.play()
                    if ClassicP:
                        player_image=player_imageClassic
                        player_imageR=player_imageClassicR
                        EnemyPic='image/enemy.png'
                        BulletPic='image/bullet.png'
                        ammocount= 200
                        platform_img=platformClassic_img
                        game_map=Classic_map
                        background_image=backgroundClassic_image
                        #loading in background music
                        mixer.music.load('sound/BGMA.mp3')
                    if AncientP:
                        player_image=player_imageAncient
                        player_imageR=player_imageAncientR
                        EnemyPic='image/enemy2.png'
                        BulletPic='image/bullet2.png'
                        ammocount= 150
                        platform_img=platformAncient_img
                        game_map=Ancient_map
                        background_image=backgroundAncient_image
                        #loading in background music
                        mixer.music.load('sound/BGMA.mp3')

                    Opening=False
        pygame.display.update()

    #Enemy lists:
    EnemyImg=[]
    enemyX= []
    enemyY= []
    enemyX_change=[]
    enemyY_change=[]
    num_of_enemies= 8

    for i in range(num_of_enemies):
        EnemyImg.append(pygame.image.load(EnemyPic))
        enemyX.append(random.randint(0, 360))
        enemyY.append(random.randint(-150, -50))
        enemyX_change.append(2)
        enemyY_change.append(30)

    #creates instance of bullet and background
    Bullet=Bullet(player_rect.x,player_rect.y,BulletPic,ammocount)
    scrollingbackground= scrollbackground(background_image,0,0)

    #Start Playing BGM
    mixer.music.play(-1)

    #Initiate Game ending situation:
    Die=0
    Escape=0
    # Game while loop:
    scroll=0
    run=True
    while run:

        screen.fill((111,111,111))
        scrollingbackground.scroll(scroll)
        scrollingbackground.draw()

        for event in pygame.event.get():# Event Loop
            if event.type==QUIT:# Check for window quits
                pygame.quit() # stop pygame
                sys.exit() #stop script

            # Responding for keys
            if event.type ==KEYDOWN:
                if event.key==K_RIGHT:
                    moving_right=True
                if event.key ==K_LEFT:
                    moving_left= True
                if event.key == pygame.K_SPACE:
                    #Adjust state of bullet
                    if Bullet.checkammo() >0:

                        if Bullet.getbullet_state() is "ready":
                            Bullet.newbulletX(player_rect.x)
                            Bullet.newbulletY(player_rect.y)
                            Bullet.fire_bullet(Bullet.getBulletX(),Bullet.getBulletY())
                            BulletSound.play()
                            Bullet.useammo()
                if event.key ==K_UP:
                    if air_timer<6:
                        vertical_momentum =-8
                        # Adding sound for jumping
                        Jump_Sound=mixer.Sound('sound/jumping.wav')
                        Jump_Sound.play()
            if event.type ==KEYUP:
                if event.key== K_RIGHT:
                    moving_right= False
                if event.key ==K_LEFT:
                    moving_left = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0


    # Bullet movement
    # so that the bullet goes back to player_rect.y
        if Bullet.getBulletY() <=0:
            Bullet.newbulletY(player_rect.y)
            Bullet.newbullet_state("ready")
        if Bullet.getbullet_state() is "fire":
            Bullet.fire_bullet(Bullet.getBulletX(),Bullet.getBulletY())
            Bullet.newbulletY(Bullet.getBulletY()- Bullet.getbulletY_change())



    # Function that draws the iceicle platforms:
        tile_rects =[]

        y=0
        for layer in game_map:
            x=0
            for tile in layer:
                if tile==1:
                    screen.blit(platform_img,(x*32-scroll,y*32))
                if tile != 0:
                    tile_rects.append(pygame.Rect(x*32-scroll,y*32,32,32))
                x +=1
            y +=1


    # returns True and Flase according to player's movement
        player_movement=[0,0]
        if moving_right ==True:
            player_movement[0] +=3
        if moving_left ==True:
            player_movement[0] -=3

        player_movement[1] += vertical_momentum
        vertical_momentum += 0.3
        if vertical_momentum>4:
            vertical_momentum =4


        player_rect.x, player_rect.y ,collisions = move(player_rect,player_movement,tile_rects)

        #test for whether collided to the ground (avoid player jumping in half air)
        if collisions['bottom'] ==True:
            air_timer =0
            vertical_momentum =0
        else:
            air_timer +=1

        # player screen collision test
        collision_screen(player_rect)

        # Scrolls down tiles
        scroll += 0.3


        #End Game function:
        if player_rect.y>480:
            mixer.music.stop()
            CollidewithEnemy.play()
            Die=1 #End Game by dying
            time.sleep(1.5)
            break


        # display player +fill
        if player_movement[0]>1:
            DrawPlayer(player_imageR,player_rect.x,player_rect.y)
        elif player_movement[0]<0:
            DrawPlayer(player_image,player_rect.x,player_rect.y)
        else:
            DrawPlayer(player_imageR,player_rect.x,player_rect.y)

    #checking for boundaries of enemy and collision with player
        for i in range(num_of_enemies):
            distanceX= math.sqrt(math.pow(enemyX[i]-player_rect.x,2)+math.pow(enemyY[i]-player_rect.y,2))
            if distanceX<27:
                mixer.music.stop()
                CollidewithEnemy.play()
                Die=1 # end game by dying
                time.sleep(2)
                run=False
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 2
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 370:
                enemyX_change[i] = -2
                enemyY[i] += enemyY_change[i]

    #checking collisions for bullet and enemies:
            collision = BulletisCollision(enemyX[i], enemyY[i], Bullet.getBulletX(), Bullet.getBulletY())
            if collision:
                Bullet.newbulletY(player_rect.y)
                Bullet.newbullet_state("ready")
                score_value += 1

                enemyX[i] = random.randint(30,360 )
                enemyY[i] = random.randint(-30, 80)
            DrawEnemy(enemyX[i], enemyY[i],i)

    # Display the Score
        show_score(textX,textY)

    # Display the ammo
        show_ammo(textX2,textY2)

    # Draw Directions:
        directioncheck(direction_key,direction_arrow)

    # detect whether player won or not:
        if score_value>100:
            mixer.music.stop()
            Door_GameSound.play()
            Escape=1#End game by escaping
            screen.blit(Won_Light,(300,50))
            screen.blit(Won_Door,(300,50))
            pygame.display.update()
            time.sleep(2.5)
            run=False



        # scales up the display surface and draws it on screen
        #screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))

        pygame.display.update() #update display
        clock.tick(60) #maintains 60 FPS

    #Play Die music if player died
    if Die==1:
        End_GameSound.play()
    if Escape==1 :
        Win_GameSound.play()

    # After the game ends:
    end=True
    while end:
        for event in pygame.event.get():# Event Loop
            if event.type==QUIT:# Check for window quits
                pygame.quit() # stop pygame
                sys.exit() #stop script
            elif event.type==pygame.MOUSEBUTTONDOWN:
                return main()

        if Die==1:
            screen.blit(End_image,(0,0))
            scored1=fontd1.render("Your Score:"+str(score_value),True,(255,255,255))
            exitd=fontd2.render("<Click Screen to Restart>",True,(96,247,172))
            screen.blit(scored1,(120,390))
            screen.blit(exitd,(120,460))
        if Escape==1 :
            screen.blit(Escape_image,(0,0))
            exitd=fontd2.render("<Click Screen to Restart>",True,(96,247,172))
            screen.blit(exitd,(120,460))





        pygame.display.update()


main()
