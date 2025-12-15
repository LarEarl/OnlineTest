import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OnlineTest.settings')
django.setup()

from courses.models import Course, Module, Lesson
from tests_app.models import Test, Question, AnswerOption

# Создаём курс
course = Course.objects.create(
    title='Python для начинающих',
    slug='python-dlya-nachinayushchikh',
    description='Полный курс по основам программирования на Python. Идеально подходит для тех, кто только начинает свой путь в программировании.',
    is_posted=True
)
print(f'✅ Курс создан: {course.title}')

# Модуль 1
module1 = Module.objects.create(
    course=course,
    name='Введение в Python',
    slug='vvedenie-v-python',
    description='Знакомство с языком программирования Python',
    order=1
)
print(f'✅ Модуль 1: {module1.name}')

# Уроки модуля 1
lesson1 = Lesson.objects.create(
    module=module1,
    title='Что такое Python?',
    content='Python - это высокоуровневый язык программирования, созданный Гвидо ван Россумом в 1991 году.\n\nОсновные преимущества Python:\n- Простой и понятный синтаксис\n- Большое количество библиотек\n- Кроссплатформенность\n- Активное сообщество\n\nPython используется в веб-разработке, анализе данных, машинном обучении, автоматизации и многих других областях.',
    video_url='https://www.youtube.com/watch?v=_uQrJ0TkZlc',
    order=1,
    has_test=False
)
print(f'  📝 Урок 1.1: {lesson1.title}')

lesson2 = Lesson.objects.create(
    module=module1,
    title='Установка Python',
    content='Для начала работы с Python необходимо установить интерпретатор.\n\nШаги установки:\n1. Перейдите на сайт python.org\n2. Скачайте последнюю версию Python\n3. Запустите установщик\n4. Не забудьте отметить "Add Python to PATH"\n5. Завершите установку\n\nПроверка установки:\nОткройте командную строку и введите:\npython --version\n\nЕсли установка прошла успешно, вы увидите номер версии Python.',
    order=2,
    has_test=True
)
print(f'  📝 Урок 1.2: {lesson2.title}')

# Тест для урока 2
test1 = Test.objects.create(
    lesson=lesson2,
    title='Тест: Установка Python',
    description='Проверьте свои знания об установке Python'
)

# Вопросы для теста
q1 = Question.objects.create(
    test=test1,
    text='Какую команду нужно ввести для проверки версии Python?',
    is_code=False,
    order=1
)
AnswerOption.objects.create(question=q1, text='python --version', is_correct=True)
AnswerOption.objects.create(question=q1, text='python -v', is_correct=False)
AnswerOption.objects.create(question=q1, text='check python', is_correct=False)
AnswerOption.objects.create(question=q1, text='python version', is_correct=False)

q2 = Question.objects.create(
    test=test1,
    text='Что нужно отметить при установке Python, чтобы можно было запускать его из любой папки?',
    is_code=False,
    order=2
)
AnswerOption.objects.create(question=q2, text='Add Python to PATH', is_correct=True)
AnswerOption.objects.create(question=q2, text='Install for all users', is_correct=False)
AnswerOption.objects.create(question=q2, text='Create desktop shortcut', is_correct=False)
AnswerOption.objects.create(question=q2, text='Download documentation', is_correct=False)

print(f'  ✅ Тест создан: {test1.title} (2 вопроса)')

lesson3 = Lesson.objects.create(
    module=module1,
    title='Первая программа Hello World',
    content='Давайте напишем вашу первую программу на Python!\n\nОткройте текстовый редактор или IDE и введите:\n\nprint("Hello, World!")\n\nСохраните файл как hello.py и запустите:\n\npython hello.py\n\nПоздравляем! Вы написали свою первую программу на Python.\n\nФункция print() выводит текст на экран. Текст должен быть в кавычках.',
    order=3,
    has_test=True
)
print(f'  📝 Урок 1.3: {lesson3.title}')

