"""
Модульные тесты для класса Apple.

Тестирует класс Apple (Яблоко), который является наследником GameObject.
Яблоко появляется в случайных местах и служит едой для змейки.

Тесты проверяют:
- Инициализацию яблока
- Проверку поедания яблока змейкой
- Перемещение яблока в новую позицию
- Отрисовку яблока
"""

import unittest
import pygame
from game.apple import Apple
from game.base import GameObject


class TestAppleInitialization(unittest.TestCase):
    """Тесты инициализации яблока."""

    @classmethod
    def setUpClass(cls):
        """Инициализация Pygame перед всеми тестами класса."""
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        """Завершение работы Pygame после всех тестов класса."""
        pygame.quit()

    def test_init_default_grid(self):
        """Тест создания яблока с параметрами по умолчанию."""
        apple = Apple(position=(10, 10))

        self.assertEqual(apple.position, (10, 10))
        self.assertEqual(apple.grid_width, 40)
        self.assertEqual(apple.grid_height, 30)
        self.assertEqual(apple.size, 20)

    def test_init_custom_grid(self):
        """Тест создания яблока с пользовательским размером сетки."""
        apple = Apple(
            position=(5, 5),
            grid_width=50,
            grid_height=40
        )

        self.assertEqual(apple.position, (5, 5))
        self.assertEqual(apple.grid_width, 50)
        self.assertEqual(apple.grid_height, 40)

    def test_init_custom_size(self):
        """Тест создания яблока с пользовательским размером."""
        apple = Apple(position=(10, 10), size=30)

        self.assertEqual(apple.size, 30)

    def test_init_color_is_red(self):
        """Тест, что яблоко всегда красного цвета."""
        apple = Apple(position=(0, 0))

        self.assertEqual(apple.color, (255, 0, 0))

    def test_inherits_from_game_object(self):
        """Тест, что Apple наследуется от GameObject."""
        apple = Apple(position=(0, 0))

        self.assertIsInstance(apple, GameObject)
        self.assertTrue(issubclass(Apple, GameObject))


class TestAppleIsEaten(unittest.TestCase):
    """Тесты проверки поедания яблока."""

    @classmethod
    def setUpClass(cls):
        """Инициализация Pygame перед всеми тестами класса."""
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        """Завершение работы Pygame после всех тестов класса."""
        pygame.quit()

    def setUp(self):
        """Создание яблока перед каждым тестом."""
        self.apple = Apple(position=(10, 10))

    def test_is_eaten_true(self):
        """Тест, что яблоко съедено, если голова в той же позиции."""
        self.assertTrue(self.apple.is_eaten((10, 10)))

    def test_is_eaten_false_different_both(self):
        """Тест, что яблоко не съедено при разных координатах."""
        self.assertFalse(self.apple.is_eaten((11, 11)))

    def test_is_eaten_false_different_x(self):
        """Тест, что яблоко не съедено при разной X координате."""
        self.assertFalse(self.apple.is_eaten((11, 10)))

    def test_is_eaten_false_different_y(self):
        """Тест, что яблоко не съедено при разной Y координате."""
        self.assertFalse(self.apple.is_eaten((10, 11)))

    def test_is_eaten_false_far_away(self):
        """Тест, что яблоко не съедено при далекой позиции."""
        self.assertFalse(self.apple.is_eaten((30, 20)))

    def test_is_eaten_returns_boolean(self):
        """Тест, что метод возвращает булево значение."""
        result = self.apple.is_eaten((10, 10))
        self.assertIsInstance(result, bool)


