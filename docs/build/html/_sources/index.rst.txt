.. snake documentation master file, created by
   sphinx-quickstart on Mon Jun  1 19:06:06 2026.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Документация игры "Змейка"
===========================

Добро пожаловать в документацию игры "Змейка"!
Эта игра создана с использованием Pygame и демонстрирует принципы ООП.

Содержание
----------

.. toctree::
   :maxdepth: 2
   :caption: Оглавление:

   introduction
   installation
   usage
   modules
   api
   tests
   database
   changelog

Основные возможности
--------------------

* Классический геймплей змейки
* Настраиваемые параметры через командную строку
* Сохранение результатов в базу данных
* Полная документация и тесты
* Объектно-ориентированная архитектура

Быстрый старт
-------------

.. code-block:: bash

   # Установка зависимостей
   pip install -r requirements.txt

   # Запуск игры
   python main.py

   # Запуск с параметрами
   python main.py --player "Игрок" --speed 15

Индексы и таблицы
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