# Тест для урока 3
test2 = Test.objects.create(
    lesson=lesson3,
    title='Тест: Hello World',
    description='Проверьте понимание первой программы'
)

q3 = Question.objects.create(
    test=test2,
    text='Какая функция используется для вывода текста на экран?',
    is_code=False,
    order=1
)
AnswerOption.objects.create(question=q3, text='print()', is_correct=True)
AnswerOption.objects.create(question=q3, text='output()', is_correct=False)
AnswerOption.objects.create(question=q3, text='display()', is_correct=False)
AnswerOption.objects.create(question=q3, text='show()', is_correct=False)

print(f'  ✅ Тест создан: {test2.title} (1 вопрос)')

# Модуль 2
module2 = Module.objects.create(
    course=course,
    name='Переменные и типы данных',
    slug='peremennye-i-tipy-dannykh',
    description='Изучение переменных и основных типов данных в Python',
    order=2
)
print(f'✅ Модуль 2: {module2.name}')

lesson4 = Lesson.objects.create(
    module=module2,
    title='Что такое переменные',
    content='Переменная - это именованная область памяти для хранения данных.\n\nПример создания переменной:\nname = "Иван"\nage = 25\n\nПравила именования переменных:\n- Можно использовать буквы, цифры и подчёркивание\n- Имя не может начинаться с цифры\n- Имена чувствительны к регистру (Name и name - разные переменные)\n- Нельзя использовать зарезервированные слова Python\n\nХорошие имена: user_name, total_price, counter\nПлохие имена: x, a, temp, data',
    order=1,
    has_test=False
)
print(f'  📝 Урок 2.1: {lesson4.title}')

lesson5 = Lesson.objects.create(
    module=module2,
    title='Числа: int и float',
    content='В Python есть два основных числовых типа:\n\nint (целые числа):\nage = 25\ncount = 100\nnegative = -5\n\nfloat (дробные числа):\nprice = 19.99\ntemperature = -3.5\npi = 3.14159\n\nОперации с числами:\n+ сложение\n- вычитание\n* умножение\n/ деление\n// целочисленное деление\n% остаток от деления\n** возведение в степень\n\nПример:\na = 10\nb = 3\nprint(a + b)  # 13\nprint(a / b)  # 3.333...\nprint(a // b) # 3\nprint(a ** b) # 1000',
    order=2,
    has_test=True
)
print(f'  📝 Урок 2.2: {lesson5.title}')

# Тест для урока 5
test3 = Test.objects.create(
    lesson=lesson5,
    title='Тест: Числа в Python',
    description='Проверка знаний о числовых типах'
)

q4 = Question.objects.create(
    test=test3,
    text='Какой тип данных используется для хранения дробных чисел?',
    is_code=False,
    order=1
)
AnswerOption.objects.create(question=q4, text='float', is_correct=True)
AnswerOption.objects.create(question=q4, text='int', is_correct=False)
AnswerOption.objects.create(question=q4, text='double', is_correct=False)
AnswerOption.objects.create(question=q4, text='decimal', is_correct=False)

q5 = Question.objects.create(
    test=test3,
    text='Чему равно выражение 10 // 3 в Python?',
    is_code=False,
    order=2
)
AnswerOption.objects.create(question=q5, text='3', is_correct=True)
AnswerOption.objects.create(question=q5, text='3.333', is_correct=False)
AnswerOption.objects.create(question=q5, text='4', is_correct=False)
AnswerOption.objects.create(question=q5, text='1', is_correct=False)

print(f'  ✅ Тест создан: {test3.title} (2 вопроса)')

print()
print('🎉 Демонстрационный курс успешно создан!')
print(f'📚 Курс: {course.title}')
print(f'📖 Модулей: 2')
print(f'📝 Уроков: 5')
print(f'✅ Тестов: 3 (5 вопросов)')

# ============================================
# КУРС 2: JavaScript для веб-разработки
# ============================================

