"""
Модульные тесты для класса Snake.

Тестирует класс Snake, который управляет поведением змейки:
движением, ростом, изменением направления и столкновениями.

Также тестирует перечисление Direction для направлений движения.
"""

import unittest
import pygame
from game.snake import Snake, Direction


class TestSnakeInitialization(unittest.TestCase):
    """Тесты инициализации змейки."""

    @classmethod
    def setUpClass(cls):
        """Инициализация Pygame перед всеми тестами класса."""
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        """Завершение работы Pygame после всех тестов класса."""
        pygame.quit()

    def test_init_default_values(self):
        """Тест создания змейки с параметрами по умолчанию."""
        snake = Snake()

        self.assertEqual(snake.get_head_position(), (20, 15))
        self.assertEqual(len(snake.body), 1)
        self.assertEqual(snake.direction, Direction.RIGHT)
        self.assertFalse(snake.grow_flag)
        self.assertEqual(snake.grid_width, 40)
        self.assertEqual(snake.grid_height, 30)
        self.assertEqual(snake.size, 20)

    def test_init_custom_position(self):
        """Тест создания змейки с пользовательской позицией."""
        snake = Snake(start_position=(10, 10))

        self.assertEqual(snake.get_head_position(), (10, 10))
        self.assertEqual(len(snake.body), 1)

    def test_init_custom_grid_size(self):
        """Тест создания змейки с пользовательским размером сетки."""
        snake = Snake(grid_width=50, grid_height=40)

        self.assertEqual(snake.grid_width, 50)
        self.assertEqual(snake.grid_height, 40)

    def test_init_custom_cell_size(self):
        """Тест создания змейки с пользовательским размером клетки."""
        snake = Snake(size=30)

        self.assertEqual(snake.size, 30)

    def test_init_body_structure(self):
        """Тест структуры тела змейки при инициализации."""
        snake = Snake()

        self.assertIsInstance(snake.body, list)
        self.assertEqual(len(snake.body), 1)
        self.assertEqual(snake.body[0], (20, 15))
        self.assertIsInstance(snake.body[0], tuple)
        self.assertEqual(len(snake.body[0]), 2)

    def test_init_color(self):
        """Тест цвета змейки."""
        snake = Snake()

        self.assertEqual(snake.color, (0, 255, 0))  # Зеленый


class TestSnakeMovement(unittest.TestCase):
    """Тесты движения змейки."""

    @classmethod
    def setUpClass(cls):
        """Инициализация Pygame перед всеми тестами класса."""
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        """Завершение работы Pygame после всех тестов класса."""
        pygame.quit()

    def setUp(self):
        """Создание новой змейки перед каждым тестом."""
        self.snake = Snake(start_position=(20, 15))

    def test_move_right(self):
        """Тест движения вправо."""
        self.snake.direction = Direction.RIGHT
        self.snake.move()

        self.assertEqual(self.snake.get_head_position(), (21, 15))
        self.assertEqual(len(self.snake.body), 1)

    def test_move_left(self):
        """Тест движения влево."""
        self.snake.direction = Direction.LEFT
        self.snake.move()

        self.assertEqual(self.snake.get_head_position(), (19, 15))
        self.assertEqual(len(self.snake.body), 1)

    def test_move_up(self):
        """Тест движения вверх."""
        self.snake.direction = Direction.UP
        self.snake.move()

        self.assertEqual(self.snake.get_head_position(), (20, 14))
        self.assertEqual(len(self.snake.body), 1)

    def test_move_down(self):
        """Тест движения вниз."""
        self.snake.direction = Direction.DOWN
        self.snake.move()

        self.assertEqual(self.snake.get_head_position(), (20, 16))
        self.assertEqual(len(self.snake.body), 1)

    def test_move_multiple_times_same_direction(self):
        """Тест многократного движения в одном направлении."""
        for _ in range(10):
            self.snake.move()

        self.assertEqual(self.snake.get_head_position(), (30, 15))
        self.assertEqual(len(self.snake.body), 1)

    def test_move_updates_head_position(self):
        """Тест, что позиция головы обновляется после движения."""
        old_head = self.snake.get_head_position()
        self.snake.move()
        new_head = self.snake.get_head_position()

        self.assertNotEqual(old_head, new_head)
        self.assertEqual(new_head, self.snake.body[0])
        self.assertEqual(self.snake.position, new_head)

    def test_body_follows_head(self):
        """Тест, что тело следует за головой."""
        # Растим змейку до длины 3
        self.snake.grow()
        self.snake.move()
        self.snake.grow()
        self.snake.move()

        # Двигаемся еще раз
        self.snake.move()

        # Проверяем, что длина не изменилась (не было grow перед move)
        self.assertEqual(len(self.snake.body), 3)
        # Голова на новой позиции
        self.assertEqual(self.snake.body[0], (23, 15))
        # Второй сегмент на месте старой головы
        self.assertEqual(self.snake.body[1], (22, 15))
        # Третий сегмент на месте старого второго
        self.assertEqual(self.snake.body[2], (21, 15))


