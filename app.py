import sys
import pygame
from pygame.locals import *
from random import randint

pygame.init()

musica_de_fundo = pygame.mixer_music.load('musica.mp3')
pygame.mixer.music.play(-1)

barulho_da_colisao = pygame.mixer.Sound('coin.wav')


y_cobra = 0
x_cobra = 0

velocidade = 10
x_controle = velocidade
y_controle = 0

x_maca = randint(40,600)
y_maca = randint(50,430)

pontos = 0
placar = pygame.font.Font(None, 36)
game_over = False
altura_tela = 480
largura_tela = 640

relogio = pygame.time.Clock()
tela = pygame.display.set_mode((640,480))
pygame.display.set_caption("Snake Attak")

lista_cobra = []
tamanho_inicial = 5
def aumenta_cobra(lista_cobra):
    for XeY in lista_cobra:
        #XeY = [x,y]
        #XeY[0] = x
        #XeY[1] = y
        pygame.draw.rect(tela, (0,200,0), (XeY[0],XeY[1], 20,20))

def restart_game():
    global x_cobra, y_cobra, pontos, tamanho_inicial, lista_cobra, game_over
    game_over = False
    x_cobra = 0
    y_cobra = 0
    pontos = 0
    tamanho_inicial = 5
    lista_cobra = []


while True:
    relogio.tick(30)
    tela.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
          
            if event.key == K_a and x_controle != 10:
                x_controle = -10
                y_controle = 0
            if event.key == K_d and x_controle != -10:
                x_controle = 10
                y_controle = 0
            if event.key == K_w and y_controle != 10:
                x_controle = 0
                y_controle = -10
            if event.key == K_s and y_controle != -10:
                x_controle = 0
                y_controle = 10

            
    x_cobra = x_cobra + x_controle
    y_cobra = y_cobra + y_controle
    if x_cobra > largura_tela:
        x_cobra = 0
    if x_cobra < 0:
        x_cobra = largura_tela
    if y_cobra > altura_tela:
        y_cobra = 0
    if y_cobra < 0:
        y_cobra = altura_tela



    cobra = pygame.draw.rect(tela, (0,255,0), (x_cobra,y_cobra,20,20))
    maca = pygame.draw.rect(tela, (255,0,0), (x_maca,y_maca,20,20))

    texto = placar.render("Pontos: " + str(pontos), True, (255,255,255))
    tela.blit(texto, (10, 10))

    if cobra.colliderect(maca):
        print("colidiu")
        x_maca = randint(40,600)
        y_maca = randint(50,430)
        #pontos = pontos + 1
        pontos += 1
        barulho_da_colisao.play()
        tamanho_inicial += 1
    
    

    lista_cabeca = []
    lista_cabeca.append(x_cobra)
    lista_cabeca.append(y_cobra)
    
    lista_cobra.append(lista_cabeca)

    if lista_cobra.count(lista_cabeca) > 1:
        game_over = True
        while game_over:
            tela.fill((0,0,0))
            game_over_texto = placar.render("Game Over! ", True, (255,0,0))
            game_over_subtitulo = placar.render("Pressione R para reiniciar", True, (255,255,255))

            tela.blit(game_over_texto, (largura_tela // 2 - 100, altura_tela // 2 - 20))
            tela.blit(game_over_subtitulo, (largura_tela // 2 - 150, altura_tela // 2 + 20))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        restart_game()

    if len(lista_cobra) > tamanho_inicial:
        del lista_cobra[0]

    aumenta_cobra(lista_cobra)

    pygame.display.update()
