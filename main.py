import sys

import pygame
from random import randint

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 1500, 900

FPS = 30
COORD_LIMIT_y = 240

clock = pygame.time.Clock()

MAIN_SPRITES = pygame.sprite.Group()
ROCKETS_SPRITES = pygame.sprite.Group()
METEORS_SPRITES = pygame.sprite.Group()
BLAST_SPRITES = pygame.sprite.Group()
BULLETS_SPRITES = pygame.sprite.Group()


class Bullet:
    def __init__(self):
        self.speed = 20
        self.skin = pygame.sprite.Sprite()
        self.skin.image = pygame.image.load("sprites/particles/dot.png").convert_alpha()
        self.skin.rect = self.skin.image.get_rect()
        self.skin.rect.x = randint(530, 970)
        self.skin.rect.y = 200


class Meteor:
    def __init__(self):
        self.skin = pygame.sprite.Sprite()
        self.skin.image = pygame.image.load("sprites/particles/Fireball.png").convert_alpha()
        self.skin.rect = self.skin.image.get_rect()
        self.rand = randint(50, 1450)
        self.skin.rect.x = self.rand
        self.skin.rect.y = -170


class Blast:
    def __init__(self):
        self.skin = pygame.sprite.Sprite()
        self.skin.image = pygame.image.load("sprites/particles/blast.png").convert_alpha()
        self.skin.rect = self.skin.image.get_rect()
        self.rand = randint(50, 1450)
        self.skin.rect.x = 740
        self.skin.rect.y = 220


class Boss:
    def __init__(self):
        self.hp = 30
        self.skin = pygame.sprite.Sprite()
        self.skin.image = pygame.image.load("sprites/bossNBLast.png").convert_alpha()
        self.skin.rect = self.skin.image.get_rect()
        self.skin.rect.x = 580
        self.skin.rect.y = 35
        MAIN_SPRITES.add(self.skin)

    def sky_fall(self):
        meteor = Meteor()
        METEORS_SPRITES.add(meteor.skin)

    def launcher(self):
        blast = Blast()
        BLAST_SPRITES.add(blast.skin)

    def shot(self):
        bullet = Bullet()
        BULLETS_SPRITES.add(bullet.skin)


class Rocket:
    def __init__(self):
        self.skin = pygame.sprite.Sprite()
        self.skin.image = pygame.image.load("sprites/RocketFix2.png").convert_alpha()
        self.skin.rect = self.skin.image.get_rect()
        self.skin.rect.center = pygame.mouse.get_pos()
        self.skin.rect.y -= 30


class Player:
    def __init__(self):
        self.hp = 10
        self.skin = pygame.sprite.Sprite()
        self.skin.image = pygame.image.load("sprites/ships/spaceship.png").convert_alpha()
        self.skin.rect = self.skin.image.get_rect()
        MAIN_SPRITES.add(self.skin)

    def update_pos(self):  # Обновление позиции коробля по координатам мыши
        x, y = pygame.mouse.get_pos()
        if y < COORD_LIMIT_y:
            y = COORD_LIMIT_y
        self.skin.rect.center = x, y
        # Корректировка координат, чтобы корабль находился в центре курсора

    def shot(self):
        rocket = Rocket()
        ROCKETS_SPRITES.add(rocket.skin)


