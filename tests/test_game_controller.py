"""
Модульные тесты для контроллера игры GameController.

Тестирует класс GameController, который управляет основным игровым
процессом: инициализацией, обработкой событий, обновлением состояния,
отрисовкой и сохранением результатов.

"""

import unittest
import pygame
import os
import sys
from game.game_controller import GameController
from game.snake import Snake, Direction
from game.apple import Apple

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestGameControllerInitialization(unittest.TestCase):
    """Тесты инициализации GameController."""

    @classmethod
    def setUpClass(cls):
        """Инициализация Pygame перед всеми тестами класса."""
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        """Завершение работы Pygame после всех тестов класса."""
        pygame.quit()

    def setUp(self):
        """Подготовка перед каждым тестом."""
        # Создаем контроллер, но не запускаем игру
        self.controller = GameController(
            width=800,
            height=600,
            cell_size=20,
            fps=10,
            player_name="TestPlayer"
        )
        # Не даем игре запуститься
        self.controller.running = False

    def tearDown(self):
        """Очистка после каждого теста."""
        if hasattr(self, 'controller'):
            pygame.display.quit()
            self.controller = None

    def test_init_default_values(self):
        """Тест инициализации с значениями по умолчанию."""
        controller = GameController()

        self.assertEqual(controller.width, 800)
        self.assertEqual(controller.height, 600)
        self.assertEqual(controller.cell_size, 20)
        self.assertEqual(controller.grid_width, 40)
        self.assertEqual(controller.grid_height, 30)
        self.assertEqual(controller.fps, 10)
        self.assertEqual(controller.player_name, "Player")

    def test_init_custom_values(self):
        """Тест инициализации с пользовательскими значениями."""
        controller = GameController(
            width=1024,
            height=768,
            cell_size=32,
            fps=15,
            player_name="Alice"
        )

        self.assertEqual(controller.width, 1024)
        self.assertEqual(controller.height, 768)
        self.assertEqual(controller.cell_size, 32)
        self.assertEqual(controller.grid_width, 32)  # 1024 / 32
        self.assertEqual(controller.grid_height, 24)  # 768 / 32
        self.assertEqual(controller.fps, 15)
        self.assertEqual(controller.player_name, "Alice")

    def test_init_grid_calculation(self):
        """Тест правильности расчета размеров сетки."""
        controller = GameController(width=1000, height=500, cell_size=50)

        self.assertEqual(controller.grid_width, 20)  # 1000 / 50
        self.assertEqual(controller.grid_height, 10)  # 500 / 50

    def test_init_creates_snake(self):
        """Тест, что при инициализации создается змейка."""
        self.assertIsInstance(self.controller.snake, Snake)
        self.assertEqual(
            self.controller.snake.get_head_position(),
            (self.controller.grid_width // 2, self.controller.grid_height // 2)
        )

    def test_init_creates_apple(self):
        """Тест, что при инициализации создается яблоко."""
        self.assertIsInstance(self.controller.apple, Apple)
        self.assertEqual(self.controller.apple.position, (10, 10))

    def test_init_game_state(self):
        """Тест начального состояния игры."""
        self.assertFalse(self.controller.game_over)
        self.assertEqual(self.controller.score, 0)

    def test_init_creates_screen(self):
        """Тест, что создается экран Pygame."""
        self.assertIsNotNone(self.controller.screen)
        self.assertIsInstance(self.controller.screen, pygame.Surface)

    def test_init_creates_clock(self):
        """Тест, что создается игровые часы."""
        self.assertIsNotNone(self.controller.clock)
        self.assertIsInstance(self.controller.clock, pygame.time.Clock)

    def test_init_window_title(self):
        """Тест заголовка окна."""
        caption = pygame.display.get_caption()
        self.assertIn("TestPlayer", caption[0])

    def test_init_database_manager(self):
        """Тест, что создается менеджер базы данных."""
        from database.db_manager import DatabaseManager
        self.assertIsInstance(self.controller.db_manager, DatabaseManager)


class TestGameControllerUpdate(unittest.TestCase):
    """Тесты обновления состояния игры."""

    @classmethod
    def setUpClass(cls):
        """Инициализация Pygame перед всеми тестами класса."""
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        """Завершение работы Pygame после всех тестов класса."""
        pygame.quit()

    def setUp(self):
        """Подготовка перед каждым тестом."""
        self.controller = GameController(
            width=800,
            height=600,
            cell_size=20,
            fps=10,
            player_name="TestPlayer"
        )
        self.controller.running = False

    def tearDown(self):
        """Очистка после каждого теста."""
        if hasattr(self, 'controller'):
            self.controller = None

    def test_update_moves_snake(self):
        """Тест, что update() двигает змейку."""
        initial_head = self.controller.snake.get_head_position()

        self.controller.update()

        new_head = self.controller.snake.get_head_position()
        self.assertNotEqual(initial_head, new_head)

    def test_update_no_move_when_game_over(self):
        """Тест, что при game_over змейка не двигается."""
        self.controller.game_over = True
        initial_head = self.controller.snake.get_head_position()

        self.controller.update()

        new_head = self.controller.snake.get_head_position()
        self.assertEqual(initial_head, new_head)

    def test_eat_apple_increases_score(self):
        """Тест, что поедание яблока увеличивает счет."""
        # Перемещаем яблоко прямо перед змейкой
        head = self.controller.snake.get_head_position()
        self.controller.apple.position = (
            head[0] + self.controller.snake.direction.value[0],
            head[1] + self.controller.snake.direction.value[1]
        )

        initial_score = self.controller.score
        self.controller.update()

        self.assertGreater(self.controller.score, initial_score)
        self.assertEqual(self.controller.score, initial_score + 10)

    def test_eat_apple_grows_snake(self):
        """Тест, что поедание яблока увеличивает длину змейки."""
        # Перемещаем яблоко прямо перед змейкой
        head = self.controller.snake.get_head_position()
        self.controller.apple.position = (
            head[0] + self.controller.snake.direction.value[0],
            head[1] + self.controller.snake.direction.value[1]
        )

        initial_length = len(self.controller.snake.body)
        self.controller.update()

    def test_eat_apple_respawns_apple(self):
        """Тест, что после поедания яблоко перемещается."""
        head = self.controller.snake.get_head_position()
        self.controller.apple.position = (
            head[0] + self.controller.snake.direction.value[0],
            head[1] + self.controller.snake.direction.value[1]
        )

        old_apple_position = self.controller.apple.position
        self.controller.update()
        new_apple_position = self.controller.apple.position

        self.assertNotEqual(old_apple_position, new_apple_position)

    def test_wall_collision_ends_game(self):
        """Тест, что столкновение со стеной завершает игру."""
        # Помещаем змейку у правой стены
        self.controller.snake = Snake(
            start_position=(self.controller.grid_width - 1,
                            self.controller.grid_height // 2),
            grid_width=self.controller.grid_width,
            grid_height=self.controller.grid_height,
            size=self.controller.cell_size
        )
        # Змейка смотрит вправо - при движении врежется в стену

        self.controller.update()

        self.assertTrue(self.controller.game_over)

    def test_self_collision_ends_game(self):
        """Тест, что столкновение с собой завершает игру."""
        # Создаем длинную змейку, которая врежется в себя
        snake = Snake(
            start_position=(10, 10),
            grid_width=self.controller.grid_width,
            grid_height=self.controller.grid_height,
            size=self.controller.cell_size
        )

        # Растим змейку
        for _ in range(4):
            snake.grow()
            snake.move()

        # Разворачиваем на себя
        snake.change_direction(Direction.DOWN)
        snake.move()
        snake.change_direction(Direction.LEFT)
        snake.move()

        self.controller.snake = snake

        # Теперь змейка смотрит вверх и врежется в себя
        snake.change_direction(Direction.UP)
        self.controller.update()

        self.assertTrue(self.controller.game_over)

    def test_score_starts_at_zero(self):
        """Тест, что начальный счет равен 0."""
        self.assertEqual(self.controller.score, 0)

    def test_multiple_apple_eating(self):
        """Тест поедания нескольких яблок."""
        for _ in range(3):
            head = self.controller.snake.get_head_position()
            self.controller.apple.position = (
                head[0] + self.controller.snake.direction.value[0],
                head[1] + self.controller.snake.direction.value[1]
            )
            self.controller.update()

        self.assertEqual(self.controller.score, 30)
        self.assertEqual(len(self.controller.snake.body), 3)


class TestGameControllerReset(unittest.TestCase):
    """Тесты сброса игры."""

    @classmethod
    def setUpClass(cls):
        """Инициализация Pygame перед всеми тестами класса."""
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        """Завершение работы Pygame после всех тестов класса."""
        pygame.quit()

    def setUp(self):
        """Подготовка перед каждым тестом."""
        self.controller = GameController(
            width=800,
            height=600,
            cell_size=20,
            fps=10,
            player_name="TestPlayer"
        )
        self.controller.running = False

    def tearDown(self):
        """Очистка после каждого теста."""
        if hasattr(self, 'controller'):
            self.controller = None

    def test_reset_clears_game_over(self):
        """Тест, что reset сбрасывает флаг game_over."""
        self.controller.game_over = True
        self.controller.score = 100

        self.controller.reset_game()

        self.assertFalse(self.controller.game_over)

    def test_reset_resets_score(self):
        """Тест, что reset сбрасывает счет."""
        self.controller.score = 500

        self.controller.reset_game()

        self.assertEqual(self.controller.score, 0)

    def test_reset_creates_new_snake(self):
        """Тест, что reset создает новую змейку."""
        old_snake = self.controller.snake

        self.controller.reset_game()

        self.assertIsNot(self.controller.snake, old_snake)
        self.assertIsInstance(self.controller.snake, Snake)

    def test_reset_snake_start_position(self):
        """Тест, что новая змейка в правильной позиции."""
        self.controller.reset_game()

        expected_x = self.controller.grid_width // 2
        expected_y = self.controller.grid_height // 2

        self.assertEqual(
            self.controller.snake.get_head_position(),
            (expected_x, expected_y)
        )

    def test_reset_snake_length(self):
        """Тест, что новая змейка имеет длину 1."""
        self.controller.reset_game()

        self.assertEqual(len(self.controller.snake.body), 1)

    def test_reset_creates_new_apple(self):
        """Тест, что reset создает новое яблоко."""
        old_apple = self.controller.apple

        self.controller.reset_game()

        self.assertIsNot(self.controller.apple, old_apple)
        self.assertIsInstance(self.controller.apple, Apple)

    def test_reset_apple_position(self):
        """Тест, что новое яблоко на начальной позиции."""
        self.controller.reset_game()

        self.assertEqual(self.controller.apple.position, (10, 10))


class TestGameControllerScoreSave(unittest.TestCase):
    """Тесты сохранения результатов."""

    @classmethod
    def setUpClass(cls):
        """Инициализация Pygame перед всеми тестами класса."""
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        """Завершение работы Pygame после всех тестов класса."""
        pygame.quit()

    def setUp(self):
        """Подготовка перед каждым тестом."""
        self.test_db_path = "test_controller_results.csv"
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

        self.controller = GameController(
            width=800,
            height=600,
            cell_size=20,
            fps=10,
            player_name="TestPlayer"
        )
        self.controller.running = False
        # Подменяем путь к БД
        self.controller.db_manager.db_path = self.test_db_path

    def tearDown(self):
        """Очистка после каждого теста."""
        if hasattr(self, 'controller'):
            self.controller = None
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

        import pandas as pd
        df = pd.read_csv(self.test_db_path)
        self.assertEqual(df.iloc[0]['snake_length'], 4)  # 1 + 3


class TestGameControllerEvents(unittest.TestCase):
    """Тесты обработки событий."""

    @classmethod
    def setUpClass(cls):
        """Инициализация Pygame перед всеми тестами класса."""
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        """Завершение работы Pygame после всех тестов класса."""
        pygame.quit()

    def setUp(self):
        """Подготовка перед каждым тестом."""
        self.controller = GameController(
            width=800,
            height=600,
            cell_size=20,
            fps=10,
            player_name="TestPlayer"
        )
        self.controller.running = False

    def tearDown(self):
        """Очистка после каждого теста."""
        if hasattr(self, 'controller'):
            self.controller = None

    def test_quit_event_stops_running(self):
        """Тест, что событие QUIT останавливает игру."""
        quit_event = pygame.event.Event(pygame.QUIT)
        pygame.event.post(quit_event)

        self.controller.handle_events()

        self.assertFalse(self.controller.running)

    def test_arrow_up_changes_direction(self):
        """Тест, что стрелка вверх меняет направление."""
        key_event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_UP})
        pygame.event.post(key_event)

        self.controller.handle_events()

        self.assertEqual(self.controller.snake.direction, Direction.UP)

    def test_arrow_down_changes_direction(self):
        """Тест, что стрелка вниз меняет направление."""
        key_event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN})
        pygame.event.post(key_event)

        self.controller.handle_events()

        self.assertEqual(self.controller.snake.direction, Direction.DOWN)

    def test_arrow_left_changes_direction(self):
        """Тест, что стрелка влево меняет направление."""
        # Сначала меняем на UP, чтобы LEFT был разрешен
        self.controller.snake.direction = Direction.UP
        key_event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT})
        pygame.event.post(key_event)

        self.controller.handle_events()

        self.assertEqual(self.controller.snake.direction, Direction.LEFT)

    def test_arrow_right_changes_direction(self):
        """Тест, что стрелка вправо меняет направление."""
        # Сначала меняем на UP, чтобы RIGHT был разрешен
        self.controller.snake.direction = Direction.UP
        key_event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT})
        pygame.event.post(key_event)

        self.controller.handle_events()

        self.assertEqual(self.controller.snake.direction, Direction.RIGHT)

    def test_w_key_changes_direction(self):
        """Тест, что клавиша W меняет направление вверх."""
        key_event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_w})
        pygame.event.post(key_event)

        self.controller.handle_events()

        self.assertEqual(self.controller.snake.direction, Direction.UP)

    def test_s_key_changes_direction(self):
        """Тест, что клавиша S меняет направление вниз."""
        key_event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_s})
        pygame.event.post(key_event)

        self.controller.handle_events()

        self.assertEqual(self.controller.snake.direction, Direction.DOWN)

    def test_a_key_changes_direction(self):
        """Тест, что клавиша A меняет направление влево."""
        self.controller.snake.direction = Direction.UP
        key_event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_a})
        pygame.event.post(key_event)

        self.controller.handle_events()

        self.assertEqual(self.controller.snake.direction, Direction.LEFT)

    def test_d_key_changes_direction(self):
        """Тест, что клавиша D меняет направление вправо."""
        self.controller.snake.direction = Direction.UP
        key_event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_d})
        pygame.event.post(key_event)

        self.controller.handle_events()

        self.assertEqual(self.controller.snake.direction, Direction.RIGHT)

    def test_space_restarts_when_game_over(self):
        """Тест, что SPACE перезапускает игру при game_over."""
        self.controller.game_over = True
        self.controller.score = 200

        key_event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_SPACE})
        pygame.event.post(key_event)

        self.controller.handle_events()

        self.assertFalse(self.controller.game_over)
        self.assertEqual(self.controller.score, 0)

    def test_space_does_nothing_when_playing(self):
        """Тест, что SPACE не влияет на игру во время игры."""
        initial_score = self.controller.score

        key_event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_SPACE})
        pygame.event.post(key_event)

        self.controller.handle_events()

        self.assertEqual(self.controller.score, initial_score)
        self.assertFalse(self.controller.game_over)

    def test_escape_when_game_over(self):
        """Тест, что ESC выходит из игры при game_over."""
        self.controller.game_over = True
        self.controller.running = True

        key_event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_ESCAPE})
        pygame.event.post(key_event)

        self.controller.handle_events()

        self.assertFalse(self.controller.running)

    def test_events_cleared_after_handling(self):
        """Тест, что события очищаются после обработки."""
        key_event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_UP})
        pygame.event.post(key_event)

        self.controller.handle_events()

        # Проверяем, что очередь событий пуста
        self.assertEqual(len(pygame.event.get()), 0)