course2 = Course.objects.create(
    title='JavaScript для веб-разработки',
    slug='javascript-dlya-veb-razrabotki',
    description='Полный курс JavaScript. Изучите основы языка, работу с DOM, асинхронное программирование и создание интерактивных веб-приложений.',
    is_posted=True
)
print(f'\n✅ Курс создан: {course2.title}')

# Модуль 1: Основы JS
module3 = Module.objects.create(
    course=course2,
    name='Основы JavaScript',
    slug='osnovy-javascript',
    description='Знакомство с языком JavaScript и его основными концепциями',
    order=1
)
print(f'✅ Модуль 1: {module3.name}')

lesson6 = Lesson.objects.create(
    module=module3,
    title='Что такое JavaScript?',
    content='JavaScript - это язык программирования, используемый для создания интерактивных веб-приложений.\n\nИстория:\n- Создан в 1995 году Бренданом Айхом\n- Первоначально назывался Mocha, затем LiveScript, потом JavaScript\n- Стал стандартом ECMAScript\n\nВозможности:\n- Манипуляция с DOM (структурой страницы)\n- Обработка событий (клики, ввод, прокрутка)\n- Асинхронные операции (запросы к серверу)\n- Создание анимаций\n- Валидация форм\n\nГде используется:\n- Браузеры (клиентская часть)\n- Node.js (серверная часть)\n- Мобильные приложения (React Native, Flutter)\n- Десктопные приложения (Electron)',
    order=1,
    has_test=False
)
print(f'  📝 Урок 1.1: {lesson6.title}')

lesson7 = Lesson.objects.create(
    module=module3,
    title='Переменные и типы данных в JS',
    content='В JavaScript есть несколько способов объявления переменных:\n\nvar (старый способ):\nvar name = "Иван";\n\nlet (современный способ, блочная область):\nlet age = 25;\n\nconst (константа):\nconst PI = 3.14159;\n\nТипы данных:\n- string: "Hello"\n- number: 42, 3.14\n- boolean: true, false\n- undefined: переменная объявлена, но не инициализирована\n- null: отсутствие значения\n- object: {name: "Ivan"}\n- array: [1, 2, 3]\n\nПроверка типа:\nconsole.log(typeof 42);      // "number"\nconsole.log(typeof "hello");  // "string"\nconsole.log(typeof true);     // "boolean"',
    order=2,
    has_test=True
)
print(f'  📝 Урок 1.2: {lesson7.title}')

test4 = Test.objects.create(
    lesson=lesson7,
    title='Тест: Переменные в JavaScript',
    description='Проверка знаний о переменных и типах данных'
)

q6 = Question.objects.create(
    test=test4,
    text='Какой оператор используется для объявления константы в современном JavaScript?',
    is_code=False,
    order=1
)
AnswerOption.objects.create(question=q6, text='const', is_correct=True)
AnswerOption.objects.create(question=q6, text='let', is_correct=False)
AnswerOption.objects.create(question=q6, text='var', is_correct=False)
AnswerOption.objects.create(question=q6, text='constant', is_correct=False)

q7 = Question.objects.create(
    test=test4,
    text='Какой будет результат typeof "42"?',
    is_code=False,
    order=2
)
AnswerOption.objects.create(question=q7, text='"string"', is_correct=True)
AnswerOption.objects.create(question=q7, text='"number"', is_correct=False)
AnswerOption.objects.create(question=q7, text='42', is_correct=False)
AnswerOption.objects.create(question=q7, text='"undefined"', is_correct=False)

print(f'  ✅ Тест создан: {test4.title} (2 вопроса)')

