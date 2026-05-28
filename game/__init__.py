"""
Пакет game содержит основные классы для игры "Змейка".

Включает базовый класс для игровых объектов,
классы Змейки и Яблока, а также контроллер игры.
"""

from .base import GameObject
from .snake import Snake
from .apple import Apple
from .game_controller import GameController

__all__ = ['GameObject', 'Snake', 'Apple', 'GameController']