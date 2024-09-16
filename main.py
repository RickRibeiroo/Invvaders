import pygame
import os
import time
import random


pygame.mixer.init()
pygame.font.init()


WIDTH, HEIGHT = 1020, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Invvaders by RICK RIBEIRO")

# Assets (Todas as duplicações são para aumentar a escala da imagem)
# Musica
pygame.mixer.music.load(os.path.join("assets", "Pix - Space travel.mp3"))

shoot_sound = pygame.mixer.Sound(os.path.join("assets", "shoot_sfx.mp3"))
shoot_sound.set_volume(0.1)
# Jogador principal // Tamanho original = (48x48)
SPACE_SHIP = pygame.image.load(os.path.join("assets", "Main_Ship_Full_Health.png"))
SPACE_SHIP = pygame.transform.scale(SPACE_SHIP, (75,75))

# Canhão // Tamanho original = (48x48)
CANNON_MAIN = pygame.image.load(os.path.join("assets", "MainShip_Weapons_Auto_Cannon_1.png"))
CANNON_MAIN = pygame.transform.scale(CANNON_MAIN, (75,75))

LIGHT_BEAM = pygame.image.load(os.path.join("assets", "Player_beam.png"))
LIGHT_BEAM = pygame.transform.scale(LIGHT_BEAM, (25,25))

# Motor
ENGINE = pygame.image.load(os.path.join("assets", "Main_Ship_Engine.png"))
ENGINE = pygame.transform.scale(ENGINE, (75,75))

# Inimigos

# Com essa escrita, a escala dos assets é 'direta'
BON_BON = pygame.transform.scale(pygame.image.load(os.path.join("assets", "Bon_Bon_1.png")), (40,40))
ALAN = pygame.transform.scale(pygame.image.load(os.path.join("assets", "Alan_1.png")), (40,40))
LIPS = pygame.transform.scale(pygame.image.load(os.path.join("assets", "Lips_1.png")), (40,40))

ENEMY_PROJECTILE = pygame.transform.scale(pygame.image.load(os.path.join("assets", "Enemy_projectile1.png")), (40,40)) 
ENEMY_PROJECTILE_RED = pygame.transform.scale(pygame.image.load(os.path.join("assets", "Enemy_projectile_RED.png")), (40,40)) 

# Background // Tamanho original do BG = (816 x 480)
# WIN multiplicador de tamanho = 1,25x 
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "blue-preview.png")),(WIDTH, HEIGHT))
GAME_OVER_IMG = pygame.image.load(os.path.join("assets", "GAME_OVER.png"))
GAME_OVER_IMG = pygame.transform.scale(GAME_OVER_IMG, (72 * 8, 8 * 8))

class Weapon:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, velocity):
        self.y += velocity

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)

class Ship:
    COOLDOWN = 20 # 60 = 1seg = 60fps
    def __init__(self, x, y, health= 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.weapon_img = None
        self.weapon_shoot = None
        self.engine = None
        self.weapons = []
        self.cool_down_cont = 0
        self.shoot_offset = 10
        self.alternate = True

    def draw(self, window): # Coloca a nave na tela
        window.blit(self.ship_img, (self.x, self.y))
        for weapon in self.weapons:
            weapon.draw(window)
        window.blit(self.weapon_img, (self.x, self.y))
        if self.engine != None: # O player tem, mas os inimigos não
            window.blit(self.engine, (self.x, self.y + 16))

    def move_weapon_shoot(self, velocity, obj):
        self.cooldown()
        for weapon in self.weapons:
            weapon.move(velocity)
            if weapon.off_screen(HEIGHT):
                self.weapons.remove(weapon)
            elif weapon.collision(obj):
                obj.health -=10
                self.weapons.remove(weapon)

    def cooldown(self):
        if self.cool_down_cont >= self.COOLDOWN:
            self.cool_down_cont = 0
        elif self.cool_down_cont > 0:
            self.cool_down_cont += 1

    def shoot(self):                # Spawna os projéteis do JOGADOR
        if self.cool_down_cont == 0:
            weapon = Weapon(self.x + self.shoot_offset, self.y +10, self.weapon_shoot) 
            self.weapons.append(weapon)
            self.cool_down_cont = 1

            # Alterna o valor do offset para que o LIGHT_BEAM alterne   
            if self.alternate:
                self.shoot_offset = 38
            else:
                self.shoot_offset = 10
            self.alternate = not self.alternate
            shoot_sound.play()

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = SPACE_SHIP
        self.weapon_img = CANNON_MAIN
        self.engine = ENGINE
        self.weapon_shoot = LIGHT_BEAM
        self.mask = pygame.mask.from_surface(self.ship_img) # Cria uma máscara para as colisões serem 'pixel perfect'
        self.weapon_mask = pygame.mask.from_surface(self.weapon_img)
        self.engine_mask = pygame.mask.from_surface(self.engine)
        self.max_health = health

    def move_weapon_shoot(self, velocity, objs):
        self.cooldown()
        for weapon in self.weapons:
            weapon.move(velocity)
            if weapon.off_screen(HEIGHT):
                self.weapons.remove(weapon)
            else:
                for obj in objs:
                    if weapon.collision(obj):
                        obj.health -= 100  # Dano ao inimigo
                        if obj.health <= 0:  # Se a vida do inimigo chegar a zero, ele é removido
                            objs.remove(obj)
                        self.weapons.remove(weapon)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (242,76,61), (self.x, self.y + self.get_height() + 10, self.ship_img.get_width(), 10)) # Barra de vida vermelha
        pygame.draw.rect(window, (19,194,107), (self.x, self.y + self.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10)) # Barra de vida ver