lesson8 = Lesson.objects.create(
    module=module3,
    title='Функции в JavaScript',
    content='Функция - это переиспользуемый блок кода.\n\nОбъявление функции:\nfunction greet(name) {\n  console.log("Привет, " + name);\n}\n\nВызов функции:\ngreet("Иван");  // Привет, Иван\n\nФункции со значением по умолчанию:\nfunction multiply(a, b = 1) {\n  return a * b;\n}\n\nСтрелочные функции:\nconst add = (a, b) => a + b;\n\nВозвращение значения:\nfunction sum(a, b) {\n  return a + b;\n}\nconst result = sum(5, 3);  // 8',
    order=3,
    has_test=False
)
print(f'  📝 Урок 1.3: {lesson8.title}')

# Модуль 2: DOM и события
module4 = Module.objects.create(
    course=course2,
    name='DOM и события',
    slug='dom-i-sobytiya',
    description='Работа с DOM и обработка событий пользователя',
    order=2
)
print(f'✅ Модуль 2: {module4.name}')

lesson9 = Lesson.objects.create(
    module=module4,
    title='Что такое DOM?',
    content='DOM (Document Object Model) - это представление HTML-документа в виде дерева объектов.\n\nПримеры доступа к элементам:\n\n// По ID\nconst element = document.getElementById("myId");\n\n// По классу\nconst elements = document.getElementsByClassName("myClass");\n\n// По селектору (современный способ)\nconst element = document.querySelector("#myId");\nconst elements = document.querySelectorAll(".myClass");\n\nИзменение содержимого:\nelement.textContent = "Новый текст";\nelement.innerHTML = "<p>HTML код</p>";\n\nИзменение атрибутов:\nelement.setAttribute("class", "newClass");\nelement.id = "newId";',
    order=1,
    has_test=False
)
print(f'  📝 Урок 2.1: {lesson9.title}')

lesson10 = Lesson.objects.create(
    module=module4,
    title='Обработка событий',
    content='События - это действия пользователя (клики, ввод, прокрутка и т.д.).\n\nПрослушивание событий:\nelement.addEventListener("click", function() {\n  console.log("Элемент нажат!");\n});\n\nСтрелочная функция:\nelement.addEventListener("click", () => {\n  console.log("Элемент нажат!");\n});\n\nЧастые события:\n- click: клик мышью\n- submit: отправка формы\n- change: изменение значения в поле\n- keydown/keyup: нажатие клавиши\n- load: загрузка страницы\n- scroll: прокрутка страницы\n\nПример с формой:\nconst form = document.querySelector("form");\nform.addEventListener("submit", (e) => {\n  e.preventDefault();  // Отменить стандартное поведение\n  console.log("Форма отправлена!");\n});',
    order=2,
    has_test=True
)
print(f'  📝 Урок 2.2: {lesson10.title}')

test5 = Test.objects.create(
    lesson=lesson10,
    title='Тест: События в JavaScript',
    description='Проверка знаний о событиях'
)

q8 = Question.objects.create(
    test=test5,
    text='Какой метод используется для добавления обработчика события?',
    is_code=False,
    order=1
)
AnswerOption.objects.create(question=q8, text='addEventListener', is_correct=True)
AnswerOption.objects.create(question=q8, text='addEvent', is_correct=False)
AnswerOption.objects.create(question=q8, text='onEvent', is_correct=False)
AnswerOption.objects.create(question=q8, text='attachEvent', is_correct=False)

print(f'  ✅ Тест создан: {test5.title} (1 вопрос)')

# ============================================
# КУРС 3: SQL и базы данных
# ============================================

course3 = Course.objects.create(
    title='SQL и базы данных',
    slug='sql-i-bazy-dannykh',
    description='Изучите язык SQL для работы с базами данных. Создание таблиц, запросы SELECT, JOIN, агрегирование данных и оптимизация производительности.',
    is_posted=True
)
print(f'\n✅ Курс создан: {course3.title}')

# Модуль 1: Введение в SQL
module5 = Module.objects.create(
    course=course3,
    name='Введение в SQL',
    slug='vvedenie-v-sql',
    description='Основы SQL и работа с реляционными базами данных',
    order=1
)
print(f'✅ Модуль 1: {module5.name}')

