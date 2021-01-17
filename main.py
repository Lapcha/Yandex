import pygame

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 1500, 900
FPS = 144
COORD_LIMIT_y = 240
ALL_SPRITES = pygame.sprite.Group()
clock = pygame.time.Clock()
ROCKETS_SPRITES = pygame.sprite.Group()


class Bullet:
    def __init__(self):
        self.pos_x, self.pos_y = 0, 0


class Rocket:
    def __init__(self):
        self.speed = 20
        self.skin = pygame.sprite.Sprite()
        self.skin.image = pygame.image.load("sprites/RocketFix2.png").convert_alpha()
        self.skin.rect = self.skin.image.get_rect()
        self.skin.rect.center = pygame.mouse.get_pos()
        self.skin.rect.y -= 30


class Boss:
    def __init__(self):
        self.hp = 1000
        self.skin = pygame.sprite.Sprite()
        self.skin.image = pygame.image.load("sprites/bossNBLast.png").convert_alpha()
        self.skin.rect = self.skin.image.get_rect()
        self.skin.rect.x = 580
        self.skin.rect.y = 10
        ALL_SPRITES.add(self.skin)


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

    def pause():
        print("Пауза нажата")

    running = True
    CD = 0  # Перезарядка выстрелов
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause()
        CD += 1
        if CD == 30:
            player.shot()
            CD = 0
        player.update_pos()  # Постоянное обновление позиции корабля
        ALL_SPRITES.draw(screen)  # Отрисовка спрайтов
        for rocket in ROCKETS_SPRITES:
            rocket.rect.y -= 10
            if 580 <= rocket.rect.x <= 920 and rocket.rect.y <= 230:
                print("BOOM")
                rocket.kill()
                boss.hp -= 10
                print(boss.hp)
        ROCKETS_SPRITES.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.display.quit()


if __name__ == '__main__':
    main()
