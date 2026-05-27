"""
Модуль класса Змейки.

Содержит класс Snake, наследующий базовый класс GameObject.
Змейка может двигаться, расти и проверять столкновения.
"""

import pygame
from typing import Tuple, List
from enum import Enum
from .base import GameObject


class Direction(Enum):
    """
    Перечисление направлений движения змейки.
    """
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class Snake(GameObject):
    """
    Класс Змейки, наследник GameObject.

    Управляет состоянием змейки: движением, ростом,
    проверкой столкновений и отрисовкой.

    Attributes:
        body (List[Tuple[int, int]]): Список позиций сегментов змейки
        direction (Direction): Текущее направление движения
        grow_flag (bool): Флаг роста змейки
        grid_width (int): Ширина игрового поля
        grid_height (int): Высота игрового поля
    """

    def __init__(self, start_position: Tuple[int, int] = (20, 15),
                 grid_width: int = 40, grid_height: int = 30,
                 size: int = 20):
        """
        Инициализация змейки.

        Args:
            start_position: Начальная позиция головы змейки
            grid_width: Ширина поля в клетках
            grid_height: Высота поля в клетках
            size: Размер клетки в пикселях
        """
        super().__init__(start_position, size, (0, 255, 0))  # Зеленый цвет
        self.body = [start_position]  # Голова - первый элемент
        self.direction = Direction.RIGHT
        self.grow_flag = False
        self.grid_width = grid_width
        self.grid_height = grid_height

    def move(self) -> None:
        """
        Перемещение змейки в текущем направлении.

        Добавляет новую голову в направлении движения.
        Если флаг роста не установлен, удаляет хвост.
        """
        # Вычисляем новую позицию головы
        head = self.body[0]
        new_head = (
            head[0] + self.direction.value[0],
            head[1] + self.direction.value[1]
        )

        # Добавляем новую голову
        self.body.insert(0, new_head)
        self.position = new_head

        # Если не растем, удаляем хвост
        if not self.grow_flag:
            self.body.pop()
        else:
            self.grow_flag = False

    def grow(self) -> None:
        """
        Установка флага роста змейки.

        При следующем движении хвост не будет удален,
        что приведет к увеличению длины змейки.
        """
        self.grow_flag = True

    def change_direction(self, new_direction: Direction) -> None:
        """
        Изменение направления движения змейки.

        Не позволяет развернуться на 180 градусов.

        Args:
            new_direction: Новое направление движения
        """
        # Проверка, чтобы змейка не могла развернуться на месте
        opposite_directions = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }

        if new_direction != opposite_directions.get(self.direction):
            self.direction = new_direction

    def check_self_collision(self) -> bool:
        """
        Проверка столкновения змейки с самой собой.

        Returns:
            bool: True если змейка столкнулась с собой
        """
        head = self.body[0]
        return head in self.body[1:]

    def check_wall_collision(self) -> bool:
        """
        Проверка столкновения змейки со стенами.

        Returns:
            bool: True если змейка вышла за границы поля
        """
        head = self.body[0]
        return (head[0] < 0 or head[0] >= self.grid_width or
                head[1] < 0 or head[1] >= self.grid_height)

    def get_head_position(self) -> Tuple[int, int]:
        """
        Получение позиции головы змейки.

        Returns:
            Tuple[int, int]: Координаты головы змейки
        """
        return self.body[0]

    def draw(self, screen: pygame.Surface) -> None:
        """
        Отрисовка всех сегментов змейки.

        Args:
            screen: Поверхность Pygame для отрисовки
        """
        for i, segment in enumerate(self.body):
            color = (0, 200, 0) if i == 0 else self.color  # Голова темнее
            rect = pygame.Rect(
                segment[0] * self.size,
                segment[1] * self.size,
                self.size,
                self.size
            )
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (50, 50, 50), rect, 1)