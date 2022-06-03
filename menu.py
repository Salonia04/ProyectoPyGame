import pygame
import pygame_menu


pygame.init()
surface = pygame.display.set_mode((600, 400))

color_dark = (100,100,100)

def Salonia():
    from Pacman.pacman import Pacmanicon
    pass

def Alejo():
    import Simon.SimonMain
    pass

def Fini():
    import Bloques.main
    pass

menu = pygame_menu.Menu('Bienvenido :)', 400, 300)

menu.add.button('Pacman', Salonia)
menu.add.button('Ledesma dice', Alejo)
menu.add.button('Bloquesitos', Fini)
menu.add.button('Salir', pygame_menu.events.EXIT)

menu.mainloop(surface)