class TestSnakeGrowth(unittest.TestCase):
    """Тесты роста змейки."""

    @classmethod
    def setUpClass(cls):
        """Инициализация Pygame перед всеми тестами класса."""
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        """Завершение работы Pygame после всех тестов класса."""
        pygame.quit()

    def setUp(self):
        """Создание новой змейки перед каждым тестом."""
        self.snake = Snake(start_position=(20, 15))

    def test_grow_increases_length(self):
        """Тест, что рост увеличивает длину змейки."""
        initial_length = len(self.snake.body)

        self.snake.grow()
        self.snake.move()

        self.assertEqual(len(self.snake.body), initial_length + 1)

    def test_grow_flag_set(self):
        """Тест, что флаг роста устанавливается."""
        self.assertFalse(self.snake.grow_flag)

        self.snake.grow()

        self.assertTrue(self.snake.grow_flag)

    def test_grow_flag_reset_after_move(self):
        """Тест, что флаг роста сбрасывается после движения."""
        self.snake.grow()
        self.assertTrue(self.snake.grow_flag)

        self.snake.move()
        self.assertFalse(self.snake.grow_flag)

    def test_multiple_growth(self):
        """Тест множественного роста змейки."""
        for i in range(5):
            self.snake.grow()
            self.snake.move()

        self.assertEqual(len(self.snake.body), 6)  # 1 начальный + 5 рост

    def test_grow_without_move(self):
        """Тест, что без движения рост не увеличивает длину."""
        initial_length = len(self.snake.body)

        self.snake.grow()
        # Не вызываем move()

        self.assertEqual(len(self.snake.body), initial_length)
        self.assertTrue(self.snake.grow_flag)

    def test_grow_preserves_body(self):
        """Тест, что при росте сохраняются все сегменты тела."""
        self.snake.grow()
        self.snake.move()

        # Сохраняем тело после первого роста
        body_after_growth = self.snake.body.copy()

        self.snake.grow()
        self.snake.move()

        # Проверяем, что все старые сегменты на месте
        for segment in body_after_growth:
            self.assertIn(segment, self.snake.body)


class TestSnakeDirection(unittest.TestCase):
    """Тесты изменения направления змейки."""

    @classmethod
    def setUpClass(cls):
        """Инициализация Pygame перед всеми тестами класса."""
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        """Завершение работы Pygame после всех тестов класса."""
        pygame.quit()

    def setUp(self):
        """Создание новой змейки перед каждым тестом."""
        self.snake = Snake(start_position=(20, 15))

    def test_change_to_valid_direction(self):
        """Тест изменения на допустимое направление."""
        # Изначально RIGHT
        self.snake.change_direction(Direction.UP)
        self.assertEqual(self.snake.direction, Direction.UP)

        self.snake.change_direction(Direction.LEFT)
        self.assertEqual(self.snake.direction, Direction.LEFT)

        self.snake.change_direction(Direction.DOWN)
        self.assertEqual(self.snake.direction, Direction.DOWN)

        self.snake.change_direction(Direction.RIGHT)
        self.assertEqual(self.snake.direction, Direction.RIGHT)

    def test_cannot_reverse_direction_right_left(self):
        """Тест, что нельзя развернуться с RIGHT на LEFT."""
        self.snake.direction = Direction.RIGHT
        self.snake.change_direction(Direction.LEFT)

        self.assertEqual(self.snake.direction, Direction.RIGHT)

    def test_cannot_reverse_direction_left_right(self):
        """Тест, что нельзя развернуться с LEFT на RIGHT."""
        self.snake.direction = Direction.LEFT
        self.snake.change_direction(Direction.RIGHT)

        self.assertEqual(self.snake.direction, Direction.LEFT)

    def test_cannot_reverse_direction_up_down(self):
        """Тест, что нельзя развернуться с UP на DOWN."""
        self.snake.direction = Direction.UP
        self.snake.change_direction(Direction.DOWN)

        self.assertEqual(self.snake.direction, Direction.UP)

    def test_cannot_reverse_direction_down_up(self):
        """Тест, что нельзя развернуться с DOWN на UP."""
        self.snake.direction = Direction.DOWN
        self.snake.change_direction(Direction.UP)

        self.assertEqual(self.snake.direction, Direction.DOWN)


