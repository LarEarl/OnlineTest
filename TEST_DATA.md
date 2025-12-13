# Тестовые данные для заполнения базы данных OnlineTest

## Создание суперпользователя
```bash
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: admin123
```

## Данные для заполнения через админку

### 1. Курс (Course)
- **Title**: Python для начинающих
- **Description**: Полный курс по изучению Python с нуля. Вы научитесь основам программирования, работе с данными и созданию веб-приложений.
- **Slug**: python-basics
- **Image**: (загрузите любое изображение)
- **Is Posted**: ✓

### 2. Модули (Module)

#### Модуль 1:
- **Course**: Python для начинающих
- **Name**: Основы Python
- **Description**: Введение в Python, переменные, типы данных
- **Slug**: python-fundamentals
- **Order**: 0
- **Is Locked By Default**: ❌ (открыт для всех)

#### Модуль 2:
- **Course**: Python для начинающих
- **Name**: Условия и циклы
- **Description**: Изучаем if, for, while
- **Slug**: conditions-and-loops
- **Order**: 1
- **Is Locked By Default**: ✓ (закрыт)

### 3. Уроки (Lesson)

#### Урок 1 (в Модуле 1):
- **Module**: Основы Python
- **Title**: Введение в Python
- **Content**: 
```
Добро пожаловать в мир программирования на Python!

Python - это высокоуровневый язык программирования, который отличается простым и понятным синтаксисом.

Основные преимущества Python:
- Простота изучения
- Большое сообщество
- Множество библиотек
- Универсальность применения
```
- **Video URL**: https://www.youtube.com/watch?v=kqtD5dpn9C8
- **Order**: 0
- **Has Test**: ✓

#### Урок 2 (в Модуле 1):
- **Module**: Основы Python
- **Title**: Переменные и типы данных
- **Content**:
```
Переменные в Python

Переменная - это контейнер для хранения данных.

Примеры:
x = 5          # целое число (int)
y = 3.14       # число с плавающей точкой (float)
name = "John"  # строка (string)
is_valid = True # логическое значение (boolean)

Python автоматически определяет тип переменной!
```
- **Video URL**: (оставить пустым)
- **Order**: 1
- **Has Test**: ✓

### 4. Тест (Test) для Урока 1

- **Lesson**: Введение в Python
- **Title**: Проверка знаний: Введение в Python
- **Description**: Базовые вопросы о Python

### 5. Вопросы (Question) для теста

#### Вопрос 1 (Quiz):
- **Test**: Проверка знаний: Введение в Python
- **Text**: Какой из следующих языков программирования является Python?
- **Is Code**: ❌
- **Order**: 1

**Варианты ответов (AnswerOption)**:
1. Низкоуровневый язык | Is Correct: ❌
2. Высокоуровневый язык | Is Correct: ✓
3. Язык разметки | Is Correct: ❌
4. Язык запросов | Is Correct: ❌

#### Вопрос 2 (Quiz):
- **Test**: Проверка знаний: Введение в Python
- **Text**: Какое расширение имеют файлы Python?
- **Is Code**: ❌
- **Order**: 2

**Варианты ответов**:
1. .java | Is Correct: ❌
2. .py | Is Correct: ✓
3. .txt | Is Correct: ❌
4. .python | Is Correct: ❌

#### Вопрос 3 (Code):
- **Test**: Проверка знаний: Введение в Python
- **Text**: Напишите программу, которая выводит "Hello, World!"
- **Is Code**: ✓
- **Order**: 3

**Тест-кейсы (CodeTestCase)**:
1. Input Data: (пусто)
   Expected Output: Hello, World!
   Time Limit: 1.0

### 6. Тест для Урока 2

- **Lesson**: Переменные и типы данных
- **Title**: Проверка знаний: Переменные
- **Description**: Вопросы о переменных и типах данных

#### Вопрос 1 (Quiz):
- **Test**: Проверка знаний: Переменные
- **Text**: Какой оператор используется для присваивания значения переменной в Python?
- **Is Code**: ❌
- **Order**: 1

**Варианты ответов**:
1. == | Is Correct: ❌
2. = | Is Correct: ✓
3. := | Is Correct: ❌
4. -> | Is Correct: ❌

#### Вопрос 2 (Code):
- **Test**: Проверка знаний: Переменные
- **Text**: Создайте переменную x со значением 10 и выведите её
- **Is Code**: ✓
- **Order**: 2

**Тест-кейсы**:
1. Input Data: (пусто)
   Expected Output: 10
   Time Limit: 1.0

### 7. Прогресс пользователя (создается автоматически при прохождении)

После создания пользователя, можно вручную создать:

#### LessonProgress:
- **User**: (ваш тестовый пользователь)
- **Lesson**: Введение в Python
- **Is Completed**: ✓
- **Completed At**: (текущая дата)

#### ModuleProgress:
- **User**: (ваш тестовый пользователь)
- **Module**: Основы Python
- **Is Unlocked**: ✓
- **Completed Lessons Count**: 1
- **Completed At**: (оставить пустым)

## Быстрый SQL для тестов (опционально)

Если хотите быстро заполнить базу через SQL:

```sql
-- После создания через админку основных объектов (Course, Module, Lesson)
-- можно добавить тестовые данные для демонстрации
```

## URL для тестирования



- Для code вопросов нужен запущенный Celery и Docker с образом python-runner
- Quiz вопросы работают сразу через AJAX
- Убедитесь что у пользователя есть права доступа (@login_required в views)