class Enemy(Ship):
    COLOR_MAP = {
            # "color": (_ENEMY, ENEMY_PROJECTILE)
            "yellow": (BON_BON, ENEMY_PROJECTILE),
            "green": (ALAN, ENEMY_PROJECTILE_RED),
            "pink": (LIPS, ENEMY_PROJECTILE)
            
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.weapon_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.projectiles = []
    
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for projectiles in self.projectiles:
            projectiles.draw(window)

    def move(self, velocity):
        self.y += velocity # Já que a nave inimiga só se move para baixo

    def shoot(self):    
        if self.cool_down_cont == 0:
            projectile = Weapon(self.x, self.y, self.weapon_img) # self.x e self.y são de onde as balas começam
            self.projectiles.append(projectile)
            self.cool_down_cont = 1

def collide(obj1, obj2):
    diff_x = obj2.x - obj1.x
    diff_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (diff_x, diff_y)) != None # return (x, y)

def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    ship_velocity = 5
    enemy_velocity = 1
    weapon_shoot_velocity = 5
    enemy_weapon_shoot_velocity = 4

    main_font = pygame.font.Font("assets/8-BIT WONDER.ttf", 20)

    enemies = []

    wave_lenght = 5

    player = Player((WIDTH - 75) / 2, HEIGHT - 100) # Posição inicial
 
    clock = pygame.time.Clock()

    lost = False # Condição de parada para GAME OVER!
    lost_cont = 0 # Conta o tempo 

    def update_display(): # Atualiza o display
        WIN.blit(BG, (0,0)) # Seta o BG em (x = 0 , y = 0)
        # No pygame, (x = 0, y = 0) é no canto superior esquerdo, ou seja
        # x+ vai para a direita e y+ vai para baixo
        lives_label = main_font.render(f"Vidas {lives}", 1, (242, 76, 61)) # (Texto, 1 (na maioria dos casos), (RGB))
        level_label = main_font.render(f"Wave {level}", 1, (69, 140, 100))

        WIN.blit(lives_label, (10, 10)) # Blit, como antes, seve para colocar coisas na tela
        # A equação da (pos x) coloca o LEVEL no canto direito, independente do tamanho da tela
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies: # Loop para os inimigos aparecerem
            enemy.draw(WIN)

        player.draw(WIN) # Atualiza a nave

        if lost:
            game_over_rect = GAME_OVER_IMG.get_rect(center=(WIDTH/2 , HEIGHT/2))
            WIN.blit(GAME_OVER_IMG, game_over_rect.topleft)
            
        pygame.display.update() # Atualiza o display
    
    while run:
        clock.tick(FPS)
        update_display()

        # Condição de parada via inimigos
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_cont += 1

        if lost:
            if lost_cont > FPS * 3: # 60fps (seg) * (espera)
                run = False
            else:
                continue
        
        if len(enemies) == 0: # Se a quantidade de inimigos for 0, ou seja, passou de nível, aumente um level
            level += 1
            wave_lenght += 5 # Adiciona +5 inimigos na tela
            for i in range(wave_lenght):
                # Essa linha aleatoriza o nascimento de inimigos
                enemy = Enemy(random.randrange(50, WIDTH - 150), random.randrange(-1400, -75), random.choice(["yellow","green", "pink"])) # Valores negativos para que eles nasçam fora da tela
                enemies.append(enemy) # Adiciona o inimigo à (enemies)

        for event in pygame.event.get():
            # Para o jogo se clicar no X no canto
            if event.type == pygame.QUIT:
                quit()

        # Movimentação player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - ship_velocity > 0: # Esquerda
            player.x -= ship_velocity
        if keys[pygame.K_d] and player.x + ship_velocity + player.get_width() < WIDTH: # Direita
            player.x += ship_velocity
        if keys[pygame.K_w] and player.y - ship_velocity > 0: # Cima
            player.y -= ship_velocity
        if keys[pygame.K_s] and player.y + ship_velocity + player.get_height() + 20 < HEIGHT: # Baixo (+20 por conta da barra de vida)
            player.y += ship_velocity
        if keys[pygame.K_SPACE]:
            player.shoot()

        # Movimentação inimiga
        for enemy in enemies[:]:
            enemy.move(enemy_velocity)
            enemy.move_weapon_shoot(enemy_weapon_shoot_velocity, player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 20  
                enemies.remove(enemy)

            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

            for projectile in enemy.projectiles[:]: # Atualiza a movimentação dos projéteis
                projectile.move(enemy_weapon_shoot_velocity)
                if projectile.off_screen(HEIGHT):
                    enemy.projectiles.remove(projectile)
                elif collide(projectile, player):
                    player.health -= 10
                    enemy.projectiles.remove(projectile)

        player.move_weapon_shoot(-weapon_shoot_velocity, enemies)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x,y)
    surface.blit(textobj,textrect)

def button(message, x, y, width, height, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(WIN, active_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(WIN, inactive_color, (x, y, width, height))

    draw_text(message, pygame.font.Font("assets/8-BIT WONDER.ttf", 30), (255,255,255), WIN, x + width//2, y + height//2)

########################################################################################################################################

def main_menu():
    title_font = pygame.font.Font("assets/8-BIT WONDER.ttf", 30)
    
    def start_game():
        main()

    def quit_game():
        pygame.quit()
        quit()

    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=-1)
    
    run = True
    while run:
        WIN.blit(BG, (0,0))

        button("COMECAR", WIDTH//2 - 125, HEIGHT//2 - 50, 250, 50, (17,89,35), (31, 115, 52), start_game)
        button("SAIR", WIDTH//2 - 125, HEIGHT //2 + 50, 250, 50, (242,5,5), (115, 2 , 2), quit_game)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                main()

    pygame.quit()

main_menu()
