import pygame
import random
import sys

pygame.init()
win_size = 700
clock = pygame.time.Clock()
window = pygame.display.set_mode((win_size, win_size))
pygame.display.set_caption("Space Invaders")

playerImg = pygame.image.load('img/player.png').convert_alpha()
enemyImg = pygame.image.load('img/enemy.png').convert_alpha()
bulletImg = pygame.image.load('img/shot.png').convert_alpha()
enemyBulletImg = pygame.image.load('img/enemy_shot.png').convert_alpha()
backgroundImg = pygame.image.load('img/background.png').convert()
font = pygame.font.Font("img/CosmicAlien-V4Ax.ttf", 32)
endFont = pygame.font.Font("img/CosmicAlien-V4Ax.ttf", 64)

class Player():
    def __init__(self):
        self.x = win_size / 2
        self.y = win_size - 25
        self.vel = 5
        self.lifes = 2 # because it adds 1 when there are no enemies and there are none at at the beggining
        self.img = playerImg
        self.can_shoot = True
        self.draw_hitbox = False
        self.width = playerImg.get_width()
        self.height = playerImg.get_height()
        self.hitbox = (self.x, self.y, self.width, self.height)

    def draw(self, window):
        self.hitbox = (self.x - 5, self.y - 5, self.width + 10, self.height + 10)
        if self.draw_hitbox:
            pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)
        window.blit(self.img, (self.x, self.y))

class Enemy(Player):
    def __init__(self, x, y, row, column):
        Player.__init__(self)
        self.x = x
        self.y = y
        self.row = row
        self.column = column
        self.vel = 1
        self.can_shoot = False
        self.left = True # Defines direction of enemies
        self.img = enemyImg
        self.width = enemyImg.get_width()
        self.height = enemyImg.get_height()

class Bullet(Player):
    def __init__(self, player_x, player_y):
        Player.__init__(self)
        self.x =  player_x
        self.y = player_y - playerImg.get_height()
        self.vel = 7
        self.img = bulletImg
        self.width = bulletImg.get_width()
        self.height = bulletImg.get_height()

class enemyBullet(Player):
    def __init__(self, enemy_x, enemy_y):
        self.x = enemy_x
        self.y = enemy_y
        self.vel = 7
        self.draw_hitbox = False
        self.img = enemyBulletImg
        self.width = enemyBulletImg.get_width()
        self.height = enemyBulletImg.get_height()


player = Player()
player_lives = 2
bullet = Bullet(-10, -10)
enemy_bullet = enemyBullet(-20, -20)
score = 0
enemies = []
enem_bullets = []

def updateGameWindow(player, enemies, bullet):
    global score
    scoreTxt = "SCORE: " + str(score)
    livesTxt = "LIVES: " + str(player.lifes)
    text = font.render(scoreTxt, True, (0, 255, 0))
    text1 = font.render(livesTxt, True, (0, 255, 0))
    window.blit(backgroundImg, (0, 0))
    window.blit(text, (20, 10))
    window.blit(text1, (490, 10))
    player.draw(window)
    if player.can_shoot is False:
        bullet.draw(window)
    for x in enemies:
        x.draw(window)
    for x in enem_bullets:
        x.draw(window)
    if checkDefeat():
        defeatTxt = 'GAME OVER'
        text2 = endFont.render(defeatTxt, True, (255, 0, 0))
        window.blit(text2, (125,300))
    pygame.display.update()

def createEnemies(): # creates enemies
    enemy_x = 10
    enemy_y = 80
    enemy_row = 0
    enemy_column = 0
    for i in range(55):
        if i % 11 is 0 and i > 0:
            enemy_y += 40
            enemy_x = 10
            enemy_row += 1
            enemy_column = 0
        enemy = Enemy(enemy_x, enemy_y, enemy_row, enemy_column)
        enemies.append(enemy)
        enemy_x += 50
        enemy_column += 1
    return enemies

def moveEnemies(enemies): # defines enemy movement
    for enemy in enemies:
        if enemy.x == win_size - enemy.width:
            for x in enemies:
                x.y += 4
                x.left = False
        elif enemy.x == 0:
            for x in enemies:
                x.y += 4
                x.left = True
        if enemy.left:
            enemy.x += enemy.vel
        else:
            enemy.x -= enemy.vel

def hitEnemies(enemies, bullet): # defines when enemy is hit
    global score
    for x in enemies:
        try:
            if bullet.y - bullet.width < x.hitbox[1] + x.hitbox[3] and bullet.y + bullet.width > x.hitbox[1]:
                if bullet.x + bullet.width > x.hitbox[0] and bullet.x - bullet.width < x.hitbox[0] + x.hitbox[2]:
                    enemies.remove(x)
                    player.can_shoot = True
                    bullet.x = -30
                    score += 10
        except ValueError:
            player.can_shoot = True
            bullet.x = -30
            score += 10

def moveBullet(bullet, player): # defines bullet movement
    if bullet.y > 0 and not player.can_shoot:
        bullet.y -= bullet.vel
    else:
        player.can_shoot = True

def enemyShooters(): # defines which enemies can shoot but its written like shit
    for enemy in enemies:
        li = {0: [x.column for x in enemies if x.row is 0], 1: [x.column for x in enemies if x.row is 1], 2: [x.column for x in enemies if x.row is 2],
              3: [x.column for x in enemies if x.row is 3], 4: [x.column for x in enemies if x.row is 4]}
        try:
            if enemy.column not in li[enemy.row + 1]:
                 enemy.can_shoot = True
        except KeyError:
            enemy.can_shoot = True

def enemyShooting(): # defines randomly which enemies will be shooting
    for x in enemies:
        if x.can_shoot is True:
            if random.randint(0, 10000) > 9965:
                enemy_bullet = enemyBullet(x.x, x.y + x.height)
                enem_bullets.append(enemy_bullet)

    for x in enem_bullets:
        if x.y < win_size:
            x.y += x.vel
        else:
            enem_bullets.remove(x)

def hitPlayer(): # defines when player is hit
    for bullet in enem_bullets:
        if bullet.y - bullet.width < player.hitbox[1] + player.hitbox[3] and bullet.y + bullet.width > player.hitbox[1]:
            if bullet.x + bullet.width > player.hitbox[0] and bullet.x - bullet.width < player.hitbox[0] + player.hitbox[2]:
                enem_bullets.remove(bullet)
                player.lifes -= 1

def checkDefeat():
    for x in enemies:
        if x.y >= player.y:
            return True
        elif player.lifes is 0:
            return True


while True:
    clock.tick(56)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    if len(enemies) is 0:
        createEnemies()
        player.lifes += 1

    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= player.vel

    if keys[pygame.K_RIGHT] and player.x < (win_size - player.width):
        player.x += player.vel

    if keys[pygame.K_SPACE] and player.can_shoot:
        player.can_shoot = False
        bullet = Bullet(player.x, player.y)
        bullet.draw(window)

    if checkDefeat():
        player.can_shoot = False
        enem_bullets.clear()

    else:
        enemyShooters()
        enemyShooting()
        hitPlayer()
        moveEnemies(enemies)
        moveBullet(bullet, player)
        hitEnemies(enemies, bullet)
    updateGameWindow(player, enemies, bullet)