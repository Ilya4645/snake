"""
Модульные тесты для базового класса GameObject.

Тестирует базовый класс GameObject, который является основой
для всех игровых объектов в игре "Змейка".

Тесты проверяют:
- Инициализацию объекта с параметрами по умолчанию и пользовательскими
- Метод get_rect() для получения прямоугольника объекта
- Сравнение объектов через __eq__
- Отрисовку объекта на экране
"""

import unittest
import pygame
from game.base import GameObject


class TestGameObjectInitialization(unittest.TestCase):
    """Тесты инициализации GameObject."""

    @classmethod
    def setUpClass(cls):
        """Инициализация Pygame перед всеми тестами класса."""
        pygame.init()
        cls.screen = pygame.display.set_mode((800, 600))

    @classmethod
    def tearDownClass(cls):
        """Завершение работы Pygame после всех тестов класса."""
        pygame.quit()

    def test_init_with_default_values(self):
        """Тест создания объекта с параметрами по умолчанию."""
        obj = GameObject((5, 10))

        self.assertEqual(obj.position, (5, 10))
        self.assertEqual(obj.size, 20)
        self.assertEqual(obj.color, (255, 255, 255))

    def test_init_with_custom_position(self):
        """Тест создания объекта с пользовательской позицией."""
        obj = GameObject((100, 200))

        self.assertEqual(obj.position, (100, 200))
        self.assertEqual(obj.size, 20)
        self.assertEqual(obj.color, (255, 255, 255))

    def test_init_with_custom_size(self):
        """Тест создания объекта с пользовательским размером."""
        obj = GameObject((0, 0), size=40)

        self.assertEqual(obj.position, (0, 0))
        self.assertEqual(obj.size, 40)
        self.assertEqual(obj.color, (255, 255, 255))

    def test_init_with_custom_color(self):
        """Тест создания объекта с пользовательским цветом."""
        obj = GameObject((0, 0), color=(255, 0, 0))

        self.assertEqual(obj.position, (0, 0))
        self.assertEqual(obj.size, 20)
        self.assertEqual(obj.color, (255, 0, 0))

    def test_init_with_all_custom_values(self):
        """Тест создания объекта со всеми пользовательскими параметрами."""
        obj = GameObject((10, 20), 30, (0, 255, 0))

        self.assertEqual(obj.position, (10, 20))
        self.assertEqual(obj.size, 30)
        self.assertEqual(obj.color, (0, 255, 0))


class TestGameObjectGetRect(unittest.TestCase):
    """Тесты метода get_rect()."""

    @classmethod
    def setUpClass(cls):
        """Инициализация Pygame перед всеми тестами класса."""
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        """Завершение работы Pygame после всех тестов класса."""
        pygame.quit()

    def test_get_rect_default_size(self):
        """Тест get_rect() с размером по умолчанию."""
        obj = GameObject((5, 10), 20)
        rect = obj.get_rect()

        self.assertEqual(rect.x, 100)  # 5 * 20
        self.assertEqual(rect.y, 200)  # 10 * 20
        self.assertEqual(rect.width, 20)
        self.assertEqual(rect.height, 20)

    def test_get_rect_custom_size(self):
        """Тест get_rect() с пользовательским размером."""
        obj = GameObject((3, 7), 40)
        rect = obj.get_rect()

        self.assertEqual(rect.x, 120)  # 3 * 40
        self.assertEqual(rect.y, 280)  # 7 * 40
        self.assertEqual(rect.width, 40)
        self.assertEqual(rect.height, 40)

    def test_get_rect_zero_position(self):
        """Тест get_rect() с нулевой позицией."""
        obj = GameObject((0, 0), 25)
        rect = obj.get_rect()

        self.assertEqual(rect.x, 0)
        self.assertEqual(rect.y, 0)
        self.assertEqual(rect.width, 25)
        self.assertEqual(rect.height, 25)

    def test_get_rect_type(self):
        """Тест, что get_rect() возвращает pygame.Rect."""
        obj = GameObject((0, 0))
        rect = obj.get_rect()

        self.assertIsInstance(rect, pygame.Rect)


