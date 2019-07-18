import pygame
import singleton_decorator


@singleton
class input:
	
	def __init__(self):
		pygame.joystick.init()
		joys = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
		
	
	
