// AJAX обработчик для Quiz вопросов
document.addEventListener('DOMContentLoaded', function () {
    // Quiz форма
    const quizForm = document.getElementById('quiz-form');
    if (quizForm) {
        quizForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const questionId = this.dataset.questionId;
            const formData = new FormData(this);
            const csrfToken = formData.get('csrfmiddlewaretoken');
            const userAnswer = formData.get('user_answer');

            if (!userAnswer) {
                alert('Пожалуйста, выберите ответ!');
                return;
            }

            // Отправляем AJAX запрос
            fetch(`/tests_app/answer_question/${questionId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `user_answer=${userAnswer}`
            })
                .then(response => response.json())
                .then(data => {
                    const resultDiv = document.getElementById('quiz-result');
                    resultDiv.style.display = 'block';
                    resultDiv.textContent = data.message;

                    if (data.answer) {
                        resultDiv.className = 'result-message result-success';
                    } else {
                        resultDiv.className = 'result-message result-error';
                    }

                    // Отключаем форму после ответа
                    quizForm.querySelectorAll('input').forEach(input => input.disabled = true);
                    quizForm.querySelector('button[type="submit"]').disabled = true;
                })
                .catch(error => {
                    console.error('Error:', error);
                    const resultDiv = document.getElementById('quiz-result');
                    resultDiv.style.display = 'block';
                    resultDiv.textContent = 'Произошла ошибка. Попробуйте снова.';
                    resultDiv.className = 'result-message result-error';
                });
        });
    }

    // Code форма
    const codeForm = document.getElementById('code-form');
    if (codeForm) {
        codeForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const questionId = this.dataset.questionId;
            const formData = new FormData(this);
            const csrfToken = formData.get('csrfmiddlewaretoken');
            const code = formData.get('code');

            if (!code || code.trim() === '') {
                alert('Пожалуйста, введите код!');
                return;
            }

            // Показываем индикатор загрузки
            const resultDiv = document.getElementById('code-result');
            resultDiv.style.display = 'block';
            resultDiv.className = 'result-message result-info';
            document.getElementById('status-text').textContent = 'Отправка кода...';
            document.querySelector('.spinner').style.display = 'block';

            // Отправляем код на проверку
            fetch(`/tests_app/answer_code/${questionId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `code=${encodeURIComponent(code)}`
            })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('status-text').textContent = data.message;

                    // Начинаем проверять статус используя attempt_id
                    if (data.attempt_id) {
                        checkCodeStatusById(data.attempt_id);
                    }

                    // Отключаем форму
                    codeForm.querySelectorAll('textarea').forEach(textarea => textarea.disabled = true);
                    document.getElementById('submit-code-btn').disabled = true;

                    // Показываем кнопку редактирования
                    document.getElementById('reedit-code-btn').style.display = 'inline-block';
                })
                .catch(error => {
                    console.error('Error:', error);
                    document.getElementById('status-text').textContent = 'Ошибка отправки кода';
                    resultDiv.className = 'result-message result-error';
                    document.querySelector('.spinner').style.display = 'none';
                });
        });
    }

    // Кнопка для повторного редактирования кода
    const reeditBtn = document.getElementById('reedit-code-btn');
    if (reeditBtn) {
        reeditBtn.addEventListener('click', function () {
            // Включаем textarea и кнопку отправки
            document.getElementById('code-input').disabled = false;
            document.getElementById('submit-code-btn').disabled = false;

            // Скрываем результаты и кнопку редактирования
            document.getElementById('code-result').style.display = 'none';
            this.style.display = 'none';

            // Очищаем результаты
            document.getElementById('stdout-container').innerHTML = '';
            document.getElementById('stderr-container').innerHTML = '';
        });
    }

    // Кнопка завершения теста
    const finishTestBtn = document.getElementById('finish-test-btn');
    if (finishTestBtn) {
        finishTestBtn.addEventListener('click', function () {
            if (confirm('Вы уверены, что хотите завершить тест?')) {
                const questionId = this.dataset.questionId;
                // Отправляем запрос на завершение теста
                // URL можно указать любой, пользователь сам разберется
                
                fetch(`/tests_app/finish_test/${questionId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                        'Content-Type': 'application/json',
                    },
                })
                    .then(response => response.json())
                    .then(data => {
                        alert(data.message);
                        
                        // Если курс завершен, сохраняем в sessionStorage для показа достижения
                        if (data.course_completed) {
                            sessionStorage.setItem('completedCourse', data.course_name);
                        }
                        
                        // Перенаправляем на страницу прогресса, если курс завершен, иначе на курсы
                        if (data.course_completed) {
                            window.location.href = '/progress/my/';
                        } else {
                            window.location.href = '/courses/';
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert('Произошла ошибка при завершении теста');
                    });
            }
        });
    }
});

// Функция для проверки статуса выполнения кода
function checkCodeStatus(questionId) {
    // Получаем последнюю попытку пользователя для этого вопроса
    // В реальном приложении ID попытки должен возвращаться из answer_code
    // Пока используем упрощенный подход - опрашиваем endpoint каждые 2 секунды

    const maxAttempts = 30; // Максимум 60 секунд ожидания
    let attempts = 0;

    const statusInterval = setInterval(function () {
        attempts++;

        if (attempts > maxAttempts) {
            clearInterval(statusInterval);
            document.getElementById('status-text').textContent = 'Превышено время ожидания';
            document.querySelector('.spinner').style.display = 'none';
            return;
        }

        // Здесь нужно получить code_attempt_id
        // Для демонстрации используем заглушку
        // В реальном приложении answer_code должен возвращать code_attempt_id

        document.getElementById('status-text').textContent = 'Проверка кода... (' + attempts + ')';

    }, 2000);
}

// Улучшенная функция проверки с ID попытки
function checkCodeStatusById(attemptId) {
    const statusInterval = setInterval(function () {
        fetch(`/tests_app/code_status/${attemptId}/`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('status-text').textContent = `Статус: ${data.status}`;

                if (data.status === 'success' || data.status === 'failed') {
                    clearInterval(statusInterval);
                    document.querySelector('.spinner').style.display = 'none';

                    const resultDiv = document.getElementById('code-result');
                    const outputDiv = document.getElementById('execution-output');
                    outputDiv.style.display = 'block';

                    if (data.is_correct) {
                        resultDiv.className = 'result-message result-success';
                        document.getElementById('status-text').textContent = 'Код выполнен успешно!';
                    } else {
                        resultDiv.className = 'result-message result-error';
                        document.getElementById('status-text').textContent = '❌ Код содержит ошибки';
                    }

                    // Отображаем вывод
                    if (data.stdout) {
                        document.getElementById('stdout-container').innerHTML =
                            '<strong>Вывод программы:</strong><br>' + escapeHtml(data.stdout);
                    }

                    if (data.stderr) {
                        document.getElementById('stderr-container').innerHTML =
                            '<strong>Ошибки:</strong><br>' + escapeHtml(data.stderr);
                    }
                }
            })
            .catch(error => {
                console.error('Status check error:', error);
                clearInterval(statusInterval);
            });
    }, 2000);
}

// Экранирование HTML
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, function (m) { return map[m]; });
}