def main():
    pygame.init()
    pygame.mouse.set_visible(False)
    screen = pygame.display.set_mode(WINDOW_SIZE)

    pygame.display.set_icon(pygame.image.load("sprites/Logo.bmp"))
    pygame.display.set_caption("SPACE BATTLE")

    sound = pygame.mixer.Sound("Music.mp3")
    sound.set_volume(0.1)
    sound.play(-1)


    background = pygame.sprite.Sprite()
    background.image = pygame.image.load("sprites/MainPage.png").convert_alpha()
    background.rect = background.image.get_rect()
    background.rect.x = 0
    background.rect.y = 0
    MAIN_SPRITES.add(background)
    player = Player()
    boss = Boss()
    death_boss = [pygame.image.load('sprites/death/death2.png'),
                  pygame.image.load('sprites/death/death3.png'),
                  pygame.image.load('sprites/death/death4.png'), pygame.image.load('sprites/death/death5.png'),
                  pygame.image.load('sprites/death/death6.png'),
                  pygame.image.load('sprites/death/death7.png'), pygame.image.load('sprites/death/death8.png'),
                  pygame.image.load('sprites/death/death9.png'),
                  pygame.image.load('sprites/death/death10.png')]

    death_player = [pygame.image.load('sprites/P_death/death1.png'),
                    pygame.image.load('sprites/P_death/death2.png'),
                    pygame.image.load('sprites/P_death/death3.png'),
                    pygame.image.load('sprites/P_death/death4.png')]


    def terminate():
        pygame.quit()
        sys.exit()

    def show_information():
        fon = pygame.transform.scale(pygame.image.load("sprites/Information.png"), (WINDOW_WIDTH, WINDOW_HEIGHT))
        screen.blit(fon, (0, 0))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        return  # Выходим из доп инфы
            pygame.display.flip()

    def start_screen():
        fon = pygame.transform.scale(pygame.image.load("sprites/MainMenu.png"), (WINDOW_WIDTH, WINDOW_HEIGHT))
        while True:
            screen.blit(fon, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:
                        return  # начинаем игру

                    elif event.key == pygame.K_y:
                        show_information()
            pygame.display.flip()

    def end_game():
        running = False
        pygame.mouse.set_visible(True)
        if boss.hp <= 0:
            file = "sprites/WinPage.png"
        else:
            file = "sprites/LosePage.png"
        fon = pygame.image.load(file)
        while True:
            screen.blit(fon, (530, 400))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
            pygame.display.flip()
            clock.tick(FPS)

    def death_boss_drow(frame):
        for i in range(40):
            screen.blit(death_boss[frame // 5], (570, 0))
            frame += 1
            pygame.display.flip()
            clock.tick(30)
        end_game()

    def death_player_drow(frame):
        for i in range(20):
            screen.blit(death_player[frame // 5], (player.skin.rect.x, player.skin.rect.y))
            frame += 1
            pygame.display.flip()
            clock.tick(30)
        end_game()

    start_screen()
    running = True
    CD = 0  # Перезарядка выстрелов
    CDS = -200  # Перезарядка метеоров
    CDL = -125  # Перезарядка ракет
    CDB = -50  # Перезарядка пуль
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        CD += 1
        CDS += 1
        CDL += 1
        CDB += 1

        if CD == 30:
            player.shot()
            CD = 0

        if CDS == 60:
            boss.sky_fall()
            CDS = 0

        if CDL == 135:
            boss.launcher()
            CDL = 0

        if CDB == 40:
            boss.shot()
            CDB = 0

        player.update_pos()  # Постоянное обновление позиции корабля

        for rocket in ROCKETS_SPRITES:
            rocket.rect.y -= 7
            if 580 <= rocket.rect.x <= 920 and rocket.rect.y <= 230:
                rocket.kill()
                boss.hp -= 10

        for meteor in METEORS_SPRITES:
            x, y = pygame.mouse.get_pos()
            x -= 4
            y -= 12
            damage = 0
            meteor.rect.y += 8
            for x_pos in range(x, x + 11):
                if damage:
                    meteor.kill()
                    break
                for y_pos in range(y, y + 11):
                    if meteor.rect.x + 1 <= x_pos <= meteor.rect.x + 74 and meteor.rect.y - 115 <= y_pos <= meteor.rect.y + 170:
                        player.hp -= 1
                        damage = 1
                        break
            if 1000 <= meteor.rect.y:
                meteor.kill()

        for launch in BLAST_SPRITES:
            x, y = pygame.mouse.get_pos()
            x -= 4
            y -= 12
            damage = 0
            launch.rect.y += 4
            for x_pos in range(x, x + 11):
                if damage:
                    launch.kill()
                    break
                for y_pos in range(y, y + 11):
                    if launch.rect.x <= x_pos <= launch.rect.x + 25 and launch.rect.y <= y_pos <= launch.rect.y + 140:
                        player.hp -= 1
                        damage = 1
                        break
            if 1000 <= launch.rect.y:
                launch.kill()

        for bullet in BULLETS_SPRITES:
            x, y = pygame.mouse.get_pos()
            x -= 4
            y -= 12
            damage = 0
            bullet.rect.y += 8
            for x_pos in range(x, x + 11):
                if damage:
                    bullet.kill()
                    break
                for y_pos in range(y, y + 11):
                    if bullet.rect.x <= x_pos <= bullet.rect.x + 35 and bullet.rect.y <= y_pos <= bullet.rect.y + 35:
                        player.hp -= 1
                        damage = 1
                        break
            if 1000 <= bullet.rect.y:
                bullet.kill()
        if player.hp <= 0:
            death_player_drow(0)
        if boss.hp <= 0:
            death_boss_drow(0)
        # Отрисовка спрайтов
        MAIN_SPRITES.draw(screen)
        ROCKETS_SPRITES.draw(screen)
        METEORS_SPRITES.draw(screen)
        BLAST_SPRITES.draw(screen)
        BULLETS_SPRITES.draw(screen)
        font = pygame.font.Font(None, 50)
        player_hp_label = font.render(f"Здоровье игрока: {player.hp}", True, (247, 37, 188))
        boss_hp_label = font.render(f"Здоровье босса: {boss.hp}", True, (247, 37, 188))
        screen.blit(player_hp_label, (0, 0))
        screen.blit(boss_hp_label, (0, 60))
        pygame.display.flip()
        clock.tick(FPS)
        print(player.hp)
    pygame.display.quit()


if __name__ == '__main__':
    main()
