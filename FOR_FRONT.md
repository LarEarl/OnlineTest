# FOR_FRONT.md - Backend API Documentation

## 📚 Оглавление
- [Общая информация](#общая-информация)
- [Аутентификация](#аутентификация)
- [Users API](#users-api)
- [Courses API](#courses-api)
- [Tests API](#tests-api)
- [Модели данных](#модели-данных)

---

## Общая информация

### Base URL
```
http://localhost:8000/
```

### Аутентификация
Используется **Session Authentication** (Django sessions).
- После логина создается сессия
- Cookie с `sessionid` автоматически отправляется с каждым запросом
- Для защищенных endpoint'ов требуется `@login_required`

### CSRF Protection
Все POST/PUT/DELETE запросы требуют CSRF token:
```javascript
// Получить token из cookie
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

// Или из cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
```

---

## Users API

### 1. Register (Регистрация)

**Endpoint:** `POST /users/register/`

**Описание:** Регистрация нового пользователя. После регистрации пользователь неактивен до верификации email.

**Request Body (form-data):**
```
username: string (required)
email: string (required, email format)
password1: string (required, min 8 characters)
password2: string (required, must match password1)
```

**Success Response:**
- Redirect → `/users/verify/`
- Отправляется email с кодом верификации

**Error Response:**
```html
HTML форма с ошибками валидации
```

---

### 2. Verify Email (Верификация)

**Endpoint:** `POST /users/verify/`

**Описание:** Подтверждение email через код из письма.

**Request Body (form-data):**
```
email: string (required)
code: string (required, 6 digits)
```

**Success Response:**
- Пользователь активируется
- Автоматический login
- Redirect → `/users/profile/`

**Error Response:**
```html
HTML с сообщением об ошибке:
- "Пользователь с таким email не найден"
- "Код верификации не найден или истек"
- "Код неверный"
```

---

### 3. Login (Вход)

**Endpoint:** `POST /users/login/`

**Описание:** Вход в систему по username/email и паролю.

**Request Body (form-data):**
```
identifier: string (username или email)
password: string
remember_me: boolean (optional)
next: string (optional, redirect URL)
```

**Success Response:**
- Session создана
- Redirect → `next` URL или `/users/profile/`

**Error Response:**
```html
HTML с ошибкой:
- "Аккаунт не активирован. Подтвердите email."
- "Неверные данные для входа."
```

---

### 4. Logout (Выход)

**Endpoint:** 
- `GET /users/logout/` - показать страницу подтверждения
- `POST /users/logout/` - выполнить выход

**Success Response:**
- Session уничтожена
- Redirect → `/users/login/`

---

### 5. Profile (Профиль)

**Endpoint:** `GET /users/profile/`

**Auth Required:** ✅ Yes

**Success Response:**
```html
HTML страница с данными пользователя
```

---

### 6. Profile Edit (Редактирование профиля)

**Endpoint:** 
- `GET /users/profile/edit/` - форма редактирования
- `POST /users/profile/edit/` - сохранить изменения

**Auth Required:** ✅ Yes

**Request Body (form-data + files):**
```
username: string (optional)
email: string (optional)
first_name: string (optional)
last_name: string (optional)
avatar: file (optional, image)
```

**Success Response:**
- Redirect → `/users/profile/`

---

### 7. Password Change

**Endpoint:** `POST /users/password-change/`

**Auth Required:** ✅ Yes

**Request Body (form-data):**
```
old_password: string
new_password1: string
new_password2: string
```

**Success Response:**
- Redirect → `/users/profile/`

---

## Courses API

### 1. All Courses (Список курсов)

**Endpoint:** `GET /courses/all_cources/`

**Auth Required:** ❌ No

**Success Response:**
```html
HTML страница со списком всех опубликованных курсов
```

**Context Data:**
```python
{
    'cources': [
        {
            'id': int,
            'title': string,
            'description': string,
            'image': ImageField,
            'slug': string,
            'is_posted': boolean,
            'created_at': datetime
        },
        ...
    ]
}
```

---

### 2. Course Modules (Модули курса)

**Endpoint:** `GET /courses/modules/<course_slug>/`

**Auth Required:** ✅ Yes

**URL Parameters:**
- `course_slug` - slug курса (например: "python-basics")

**Success Response:**
```html
HTML страница с модулями курса
```

**Context Data:**
```python
{
    'open_moduls': [
        {
            'module': Module,  # объект модуля
            'progress': ModuleProgress,  # прогресс пользователя
            'is_open': boolean  # доступен ли модуль
        },
        ...
    ]
}
```

**Логика открытия:**
- Первый модуль (order=0) всегда открыт
- Следующие открываются только если предыдущий разблокирован (`progress.is_unlocked`)
- Список обрывается на первом закрытом модуле

---

### 3. Module Lessons (Уроки модуля)

**Endpoint:** `GET /courses/lessons/<modul_slug>/`

**Auth Required:** ✅ Yes

**URL Parameters:**
- `modul_slug` - slug модуля

**Success Response:**
```html
HTML страница с уроками модуля
```

**Context Data:**
```python
{
    'open_lessons': [
        {
            'lesson': Lesson,  # объект урока
            'progress': LessonProgress,  # прогресс
            'is_open': boolean  # всегда True
        },
        ...
    ]
}
```

**Логика:**
- Показываются уроки до первого незавершенного
- Если урок не завершен (`progress.is_completed = False`), список обрывается

---

### 4. Lesson Detail (Детали урока)

**Endpoint:** `GET /courses/lesson/<lesson_id>/`

**Auth Required:** ✅ Yes

**URL Parameters:**
- `lesson_id` - ID урока

**Success Response:**
```html
HTML страница с содержимым урока
```

**Context Data:**
```python
{
    'lesson': {
        'id': int,
        'title': string,
        'content': text,
        'video_url': string (nullable),
        'has_test': boolean,
        'module': Module,
        'order': int
    }
}
```

---

## Tests API

### 1. Lesson Test (Показать вопрос теста)

**Endpoint:** `GET /tests_app/lesson_test/<lesson_id>/<question_order>/`

**Auth Required:** ❌ No (можно добавить)

**URL Parameters:**
- `lesson_id` - ID урока
- `question_order` - порядковый номер вопроса (1, 2, 3...)

**Success Response:**
```html
HTML страница с вопросом
```

**Context Data:**
```python
{
    'question': {
        'id': int,
        'text': string,
        'is_code': boolean,
        'order': int,
        'test': Test,
        'options': [AnswerOption, ...],  # если quiz
        'code_cases': [CodeTestCase, ...]  # если code
    }
}
```

---

### 2. Answer Quiz Question (Ответить на тест)

**Endpoint:** `POST /tests_app/answer_question/<question_id>/`

**Auth Required:** ✅ Yes

**Content-Type:** `application/x-www-form-urlencoded`

**URL Parameters:**
- `question_id` - ID вопроса

**Request Body:**
```
user_answer: int (ID выбранного AnswerOption)
```

**Request Headers:**
```
X-CSRFToken: <csrf_token>
```

**Success Response:**
```json
{
    "message": "Верный ответ!",
    "answer": true
}
```

**Error Response:**
```json
{
    "message": "Ответ не верный",
    "answer": false
}
```

**Example:**
```javascript
fetch('/tests_app/answer_question/5/', {
    method: 'POST',
    headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: 'user_answer=12'
})
.then(response => response.json())
.then(data => {
    console.log(data.message); // "Верный ответ!"
    console.log(data.answer);  // true
});
```

---

### 3. Submit Code (Отправить код на проверку)

**Endpoint:** `POST /tests_app/answer_code/<question_id>/`

**Auth Required:** ✅ Yes

**Content-Type:** `application/x-www-form-urlencoded`

**URL Parameters:**
- `question_id` - ID вопроса

**Request Body:**
```
code: string (Python код, URL encoded)
```

**Request Headers:**
```
X-CSRFToken: <csrf_token>
```

**Success Response:**
```json
{
    "message": "Код успешно отправился на проверку",
    "status": "pending",
    "attempt_id": 123
}
```

**Example:**
```javascript
const code = `print("Hello, World!")`;

fetch('/tests_app/answer_code/8/', {
    method: 'POST',
    headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: `code=${encodeURIComponent(code)}`
})
.then(response => response.json())
.then(data => {
    console.log(data.attempt_id); // 123
    // Начать polling статуса
    checkStatus(data.attempt_id);
});
```

---

### 4. Check Code Status (Проверить статус выполнения)

**Endpoint:** `GET /tests_app/code_status/<code_attemp_id>/`

**Auth Required:** ❌ No (но лучше добавить)

**URL Parameters:**
- `code_attemp_id` - ID попытки выполнения кода (из answer_code response)

**Success Response:**
```json
{
    "status": "success",  // "pending" | "running" | "success" | "failed"
    "is_correct": true,   // true | false | null
    "stdout": "Hello, World!\n",
    "stderr": ""
}
```

**Polling Example:**
```javascript
function checkCodeStatus(attemptId) {
    const interval = setInterval(() => {
        fetch(`/tests_app/code_status/${attemptId}/`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success' || data.status === 'failed') {
                    clearInterval(interval);
                    
                    if (data.is_correct) {
                        alert('✅ Код выполнен успешно!');
                    } else {
                        alert('❌ Ошибка: ' + data.stderr);
                    }
                }
            });
    }, 2000); // каждые 2 секунды
}
```

---

### 5. Finish Test (Завершить тест)

**Endpoint:** `POST /tests_app/finish_test/<question_id>/`

**Auth Required:** ✅ Yes

**Content-Type:** `application/json`

**URL Parameters:**
- `question_id` - ID любого вопроса из теста (используется для получения Test)

**Request Headers:**
```
X-CSRFToken: <csrf_token>
Content-Type: application/json
```

**Success Response:**
```json
{
    "message": "Поздравляем! Тест пройден (3/3)!",
    "status": "success"
}
```

**Error Response:**
```json
{
    "message": "Тест не пройден. Правильных ответов: 2/3",
    "status": "failed"
}
```

**Логика проверки:**
- Проверяет **ВСЕ** вопросы теста
- Для quiz вопросов: берет `AnswerAttempt`
- Для code вопросов: берет последнюю успешную попытку (`status='success'`)
- Если все вопросы правильные → вызывается `complete_lesson()` → урок помечается как завершенный

**Example:**
```javascript
const questionId = 10; // последний вопрос теста

fetch(`/tests_app/finish_test/${questionId}/`, {
    method: 'POST',
    headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/json',
    }
})
.then(response => response.json())
.then(data => {
    alert(data.message);
    if (data.status === 'success') {
        window.location.href = '/courses/all_cources/';
    }
});
```

---

## Модели данных

### User
```python
{
    'id': int,
    'username': string,
    'email': string,
    'first_name': string,
    'last_name': string,
    'avatar': ImageField,
    'is_active': boolean,
    'date_joined': datetime
}
```

### Course
```python
{
    'id': int,
    'title': string,
    'description': text,
    'image': ImageField,
    'slug': string,
    'is_posted': boolean,
    'created_at': datetime
}
```

### Module
```python
{
    'id': int,
    'course': ForeignKey(Course),
    'name': string,
    'description': text,
    'slug': string,
    'order': int
}
```

### Lesson
```python
{
    'id': int,
    'module': ForeignKey(Module),
    'title': string,
    'content': text,
    'video_url': string (nullable),
    'order': int,
    'has_test': boolean,
    'created_at': datetime
}
```

### Test
```python
{
    'id': int,
    'lesson': ForeignKey(Lesson),
    'title': string,
    'description': text
}
```

### Question
```python
{
    'id': int,
    'test': ForeignKey(Test),
    'text': text,
    'is_code': boolean,  # True = code question, False = quiz
    'order': int
}
```

### AnswerOption
```python
{
    'id': int,
    'question': ForeignKey(Question),
    'text': string,
    'is_correct': boolean
}
```

### CodeTestCase
```python
{
    'id': int,
    'question': ForeignKey(Question),
    'input_data': text,
    'expected_output': text,
    'time_limit': float  # seconds
}
```

### LessonProgress
```python
{
    'id': int,
    'user': ForeignKey(User),
    'lesson': ForeignKey(Lesson),
    'is_completed': boolean,
    'completed_at': datetime (nullable)
}
```

### ModuleProgress
```python
{
    'id': int,
    'user': ForeignKey(User),
    'module': ForeignKey(Module),
    'is_unlocked': boolean,
    'completed_lessons_count': int,
    'completed_at': datetime (nullable)
}
```

### AnswerAttempt
```python
{
    'id': int,
    'user': ForeignKey(User),
    'question': ForeignKey(Question),
    'selected_options': ManyToManyField(AnswerOption),
    'text_answer': text,
    'is_correct': boolean,
    'created_at': datetime
}
```

### CodeAttempt
```python
{
    'id': int,
    'user': ForeignKey(User),
    'question': ForeignKey(Question),
    'code': text,
    'status': string,  # "pending" | "running" | "success" | "failed"
    'is_correct': boolean (nullable),
    'stdout': text,
    'stderr': text,
    'created_at': datetime,
    'finished_at': datetime (nullable)
}
```

---

## Важные замечания

### 1. Множественные попытки кода
Пользователь может отправлять код **много раз**. Каждая отправка создает новый `CodeAttempt`. При проверке теста берется **последняя успешная** попытка.

### 2. Один ответ на quiz
Для quiz вопросов используется `get_or_create` - пользователь может ответить только один раз.

### 3. Docker timeout
- По умолчанию `time_limit` из `CodeTestCase`
- Добавляется +3 секунды на запуск Docker контейнера
- Если код не выполнился за это время → timeout error

### 4. Прогресс пользователя
- Модули открываются последовательно
- Уроки показываются до первого незавершенного
- Урок завершается при успешном прохождении теста (`finish_test`)

### 5. Media files
Доступны по пути `/media/<path>` (только в DEBUG режиме)

---

## Quick Start для фронтенда

### 1. Регистрация и вход
```javascript
// 1. Регистрация
const formData = new FormData();
formData.append('username', 'testuser');
formData.append('email', 'test@example.com');
formData.append('password1', 'strongpass123');
formData.append('password2', 'strongpass123');

fetch('/users/register/', {
    method: 'POST',
    body: formData
});

// 2. Верификация (код из email)
const verifyData = new FormData();
verifyData.append('email', 'test@example.com');
verifyData.append('code', '123456');

fetch('/users/verify/', {
    method: 'POST',
    body: verifyData
});

// После верификации пользователь автоматически залогинен
```

### 2. Прохождение курса
```javascript
// 1. Получить список курсов
window.location.href = '/courses/all_cources/';

// 2. Открыть модули курса
window.location.href = '/courses/modules/python-basics/';

// 3. Открыть уроки модуля
window.location.href = '/courses/lessons/python-fundamentals/';

// 4. Открыть урок
window.location.href = '/courses/lesson/1/';

// 5. Начать тест
window.location.href = '/tests_app/lesson_test/1/1/';
```

### 3. Прохождение теста
```javascript
// Quiz вопрос
fetch('/tests_app/answer_question/5/', {
    method: 'POST',
    headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: 'user_answer=12'
})
.then(r => r.json())
.then(data => console.log(data.answer));

// Code вопрос
fetch('/tests_app/answer_code/8/', {
    method: 'POST',
    headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: `code=${encodeURIComponent(code)}`
})
.then(r => r.json())
.then(data => {
    // Polling статуса
    const interval = setInterval(() => {
        fetch(`/tests_app/code_status/${data.attempt_id}/`)
            .then(r => r.json())
            .then(status => {
                if (status.status === 'success' || status.status === 'failed') {
                    clearInterval(interval);
                    console.log('Результат:', status.is_correct);
                }
            });
    }, 2000);
});

// Завершить тест
fetch('/tests_app/finish_test/10/', {
    method: 'POST',
    headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/json',
    }
})
.then(r => r.json())
.then(data => console.log(data.message));
```

---

## Полезные ссылки

- **Admin Panel:** http://localhost:8000/admin/
- **Courses:** http://localhost:8000/courses/all_cources/
- **Profile:** http://localhost:8000/users/profile/
- **Login:** http://localhost:8000/users/login/
