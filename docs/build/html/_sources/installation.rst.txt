Установка
=========

Требования
----------

* Python 3.8 или выше
* pip (менеджер пакетов Python)
* Виртуальное окружение (рекомендуется)

Пошаговая установка
-------------------

1. Клонирование репозитория:

.. code-block:: bash

   git clone https://github.com/Ilya4645/snake.git
   cd snake

2. Создание виртуального окружения:

.. code-block:: bash

   python -m venv venv

   # Активация на Windows
   venv\Scripts\activate

   # Активация на Linux/Mac
   source venv/bin/activate

3. Установка зависимостей:

.. code-block:: bash

   pip install -r requirements.txt

Зависимости
-----------

* **pygame** - библиотека для создания игр
* **pandas** - библиотека для работы с данными
* **unittest** - фреймворк для тестирования
* **sphinx** - генератор документации

Проверка установки
------------------

.. code-block:: bash

   # Запуск тестов
   cd tests
   python -m unittest

   # Запуск игры
   python main.py