from turtle import speed
import pygame
from pygame.locals import *


pygame.init()

#Tamaño de la pantalla 
screen_width = 600
screen_height = 600

#Crea la pantalla
screen = pygame.display.set_mode((screen_width, screen_height))

#Titulo de la pantalla
pygame.display.set_caption('Breakout')

#Fuente de texto
font = pygame.font.SysFont('Constantia', 30)

#Color del fondo
bg = (234, 218, 184)
#Color de los bloques
block_black = (255,255,255)
block_red = (242, 85, 96)
block_green = (86, 174, 87)
#Color del paddle 
paddle_col = (142, 135, 123)
paddle_outline = (100, 100, 100)
#Color de texto
text_col = (78, 81, 139)



#Define las variables
cols = 6
rows = 6
clock = pygame.time.Clock()
fps = 60
live_ball = False
game_over = 0
class Wall():
    #Divide la pantalla en una cuadrícula de bloques
    def __init__(self):
        self.width = screen_width // cols
        #Altura de los bloques
        self.height = 50

    def create_wall(self):
        self.blocks = []
        #Lista vacia por bloque individual
        block_individual = []
        for row in range(rows):
            #restablece la lista de filas de bloques
            block_row = []
            #iterar a través de cada columna en esa fila
            for col in range(cols):
                #genera posiciones x e y para cada bloque y crear un rectángulo a partir de eso
                block_x = col * self.width
                block_y = row * self.height
                rect = pygame.Rect(block_x, block_y, self.width, self.height)
                #asignar la dureza del bloque en función de la fila
                if row < 2:
                    strength = 3
                elif row < 4:
                    strength = 2
                elif row < 6:
                    strength = 1
                #crea una lista en este punto para almacenar los datos de color y rect
                block_individual = [rect, strength]
                #agrega ese bloque individual a la fila de bloques
                block_row.append(block_individual)
            #agrega la fila a la lista completa de bloques
            self.blocks.append(block_row)


    def draw_wall(self):
        for row in self.blocks:
            for block in row:
                #Asigna un color basado en la dureza
                if block[1] == 3:
                    block_col = block_black
                elif block[1] == 2:
                    block_col = block_green
                elif block[1] == 1:
                    block_col = block_red
                pygame.draw.rect(screen, block_col, block[0])
                pygame.draw.rect(screen, bg, (block[0]), 2)


#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
#Clase pelota
class game_ball():
    def __init__(self, x, y):
        self.reset(x, y)


    def move(self):

        #Limite de colisiones
        collision_thresh = 5

        #Comienza con la suposición de que el muro ha sido destruido por completo
        wall_destroyed = 1
        row_count = 0
        for row in wall.blocks:
            item_count = 0
            for item in row:
                #check collision
                if self.rect.colliderect(item[0]):
                    #Chequea si la colision viene de arriba
                    if abs(self.rect.bottom - item[0].top) < collision_thresh and self.speed_y > 0:
                        self.speed_y *= -1
                    #Chequea si la colision viene de abajo
                    if abs(self.rect.top - item[0].bottom) < collision_thresh and self.speed_y < 0:
                        self.speed_y *= -1                      
                    #Chequea si la colision viene de la izquierda
                    if abs(self.rect.right - item[0].left) < collision_thresh and self.speed_x > 0:
                        self.speed_x *= -1
                    #Chequea si la colision viene de la derecha
                    if abs(self.rect.left - item[0].right) < collision_thresh and self.speed_x < 0:
                        self.speed_x *= -1
                    #Reduce la dureza del bloque por cada toque
                    if wall.blocks[row_count][item_count][1] > 1:
                        wall.blocks[row_count][item_count][1] -= 1
                    else:
                        wall.blocks[row_count][item_count][0] = (0, 0, 0, 0)

                #Chequea si el bloque se destruyo
                if wall.blocks[row_count][item_count][0] != (0, 0, 0, 0):
                    wall_destroyed = 0
                #Incrementa el contador de items
                item_count += 1
            #Incrementa el contador de filas
            row_count += 1
        #Vuelve a chequear si el muro ha sido destruido
        if wall_destroyed == 1:
            self.game_over = 1



        #Chequea la colisión con la pared izquierda y derecha
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed_x *= -1

        #Chequea la colisión con la pared superior y inferior
        if self.rect.top < 0:
            self.speed_y *= -1
        if self.rect.bottom > screen_height:
            self.game_over = -1


        #Chequea la colisión con el paddle
        if self.rect.colliderect(player_paddle):
            if abs(self.rect.bottom - player_paddle.rect.top) < collision_thresh and self.speed_y > 0:
                self.speed_y *= -1
                self.speed_x += player_paddle.direction
                if self.speed_x > self.speed_max:
                    self.speed_x = self.speed_max
                elif self.speed_x < 0 and self.speed_x < -self.speed_max:
                    self.speed_x = -self.speed_max
            else:
                self.speed_x *= -1



        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.game_over


    #Dibuja la pelota a partir de las propiedades
    def draw(self):
        pygame.draw.circle(screen, paddle_col, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)
        pygame.draw.circle(screen, paddle_outline, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad, 3)


    #Propiedades de la pelota
    def reset(self, x, y):
        self.ball_rad = 10
        self.x = x - self.ball_rad
        self.y = y
        self.rect = Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
        self.speed_x = 4
        self.speed_y = -4
        self.speed_max = 5
        self.game_over = 0

#paddle class
class Paddle():
    def __init__(self):
        self.reset()


    def move(self):
        self.direction = 0
        #Tecla para presionar
        key = pygame.key.get_pressed()
        #Tecla para mover (izquierda)
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        #Tecla para mover (derecha)
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed
            self.direction = 1

    #Dibuja el paddle
    def draw(self):
        pygame.draw.rect(screen, paddle_col, self.rect)
        pygame.draw.rect(screen, paddle_outline, self.rect, 3)


    def reset(self):
        #define las variables del paddle
        self.height = 20
        self.width = int(screen_width / cols)
        self.x = int((screen_width / 2) - (self.width / 2))
        self.y = screen_height - (self.height * 2)
        self.speed = 10
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.direction = 0

#Crea el muro
wall = Wall()
wall.create_wall()

#Crea el paddle
player_paddle = Paddle()


#Crea la bola en una posicion arriba del paddle
ball = game_ball(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)

run = True
while run:

    clock.tick(fps)
    #Se mantiene el fondo
    screen.fill(bg)

    #Dibuja todos los objetos
    wall.draw_wall()
    player_paddle.draw()
    ball.draw()

    if live_ball:
        #Dibuja paddle
        player_paddle.move()
        #Dibuja la pelota
        game_over = ball.move()
        if game_over != 0:
            live_ball = False


    #Printea las instrucciones del jugador
    if not live_ball:
        if game_over == 0:
            draw_text('APRETA DONDE QUIERAS', font, text_col, 100, screen_height // 2 + 100)
        elif game_over == 1:
            draw_text('GANASTE!', font, text_col, 240, screen_height // 2 + 50)
            draw_text('APRETA DONDE QUIERAS', font, text_col, 100, screen_height // 2 + 100)
        elif game_over == -1:
            draw_text('PERDISTE!', font, text_col, 240, screen_height // 2 + 50)
            draw_text('APRETA DONDE QUIERAS', font, text_col, 100, screen_height // 2 + 100)

    #Eventos
    for event in pygame.event.get():
        #Posibilidad de salir
        if event.type == pygame.QUIT:
            run = False
        #Revivir
        if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
            live_ball = True
            ball.reset(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)
            player_paddle.reset()
            wall.create_wall()

    pygame.display.update()

pygame.quit()
