import pygame
import sys
import random
import os
import imageio

icone_arquivo = os.path.join(os.path.dirname(os.path.abspath(__file__)), './imagem/monstre.ico')
pygame.display.set_icon(pygame.image.load(icone_arquivo))

# Inicialização do Pygame
pygame.init()

# Configurações do jogo
largura_tela = 800
altura_tela = 600
cor_fundo = (255, 255, 255)

# Configurações do menu
cor_texto = (0, 0, 0)
cor_destaque = (255, 0, 0)  # Cor da opção selecionada
fonte_menu = pygame.font.SysFont(None, 48)

# Estados do jogo
ESTADO_MENU = 0
ESTADO_JOGO = 1
ESTADO_EXPLOSAO = 2
estado_atual = ESTADO_MENU

# Função para exibir o menu
def exibir_menu(selecionado, mouse_sobre_opcao):
    texto_novo_jogo = fonte_menu.render("Novo Jogo", True, cor_destaque if selecionado == 0 or (selecionado == -1 and mouse_sobre_opcao) else cor_texto)
    texto_sair = fonte_menu.render("Sair", True, cor_destaque if selecionado == 1 or (selecionado == -1 and mouse_sobre_opcao) else cor_texto)

    retangulo_novo_jogo = texto_novo_jogo.get_rect(topleft=(largura_tela // 2 - texto_novo_jogo.get_width() // 2, altura_tela // 2 - 50))
    retangulo_sair = texto_sair.get_rect(topleft=(largura_tela // 2 - texto_sair.get_width() // 2, altura_tela // 2 + 50))

    tela.blit(texto_novo_jogo, retangulo_novo_jogo.topleft)
    tela.blit(texto_sair, retangulo_sair.topleft)

    return retangulo_novo_jogo, retangulo_sair

# Função para carregar e redimensionar uma imagem
def carregar_e_redimensionar_imagem(nome_arquivo, largura, altura):
    try:
        imagem = pygame.image.load(nome_arquivo)
        imagem_redimensionada = pygame.transform.scale(imagem, (largura, altura))
        return imagem_redimensionada
    except pygame.error as mensagem_erro:
        print(f"Não foi possível carregar a imagem {nome_arquivo}: {mensagem_erro}")
        raise SystemExit(mensagem_erro)

# Função para carregar e exibir uma animação gif
def exibir_gif(nome_arquivo, largura, altura):
    try:
        gif = pygame.image.load(nome_arquivo)
        gif_rect = gif.get_rect(center=(largura_tela // 2, altura_tela // 2))

        tela.fill(cor_fundo)
        tela.blit(gif, gif_rect)
        pygame.display.flip()
        pygame.time.delay(100)  # Ajuste o tempo de atraso conforme necessário
    except pygame.error as mensagem_erro:
        print(f"Não foi possível carregar a animação {nome_arquivo}: {mensagem_erro}")
        raise SystemExit(mensagem_erro)

# Criando a tela
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption('bombas')

# Obtém o diretório do script Python
diretorio_script = os.path.dirname(os.path.abspath(__file__))

# Carregando e redimensionando imagens do jogador, obstáculo e colisão
largura_jogador = 50
altura_jogador = 50
gif_jogador = carregar_e_redimensionar_imagem(os.path.join(diretorio_script, 'imagem', 'monstre.jpeg'), largura_jogador, altura_jogador)

largura_obstaculo = 45
altura_obstaculo = 45
imagem_obstaculo = carregar_e_redimensionar_imagem(os.path.join(diretorio_script, 'imagem', 'bomba.jpeg'), largura_obstaculo, altura_obstaculo)

largura_colisao = 50
altura_colisao = 50
gif_explosao = os.path.join(diretorio_script, 'imagem', 'explosao.png')

# Definindo a posição inicial do jogador
posicao_jogador = [largura_tela // 2 - largura_jogador // 2, altura_tela - altura_jogador - 10]

# Lista para armazenar obstáculos
obstaculos = []

# Estado do menu
selecionado = 0
mouse_sobre_opcao = False

# Loop principal do jogo
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.KEYDOWN:
            if estado_atual == ESTADO_MENU:
                if evento.key == pygame.K_RETURN:
                    if selecionado == 0:
                        estado_atual = ESTADO_JOGO
                    elif selecionado == 1:
                        pygame.quit()
                        sys.exit()
                elif evento.key == pygame.K_UP:
                    selecionado = (selecionado - 1) % 2
                elif evento.key == pygame.K_DOWN:
                    selecionado = (selecionado + 1) % 2

            elif estado_atual == ESTADO_EXPLOSAO:
                if evento.key == pygame.K_RETURN:
                    estado_atual = ESTADO_MENU

        if estado_atual == ESTADO_MENU:
            if evento.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = evento.pos
                # Verifica se o mouse está sobre as opções do menu
                retangulo_novo_jogo, retangulo_sair = exibir_menu(selecionado, mouse_sobre_opcao)
                mouse_sobre_opcao = retangulo_novo_jogo.collidepoint(mouse_x, mouse_y) or retangulo_sair.collidepoint(mouse_x, mouse_y)

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                # Verifica se o mouse clicou em alguma opção do menu
                if retangulo_novo_jogo.collidepoint(mouse_x, mouse_y):
                    estado_atual = ESTADO_JOGO
                elif retangulo_sair.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()

    if estado_atual == ESTADO_MENU:
        # Preenchendo o fundo da tela
        tela.fill(cor_fundo)

        # Exibir o menu
        exibir_menu(selecionado, mouse_sobre_opcao)

    elif estado_atual == ESTADO_JOGO:
        # Movimentação do jogador
        mouse_x, _ = pygame.mouse.get_pos()
        posicao_jogador[0] = mouse_x - largura_jogador // 2

        # Verificando colisões com obstáculos
        for obstaculo in obstaculos:
            obstaculo_rect = pygame.Rect(obstaculo[0], obstaculo[1], largura_obstaculo, altura_obstaculo)
            jogador_rect = pygame.Rect(posicao_jogador[0], posicao_jogador[1], largura_jogador, altura_jogador)

            if jogador_rect.colliderect(obstaculo_rect):
                estado_atual = ESTADO_EXPLOSAO
                obstaculos = []

        # Criando novos obstáculos em intervalos aleatórios
        if random.randint(0, 100) < 5:
            obstaculos.append([random.randint(0, largura_tela - largura_obstaculo), 0])

        # Movimentação dos obstáculos
        for obstaculo in obstaculos:
            obstaculo[1] += 5

        # Removendo obstáculos que saíram da tela
        obstaculos = [obstaculo for obstaculo in obstaculos if obstaculo[1] < altura_tela]

        # Preenchendo o fundo da tela
        tela.fill(cor_fundo)

        # Desenhando jogador e obstáculos
        tela.blit(gif_jogador, posicao_jogador)
        for obstaculo in obstaculos:
            tela.blit(imagem_obstaculo, (obstaculo[0], obstaculo[1]))

    elif estado_atual == ESTADO_EXPLOSAO:
        # Preenchendo o fundo da tela
        tela.fill(cor_fundo)

        # Exibindo a animação de explosão
        exibir_gif(gif_explosao, largura_colisao, altura_colisao)

        # Atualizando a tela
        pygame.display.flip()

        # Esperando um momento antes de voltar ao menu
        pygame.time.delay(2000)
        estado_atual = ESTADO_MENU

    # Atualizando a tela
    pygame.display.flip()

    # Controlando a taxa de atualização da tela
    pygame.time.Clock().tick(30)
