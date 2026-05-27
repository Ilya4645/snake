"""
Модуль контроллера игры.

Управляет основным игровым циклом, обработкой событий
и взаимодействием между объектами игры.
"""

import pygame
from typing import Tuple, Optional
from .snake import Snake, Direction
from .apple import Apple
from database.db_manager import DatabaseManager


class GameController:
    """
    Контроллер игры "Змейка".

    Управляет игровым процессом: инициализацией, игровым циклом,
    обработкой ввода пользователя, обновлением состояния и отрисовкой.

    Attributes:
        width (int): Ширина окна в пикселях
        height (int): Высота окна в пикселях
        cell_size (int): Размер клетки
        grid_width (int): Ширина сетки в клетках
        grid_height (int): Высота сетки в клетках
        fps (int): Частота кадров
        player_name (str): Имя игрока
    """

    def __init__(self, width: int = 800, height: int = 600,
                 cell_size: int = 20, fps: int = 10,
                 player_name: str = "Player"):
        """
        Инициализация контроллера игры.

        Args:
            width: Ширина окна в пикселях
            height: Высота окна в пикселях
            cell_size: Размер одной клетки
            fps: Частота кадров (скорость игры)
            player_name: Имя игрока
        """
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid_width = width // cell_size
        self.grid_height = height // cell_size
        self.fps = fps
        self.player_name = player_name

        # Инициализация Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(f"Snake Game - {player_name}")
        self.clock = pygame.time.Clock()

        # Создание объектов игры
        self.snake = Snake(
            start_position=(self.grid_width // 2, self.grid_height // 2),
            grid_width=self.grid_width,
            grid_height=self.grid_height,
            size=cell_size
        )
        self.apple = Apple(
            position=(10, 10),
            grid_width=self.grid_width,
            grid_height=self.grid_height,
            size=cell_size
        )

        # Состояние игры
        self.running = True
        self.game_over = False
        self.score = 0

        # База данных
        self.db_manager = DatabaseManager()

    def handle_events(self) -> None:
        """
        Обработка событий Pygame.

        Обрабатывает нажатия клавиш для управления змейкой
        и событие закрытия окна.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                else:
                    # Управление змейкой
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.snake.change_direction(Direction.UP)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.snake.change_direction(Direction.DOWN)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.snake.change_direction(Direction.LEFT)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.snake.change_direction(Direction.RIGHT)

    def update(self) -> None:
        """
        Обновление состояния игры.

        Двигает змейку, проверяет столкновения и поедание яблок.
        """
        if self.game_over:
            return

        # Двигаем змейку
        self.snake.move()

        # Проверяем столкновения
        if self.snake.check_wall_collision() or self.snake.check_self_collision():
            self.game_over = True
            self.save_game_result()
            return

        # Проверяем поедание яблока
        if self.apple.is_eaten(self.snake.get_head_position()):
            self.snake.grow()
            self.apple.respawn(self.snake.body)
            self.score += 10

    def draw(self) -> None:
        """
        Отрисовка игрового поля.

        Рисует фон, сетку, змейку, яблоко и интерфейс.
        """
        # Очистка экрана
        self.screen.fill((0, 0, 0))

        # Отрисовка сетки
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, (40, 40, 40),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, (40, 40, 40),
                             (0, y), (self.width, y))

        # Отрисовка объектов
        self.snake.draw(self.screen)
        self.apple.draw(self.screen)

        # Отрисовка счета
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        # Отрисовка Game Over
        if self.game_over:
            self.draw_game_over()

        pygame.display.flip()

    def draw_game_over(self) -> None:
        """
        Отрисовка экрана завершения игры.
        """
        # Затемнение фона
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Текст Game Over
        font_large = pygame.font.Font(None, 74)
        font_small = pygame.font.Font(None, 36)

        game_over_text = font_large.render("GAME OVER", True, (255, 0, 0))
        score_text = font_small.render(f"Final Score: {self.score}",
                                       True, (255, 255, 255))
        restart_text = font_small.render("Press SPACE to restart or ESC to quit",
                                         True, (200, 200, 200))

        # Центрирование текста
        game_over_rect = game_over_text.get_rect(
            center=(self.width // 2, self.height // 2 - 50))
        score_rect = score_text.get_rect(
            center=(self.width // 2, self.height // 2 + 20))
        restart_rect = restart_text.get_rect(
            center=(self.width // 2, self.height // 2 + 70))

        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(restart_text, restart_rect)

    def reset_game(self) -> None:
        """
        Сброс игры для нового раунда.
        """
        self.snake = Snake(
            start_position=(self.grid_width // 2, self.grid_height // 2),
            grid_width=self.grid_width,
            grid_height=self.grid_height,
            size=self.cell_size
        )
        self.apple = Apple(
            position=(10, 10),
            grid_width=self.grid_width,
            grid_height=self.grid_height,
            size=self.cell_size
        )
        self.game_over = False
        self.score = 0

    def save_game_result(self) -> None:
        """
        Сохранение результата игры в базу данных.
        """
        self.db_manager.save_game_result(
            player_name=self.player_name,
            score=self.score,
            snake_length=len(self.snake.body)
        )

    def run(self) -> None:
        """
        Запуск основного игрового цикла.

        Выполняет цикл обработки событий, обновления состояния
        и отрисовки, пока игра не будет закрыта.
        """
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)

        pygame.quit()