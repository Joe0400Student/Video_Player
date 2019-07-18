import Widgets
import pygame
import time
import Menu
import Movie
from config import FileLoader


#
# CHANGE VARIABLE TO ENABLE OUTPUT TO STDOUT
#
STDOUT: bool = True

def main():
	pygame.init()
	settings: FileLoader = FileLoader()

	#
	# INIT of the settings module and checks
	#
	res_x: int = 0
	res_y: int = 0
	fullscreen: bool = True

	if(settings.check_exists("resolution_x") and
	   settings.check_exists("resolution_y")):
		if(settings.check_exists("fullscreen")):
			fullscreen = settings.get_element("fullscreen") == "True"
		else:
			fullscreen = True
			settings.add_element("fullscreen","True")
		res_x = int(settings.get_element("resolution_x"))
		res_y = int(settings.get_element("resolution_y"))
	else:
		res_x = pygame.display.Info().current_w
		res_y = pygame.display.Info().current_h
		fullscreen = True
		
		settings.add_element("resolution_x",str(res_x))
		settings.add_element("resolution_y",str(res_y))
		settings.add_element("fullscreen","True")
	
	#
	#	DISPLAY CREATION
	#
	disp: pygame.Surface
	if fullscreen:
		disp = pygame.display.set_mode((res_x, res_y), pygame.FULLSCREEN)
	else:
		disp = pygame.display.set_mode((res_x, res_y))
	pygame.display.set_caption("PyMedia")
	

	#
	#	INSTANCE VARIABLES
	#
	
	menu = Menu.Menu(res_x,res_y,disp)
	
	menu_visibility = True
	
	widgets = Widgets.Widgets()

	cur_menu = None
	
	slideout = False
	goback = False
	set_count = 0
	#
	#	INITIAL BLACKOUT
	#
	
	
	#  |<!MAINLOOP!>|
	
	while(True):
		disp.fill((128,128,128))
		LMB: bool = pygame.mouse.get_pressed()[0]
		mouse_pos = pygame.mouse.get_pos()
		keyboard_event = pygame.event.get()
		_ = widgets.drawTitleBar(res_x, res_y, disp, True, mouse_pos, LMB)
		
		if menu_visibility:
			if cur_menu is not None:
				menu_visibility = not menu.slideOut()
				_, _ = menu.drawMenu(keyboard_event)
			elif slideout:
				slideout = not menu.slideIn()
				_, _ = menu.drawMenu(keyboard_event)
				goback = False
			else:
				cur_menu, _ = menu.drawMenu(keyboard_event)
		else:
			goback, _ = widgets.backButton(5,5,disp,mouse_pos,LMB)
		if goback:
			menu_visibility = True
			cur_menu = None
			slideout = True
		for event in keyboard_event:
			if event.type == pygame.QUIT:
				pygame.quit()
				quit(0)
		
		pygame.display.flip()
		
if __name__=='__main__':
	main()
