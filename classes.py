#
# This is the main file of this game, here we have all the classes and objects, 
# indeed pygame is really more interesting and powerful if it is used in object oriented
#
#



# We use try-except to know if we have an error when we import and to not stop the game
try:
    # We use this just to quitt the program if we can load the other libraries
	import sys
	import random
    # for the angle
	import math
	import pygame
    # this allow use to use the pygame constante like K_DOWN
	from pygame.locals import *
except ImportError as error:
	print("Unable to load the module : ", error.name)
	sys.exit(2)
if not pygame.font:
    print("Caution, disabled fonts")
if not pygame.mixer:
    print("Warning, sound off")
from classes import *
from constantes import *
from fonction import *

# declaration of the main class BallBumperApp that allow us to use the menu and the game in the same window
class BallBumperApp :
    # here we give the constructor of the class
    def __init__(self):
        # We create an empty window with our constants
        self.window = pygame.display.set_mode((window_width,window_length))
        # When we create an object BallBumperApp, we want to create a window with a title
        pygame.display.set_caption("BallBumperApp")
        # We give a color for the background, a gray, monochramtic backgroud give better performances
        self.fond = (100,)*3
        # We take a rectangle with the same size and position than our window
        self.area = self.window.get_rect()
        # We load and play the musique with our function in the "funciton.py" file
        music = load_sound("musique_transverse.wav")
        # we put True in play() to loop the music
        music.play(True)
        # group of sprites. we use this because is realy easier to display group. 
        # another realy important information, we don't use the common pygame.sprite.Group but the group pygame.sprite.RenderUpdates 
        # because with this group, we can use the technique of "dirty little rectangle"
        self.groupGlobalSprite = pygame.sprite.RenderUpdates()
        # we create an array that will contain all the rectangle of the previous sprite. 
        # with this we don't have to re-fill all the screen when we move a sprite, we just have to file is previous position
        self.previousRect= []
        # Here it is the first and the last time that we entirely fill the screen
        self.window.fill(self.fond)
        # boolean to know if the application is running for the main loop
        self.running = True
        # We start by displaying the menu with an initial score of 0, screen will also be the Game() object later
        self.screen = Menu(self, 0)
        
    # We call the method each time we pass from the menu to the game and inversely
    def _cleaning(self) :
        # We delete the last screen things like the mouse cursor
        self.screen.destroy()
        # And we empty the group of all sprites
        self.groupGlobalSprite.empty()

    # method to load the menu
    def menu(self, score = 0) :
        print("menu")
        self._cleaning()
        self.screen = Menu(self, score)

    # same with the game
    def game(self, mode) :
        print("game")
        self._cleaning()
        self.screen = game(self, mode)

    # a method quit to stop the main loop by changing the bool running
    def quit(self, tmp = 0) :
        self.running = False

    # This method allow use to just put app.update() in the main loop, it is call 60 time per sec
    def update(self) :
        # we look at all the event
        events = pygame.event.get()
        for event in events :
            # if we click on the red crose or alt + F4 / cmd + q
            if event.type == pygame.QUIT :
                self.quit()
                return
        # Here we update the screen (menu or game)
        self.screen.update(events)
        # Here we update all the sprites, indeed all our componants have a method update
        self.groupGlobalSprite.update()
        # This for loop is very importante, here we fill just the previous position of our objet 
        # So we don't have to re-fill all the screen when we move a sprite
        for rect in self.previousRect:
            self.window.fill(self.fond, rect)
        # draw just put the different sprite on the window before the refreash
        # because we use a RenderUpdates group, draw() also give the array of all rectangle of the sprites
        self.previousRect = self.groupGlobalSprite.draw(self.window)
        # Now we just have to update the window
        pygame.display.update()




