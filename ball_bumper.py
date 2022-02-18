#
# Ball Bumper
# This game use ball and plateform in 3 differents games :
# - In the first game, we can controle the gravity and we must take the bonus (yellow) and not touch the plateform
# - In the second, we play a plateform and we must survive without touching the balls
# - In the last one, we controle the gravity and we survive the maximum time jumping on the plateforms 
#



# We import the file that contain the classes
from classes import *



# We create an object BallBumperApp, with this we can use the menu and the game in the same window
app = BallBumperApp()
# We we call the method menu of the classe BallBumperApp (this method link to another classe Menu)
app.menu()
# We create an object clock to have a regular fps
clock = pygame.time.Clock()
# we call this to reapet an evenement if we keeep pushing a key
pygame.key.set_repeat(100, 30)
#main loop
while app.running :
	# we wait because we don't want to update more than 60 fps
	clock.tick(60)
	# We update the class BallBumperApp
	app.update()
