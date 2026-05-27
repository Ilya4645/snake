"""
Базовый класс для игровых объектов.

Этот модуль содержит базовый класс GameObject,
который описывает геометрию квадрата на игровом поле.
"""

import pygame
from typing import Tuple


class GameObject:
    """
    Базовый класс для всех игровых объектов.

    Предоставляет базовую функциональность для работы
    с геометрией квадрата на игровом поле.

    Attributes:
        position (Tuple[int, int]): Позиция объекта на сетке (x, y)
        size (int): Размер квадрата в пикселях
        color (Tuple[int, int, int]): Цвет объекта в формате RGB
    """

    def __init__(self, position: Tuple[int, int], size: int = 20,
                 color: Tuple[int, int, int] = (255, 255, 255)):
        """
        Инициализация игрового объекта.

        Args:
            position: Кортеж с координатами (x, y) на сетке
            size: Размер квадрата в пикселях (по умолчанию 20)
            color: RGB цвет объекта (по умолчанию белый)
        """
        self.position = position
        self.size = size
        self.color = color

    def draw(self, screen: pygame.Surface) -> None:
        """
        Отрисовка объекта на экране.

        Args:
            screen: Поверхность Pygame для отрисовки
        """
        rect = pygame.Rect(
            self.position[0] * self.size,
            self.position[1] * self.size,
            self.size,
            self.size
        )
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, (50, 50, 50), rect, 1)  # Граница

    def get_rect(self) -> pygame.Rect:
        """
        Получение прямоугольника объекта.

        Returns:
            pygame.Rect: Прямоугольник объекта в пикселях
        """
        return pygame.Rect(
            self.position[0] * self.size,
            self.position[1] * self.size,
            self.size,
            self.size
        )

    def __eq__(self, other: 'GameObject') -> bool:
        """
        Сравнение двух игровых объектов по позиции.

        Args:
            other: Другой игровой объект для сравнения

        Returns:
            bool: True если объекты находятся в одной позиции
        """
        if not isinstance(other, GameObject):
            return False
        return self.position == other.position