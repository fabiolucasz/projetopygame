import sys
import pygame 
from pygame.locals import *
from random import randint

pygame.init()
y_cobra = 0
x_cobra = 0
x_maca = randint(40, 600)
y_maca = randint(50, 430)

altura = 480
largura = 640
relogio = pygame.time.Clock()
tela = pygame.display.set_mode((640,480))
pygame.display.set_caption("Snake Attack")
lista_cobra = []
def aumenta_cobra(lista_cobra):
    for XeY in lista_cobra:
        #XeY = [x,y]
        #XeY[0] = x
        #XeY[1] = y
        pygame.draw.rect(tela, (0,200,0), (XeY[0],XeY[1], 20,20))

while True:
    relogio.tick(60)
    tela.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if pygame.key.get_pressed()[K_a]:
        if x_cobra <= 0:
            x_cobra = largura
        x_cobra = x_cobra - 20
    if pygame.key.get_pressed()[K_d]:
        if x_cobra >= largura:
            x_cobra = 0
        x_cobra = x_cobra + 20
    if pygame.key.get_pressed()[K_w]:
        y_cobra = y_cobra - 20
    if pygame.key.get_pressed()[K_s]:
        y_cobra = y_cobra + 20

    cobra = pygame.draw.rect(tela, (0,200,0), (x_cobra,y_cobra,20,20))
    maca = pygame.draw.rect(tela,(255,0,0),(x_maca,y_maca,20,20))

    if cobra.colliderect(maca):
        print("colidiu")
        x_maca = randint(40, 600)
        y_maca = randint(50,430)

    lista_cabeca = []
    lista_cabeca.append(x_cobra)
    lista_cabeca.append(y_cobra)
    
    lista_cobra.append(lista_cabeca)

    aumenta_cobra(lista_cobra)

    pygame.display.update()