import pygame
import random
import sys

# Inicialização
pygame.init()
WIDTH, HEIGHT = 800, 600
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo Nave Atari")
clock = pygame.time.Clock()

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 255, 0)

# Fontes
font = pygame.font.SysFont("Arial", 28)
big_font = pygame.font.SysFont("Arial", 48)

# Nave
nave_width, nave_height = 60, 30
nave = pygame.Rect(WIDTH // 2 - nave_width // 2, HEIGHT - 60, nave_width, nave_height)
nave_speed = 5

# Tiro
tiros = []
tiro_width, tiro_height = 5, 10
tiro_speed = -7

# Inimigos
inimigos = []
inimigo_width, inimigo_height = 40, 30
inimigo_speed = 3
spawn_event = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_event, 1000)

# Score
score = 0

# Estados do jogo
START, PLAYING, GAME_OVER = 0, 1, 2
estado = START

def reset_game():
    global nave, tiros, inimigos, score
    nave.x = WIDTH // 2 - nave_width // 2
    tiros = []
    inimigos = []
    score = 0

def desenhar_tela_inicial():
    screen.fill(BLACK)
    titulo = big_font.render("JOGO DA NAVE", True, WHITE)
    instrucoes = font.render("Pressione qualquer tecla para começar", True, WHITE)
    screen.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, HEIGHT // 3))
    screen.blit(instrucoes, (WIDTH // 2 - instrucoes.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()

def desenhar_tela_game_over():
    screen.fill(BLACK)
    msg = big_font.render("GAME OVER", True, RED)
    restart = font.render("Pressione qualquer tecla para reiniciar", True, WHITE)
    final_score = font.render(f"Pontuação: {score}", True, GREEN)
    screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 3))
    screen.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, HEIGHT // 2))
    screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, HEIGHT // 1.5))
    pygame.display.flip()

def desenhar_jogo():
    screen.fill(BLACK)
    # Nave
    pygame.draw.rect(screen, GREEN, nave)

    # Tiros
    for tiro in tiros:
        pygame.draw.rect(screen, WHITE, tiro)

    # Inimigos
    for inimigo in inimigos:
        pygame.draw.rect(screen, RED, inimigo)

    # Score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH - score_text.get_width() - 20, 20))

    pygame.display.flip()

# Loop principal
running = True
while running:
    clock.tick(FPS)

    if estado == START:
        desenhar_tela_inicial()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                estado = PLAYING
                reset_game()

    elif estado == GAME_OVER:
        desenhar_tela_game_over()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                estado = START

    elif estado == PLAYING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == spawn_event:
                x = random.randint(0, WIDTH - inimigo_width)
                inimigos.append(pygame.Rect(x, 0, inimigo_width, inimigo_height))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    tiro = pygame.Rect(nave.centerx - tiro_width // 2, nave.y, tiro_width, tiro_height)
                    tiros.append(tiro)

        # Movimento nave
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and nave.left > 0:
            nave.x -= nave_speed
        if keys[pygame.K_d] and nave.right < WIDTH:
            nave.x += nave_speed

        # Movimento tiros
        for tiro in tiros[:]:
            tiro.y += tiro_speed
            if tiro.bottom < 0:
                tiros.remove(tiro)

        # Movimento inimigos
        for inimigo in inimigos[:]:
            inimigo.y += inimigo_speed
            if inimigo.colliderect(nave):
                estado = GAME_OVER
            if inimigo.top > HEIGHT:
                inimigos.remove(inimigo)

        # Colisões
        for tiro in tiros[:]:
            for inimigo in inimigos[:]:
                if tiro.colliderect(inimigo):
                    tiros.remove(tiro)
                    inimigos.remove(inimigo)
                    score += 10
                    break

        desenhar_jogo()

pygame.quit()
sys.exit()