lesson11 = Lesson.objects.create(
    module=module5,
    title='Что такое база данных?',
    content='База данных (БД) - это организованное хранилище информации.\n\nЗачем нужны БД:\n- Надёжное хранение больших объёмов данных\n- Быстрый поиск и выборка информации\n- Обеспечение целостности данных\n- Масштабируемость приложений\n\nТипы БД:\n- Реляционные (MySQL, PostgreSQL, Oracle) - таблицы с связями\n- NoSQL (MongoDB, Redis) - документы, ключ-значение\n- Графовые (Neo4j) - граф данных\n\nРеляционные БД состоят из:\n- Таблиц (структурированные данные)\n- Строк (записи)\n- Столбцов (поля)\n- Ключей (уникальные идентификаторы и связи)',
    order=1,
    has_test=False
)
print(f'  📝 Урок 1.1: {lesson11.title}')

lesson12 = Lesson.objects.create(
    module=module5,
    title='Основные SQL команды',
    content='SQL - язык для работы с БД.\n\nСоздание таблицы:\nCREATE TABLE users (\n  id INT PRIMARY KEY AUTO_INCREMENT,\n  name VARCHAR(100),\n  email VARCHAR(100),\n  age INT\n);\n\nВставка данных:\nINSERT INTO users (name, email, age)\nVALUES ("Иван", "ivan@example.com", 25);\n\nВыборка данных:\nSELECT * FROM users;\nSELECT name, email FROM users WHERE age > 20;\n\nОбновление данных:\nUPDATE users SET age = 26 WHERE name = "Иван";\n\nУдаление данных:\nDELETE FROM users WHERE id = 1;',
    order=2,
    has_test=True
)
print(f'  📝 Урок 1.2: {lesson12.title}')

test6 = Test.objects.create(
    lesson=lesson12,
    title='Тест: SQL команды',
    description='Проверка знаний об основных SQL операциях'
)

q9 = Question.objects.create(
    test=test6,
    text='Какая команда используется для создания таблицы?',
    is_code=False,
    order=1
)
AnswerOption.objects.create(question=q9, text='CREATE TABLE', is_correct=True)
AnswerOption.objects.create(question=q9, text='NEW TABLE', is_correct=False)
AnswerOption.objects.create(question=q9, text='MAKE TABLE', is_correct=False)
AnswerOption.objects.create(question=q9, text='INSERT TABLE', is_correct=False)

q10 = Question.objects.create(
    test=test6,
    text='Какая команда используется для обновления данных?',
    is_code=False,
    order=2
)
AnswerOption.objects.create(question=q10, text='UPDATE', is_correct=True)
AnswerOption.objects.create(question=q10, text='MODIFY', is_correct=False)
AnswerOption.objects.create(question=q10, text='CHANGE', is_correct=False)
AnswerOption.objects.create(question=q10, text='ALTER', is_correct=False)

print(f'  ✅ Тест создан: {test6.title} (2 вопроса)')

lesson13 = Lesson.objects.create(
    module=module5,
    title='WHERE и фильтрация',
    content='Предложение WHERE используется для фильтрации данных.\n\nПримеры:\n\n-- Равенство\nSELECT * FROM users WHERE age = 25;\n\n-- Сравнение\nSELECT * FROM users WHERE age > 20;\nSELECT * FROM users WHERE age < 30;\nSELECT * FROM users WHERE age >= 18;\n\n-- Логические операторы\nSELECT * FROM users WHERE age > 20 AND city = "Moscow";\nSELECT * FROM users WHERE age > 20 OR city = "SPB";\nSELECT * FROM users WHERE NOT age = 25;\n\n-- IN (в списке значений)\nSELECT * FROM users WHERE city IN ("Moscow", "SPB", "KZN");\n\n-- LIKE (поиск по образцу)\nSELECT * FROM users WHERE name LIKE "И%";  -- Начинается с И',
    order=3,
    has_test=False
)
print(f'  📝 Урок 1.3: {lesson13.title}')

