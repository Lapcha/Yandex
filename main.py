import pygame
from random import randint

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 1500, 900

FPS = 144
COORD_LIMIT_y = 240

clock = pygame.time.Clock()

ALL_SPRITES = pygame.sprite.Group()
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
        self.x = randint(530, 970)
        self.y = 200
        self.skin.rect.center = self.x, self.y


class Meteor:
    def __init__(self):
        self.skin = pygame.sprite.Sprite()
        self.skin.image = pygame.image.load("sprites/particles/Fireball.png").convert_alpha()
        self.skin.rect = self.skin.image.get_rect()
        self.rand = randint(50, 1450)
        self.skin.rect.center = self.rand, -170


class Blast:
    def __init__(self):
        self.skin = pygame.sprite.Sprite()
        self.skin.image = pygame.image.load("sprites/particles/blast.png").convert_alpha()
        self.skin.rect = self.skin.image.get_rect()
        self.rand = randint(50, 1450)
        self.skin.rect.center = 750, 220


class Boss:
    def __init__(self):
        self.hp = 10
        self.skin = pygame.sprite.Sprite()
        self.skin.image = pygame.image.load("sprites/bossNBLast.png").convert_alpha()
        self.skin.rect = self.skin.image.get_rect()
        self.skin.rect.x = 580
        self.skin.rect.y = 35
        self.alive = 1
        ALL_SPRITES.add(self.skin)

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
        ALL_SPRITES.add(self.skin)

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
    pygame.mouse.set_visible(True)
    screen = pygame.display.set_mode(WINDOW_SIZE)

    background = pygame.sprite.Sprite()
    background.image = pygame.image.load("sprites/MainPage.png").convert_alpha()
    background.rect = background.image.get_rect()
    background.rect.x = 0
    background.rect.y = 0
    ALL_SPRITES.add(background)
    player = Player()
    boss = Boss()
    frame = 0
    death_boss = [pygame.image.load('sprites/death/death2.png'),
                  pygame.image.load('sprites/death/death3.png'),
                  pygame.image.load('sprites/death/death4.png'), pygame.image.load('sprites/death/death5.png'),
                  pygame.image.load('sprites/death/death6.png'),
                  pygame.image.load('sprites/death/death7.png'), pygame.image.load('sprites/death/death8.png'),
                  pygame.image.load('sprites/death/death9.png'),
                  pygame.image.load('sprites/death/death10.png')]

    def pause():
        print("Пауза нажата")

    def death_boss_drow(frame):
        for i in range(45):
            if frame + 1 >= 45:
                frame = 0
            screen.blit(death_boss[frame // 5], (570, 0))
            frame += 1
            pygame.display.flip()
            clock.tick(30)


    running = True

    CD = 0  # Перезарядка выстрелов
    CDS = 0  # Перезарядка метеоров
    CDL = 0  # Перезарядка ракет
    CDB = 0  # Перезарядка пуль
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:

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
                print("BOOM")
                rocket.kill()
                boss.hp -= 10
                print(boss.hp)

        for meteor in METEORS_SPRITES:
            meteor.rect.y += 8
            if 1000 <= meteor.rect.y:
                meteor.kill()

        for launch in BLAST_SPRITES:
            launch.rect.y += 4
            if 1000 <= launch.rect.y:
                launch.kill()

        for bullet in BULLETS_SPRITES:
            bullet.rect.y += 8
            if 1000 <= bullet.rect.y:
                bullet.kill()

        ALL_SPRITES.draw(screen)
        ROCKETS_SPRITES.draw(screen)
        METEORS_SPRITES.draw(screen)
        BLAST_SPRITES.draw(screen)
        BULLETS_SPRITES.draw(screen)
        if boss.hp <= 0 and boss.alive == 1:
            boss.skin.kill()
            death_boss_drow(frame)
            boss.alive = 0
        pygame.display.flip()
        clock.tick(FPS)
    pygame.display.quit()


if __name__ == '__main__':
    main()
