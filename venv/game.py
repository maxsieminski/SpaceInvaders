import pygame
import random
import time
import sys
import os

pygame.init()
win_size = 700
clock = pygame.time.Clock()
window = pygame.display.set_mode((win_size, win_size))
pygame.display.set_caption("Space Invaders")

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


pic1 = resource_path('img/player.png')
pic2 = resource_path('img/enemy.png')
pic3 = resource_path('img/shot.png')
pic4 = resource_path('img/enemy_shot.png')
pic5 = resource_path('img/background.png')
font1 = resource_path("img/CosmicAlien-V4Ax.ttf")

playerImg = pygame.image.load(pic1).convert_alpha()
enemyImg = pygame.image.load(pic2).convert_alpha()
bulletImg = pygame.image.load(pic3).convert_alpha()
enemyBulletImg = pygame.image.load(pic4).convert_alpha()
backgroundImg = pygame.image.load(pic5).convert()
font = pygame.font.Font(font1, 32)
menuFont = pygame.font.Font(font1, 48)
endFont = pygame.font.Font(font1, 64)

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
        window.blit(self.img, (round(self.x), round(self.y)))

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
        self.vel = 9
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

def createEnemies(enemies): # creates enemies
    enemy_x = 10
    enemy_y = 80
    enemy_row = 0
    enemy_column = 0
    for i in range(60):
        if i % 12 == 0 and i > 0:
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
    if any(enemy.x == win_size - enemy.width or enemy.x == 0 for enemy in enemies):
        for x in enemies:
            x.y += 6
            x.left = not x.left
    if any(enemy.left for enemy in enemies):
        for enemy in enemies:
            enemy.x += enemy.vel
    else:
        for enemy in enemies:
            enemy.x -= enemy.vel

def hitEnemies(enemies, bullet, score, player, diffculty): # defines when enemy is hit
    for x in enemies:
        try:
            if bullet.y - bullet.width < x.hitbox[1] + x.hitbox[3] and bullet.y + bullet.width > x.hitbox[1]:
                if bullet.x + bullet.width > x.hitbox[0] and bullet.x - bullet.width < x.hitbox[0] + x.hitbox[2]:
                    enemies.remove(x)
                    player.can_shoot = True
                    bullet.x = -30
                    if diffculty == "EASY":
                        score += 5
                    if diffculty == "MEDIUM":
                        score += 10
                    if diffculty == "HARD":
                        score += 15
        except ValueError:
            player.can_shoot = True
            bullet.x = -30
            if diffculty == "EASY":
                score += 5
            if diffculty == "MEDIUM":
                score += 10
            if diffculty == "HARD":
                score += 15
    return score

def moveBullet(bullet, player): # defines bullet movement
    if bullet.y > 0 and not player.can_shoot:
        bullet.y -= bullet.vel
    else:
        player.can_shoot = True

def enemyShooters(enemies): # defines which enemies can shoot but its written like shit
    for enemy in enemies:
        li = {0: [x.column for x in enemies if x.row == 0], 1: [x.column for x in enemies if x.row == 1], 2: [x.column for x in enemies if x.row == 2],
              3: [x.column for x in enemies if x.row == 3], 4: [x.column for x in enemies if x.row == 4]}
        try:
            if enemy.column not in li[enemy.row + 1]:
                 enemy.can_shoot = True
        except KeyError:
            enemy.can_shoot = True

def enemyShooting(enemies, enem_bullets, difficulty): # defines randomly which enemies will be shooting
    for x in enemies:
        if x.can_shoot is True:
            if difficulty == "EASY":
                if random.randint(0, 10000) > 9985:
                    enemy_bullet = enemyBullet(x.x, x.y + x.height)
                    enem_bullets.append(enemy_bullet)
            elif difficulty == "MEDIUM":
                if random.randint(0, 10000) > 9970:
                    enemy_bullet = enemyBullet(x.x, x.y + x.height)
                    enem_bullets.append(enemy_bullet)
            elif difficulty == "HARD":
                if random.randint(0, 10000) > 9950:
                    enemy_bullet = enemyBullet(x.x, x.y + x.height)
                    enem_bullets.append(enemy_bullet)

    for x in enem_bullets:
        if x.y < win_size:
            x.y += x.vel
        else:
            enem_bullets.remove(x)

def hitPlayer(enem_bullets, player): # defines when player is hit
    for bullet in enem_bullets:
        if bullet.y - bullet.width < player.hitbox[1] + player.hitbox[3] and bullet.y + bullet.width > player.hitbox[1]:
            if bullet.x + bullet.width > player.hitbox[0] and bullet.x - bullet.width < player.hitbox[0] + player.hitbox[2]:
                enem_bullets.remove(bullet)
                player.lifes -= 1

def checkDefeat(enemies, player):
    for x in enemies:
        if x.y >= player.y:
            return True
        elif player.lifes <= 0:
            return True

