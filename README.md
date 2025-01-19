# Разработка системы
## 1. Концепция информационной системы
Концепция системы: Автоматизированный экзаменационный терминал
Описание: система предназначена для проведения тестирования знаний студентов. 
Она автоматизирует процесс экзаменов, обеспечивает объективность оценки, хранение результатов и удобство администрирования тестов.

## 2. Функциональные требования

Система предназначена для проведения автоматизированного тестирования знаний студентов и управления процессом экзаменов преподавателями. В ней реализованы следующие функциональные модули:

---

### 2.1 Регистрация и авторизация

#### Пользовательские роли:
- **Студенты:** могут просматривать доступные тесты, запускать тесты, сохранять прогресс и просматривать свои результаты.
- **Преподаватели:** создают тесты, добавляют вопросы, активируют доступ к тестам для студентов, анализируют результаты.

#### Основные функции:
- Регистрация новых пользователей.
- Авторизация через логин и пароль.
- Разделение ролей и проверка прав доступа.

---

### 2.2 Управление курсами

#### Курсы:
- Преподаватели создают курсы.
- Студенты видят доступные курсы, к которым они подключены.

#### Основные функции:
- Создание и редактирование курсов.
- Привязка студентов к курсу.
- Привязка тестов к курсу.

---

### 2.3 Управление тестами

#### Основные функции:
1. **Создание тестов:**
   - Преподаватели создают тесты, задают название, тайм-лимит, и при необходимости устанавливают сроки выполнения.

2. **Добавление вопросов:**
   - Возможность добавлять текстовые вопросы.
   - Указание вариантов ответов и правильного ответа.

3. **Активация доступа:**
   - Преподаватель активирует тест для студентов, задавая дедлайн.

4. **Запуск и завершение:**
   - Студенты могут запускать активные тесты.
   - Система автоматически завершает тест по истечении времени или при завершении студентом.

---

### 2.4 Прохождение тестов

#### Основные функции:
1. **Просмотр доступных тестов:**
   - Студент видит список активных тестов, доступных для прохождения.

2. **Запуск теста:**
   - При запуске теста начинается отсчет времени.
   - Система фиксирует ответы студента в режиме реального времени.

3. **Завершение теста:**
   - Система сравнивает ответы студента с правильными.
   - Сохраняет результаты в базу данных.

---

### 2.5 Анализ результатов

#### Основные функции:
1. **Сохранение результатов:**
   - Результаты тестирования сохраняются в базу данных.
   - Включают количество правильных ответов.

2. **Просмотр преподавателем:**
   - Преподаватели могут видеть статистику по студентам.
   - Возможность выгрузки отчетов.

3. **Просмотр студентом:**
   - Студенты могут видеть свои результаты после завершения теста.

## 3. Архитектура системы
Система предназначена для проведения автоматизированного тестирования знаний студентов и управления процессом экзаменов преподавателями. В ней реализованы следующие функциональные модули:

