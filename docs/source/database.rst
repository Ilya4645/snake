База данных
===========

Структура базы данных
---------------------

Результаты игр сохраняются в CSV-файл ``game_results.csv`` со следующими колонками:

* **timestamp** - дата и время игры
* **player_name** - имя игрока
* **score** - набранные очки
* **snake_length** - длина змейки

Работа с базой данных
---------------------

Сохранение результатов
~~~~~~~~~~~~~~~~~~~~~

Результаты автоматически сохраняются после каждой игры:

.. code-block:: python

   db_manager = DatabaseManager()
   db_manager.save_game_result(
       player_name="Игрок",
       score=100,
       snake_length=5
   )

Получение статистики
~~~~~~~~~~~~~~~~~~~~

Статистика конкретного игрока:

.. code-block:: python

   player_stats = db_manager.get_player_statistics("Игрок")

Топ-10 лучших результатов:

.. code-block:: python

   top_scores = db_manager.get_top_scores(10)

Все игры:

.. code-block:: python

   all_games = db_manager.get_all_games()

Анализ данных с Pandas
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pandas as pd

   # Загрузка данных
   df = pd.read_csv('game_results.csv')

   # Лучший результат
   print(df['score'].max())

   # Средний счет
   print(df['score'].mean())

   # Группировка по игрокам
   print(df.groupby('player_name')['score'].mean())