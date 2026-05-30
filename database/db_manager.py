"""
Модуль управления базой данных.

Обеспечивает сохранение и загрузку результатов игры
с использованием библиотеки Pandas.
"""

import pandas as pd
import os
from datetime import datetime
from typing import Optional


class DatabaseManager:
    """
    Менеджер базы данных для сохранения результатов игры.

    Использует Pandas DataFrame для хранения и управления
    статистикой игр в CSV-файле.

    Attributes:
        db_path (str): Путь к файлу базы данных CSV
        columns (list): Список колонок в базе данных
    """

    def __init__(self, db_path: str = "game_results.csv"):
        """
        Инициализация менеджера базы данных.

        Args:
            db_path: Путь к файлу CSV с результатами
        """
        self.db_path = db_path
        self.columns = ['timestamp', 'player_name', 'score', 'snake_length']

        # Создаем файл базы данных, если его нет
        if not os.path.exists(self.db_path):
            self._create_empty_db()

    def _create_empty_db(self) -> None:
        """
        Создание пустой базы данных.

        Создает CSV-файл с заголовками колонок.
        """
        df = pd.DataFrame(columns=self.columns)
        df.to_csv(self.db_path, index=False)

    def save_game_result(self, player_name: str, score: int,
                         snake_length: int) -> None:
        """
        Сохранение результата игры.

        Args:
            player_name: Имя игрока
            score: Набранные очки
            snake_length: Длина змейки в конце игры
        """
        # Загружаем существующие данные
        df = pd.read_csv(self.db_path)

        # Создаем новую запись
        new_record = pd.DataFrame({
            'timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            'player_name': [player_name],
            'score': [score],
            'snake_length': [snake_length]
        })

        # Добавляем запись и сохраняем
        df = pd.concat([df, new_record], ignore_index=True)
        df.to_csv(self.db_path, index=False)

    def get_player_statistics(self, player_name: str) -> pd.DataFrame:
        """
        Получение статистики конкретного игрока.

        Args:
            player_name: Имя игрока

        Returns:
            DataFrame: Статистика игрока
        """
        df = pd.read_csv(self.db_path)
        return df[df['player_name'] == player_name]

    def get_top_scores(self, limit: int = 10) -> pd.DataFrame:
        """
        Получение лучших результатов.

        Args:
            limit: Количество возвращаемых записей

        Returns:
            DataFrame: Топ результатов
        """
        df = pd.read_csv(self.db_path)
        return df.nlargest(limit, 'score')

    def get_all_games(self) -> pd.DataFrame:
        """
        Получение всех записей из базы данных.

        Returns:
            DataFrame: Все записи
        """
        return pd.read_csv(self.db_path)