import sys
import pygame
from pygame.locals import *
from random import randint

pygame.init()

musica_de_fundo = pygame.mixer_music.load('musica.mp3')
pygame.mixer.music.play(-1)

barulho_da_colisao = pygame.mixer.Sound('coin.wav')

# Cobra Verde (Jogador 1)
x_cobra = 0
y_cobra = 0
x_controle = 10
y_controle = 0
lista_cobra = []
tamanho_inicial = 5
pontos = 0

# Cobra Azul (Jogador 2)
x_cobra2 = 100
y_cobra2 = 0
x2_controle = 10
y2_controle = 0
lista_cobra2 = []
tamanho2_inicial = 5
pontos2 = 0

# Geral
x_maca = randint(40,600)
y_maca = randint(50,430)
placar = pygame.font.Font(None, 36)
game_over = False
altura_tela = 480
largura_tela = 640

relogio = pygame.time.Clock()
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Snake Attak - 2 Jogadores")

def aumenta_cobra(lista, cor):
    for XeY in lista:
        pygame.draw.rect(tela, cor, (XeY[0], XeY[1], 20, 20))

def restart_game():
    global x_cobra, y_cobra, x_controle, y_controle, lista_cobra, tamanho_inicial, pontos
    global x_cobra2, y_cobra2, x2_controle, y2_controle, lista_cobra2, tamanho2_inicial, pontos2
    global x_maca, y_maca, game_over

    # Jogador 1
    x_cobra = 0
    y_cobra = 0
    x_controle = 10
    y_controle = 0
    lista_cobra = []
    tamanho_inicial = 5
    pontos = 0

    # Jogador 2
    x_cobra2 = 100
    y_cobra2 = 0
    x2_controle = 10
    y2_controle = 0
    lista_cobra2 = []
    tamanho2_inicial = 5
    pontos2 = 0

    # Comum
    x_maca = randint(40,600)
    y_maca = randint(50,430)
    game_over = False

while True:
    relogio.tick(30)
    tela.fill((0,0,0))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            # Jogador 1 - Teclas WASD
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

            # Jogador 2 - Teclas SETAS
            if event.key == K_LEFT and x2_controle != 10:
                x2_controle = -10
                y2_controle = 0
            if event.key == K_RIGHT and x2_controle != -10:
                x2_controle = 10
                y2_controle = 0
            if event.key == K_UP and y2_controle != 10:
                x2_controle = 0
                y2_controle = -10
            if event.key == K_DOWN and y2_controle != -10:
                x2_controle = 0
                y2_controle = 10

            # Reiniciar jogo
            if event.key == K_r:
                restart_game()

    # Movimento Jogador 1
    x_cobra += x_controle
    y_cobra += y_controle

    # Movimento Jogador 2
    x_cobra2 += x2_controle
    y_cobra2 += y2_controle

    # Tela circular (atravessa e volta)
    x_cobra %= largura_tela
    y_cobra %= altura_tela
    x_cobra2 %= largura_tela
    y_cobra2 %= altura_tela

    # Desenha maçã
    maca = pygame.draw.rect(tela, (255,0,0), (x_maca, y_maca, 20, 20))

    # Verifica colisão J1
    cobra = pygame.draw.rect(tela, (0,255,0), (x_cobra, y_cobra, 20, 20))
    if cobra.colliderect(maca):
        x_maca = randint(40,600)
        y_maca = randint(50,430)
        pontos += 1
        tamanho_inicial += 1
        barulho_da_colisao.play()

    # Verifica colisão J2
    cobra2 = pygame.draw.rect(tela, (0,0,255), (x_cobra2, y_cobra2, 20, 20))
    if cobra2.colliderect(maca):
        x_maca = randint(40,600)
        y_maca = randint(50,430)
        pontos2 += 1
        tamanho2_inicial += 1
        barulho_da_colisao.play()

    # Atualiza corpo da cobra verde (J1)
    cabeca = [x_cobra, y_cobra]
    lista_cobra.append(cabeca)
    if len(lista_cobra) > tamanho_inicial:
        del lista_cobra[0]

    # Atualiza corpo da cobra azul (J2)
    cabeca2 = [x_cobra2, y_cobra2]
    lista_cobra2.append(cabeca2)
    if len(lista_cobra2) > tamanho2_inicial:
        del lista_cobra2[0]

    # Verifica colisão consigo mesmo (J1)
    if lista_cobra.count(cabeca) > 1 or lista_cobra2.count(cabeca2) > 1:
        game_over = True

    if game_over:
        while game_over:
            tela.fill((0,0,0))
            texto1 = placar.render("Game Over!", True, (255,0,0))
            texto2 = placar.render("Pressione R para reiniciar", True, (255,255,255))
            tela.blit(texto1, (largura_tela // 2 - 100, altura_tela // 2 - 20))
            tela.blit(texto2, (largura_tela // 2 - 150, altura_tela // 2 + 20))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_r:
                    restart_game()

    # Desenha as cobras
    aumenta_cobra(lista_cobra, (0,255,0))  # verde
    aumenta_cobra(lista_cobra2, (0,0,255))  # azul

    # Placar
    texto_pontos = placar.render(f"Verde: {pontos}   Azul: {pontos2}", True, (255,255,255))
    tela.blit(texto_pontos, (10,10))

    pygame.display.update()
