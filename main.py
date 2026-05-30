"""
Главный модуль игры "Змейка".

Точка входа в игру. Обрабатывает аргументы командной строки
и запускает игровой процесс.

Примеры использования:
    python main.py
    python main.py --player "John" --speed 15
    python main.py -p "Alice" -s 20 -w 1024 -e 768
"""

import argparse
from game.game_controller import GameController


def parse_arguments() -> argparse.Namespace:
    """
    Парсинг аргументов командной строки.

    Returns:
        Namespace: Объект с аргументами командной строки

    Аргументы:
        --player, -p: Имя игрока (по умолчанию "Player")
        --speed, -s: Скорость игры в FPS (по умолчанию 10)
        --width, -w: Ширина окна в пикселях (по умолчанию 800)
        --height, -e: Высота окна в пикселях (по умолчанию 600)
        --cell-size, -c: Размер клетки (по умолчанию 20)
    """
    parser = argparse.ArgumentParser(
        description='Snake Game with Pygame',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Примеры:
  python main.py
  python main.py --player "John" --speed 15
  python main.py -p "Alice" -s 20 -w 1024 -e 768
        '''
    )

    parser.add_argument(
        '--player', '-p',
        type=str,
        default='Player',
        help='Имя игрока (по умолчанию: Player)'
    )

    parser.add_argument(
        '--speed', '-s',
        type=int,
        default=10,
        help='Скорость игры (FPS, по умолчанию: 10)'
    )

    parser.add_argument(
        '--width', '-w',
        type=int,
        default=800,
        help='Ширина окна в пикселях (по умолчанию: 800)'
    )

    parser.add_argument(
        '--height', '-e',
        type=int,
        default=600,
        help='Высота окна в пикселях (по умолчанию: 600)'
    )

    parser.add_argument(
        '--cell-size', '-c',
        type=int,
        default=20,
        help='Размер клетки в пикселях (по умолчанию: 20)'
    )

    return parser.parse_args()


def main() -> None:
    """
    Главная функция запуска игры.

    Получает аргументы командной строки, создает контроллер игры
    и запускает игровой процесс.
    """
    # Получаем аргументы командной строки
    args = parse_arguments()

    print(f"Запуск игры 'Змейка' для игрока: {args.player}")
    print(f"Скорость: {args.speed} FPS")
    print(f"Размер окна: {args.width}x{args.height}")
    print(f"Размер клетки: {args.cell_size}")
    print("\nУправление:")
    print("  Стрелки или WASD - движение змейки")
    print("  SPACE - рестарт после проигрыша")
    print("  ESC - выход из игры")

    # Создаем и запускаем игру
    game = GameController(
        width=args.width,
        height=args.height,
        cell_size=args.cell_size,
        fps=args.speed,
        player_name=args.player
    )

    game.run()


if __name__ == "__main__":
    main()