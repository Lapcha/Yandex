import pygame

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 1500, 900
FPS = 144
COORD_LIMIT_y = 240
ALL_SPRITES = pygame.sprite.Group()
clock = pygame.time.Clock()


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
        self.skin.rect.x, self.skin.rect.y = x, y
        # Корректировка координат, чтобы корабль находился в центре курсора
        self.skin.rect.x -= 35
        self.skin.rect.y -= 34



def main():
    pygame.init()
    pygame.mouse.set_visible(False)
    screen = pygame.display.set_mode(WINDOW_SIZE)

    background = pygame.sprite.Sprite()
    background.image = pygame.image.load("sprites/MainPage.png").convert_alpha()
    background.rect = background.image.get_rect()
    background.rect.x = 0
    background.rect.y = 0
    ALL_SPRITES.add(background)
    player = Player()

    def pause():
        print("Пауза нажата")

    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pause()
                if event.key == pygame.K_q:
                    player.shot()
        player.update_pos()  # Постоянное обновление позиции корабля
        ALL_SPRITES.draw(screen)  # Отрисовка спрайтов
        pygame.display.flip()
        clock.tick(FPS)
    pygame.display.quit()


if __name__ == '__main__':
    main()
