import pygame
import random
from pygame.locals import *

# Константы
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)


class GameObject:
    """
    Базовый класс для всех игровых объектов.
    
    Атрибуты:
        position (tuple): Позиция объекта на игровом поле (x, y)
        body_color (tuple): Цвет объекта в формате RGB
    """
    
    def __init__(self, position=None, body_color=None):
        """
        Инициализирует игровой объект.
        
        Args:
            position (tuple, optional): Начальная позиция объекта. По умолчанию центр экрана.
            body_color (tuple, optional): Цвет объекта. По умолчанию None.
        """
        if position is None:
            position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.position = position
        self.body_color = body_color
    
    def draw(self, surface):
        """
        Абстрактный метод для отрисовки объекта.
        
        Args:
            surface: Поверхность Pygame для отрисовки
        """
        pass


class Apple(GameObject):
    """
    Класс для представления яблока в игре.
    
    Наследуется от GameObject.
    """
    
    def __init__(self):
        """Инициализирует яблоко со случайной позицией и красным цветом."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()
    
    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)
    
    def draw(self, surface):
        """
        Отрисовывает яблоко на игровой поверхности.
        
        Args:
            surface: Поверхность Pygame для отрисовки
        """
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, (255, 255, 255), rect, 1)


class Snake(GameObject):
    """
    Класс для представления змейки в игре.
    
    Наследуется от GameObject.
    
    Атрибуты:
        length (int): Текущая длина змейки
        positions (list): Список позиций всех сегментов змейки
        direction (tuple): Текущее направление движения
        next_direction (tuple): Следующее направление движения
        last (tuple): Позиция последнего удаленного сегмента
    """
    
    def __init__(self):
        """Инициализирует змейку с начальными параметрами."""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.reset()
    
    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        center_x = (SCREEN_WIDTH // 2) // GRID_SIZE * GRID_SIZE
        center_y = (SCREEN_HEIGHT // 2) // GRID_SIZE * GRID_SIZE
        self.positions = [(center_x, center_y)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
    
    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            # Запрещаем движение в противоположном направлении
            opposite_directions = {
                UP: DOWN, DOWN: UP, 
                LEFT: RIGHT, RIGHT: LEFT
            }
            if self.next_direction != opposite_directions.get(self.direction):
                self.direction = self.next_direction
            self.next_direction = None
    
    def get_head_position(self):
        """
        Возвращает позицию головы змейки.
        
        Returns:
            tuple: Позиция головы змейки (x, y)
        """
        return self.positions[0]
    
    def move(self):
        """Обновляет позицию змейки, добавляя новую голову и удаляя хвост."""
        head = self.get_head_position()
        x, y = self.direction
        new_x = (head[0] + (x * GRID_SIZE)) % SCREEN_WIDTH
        new_y = (head[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT
        new_head = (new_x, new_y)
        
        # Проверка на столкновение с собой
        if new_head in self.positions[1:]:
            self.reset()
            return
        
        # Добавляем новую голову
        self.positions.insert(0, new_head)
        
        # Сохраняем последний сегмент для стирания
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None
    
    def draw(self, surface):
        """
        Отрисовывает змейку на экране.
        
        Args:
            surface: Поверхность Pygame для отрисовки
        """
        # Стираем последний сегмент
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)
        
        # Отрисовываем все сегменты змейки
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, (255, 255, 255), rect, 1)


def handle_keys(snake):
    """
    Обрабатывает нажатия клавиш для изменения направления змейки.
    
    Args:
        snake (Snake): Объект змейки, направление которой нужно изменить
    """
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                snake.next_direction = UP
            elif event.key == K_DOWN:
                snake.next_direction = DOWN
            elif event.key == K_LEFT:
                snake.next_direction = LEFT
            elif event.key == K_RIGHT:
                snake.next_direction = RIGHT


def main():
    """Основная функция игры, содержащая главный игровой цикл."""
    pygame.init()
    
    # Создание экрана
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Изгиб Питона')
    
    # Создание игровых объектов
    snake = Snake()
    apple = Apple()
    
    # Создание часов для контроля FPS
    clock = pygame.time.Clock()
    
    # Главный игровой цикл
    while True:
        # Обработка событий
        handle_keys(snake)
        
        # Обновление направления змейки
        snake.update_direction()
        
        # Движение змейки
        snake.move()
        
        # Проверка, съела ли змейка яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            # Убедимся, что яблоко не появится на змейке
            while apple.position in snake.positions:
                apple.randomize_position()
        
        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        
        # Обновление экрана
        pygame.display.update()
        
        # Контроль FPS
        clock.tick(10)  # 10 кадров в секунду для комфортной игры


if __name__ == "__main__":
    main()