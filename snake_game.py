import random
import pygame
from pygame.locals import K_DOWN, K_LEFT, K_RIGHT, K_UP, KEYDOWN, QUIT


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 15

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self):
        """База для инициализации."""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """База для рисовалки."""
        pass


class Apple(GameObject):
    """Яблоко."""

    def __init__(self):
        """Делаем яблочко."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Случайная позиция яблочка."""
        self.position = (
            random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self):
        """Рисуем яблочко."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Змейка (питон)."""

    def __init__(self):
        """Делаем змею."""
        super().__init__()
        self.reset()
        self.body_color = SNAKE_COLOR
        self.next_direction = None
        self.last = None
        self.length = 5

    def update_direction(self):
        """Обновляем направоление движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Где голова."""
        return self.positions[0]

    def move(self):
        """Движение - жизнь."""
        # Получаем текущую позицию головы
        head_x, head_y = self.get_head_position()

        # Вычисляем новую позицию головы
        dx, dy = self.direction
        new_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT

        # Проверяем столкновение с собой
        if (new_x, new_y) in self.positions[2:]:
            self.reset()
            return

        # Сохраняем последнюю позицию для затирания
        self.last = self.positions[-1]

        # Добавляем новую голову
        self.positions.insert(0, (new_x, new_y))

        # Удаляем хвост, если змейка не выросла
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Рисуем змею."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Параметры после смерти."""
        self.length = 5
        self.positions = [self.position]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])


def handle_keys(game_object):
    """Кнопочки жмем."""
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == KEYDOWN:
            if event.key == K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Делаем все-все."""
    # Инициализация PyGame:
    pygame.init()

    # Создание экземпляров классов
    snake = Snake()
    apple = Apple()

    while True:
        # Ограничение скорости игры
        clock.tick(SPEED)

        # Обработка событий
        handle_keys(snake)

        # Обновление направления змейки
        snake.update_direction()

        # Перемещение змейки
        snake.move()

        # Проверка, съела ли змейка яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            # Убедимся, что яблоко не появляется на змейке
            while apple.position in snake.positions:
                apple.randomize_position()

        # Очистка экрана
        screen.fill(BOARD_BACKGROUND_COLOR)

        # Отрисовка объектов
        apple.draw()
        snake.draw()

        # Обновление экрана
        pygame.display.update()


if __name__ == '__main__':
    main()
