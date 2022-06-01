import pygame
import pygame_menu

pygame.init()
surface = pygame.display.set_mode((600, 400))

color_dark = (100,100,100)

def Salonia():
    from Pacman.pacman import Pacmanicon
    pass

def Fini():
    # Do the job here !
    pass

def Alejo():
    # Do the job here !
    pass

menu = pygame_menu.Menu('Bienvenido =D', 400, 300)

menu.add.button('Pacman', Salonia)
menu.add.button('Romper bloques', Fini)
menu.add.button('Cubos randoms', Alejo)
menu.add.button('Salir', pygame_menu.events.EXIT)

menu.mainloop(surface)