![архитектура2](https://github.com/user-attachments/assets/5dafb444-82ac-4c63-8a0c-842c72f43e20)
---
### Backend (Серверная часть)
Backend обрабатывает все бизнес-логически операции и взаимодействует с базой данных через API.
- **Фреймворк:** FastAPI (Python).
- **Основные функции:**
  - Реализация REST API.
  - Управление пользователями (регистрация, авторизация, роли).
  - CRUD-операции для тестов, вопросов и курсов.
  - Управление прогрессом тестов (запуск, завершение, сохранение результатов).
  - Проверка ответов студентов и расчет результатов тестирования.

##### Основные модули:
- **Авторизация:** Реализуется с использованием `pyjwt` и `bcrypt` для хэширования паролей и работы с JWT-токенами.
- **Работа с базой данных:** `SQLAlchemy` для взаимодействия с PostgreSQL, `asyncpg` для асинхронного соединения.
- **Обработка тестов:** Создание, управление и завершение тестов.
- **API эндпоинты:** REST API для взаимодействия с клиентом.

##### Основные зависимости:
- **FastAPI:** Фреймворк для разработки API.
- **Alembic:** Для миграции базы данных.
- **Pydantic:** Для валидации данных и использования моделей.
- **Python-dotenv:** Для работы с конфигурацией через `.env` файлы.

![bd](https://github.com/user-attachments/assets/f19efeec-6a07-4623-bece-23ebf28330e3)
### База данных (Data Layer)**
Реляционная база данных используется для хранения всей информации о пользователях, тестах, курсах, результатах тестирования и связанных данных.
- **СУБД:** PostgreSQL или MySQL.
- **Основные таблицы:**
  - **`users`**: Хранение данных о пользователях (логин, пароль, роль).
  - **`profile`**: Информация о профиле пользователей (имя, возраст, email).
  - **`courses`**: Список курсов, привязанных к преподавателям.
  - **`tests`**: Список тестов с параметрами (название, тайм-лимит, статус).
  - **`questions`**: Список вопросов с текстом, вариантами ответов и правильным ответом.
  - **`test_progress`**: Хранение данных о прогрессе тестов студентов.

### Технологический стек

#### Backend:
- **FastAPI:** Фреймворк для создания REST API.
- **SQLAlchemy:** Для работы с базой данных.
- **Alembic:** Миграции схем базы данных.
- **asyncpg:** Асинхронное соединение с PostgreSQL.
- **bcrypt:** Хэширование паролей.
- **pyjwt:** Генерация и проверка JWT-токенов.

#### DevTools:
- **pytest:** Для юнит-тестирования.
- **pytest-asyncio:** Тестирование асинхронных функций.
- **black:** Форматирование кода.


## 3.1 Внутреннее устройство модуля системы, который будет тестироваться

В модуле будут тестироваться две основные сущности: **`Test`** и **`TestProgress`**. Эти сущности отвечают за управление тестами, прохождение тестов, сохранение прогресса студентов и фиксацию результатов.

---

### Входные данные модуля

1. **`Test`**:
   - `name`: Название теста.
   - `time_limit`: Время, отведенное на прохождение теста (в минутах).
   - `creator_id`: ID преподавателя, создавшего тест.
   - `questions`: Список вопросов, связанных с тестом.

2. **`TestProgress`**:
   - `test_id`: ID теста, который проходит студент.
   - `participant_id`: ID студента, проходящего тест.
   - `created_at`: Дата создания прогресса теста.
   - `status`: Текущий статус прохождения теста (готов, начат, закончен, просрочено).
   - `deadline_date`: Дата окончания доступности теста.
   - `attempt_date`: Время начала попытки.
   - `timelimit`: Таймер для текущей попытки теста.
   - `count_current_answer`: Количество ответов, уже предоставленных студентом.
   - `result_test`: Результаты ответов студента (список связанных объектов `TestProgressResult`).

3. **`TestProgressResult`**:
   - `test_progress_id`: ID текущего прогресса теста.
   - `text_question`: Текст вопроса.
   - `options`: Массив вариантов ответа.
   - `correct_answer`: Правильный ответ на вопрос.
   - `student_answer`: Ответ, предоставленный студентом.

---

### Основные задачи модуля

#### 1. Управление тестами (сущность `Test`):
- Создание теста с указанием времени и вопросов.
- Связь теста с курсами.
- Доступ к списку вопросов, связанных с тестом.

#### 2. Управление прогрессом теста (сущность `TestProgress`):
- Создание прогресса теста при начале попытки.
- Отслеживание текущего статуса (готов, начат, завершен, просрочен).
- Сохранение времени начала теста.
- Фиксация ответов студента в реальном времени.

#### 3. Сохранение результатов (сущность `TestProgressResult`):
- Хранение вопросов и вариантов ответов.
- Сохранение правильного и предоставленного ответа.
- Генерация итогового результата (процент правильных ответов).

---

### Алгоритм работы модуля

1. **Создание теста:**
   - Преподаватель через API создает тест, указывая название и время.
   - Тест сохраняется в таблице `Test`, и вопросы привязываются к тесту через `TestQuestionAssociation`.

2. **Получение доступа для прохождения теста**
   - Преподаватель активирует доступ до теста, указывая лимит и дедлайн для его прохождения

3. **Запуск теста:**
   - Студент инициирует прохождение теста.
   - В таблице `TestProgress` создается запись с текущей датой, статусом "начат" и привязкой к тесту.
   - Система фиксирует таймер и отслеживает оставшееся время.

4. **Процесс прохождения теста:**
   - При ответе студента на вопрос:
     - Ответ сохраняется в `TestProgressResult`.
     - Поле `count_current_answer` в `TestProgress` обновляется.
   - После завершения:
     - Сравниваются правильные и предоставленные ответы.
     - Результат сохраняется в таблице `TestProgress`.

5. **Завершение теста:**
   - Если время истекло или студент завершил тест:
     - Статус обновляется на "завершен" или "просрочен".
     - Итоговые результаты сохраняются.