# Модуль 2: JOIN и агрегирование
module6 = Module.objects.create(
    course=course3,
    name='JOIN и агрегирование',
    slug='join-i-agregirovanie',
    description='Объединение таблиц и агрегирование данных',
    order=2
)
print(f'✅ Модуль 2: {module6.name}')

lesson14 = Lesson.objects.create(
    module=module6,
    title='JOIN - объединение таблиц',
    content='JOIN позволяет объединить данные из нескольких таблиц.\n\nТипы JOIN:\n\nINNER JOIN (пересечение):\nSELECT users.name, orders.total\nFROM users\nINNER JOIN orders ON users.id = orders.user_id;\n\nLEFT JOIN (все из левой таблицы):\nSELECT users.name, orders.total\nFROM users\nLEFT JOIN orders ON users.id = orders.user_id;\n\nRIGHT JOIN (все из правой таблицы):\nSELECT users.name, orders.total\nFROM users\nRIGHT JOIN orders ON users.id = orders.user_id;\n\nFULL OUTER JOIN (все данные):\nSELECT users.name, orders.total\nFROM users\nFULL OUTER JOIN orders ON users.id = orders.user_id;',
    order=1,
    has_test=False
)
print(f'  📝 Урок 2.1: {lesson14.title}')

lesson15 = Lesson.objects.create(
    module=module6,
    title='Агрегирующие функции',
    content='Агрегирующие функции обрабатывают множество значений и возвращают одно.\n\nОсновные функции:\n\nCOUNT() - подсчёт строк:\nSELECT COUNT(*) FROM users;\nSELECT COUNT(email) FROM users;\n\nSUM() - сумма:\nSELECT SUM(total) FROM orders;\n\nAVG() - среднее значение:\nSELECT AVG(age) FROM users;\n\nMAX() / MIN() - максимум / минимум:\nSELECT MAX(salary) FROM employees;\nSELECT MIN(age) FROM users;\n\nГруппировка (GROUP BY):\nSELECT city, COUNT(*) as count\nFROM users\nGROUP BY city;\n\nФильтрация групп (HAVING):\nSELECT city, COUNT(*) as count\nFROM users\nGROUP BY city\nHAVING COUNT(*) > 5;',
    order=2,
    has_test=True
)
print(f'  📝 Урок 2.2: {lesson15.title}')

test7 = Test.objects.create(
    lesson=lesson15,
    title='Тест: Агрегирование',
    description='Проверка знаний о GROUP BY и агрегирующих функциях'
)

q11 = Question.objects.create(
    test=test7,
    text='Какая функция используется для подсчёта количества строк?',
    is_code=False,
    order=1
)
AnswerOption.objects.create(question=q11, text='COUNT()', is_correct=True)
AnswerOption.objects.create(question=q11, text='SUM()', is_correct=False)
AnswerOption.objects.create(question=q11, text='TOTAL()', is_correct=False)
AnswerOption.objects.create(question=q11, text='NUMBER()', is_correct=False)

print(f'  ✅ Тест создан: {test7.title} (1 вопрос)')

print()
print('🎉 ВСЕ ДЕМОНСТРАЦИОННЫЕ КУРСЫ СОЗДАНЫ!')
print()
print('📚 Курс 1: Python для начинающих')
print('   📖 Модулей: 2 | 📝 Уроков: 5 | ✅ Тестов: 3')
print()
print('📚 Курс 2: JavaScript для веб-разработки')
print('   📖 Модулей: 2 | 📝 Уроков: 5 | ✅ Тестов: 2')
print()
print('📚 Курс 3: SQL и базы данных')
print('   📖 Модулей: 2 | 📝 Уроков: 5 | ✅ Тестов: 2')
print()
print('📊 ИТОГО: 3 курса | 6 модулей | 15 уроков | 7 тестов')
