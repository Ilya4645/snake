"""
Модуль класса Яблока.

Содержит класс Apple, наследующий базовый класс GameObject.
Яблоко - это еда для змейки, при поедании которой змейка растет.
"""

import random
from typing import Tuple, List
from .base import GameObject


class Apple(GameObject):
    """
    Класс Яблока, наследник GameObject.

    Представляет яблоко на игровом поле. При поедании змейкой
    яблоко перемещается в новую случайную позицию.

    Attributes:
        grid_width (int): Ширина игрового поля в клетках
        grid_height (int): Высота игрового поля в клетках
    """

    def __init__(self, position: Tuple[int, int], grid_width: int = 40,
                 grid_height: int = 30, size: int = 20):
        """
        Инициализация яблока.

        Args:
            position: Начальная позиция яблока
            grid_width: Ширина поля в клетках
            grid_height: Высота поля в клетках
            size: Размер клетки в пикселях
        """
        super().__init__(position, size, (255, 0, 0))  # Красный цвет
        self.grid_width = grid_width
        self.grid_height = grid_height

    def respawn(self, snake_positions: List[Tuple[int, int]]) -> None:
        """
        Перемещение яблока в новую случайную позицию.

        Яблоко не может появиться на позиции, занятой змейкой.

        Args:
            snake_positions: Список позиций, занятых змейкой
        """
        while True:
            new_position = (
                random.randint(0, self.grid_width - 1),
                random.randint(0, self.grid_height - 1)
            )
            # Проверяем, что новая позиция не занята змейкой
            if new_position not in snake_positions:
                self.position = new_position
                break

    def is_eaten(self, snake_head_position: Tuple[int, int]) -> bool:
        """
        Проверка, съедено ли яблоко.

        Args:
            snake_head_position: Позиция головы змейки

        Returns:
            bool: True если яблоко съедено
        """
        return self.position == snake_head_position