# Classe to display the menu and the score of the last game
class Menu :
    # For the initialisation, we take the application var and also the score
    def __init__(self, application, score) :
        self.app = application
        # mode -1 corespond to a ball that move on the two axis, we create a ball just for the background
        self.mode = -1
        self.ball = Ball(self, -5, -1)
        self.app.groupGlobalSprite.add(self.ball)
        # we use two colors : one when we don't touche anything, one when we have our cursor on the button
        self.basicColor = (60, 60, 60)
        self.overviewColor = (20, 20, 20)
        font = pygame.font.SysFont('Helvetica', 24, bold=True)
        # name of the button and the associated comand, here we display the score whith a button because a simple text is not a sprite 
        # so it's simpler this way 
        choice = (
            ('Score : '+str(score), application.menu, 0),
            ('Play gamemode 1', application.game, 1),
            ('Play gamemode 2', application.game, 2),
            ('Play gamemode 3', application.game, 3),
            ('Quit', application.quit, 0)
        )
        # coordinate of the first button
        x = 640
        y = 100
        # list of all the button
        self._buttons = []
        for texte, cmd, mode in choice :
            # We create each object button 
            mb = button(texte, self.basicColor, font, x, y, 200, 50, cmd, mode)
            # To fill the list
            self._buttons.append(mb)
            # we add 100 to the y axis between each button
            y += 100
            # we don't forget to add these sprite to our group sprite
            for group in self.app.groupGlobalSprite :
                self.app.groupGlobalSprite.add(mb)
        
    def update(self, events):
        # Mouse.get_pressed give a bool for all the button of the mouse that are press,
        # We use just want the left clic so we use *_ for the other
        leftClic, *_ = pygame.mouse.get_pressed()
        # We look at the pointeur position
        posPointeur = pygame.mouse.get_pos()
        # We update each button
        for button in self._buttons :
            # If the mouse is on a button
            if button.rect.collidepoint(*posPointeur) :
                # We change the cursor
                pygame.mouse.set_cursor(*pygame.cursors.tri_left)
                # And the color of the button
                button.design(self.overviewColor)
                # if we clic
                if leftClic :
                    # we call the comand of our button
                    button.executeCommand()
                break
            else :
                # the mouse is not on the button
                button.design(self.basicColor)
        else :
            # pointer default initialization
            pygame.mouse.set_cursor(*pygame.cursors.arrow)

    def destroy(self) :
        pygame.mouse.set_cursor(*pygame.cursors.arrow) # pointer default initialization when we change from menu to game




# we create a class who inherits from the pygame class Sprite
class button(pygame.sprite.Sprite) :
    # constructor :
    def __init__(self, texte, couleur, font, x, y, largeur, hauteur, command, mode):
        # we call the Sprite constructor
        pygame.sprite.Sprite.__init__(self)
        self.mode = mode
        self._command = command
        # We create a rectangle that we will fill with text
        self.image = pygame.Surface((largeur, hauteur))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.texte = font.render(texte, True, (0, 0, 0))
        self.rectTexte = self.texte.get_rect()
        self.rectTexte.center = (largeur/2, hauteur/2)
        self.design(couleur)

    # method to fill the button
    def design(self, couleur) :
        self.image.fill(couleur)
        self.image.blit(self.texte, self.rectTexte)

    # method that call the command of a button
    def executeCommand(self) :
        self._command(self.mode)