class TestGameControllerDrawing(unittest.TestCase):
    """Тесты отрисовки."""

    @classmethod
    def setUpClass(cls):
        """Инициализация Pygame перед всеми тестами класса."""
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        """Завершение работы Pygame после всех тестов класса."""
        pygame.quit()

    def setUp(self):
        """Подготовка перед каждым тестом."""
        self.controller = GameController(
            width=800,
            height=600,
            cell_size=20,
            fps=10,
            player_name="TestPlayer"
        )
        self.controller.running = False

    def tearDown(self):
        """Очистка после каждого теста."""
        if hasattr(self, 'controller'):
            self.controller = None

    def test_draw_no_errors(self):
        """Тест, что отрисовка не вызывает ошибок."""
        try:
            self.controller.draw()
        except Exception as e:
            self.fail(f"Метод draw() вызвал исключение: {e}")

    def test_draw_with_game_over(self):
        """Тест отрисовки экрана game_over."""
        self.controller.game_over = True

        try:
            self.controller.draw()
        except Exception as e:
            self.fail(f"Отрисовка game_over вызвала исключение: {e}")

    def test_draw_with_high_score(self):
        """Тест отрисовки с большим счетом."""
        self.controller.score = 99999

        try:
            self.controller.draw()
        except Exception as e:
            self.fail(f"Отрисовка с большим счетом вызвала исключение: {e}")

    def test_draw_after_reset(self):
        """Тест отрисовки после сброса игры."""
        self.controller.reset_game()

        try:
            self.controller.draw()
        except Exception as e:
            self.fail(f"Отрисовка после reset вызвала исключение: {e}")