def updateGameWindow(player, enemies, bullet, score, enem_bullets):
    scoreTxt = "SCORE: " + str(score)
    livesTxt = "LIVES: " + str(player.lifes)
    text = font.render(scoreTxt, True, (0, 255, 0))
    text1 = font.render(livesTxt, True, (0, 255, 0))
    window.blit(backgroundImg, (0, 0))
    window.blit(text, (20, 10))
    window.blit(text1, (490, 10))
    player.draw(window)
    if not checkDefeat(enemies, player):
        if player.can_shoot is False:
            bullet.draw(window)
        for x in enemies:
            x.draw(window)
        for x in enem_bullets:
            x.draw(window)
    if checkDefeat(enemies, player):
        defeatTxt = 'GAME OVER'
        text2 = endFont.render(defeatTxt, True, (255, 0, 0))
        window.blit(text2, (125,300))
    pygame.display.update()


def main(difficulty):
    player = Player()
    player_lives = 2
    bullet = Bullet(-10, -10)
    enemy_bullet = enemyBullet(-20, -20)
    score = 0
    enemies = []
    enem_bullets = []
    halt = False

    while True:
        clock.tick(56)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        if len(enemies) == 0:
            createEnemies(enemies)
            player.lifes += 1

        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= player.vel

        if keys[pygame.K_RIGHT] and player.x < (win_size - player.width):
            player.x += player.vel

        if keys[pygame.K_SPACE] and player.can_shoot:
            player.can_shoot = False
            bullet = Bullet(player.x, player.y)
            bullet.draw(window)

        if checkDefeat(enemies, player):
            player.can_shoot = False
            enem_bullets.clear()

        if keys[pygame.K_ESCAPE] and checkDefeat(enemies, player):
            mainMenu()
            break

        if keys[pygame.K_ESCAPE]:
            halt = not halt

        else:
            if halt == False:
                enemyShooters(enemies)
                enemyShooting(enemies, enem_bullets, difficulty)
                hitPlayer(enem_bullets, player)
                moveEnemies(enemies)
                moveBullet(bullet, player)
                if not checkDefeat(enemies, player):
                    score = hitEnemies(enemies, bullet, score, player, difficulty)
                updateGameWindow(player, enemies, bullet, score, enem_bullets)


def mainMenu():
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    headText = endFont.render("SPACE INVADERS", True, GREEN)
    inMenu = True
    choice = 0
    difficulty = "EASY"

    while inMenu:
        clock.tick(7)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        if keys[pygame.K_DOWN] and choice == 0:
            choice = 1
        elif keys[pygame.K_UP] and choice == 0:
            choice = 2
        elif keys[pygame.K_UP] and choice == 1:
            choice = 0
        elif keys[pygame.K_DOWN] and choice == 1:
            choice = 2
        elif keys[pygame.K_UP] and choice == 2:
            choice = 1
        elif keys[pygame.K_DOWN] and choice == 2:
            choice = 0
        if keys[pygame.K_RIGHT] and difficulty == "EASY" and choice == 1:
            difficulty = "MEDIUM"
        elif keys[pygame.K_RIGHT] and difficulty == "MEDIUM" and choice == 1:
            difficulty = "HARD"
        elif keys[pygame.K_RIGHT] and difficulty == "HARD" and choice == 1:
            difficulty = "EASY"
        elif keys[pygame.K_LEFT] and difficulty == "EASY" and choice == 1:
            difficulty = "HARD"
        elif keys[pygame.K_LEFT] and difficulty == "HARD" and choice == 1:
            difficulty = "MEDIUM"
        elif keys[pygame.K_LEFT] and difficulty == "MEDIUM" and choice == 1:
            difficulty = "EASY"

        if choice == 0:
            playText = menuFont.render("PLAY GAME", True, RED)
            difficultyText = menuFont.render("DIFFICLUTY: " + difficulty, True, GREEN)
            quitText = menuFont.render("EXIT", True, GREEN)
        if choice == 1:
            playText = menuFont.render("PLAY GAME", True, GREEN)
            difficultyText = menuFont.render("DIFFICLUTY: " + difficulty, True, RED)
            quitText = menuFont.render("EXIT", True, GREEN)
        if choice == 2:
            playText = menuFont.render("PLAY GAME", True, GREEN)
            difficultyText = menuFont.render("DIFFICLUTY: " + difficulty, True, GREEN)
            quitText = menuFont.render("EXIT", True, RED)
        if keys[pygame.K_RETURN] and choice != 1:
            break

        window.blit(backgroundImg, (0, 0))
        window.blit(headText, (20, 100))
        window.blit(playText, (10, round(win_size / 2 - 50)))
        window.blit(difficultyText, (10, round(win_size / 2 + 50)))
        window.blit(quitText, (10, round(win_size / 2 + 150)))
        pygame.display.update()

    if choice == 0:
        main(difficulty)
    else:
        pygame.quit()
        sys.exit(0)

mainMenu()