# class that gather all the elements and inputs for the game
class game :
    # constructors
    def __init__(self, app, mode):
        self.mode = mode    
        self.app = app
        self.score = 0
        self.time = 0
        # we create different elements according to the gamemode
        if self.mode == 1:
            # we have an only ball
            self.ball = Ball(self, 5, -2)
            # we create a group with all the sprite bonus, group allow us to use detection 
            # but also to delete the bonus after their have cross the screen
            self.groupBonus = pygame.sprite.Group(Bonus(self))
            # we want to create a group of plateform with the first one that spawn at the edge of the window
            self.groupPlateform = pygame.sprite.Group(Platform(self, window_width-20,random.randint(0, window_length-10), random.randint(0, 360)))
            #we put all these new component on our groupGlobalSprite
            for bonus in self.groupBonus:
                for plateform in self.groupPlateform:
                     self.app.groupGlobalSprite.add(self.ball, bonus, plateform)
        #same for the other gamemode but we change the only object and the group
        elif self.mode == 2:
            self.plateform = Platform(self, 600, 350, 0)
            self.groupBall = pygame.sprite.Group()
            self.groupBall.add(Ball(self, 5, -2))
            for ball in self.groupBall:
                self.app.groupGlobalSprite.add(ball, self.plateform)
        else:
            self.ball = Ball(self, 5, -2)
            self.groupPlateform = pygame.sprite.Group()
            self.groupPlateform.add(Platform(self, 200, 650, -5), Platform(self, 700, 650, -5))
            for plateform in self.groupPlateform :
                self.app.groupGlobalSprite.add(self.ball, plateform)


    # Method that read the input during the game. it is also check if the game is over
    def update(self, events) :
        # we increase the time at each frame (60 time per sec)
        self.time += 1
        # in the list of all the event
        for event in events:
            # when a button is press
            if event.type == KEYDOWN:
                # Different input for each gamemode
                if self.mode == 1:
                    # we can change the gravity with right and left key
                    if (event.key == K_RIGHT):
                        self.ball.changeGravity(-1)
                    if (event.key == K_LEFT):
                        self.ball.changeGravity(1)
                elif self.mode == 2:
                    # we can rotate the plateform
                    if (event.key == K_RIGHT):
                        self.plateform.rotation(5)
                    if (event.key == K_LEFT):
                        self.plateform.rotation(-5)
                    # we can use zqsd to move the plateform
                    if (event.key == K_z):
                        self.plateform.rect = self.plateform.rect.move(0,-10)
                    if (event.key == K_s):
                        self.plateform.rect = self.plateform.rect.move(0,10)
                    if (event.key == K_q):
                        self.plateform.rect = self.plateform.rect.move(-10,0)
                    if (event.key == K_d):
                        self.plateform.rect = self.plateform.rect.move(10,0)
                else:
                    # we can change the gravity with right and left key
                    if (event.key == K_RIGHT):
                        self.ball.changeGravity(-0.1)
                    if (event.key == K_LEFT):
                        self.ball.changeGravity(0.1)
                # if we press M we return to the menu
                if (event.key == K_m):
                    self.app.menu(self.score)
        # we call the function gameover to check if the game is over
        self.gameover()
        # we call collect() to know if we have taken a bonus
        self.collect()
        # every 5 sec we spawn an element accordind to the gamemode
        if self.time%100 == 0:
            if self.mode == 1:
                p = Platform(self, window_width,random.randint(0, window_length-10), random.randint(0, 360))
                self.groupPlateform.add(p)
                b = Bonus(self)
                self.groupBonus.add(b)
                self.app.groupGlobalSprite.add(p, b)
            elif self.mode == 2:
                b = Ball(self, random.randint(-5,5), random.randint(-5,5))
                self.groupBall.add(b)
                self.app.groupGlobalSprite.add(b)
        #this commentary is just to show how work the hit box on the 2 gamemode
        #pygame.draw.rect(self.app.window, (0,0,0), self.plateform.rect)

    # check the lose conditions
    def gameover(self):
        if self.mode == 1:
            # if your sprites colide : we kill all the sprite and go back to the menu
            if pygame.sprite.spritecollide(self.ball, self.groupPlateform, False) != []:
                for p in self.groupPlateform:
                    p.kill()
                for b in self.groupBonus:
                    b.kill()
                self.ball.kill()
                 # in this gamemode, the score is the number of collect bonus
                self.app.menu(self.score)
        elif self.mode == 2:
            # here the condition are interesting:
            # if the hit box(the box that contain our sprite) touche another box,
            # we check if the mask, that is to say the real pixel also touch, if yes, gameover
            # We check before if the box collide because it is faster
            # another way to lose is simply to touch the edge
            if pygame.sprite.spritecollide(self.plateform, self.groupBall, False) != [] and pygame.sprite.collide_mask(self.plateform, pygame.sprite.spritecollide(self.plateform, self.groupBall, False)[0]) != None or not self.app.area.contains(self.plateform):
                for b in self.groupBall:
                    b.kill()
                self.plateform.kill()
                # in this gamemode, the score is the time
                self.score = self.time
                self.app.menu(self.score)
        else:
            # if the ball touch the edge
            if not self.app.area.contains(self.ball):
                for p in self.groupPlateform:
                    p.kill()
                self.ball.kill()
                self.score = self.time
                # in this gamemode, the score is the time
                self.app.menu(self.score)

    def collect(self):
        # if our ball touch a bonus, we delete this bonus (it is the False bool at the end) and we increase the score
        if self.mode == 1 and pygame.sprite.spritecollide(self.ball, self.groupBonus, True) != []: #dokill = true
            self.score += 1

    # just to explain in the console that the game is over
    def destroy(self):
        print("gameover")



