#
# This file is for the functions that we use in various classes to look for pictures and sound
#




# We use try-except to know if we have an error when we import
try:
	import os
	import pygame
except ImportError as error:
	print("Unable to load the module : ", error.name)
	sys.exit(2)
if not pygame.mixer:
    print("Warning, sound off")
from classes import *


# Initialization pygame
pygame.init()

# This function load any image, solid or transparent with its name.
def load_image(name):
	# With os we take the full path
	fullname = os.path.join('data', name)
	# We use try/exept to not stop the program if it's doesn't work
	try:
		# We load the image
		image = pygame.image.load(fullname)
		# We check if it is not transparent
		if image.get_alpha() is None:
			# If it is solid, we use .convert() so that all the images are in the same colormetric space and thus do not slow down the program.
			image = image.convert()
		else:
			# Here it is the same but we also takes into account the transparency
			image = image.convert_alpha()
	except pygame.error:
        	print ("Unable to load the image : ", fullname)
        	raise SystemExit
	# We return the image and the associated rectangle
	return image, image.get_rect()

# basicely the same but for the sound
def load_sound(name):
	# little tricky, here we create this class juste to return something and not crash the program
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print("Unable to load sound : ", name)
        raise SystemExit
    return sound