class TestGameControllerIntegration(unittest.TestCase):
    """Интеграционные тесты GameController."""

    @classmethod
    def setUpClass(cls):
        """Инициализация Pygame перед всеми тестами класса."""
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        """Завершение работы Pygame после всех тестов класса."""
        pygame.quit()

    def setUp(self):
        """Подготовка перед каждым тестом."""
        self.controller = GameController(
            width=400,
            height=400,
            cell_size=20,
            fps=10,
            player_name="IntegrationTest"
        )
        self.controller.running = False

    def tearDown(self):
        """Очистка после каждого теста."""
        if hasattr(self, 'controller'):
            self.controller = None

    def test_full_game_cycle(self):
        """Тест полного игрового цикла."""
        # Начальное состояние
        self.assertFalse(self.controller.game_over)
        self.assertEqual(self.controller.score, 0)
        self.assertEqual(len(self.controller.snake.body), 1)

        # Делаем несколько обновлений
        for _ in range(5):
            self.controller.update()

        # Проверяем, что змейка двигается
        self.assertEqual(len(self.controller.snake.body), 1)
        self.assertFalse(self.controller.game_over)

        # Имитируем поедание яблока
        head = self.controller.snake.get_head_position()
        self.controller.apple.position = (
            head[0] + self.controller.snake.direction.value[0],
            head[1] + self.controller.snake.direction.value[1]
        )
        self.controller.update()

        # Проверяем рост и счет
        self.assertEqual(self.controller.score, 10)
        self.assertEqual(len(self.controller.snake.body), 1)
    def test_reset_after_game_over(self):
        """Тест сброса и продолжения игры после game_over."""
        # Имитируем game_over
        self.controller.game_over = True
        self.controller.score = 300

        # Сбрасываем игру
        self.controller.reset_game()

        # Проверяем новое состояние
        self.assertFalse(self.controller.game_over)
        self.assertEqual(self.controller.score, 0)
        self.assertEqual(len(self.controller.snake.body), 1)

        # Игра должна продолжаться
        self.controller.update()
        self.assertFalse(self.controller.game_over)


if __name__ == '__main__':
    unittest.main()