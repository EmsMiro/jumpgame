import pgzrun
from plataformer import * 

# constantes dos tiles
TILE_SIZE = 18
ROWS = 50
COLS = 30

# constantes do mapa
WIDTH = TILE_SIZE * ROWS
HEIGHT = TILE_SIZE * COLS
TITLE = "Jump Game"
game_state = "menu" #estado inicial do game, na menu inicial
music_on = True #estado inicial da música
coin_sound = sounds.coin  # Carrega o som da moeda


# cria a camada do menu inicial
menu_background = pygame.Surface((WIDTH, HEIGHT))
menu_background.fill((100, 100, 255))  # cor azulada para o fundo 
menu_background.set_alpha(150)  # efeito de desfoque

# botão "Play"
play_button = Rect(WIDTH//2 - 75, HEIGHT//2 - 25, 150, 50)

#botão musica on/off
music_button = Rect(WIDTH//2 - 75, HEIGHT//2 + 40, 150, 50)

#construção do mapa
platforms = build("levelonemap_plataforms.csv", TILE_SIZE)
obstacles = build("levelonemap_obstacles.csv", TILE_SIZE)
mushrooms = build("levelonemap_mushrooms.csv", TILE_SIZE)

#sprites do personagem
color_key = (0,0,0)
redpanda_stand = Sprite("redpanda.png", (0,32,32,32), 4, color_key, 10)
redpanda_walk = Sprite("redpanda.png", (0,64,32,32), 8, color_key, 5)

#criando o personagem principal
player = SpriteActor (redpanda_stand)
player.bottomleft = (10, HEIGHT - TILE_SIZE)
# variáveis de controle do personagem
player.velocity_x = 3
player.velocity_y = 0
player.jumping = False
player.alive = True

#variáveis globais
gravity = 1
jump_velocity = -10
over = False
win = False

#variáveis do mapa
score = 0

#função q inicia a múscia
def toggle_music():
    global music_on
    if music_on:
        music.stop()
    else:
        music.play('happysong')
    music_on = not music_on

#toca a música ao iniciar o game
music.play('happysong')

def draw():
    screen.clear()
    #screen.fill("skyblue")
    if game_state == "menu":
        screen.blit(menu_background, (0, 0))  # Aplica o fundo desfocado
        screen.draw.text("Jump Game", center=(WIDTH // 2, HEIGHT // 4), fontsize=50, color="white")
        #botão play/start game
        screen.draw.filled_rect(play_button, "orange")
        screen.draw.text("Play", center=play_button.center, fontsize=30, color="white")

        #botão music on/off
        screen.draw.filled_rect(music_button, "gray")
        music_text = "MUSIC ON" if music_on else "Music OFF"
        screen.draw.text(music_text, center=music_button.center, fontsize=30)
        
    elif game_state == "game":
        screen.fill("skyblue")  # Fundo do jogo        
            
        #desenhando todas as camadas das plataformas
        for plataform in platforms:
            plataform.draw()

        #desenhando todos as camadas de obstáculos
        for obstacle in obstacles:
            obstacle.draw()

        #desenhando todos os cogumelos coletáveis das camadas
        for mushroom in mushrooms:
            mushroom.draw()

        #função que desenha o personagem
        if player.alive:
            player.draw()
        
        #criando o score no canto superior direito da tela
        screen.draw.text(f"Score: {score}", (WIDTH - 120, 10), fontsize=30, color="black")

    # mostra mensagem de game over
    if over:
        screen.draw.text("GAME OVER", center=(WIDTH/2, HEIGHT/2))
    if win:
        screen.draw.text("YOU WIN!", center=(WIDTH/2, HEIGHT/2))


def update():
    global over, win, score
    if game_state == "game":
        pass  
    # controle de movimento p/esquerda
    if keyboard.LEFT and player.midleft[0] > 0:
        player.x -= player.velocity_x
        player.sprite = redpanda_walk
        player.flip_x = True #espelhar o sprite do personagem p/esquerda
        # se o personagem colidir com a plata forma
        if player.collidelist(platforms) != -1:
            # seleciona o objeto com o qual ele colidiu
            object = platforms[player.collidelist(platforms)]
            player.x = object.x + (object.width / 2 + player.width / 2)

    #controle de movimento p/direita
    elif keyboard.RIGHT and player.midright[0] < WIDTH:
        player.x += player.velocity_x
        player.sprite = redpanda_walk
        player.flip_x = False #mantém o espelhamento do sprite p/direita
         # se o personagem colidir com a plata forma
        if player.collidelist(platforms) != -1:
            # seleciona o objeto com o qual ele colidiu
            object = platforms[player.collidelist(platforms)]
            player.x = object.x - (object.width / 2 + player.width / 2)

    #controle da gravidade
    player.y += player.velocity_y
    player.velocity_y += gravity
    # colisão do personagem com plataformas
    if player.collidelist(platforms) != -1:
        # pegando o objeto que o personagem colidiu
        object = platforms[player.collidelist(platforms)]

        #movimento pra baixo => bater no chão
        if player.velocity_y >= 0:
            player.y = object.y - (object.height / 2 + player.height / 2)
            player.jumping = False
        #movimento pra cima e bater com a cabeça
        else: 
            player.y = object.y + (object.height / 2 + player.height / 2)
        #player.y = object.y - (object.height / 2 + player.height / 2)
        player.velocity_y = 0

        # verificação de colisão com obstáculos
        if player.collidelist(obstacles)!= -1:
            player.alive = False
            over = True
        # verificação de colisão com os cogumelos
        for mushroom in mushrooms:
            if player.colliderect(mushroom):
                coin_sound.play() #som de coleta de objeto
                mushrooms.remove(mushroom)
                score += 1 #aumenta o placar do score de cogumelos
        if len(mushrooms) == 0:
            win = True


def on_key_down(key):
    if key == keys.UP and not player.jumping:
        player.velocity_y = jump_velocity
        player.jumping = True

def on_key_up(key):
    if key == keys.LEFT or key == keys.RIGHT:
        player.sprite = redpanda_stand
        # mantém o flip_x correto dependendo da última direção
        if key == keys.LEFT:
            player.flip_x = True
        elif key == keys.RIGHT:
            player.flip_x = False

def on_mouse_down(pos):
    global game_state, music_on
    
    if game_state == "menu" and play_button.collidepoint(pos):
        game_state = "game"  # troca pro jogo
    elif music_button.collidepoint(pos):
        toggle_music() #alterna o estado da música
        
    

pgzrun.go()