class TestSnakeCollisions(unittest.TestCase):
    """Тесты столкновений змейки."""

    @classmethod
    def setUpClass(cls):
        """Инициализация Pygame перед всеми тестами класса."""
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        """Завершение работы Pygame после всех тестов класса."""
        pygame.quit()

    def test_wall_collision_left(self):
        """Тест столкновения с левой стеной."""
        snake = Snake(start_position=(39, 15), grid_width=40)
        snake.change_direction(Direction.LEFT)
        snake.move()

        self.assertTrue(snake.check_wall_collision())

    def test_wall_collision_right(self):
        """Тест столкновения с правой стеной."""
        snake = Snake(start_position=(39, 15), grid_width=40)
        # По умолчанию движется RIGHT
        snake.move()

        self.assertTrue(snake.check_wall_collision())

    def test_wall_collision_top(self):
        """Тест столкновения с верхней стеной."""
        snake = Snake(start_position=(20, 0))
        snake.change_direction(Direction.UP)
        snake.move()

        self.assertTrue(snake.check_wall_collision())

    def test_wall_collision_bottom(self):
        """Тест столкновения с нижней стеной."""
        snake = Snake(start_position=(20, 29), grid_height=30)
        snake.change_direction(Direction.DOWN)
        snake.move()

        self.assertTrue(snake.check_wall_collision())

    def test_no_wall_collision_inside_grid(self):
        """Тест отсутствия столкновения внутри сетки."""
        snake = Snake(start_position=(20, 15))
        snake.move()

        self.assertFalse(snake.check_wall_collision())

    def test_no_wall_collision_at_safe_position(self):
        """Тест отсутствия столкновения на безопасной позиции."""
        snake = Snake(start_position=(10, 10))

        for _ in range(10):
            snake.move()
            self.assertFalse(snake.check_wall_collision())
    def test_no_self_collision_short_snake(self):
        """Тест, что короткая змейка не сталкивается с собой."""
        snake = Snake(start_position=(10, 10))

        # Змейка длины 1
        self.assertFalse(snake.check_self_collision())

        # Змейка длины 2
        snake.grow()
        snake.move()
        self.assertFalse(snake.check_self_collision())

        # Змейка длины 3
        snake.grow()
        snake.move()
        self.assertFalse(snake.check_self_collision())


class TestSnakeDrawing(unittest.TestCase):
    """Тесты отрисовки змейки."""

    @classmethod
    def setUpClass(cls):
        """Инициализация Pygame и создание экрана."""
        pygame.init()
        cls.screen = pygame.display.set_mode((800, 600))

    @classmethod
    def tearDownClass(cls):
        """Завершение работы Pygame."""
        pygame.quit()

    def test_draw_single_segment(self):
        """Тест отрисовки змейки из одного сегмента."""
        snake = Snake(start_position=(5, 5))

        try:
            snake.draw(self.screen)
        except Exception as e:
            self.fail(f"Отрисовка змейки из 1 сегмента вызвала исключение: {e}")

    def test_draw_multiple_segments(self):
        """Тест отрисовки змейки из нескольких сегментов."""
        snake = Snake(start_position=(10, 10))

        # Растим змейку
        for _ in range(5):
            snake.grow()
            snake.move()

        try:
            snake.draw(self.screen)
        except Exception as e:
            self.fail(f"Отрисовка змейки из {len(snake.body)} сегментов вызвала исключение: {e}")

    def test_draw_at_boundaries(self):
        """Тест отрисовки змейки на границах экрана."""
        positions = [
            (0, 0),  # Верхний левый угол
            (39, 0),  # Верхний правый угол
            (0, 29),  # Нижний левый угол
            (39, 29),  # Нижний правый угол
        ]

        for pos in positions:
            snake = Snake(start_position=pos)
            try:
                snake.draw(self.screen)
            except Exception as e:
                self.fail(f"Отрисовка в позиции {pos} вызвала исключение: {e}")


class TestDirectionEnum(unittest.TestCase):
    """Тесты перечисления Direction."""

    def test_direction_values(self):
        """Тест значений направлений."""
        self.assertEqual(Direction.UP.value, (0, -1))
        self.assertEqual(Direction.DOWN.value, (0, 1))
        self.assertEqual(Direction.LEFT.value, (-1, 0))
        self.assertEqual(Direction.RIGHT.value, (1, 0))

    def test_direction_count(self):
        """Тест количества направлений."""
        directions = list(Direction)
        self.assertEqual(len(directions), 4)

    def test_all_directions_present(self):
        """Тест наличия всех направлений."""
        self.assertIn(Direction.UP, Direction)
        self.assertIn(Direction.DOWN, Direction)
        self.assertIn(Direction.LEFT, Direction)
        self.assertIn(Direction.RIGHT, Direction)

    def test_direction_is_enum(self):
        """Тест, что Direction является перечислением."""
        from enum import Enum
        self.assertTrue(issubclass(Direction, Enum))


if __name__ == '__main__':
    unittest.main()