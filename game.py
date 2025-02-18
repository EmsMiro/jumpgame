import pgzrun
from plataformer import * 

# constantes da plataforma
TILE_SIZE = 18
ROWS = 50
COLS = 30

# constantes dos tiles
WIDTH = TILE_SIZE * ROWS
HEIGHT = TILE_SIZE * COLS
TITLE = "Jump Game"

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

def draw():
    screen.clear()
    screen.fill("skyblue")
    
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
    
    # mostra mensagem de game over
    if over:
        screen.draw.text("GAME OVER", center=(WIDTH/2, HEIGHT/2))
    if win:
        screen.draw.text("YOU WIN!", center=(WIDTH/2, HEIGHT/2))

def update():
    global over, win
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
                mushrooms.remove(mushroom)
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
pgzrun.go()