# Class that allow us to create ball object
class Ball(pygame.sprite.Sprite):
    # constructor
    def __init__(self, game, Vx, Vy):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.gravity = gravity
        # we use our function load_image
        self.image, self.rect = load_image("ball.png")
        self.rect.x = 200
        self.rect.y = 50
        self.Vx = Vx
        self.Vy = Vy

    # We must have an update function to use the group.update()
    def update(self):
        self.calc_new_pos() 

    # This function is to compute all the movements with an without colisio 
    def calc_new_pos(self):
        # kinetic equation : Vf = Vi*t + 1/2*a*t^ 2 
        # we calculate every second the next displacement so t=1 -> Vf = Vi + cst(gravity)
        self.rect.y += self.Vy
        # we use the x displacement only for the the menu and the second game
        if (self.game.mode == -1 or self.game.mode == 2):
            self.rect.x += self.Vx
        # We call the colision method
        if(self.colision() == False):
            self.Vy += self.gravity

    def colision(self):
        # We have a colision when we hit the edge
        if not self.game.app.area.contains(self.rect):
            tl = not self.game.app.area.collidepoint(self.rect.topleft)
            tr = not self.game.app.area.collidepoint(self.rect.topright)
            bl = not self.game.app.area.collidepoint(self.rect.bottomleft)
            br = not self.game.app.area.collidepoint(self.rect.bottomright)
            # If it is on the horizontal axis
            if((tr and tl) or (br and bl)):
                # When the ball bump it is losing energie
                self.Vy = -self.Vy*friction
            # If it is on the vertical axis
            if((tl and bl) or (tr and br)):
                self.Vx = -self.Vx*friction
            return True
        # if the rect of the ball touche a rect of a plateform
        if self.game.mode == 3 and pygame.sprite.spritecollide(self, self.game.groupPlateform, False) != []:
            # and the mask also collide
            if pygame.sprite.collide_mask(self, pygame.sprite.spritecollide(self, self.game.groupPlateform, False)[0]) != None :
                # we add the value according to the angle of the ball and the plateform
                self.Vy = (-self.Vy + 2*math.sin(math.radians(pygame.sprite.spritecollide(self, self.game.groupPlateform, False)[0].angle+math.pi)))*friction
                self.Vx = (self.Vx + 2*math.cos(math.radians(pygame.sprite.spritecollide(self, self.game.groupPlateform, False)[0].angle+math.pi)))*friction
                return True
        return False
        
    # a simple function to change the gravity
    def changeGravity(self, x):
        # when we are in  mode 3, we can't have a negative gravity
        if (self.game.mode != 3) or (self.gravity + x > 0.1):
            self.gravity += x
        print(self.gravity)



# Class that allow us to create ball object
class Platform(pygame.sprite.Sprite):
    def __init__(self,game, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        # we use our function load_image
        self.image, self.rect = load_image("platform.png")
        # we save two time the original to not have problem on rotation, we will always return to an angle 0
        self.original = self.image
        self.rect.x = x
        self.rect.y = y
        self.angle = angle
        if self.angle != 0:
            self.rotation(self.angle)
        self.game = game

    def update(self):
        # the plateform move only in the gamemode 1 and 3
        if (self.game.mode == 1 or self.game.mode == 3):
            self._move()
    
    # method to rotate an image
    def rotation(self, angle):
        centre = self.rect.center
        # We add the new angle
        self.angle += angle
        # If we have a complete turn, we return at 0 because pygame.transform.rotate can change the size of the image if we turn to much
        if self.angle >= 360:
            self.angle = 0
            self.image = self.original
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.angle)
        # The new rectangle of the plateform will be the smallest rect that contains the plateform
        self.rect = self.image.get_rect(center = centre)

    # Method to move our plateform
    def _move(self):
        newpos = self.rect.move((-5 , 0))
        # if the new position of the plateform is not one the window
        if not self.game.app.area.colliderect(newpos) and self.rect.x < 0:
            # we put the plateform on the right
            newpos = self.rect.move((window_width-5, 0))
        self.rect = newpos



# class similar to plateform just to create bonus object
class Bonus(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("bonus.png")
        self.rect.x = window_width-40
        # we give a random y start position
        self.rect.y = random.randint(0, window_length-10)
        self.game = game

    def update(self):
        # if the bonus leave the window, it disapear
        if not self.game.app.area.contains(self.rect):
            self.kill()
        self._move()

    def _move(self):
        self.rect = self.rect.move((-8 , 0))
            