class TestAppleRespawn(unittest.TestCase):
    """Тесты перемещения яблока."""

    @classmethod
    def setUpClass(cls):
        """Инициализация Pygame перед всеми тестами класса."""
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        """Завершение работы Pygame после всех тестов класса."""
        pygame.quit()

    def setUp(self):
        """Создание яблока перед каждым тестом."""
        self.apple = Apple(
            position=(5, 5),
            grid_width=20,
            grid_height=20
        )

    def test_respawn_changes_position(self):
        """Тест, что после respawn позиция меняется."""
        original_position = self.apple.position

        self.apple.respawn([(10, 10)])

        self.assertNotEqual(self.apple.position, original_position)

    def test_respawn_not_on_snake(self):
        """Тест, что яблоко не появляется на позиции змейки."""
        snake_positions = [(10, 10), (10, 11), (10, 12)]

        for _ in range(20):
            self.apple.respawn(snake_positions)
            self.assertNotIn(
                self.apple.position, snake_positions,
                f"Яблоко появилось на позиции змейки: {self.apple.position}"
            )

    def test_respawn_within_bounds(self):
        """Тест, что яблоко появляется в пределах сетки."""
        for _ in range(100):
            self.apple.respawn([])

            x, y = self.apple.position

            self.assertGreaterEqual(x, 0, f"X={x} меньше 0")
            self.assertLess(x, self.apple.grid_width, f"X={x} >= {self.apple.grid_width}")
            self.assertGreaterEqual(y, 0, f"Y={y} меньше 0")
            self.assertLess(y, self.apple.grid_height, f"Y={y} >= {self.apple.grid_height}")

    def test_respawn_different_positions(self):
        """Тест, что яблоко появляется в разных местах."""
        positions = set()

        for _ in range(50):
            self.apple.respawn([])
            positions.add(self.apple.position)

        # Маловероятно, что все 50 вызовов дадут одну позицию
        self.assertGreater(len(positions), 1)

    def test_respawn_with_full_snake(self):
        """Тест respawn когда змейка занимает почти все поле."""
        # Создаем змейку, которая занимает почти все поле
        snake_positions = []
        for x in range(18):  # Оставляем 2 колонки
            for y in range(18):  # Оставляем 2 строки
                snake_positions.append((x, y))

        # Яблоко должно найти свободное место
        self.apple.respawn(snake_positions)

        self.assertNotIn(self.apple.position, snake_positions)

    def test_respawn_preserves_other_properties(self):
        """Тест, что при respawn сохраняются другие свойства."""
        original_size = self.apple.size
        original_color = self.apple.color
        original_grid_width = self.apple.grid_width
        original_grid_height = self.apple.grid_height

        self.apple.respawn([])

        self.assertEqual(self.apple.size, original_size)
        self.assertEqual(self.apple.color, original_color)
        self.assertEqual(self.apple.grid_width, original_grid_width)
        self.assertEqual(self.apple.grid_height, original_grid_height)


class TestAppleDrawing(unittest.TestCase):
    """Тесты отрисовки яблока."""

    @classmethod
    def setUpClass(cls):
        """Инициализация Pygame и создание экрана."""
        pygame.init()
        cls.screen = pygame.display.set_mode((800, 600))

    @classmethod
    def tearDownClass(cls):
        """Завершение работы Pygame."""
        pygame.quit()

    def test_draw_no_errors(self):
        """Тест, что отрисовка не вызывает ошибок."""
        apple = Apple(position=(10, 10))

        try:
            apple.draw(self.screen)
        except Exception as e:
            self.fail(f"Отрисовка яблока вызвала исключение: {e}")

    def test_draw_at_corners(self):
        """Тест отрисовки яблока в углах экрана."""
        corners = [
            (0, 0),  # Верхний левый
            (39, 0),  # Верхний правый
            (0, 29),  # Нижний левый
            (39, 29),  # Нижний правый
        ]

        for pos in corners:
            apple = Apple(position=pos)
            try:
                apple.draw(self.screen)
            except Exception as e:
                self.fail(f"Отрисовка в позиции {pos} вызвала исключение: {e}")

    def test_draw_multiple_apples(self):
        """Тест отрисовки нескольких яблок."""
        apples = [
            Apple(position=(5, 5)),
            Apple(position=(15, 15)),
            Apple(position=(25, 25)),
        ]

        try:
            for apple in apples:
                apple.draw(self.screen)
        except Exception as e:
            self.fail(f"Отрисовка нескольких яблок вызвала исключение: {e}")

    def test_draw_after_respawn(self):
        """Тест отрисовки яблока после перемещения."""
        apple = Apple(position=(10, 10))
        apple.respawn([])

        try:
            apple.draw(self.screen)
        except Exception as e:
            self.fail(f"Отрисовка после respawn вызвала исключение: {e}")


if __name__ == '__main__':
    unittest.main()