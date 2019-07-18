import config
import tidalapi
from cryptography.fernet import Fernet
import Widgets
import pygame
import singleton_decorator

@singleton
class Tidal:
	
	def __init__(self):
		settings: config = 