class TestGameObjectEquality(unittest.TestCase):
    """Тесты сравнения объектов GameObject."""

    @classmethod
    def setUpClass(cls):
        """Инициализация Pygame перед всеми тестами класса."""
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        """Завершение работы Pygame после всех тестов класса."""
        pygame.quit()

    def test_equal_same_position(self):
        """Тест равенства объектов с одинаковой позицией."""
        obj1 = GameObject((5, 10))
        obj2 = GameObject((5, 10))

        self.assertEqual(obj1, obj2)

    def test_equal_same_position_different_size(self):
        """Тест равенства объектов с одинаковой позицией, но разным размером."""
        obj1 = GameObject((5, 10), size=20)
        obj2 = GameObject((5, 10), size=30)

        self.assertEqual(obj1, obj2)

    def test_equal_same_position_different_color(self):
        """Тест равенства объектов с одинаковой позицией, но разным цветом."""
        obj1 = GameObject((5, 10), color=(255, 0, 0))
        obj2 = GameObject((5, 10), color=(0, 255, 0))

        self.assertEqual(obj1, obj2)

    def test_not_equal_different_position(self):
        """Тест неравенства объектов с разными позициями."""
        obj1 = GameObject((5, 10))
        obj2 = GameObject((10, 5))

        self.assertNotEqual(obj1, obj2)

    def test_not_equal_different_type(self):
        """Тест неравенства с объектами другого типа."""
        obj = GameObject((5, 10))

        self.assertNotEqual(obj, "string")
        self.assertNotEqual(obj, 123)
        self.assertNotEqual(obj, None)
        self.assertNotEqual(obj, (5, 10))
        self.assertNotEqual(obj, [5, 10])

    def test_equal_same_object(self):
        """Тест равенства объекта самому себе."""
        obj = GameObject((5, 10))

        self.assertEqual(obj, obj)


class TestGameObjectDraw(unittest.TestCase):
    """Тесты отрисовки GameObject."""

    @classmethod
    def setUpClass(cls):
        """Инициализация Pygame и создание экрана перед всеми тестами."""
        pygame.init()
        cls.screen = pygame.display.set_mode((800, 600))

    @classmethod
    def tearDownClass(cls):
        """Завершение работы Pygame после всех тестов."""
        pygame.quit()

    def test_draw_no_errors(self):
        """Тест, что отрисовка не вызывает ошибок."""
        obj = GameObject((5, 10))

        try:
            obj.draw(self.screen)
        except Exception as e:
            self.fail(f"Метод draw() вызвал исключение: {e}")

    def test_draw_at_origin(self):
        """Тест отрисовки в начале координат."""
        obj = GameObject((0, 0))

        try:
            obj.draw(self.screen)
        except Exception as e:
            self.fail(f"Отрисовка в (0,0) вызвала исключение: {e}")

    def test_draw_at_boundary(self):
        """Тест отрисовки на границе экрана."""
        obj = GameObject((39, 29))  # Граница при размере 20

        try:
            obj.draw(self.screen)
        except Exception as e:
            self.fail(f"Отрисовка на границе вызвала исключение: {e}")

    def test_draw_multiple_objects(self):
        """Тест отрисовки нескольких объектов."""
        objects = [
            GameObject((0, 0)),
            GameObject((10, 10)),
            GameObject((20, 20)),
        ]

        try:
            for obj in objects:
                obj.draw(self.screen)
        except Exception as e:
            self.fail(f"Отрисовка нескольких объектов вызвала исключение: {e}")


class TestGameObjectProperties(unittest.TestCase):
    """Тесты свойств GameObject."""

    @classmethod
    def setUpClass(cls):
        """Инициализация Pygame перед всеми тестами класса."""
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        """Завершение работы Pygame после всех тестов класса."""
        pygame.quit()

    def test_position_type(self):
        """Тест, что позиция является кортежем целых чисел."""
        obj = GameObject((5, 10))

        self.assertIsInstance(obj.position, tuple)
        self.assertEqual(len(obj.position), 2)
        self.assertIsInstance(obj.position[0], int)
        self.assertIsInstance(obj.position[1], int)

    def test_size_type(self):
        """Тест, что размер является целым числом."""
        obj = GameObject((0, 0))

        self.assertIsInstance(obj.size, int)

    def test_color_type_and_range(self):
        """Тест, что цвет является кортежем из трех целых чисел 0-255."""
        obj = GameObject((0, 0))

        self.assertIsInstance(obj.color, tuple)
        self.assertEqual(len(obj.color), 3)

        for component in obj.color:
            self.assertIsInstance(component, int)
            self.assertGreaterEqual(component, 0)
            self.assertLessEqual(component, 255)

    def test_position_is_tuple_of_ints(self):
        """Тест, что координаты позиции - целые числа."""
        obj = GameObject((10, 20))
        x, y = obj.position

        self.assertIsInstance(x, int)
        self.assertIsInstance(y, int)


if __name__ == '__main__':
    unittest.main()