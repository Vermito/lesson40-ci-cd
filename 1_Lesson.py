""" CI/CD c GitHub Actions
На предыдущих уроках мы прошли долгий путь в разработке нашей онлайн-библиотеки:

Мы научились писать тесты - unit-тесты с pytest, интеграционные тесты с TestClient, работать с мокированием и
фикстурами. Научились проверять нагрузку с Locust и анализировать безопасность с Bandit. Теперь у нас есть надёжный
набор тестов, который гарантирует качество кода.

Мы успешно сдали третий экзамен, продемонстрировав знания архитектуры, тестирования и безопасности нашего
микросервисного проекта.

Но возникает важный вопрос: как гарантировать, что код, который мы пишем сегодня, не сломает то, что работало
вчера?

Представьте ситуацию: вы работаете в команде из 5 разработчиков над онлайн-библиотекой. Адам добавляет новую
функцию поиска книг по жанру, Тамерлан рефакторит систему уведомлений, а вы оптимизируете базу данных. Каждый
работает в своей ветке Git. Как убедиться, что когда все эти изменения объединятся в главную ветку, система продолжит
работать корректно?

Проблемы ручного подхода:

1. Забывчивость: Разработчик может забыть запустить тесты перед push
2. Локальная среда: "У меня на машине работает" - классическая отговорка, когда на сервере всё падает
3. Человеческий фактор: Пропущенные тесты, неправильная последовательность действий
4. Медленный feedback: Узнаёте о проблемах через часы или дни после коммита
5. Деплой в полночь: Кто-то должен вручную заливать код на продакшн сервер
Сегодня мы решим эти проблемы, внедрив CI/CD (Continuous Integration / Continuous Deployment) с помощью GitHub
Actions. Это автоматизированная система, которая будет:

· Запускать все тесты при каждом push
• Проверять качество кода (линтеры, форматирование)
· Анализировать безопасность
· Автоматически деплоить на сервер при успешных проверках

Всё это будет происходить автоматически, без вашего участия, и вы будете получать уведомления о результатах за
считанные минуты!

Концепции CI/CD

Что такое Cl/CD и зачем это нужно?
CI/CD - это набор практик автоматизации, который превращает разработку из хаоса в упорядоченный процесс.

Аналогия из жизни

Представьте строительство дома:

Без CI/CD (старый подход):
• Каждый строитель работает месяцами отдельно
· В конце пытаются собрать всё вместе
• Обнаруживают, что окна не подходят к проёмам
· Тратят недели на исправление
• Риск катастрофы на финальной стадии
С CI/CD (современный подход):

• Каждый день проверяется, что новые элементы совместимы
• Проблемы обнаруживаются сразу (окно не влезает? Узнали через час!)
· Дом строится постепенно, но надёжно
• Можно показывать заказчику промежуточные результаты

Continuous Integration (Непрерывная интеграция)
Что это: Автоматическая проверка каждого изменения кода.
Процесс:
1) пишет код
2) Делает commit и push в GitHub
3) GitHub Actions автоматически:
    1. Скачивает код
    2. Устанавливает зависимости
    3. 3anyckaeT TeCTы
    4. Проверяет качество кода
    5. Анализирует безопасность

4) Результат: Всё OК или Есть проблемы
5) Разработчик получает уведомление

# Адам добавляет новую функцию в catalog/app.py
@app.get("/books/genre/{genre}")
async def get_books_by_genre(genre: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        text("SELECT * FROM books WHERE genre = :genre"),
        {"genre": genre}
    )
    return result.fetchall()

Он делает `git push`, и через 2 минуты получает уведомление:

❌ CI Failed
- ✅ Tests passed (45/45)
- ❌ Linting failed: Line too long (89 > 88 characters)
- ✅ Security check passed

Адам сразу видит проблему и исправляет её, не дожидаясь code review.

Continuous Delivery (Непрерывная доставка)

Что это: Автоматическая подготовка кода к деплою, но финальное развертывание делается вручную.

Процесс:

CI прошёл успешно ✅
      ↓
Автоматически создаётся:
  - Docker образы
  - Артефакты сборки
  - Release notes
      ↓
Код готов к деплою
      ↓
Team Lead нажимает кнопку "Deploy to Production"
      ↓
Код попадает на продакшн

Когда использовать: Для критичных систем (банки, медицина), где нужен контроль человека перед деплоем.

Continuous Deployment (Непрерывное развертывание)

Что это: Полная автоматизация — код автоматически деплоится на продакшн после успешных проверок.

Процесс:

CI прошёл успешно ✅
      ↓
Автоматически:
  1. Создаются Docker образы
  2. Деплой на staging сервер
  3. Запуск smoke-тестов на staging
  4. Деплой на production
  5. Мониторинг метрик
      ↓
Код на продакшене через 5-10 минут после push!

Когда использовать: Для web-приложений с хорошим покрытием тестами (наша библиотека подходит!).

Проблемы, которые решает CI/CD

Проблема 1: "У меня работает!"

Без CI/CD:

# Разработчик на Windows пишет код
def read_config():
    return open("C:\\config\\settings.ini").read()

# На его машине работает ✅
# На Linux сервере падает ❌

С CI/CD:

# В GitHub Actions тесты запускаются на Linux
- name: Run tests
  run: pytest tests/

# Результат через 2 минуты:
# ❌ FileNotFoundError: No such file or directory: 'C:\\config\\settings.ini'

Разработчик сразу видит проблему и исправляет:

import os
from pathlib import Path

def read_config():
    config_path = Path(__file__).parent / "config" / "settings.ini"
    return config_path.read_text()

Проблема 2: Забытые тесты

Без CI/CD:

# Разработчик спешит и забывает проверить
git add .
git commit -m "Fixed ISBN validation"
git push
# Через неделю в продакшене: баг!

С CI/CD:

# Автоматически при каждом push:
- pytest tests/
- coverage report --fail-under=85

# Если тесты не пройдены -> коммит отклоняется

Проблема 3: Несовместимость изменений

Без CI/CD:

День 1: Адам меняет структуру таблицы books
День 5: Тамерлан меняет API endpoint, не зная об изменении
День 7: Merge -> всё ломается

День 1: Адам делает PR -> CI проверяет тесты ✅
День 5: Тамерлан делает PR -> CI показывает конфликт ❌
  - 3 integration теста упали
  - Проблема в endpoints test_get_book()
Исправляют ДО merge, а не после

Проблема 4: Медленный feedback

Без CI/CD: Узнаёте о проблемах через дни или недели

С CI/CD: Получаете уведомления через минуты:

Email: CI Failed for commit abc123
Slack: @yourname Your build failed
GitHub: Red X next to your commit

Экономическая выгода CI/CD

Исследования показывают:

• Компании с CI/CD выпускают релизы в 200 раз чаще
• Время на исправление багов сокращается на 96% (часы вместо недель)
• Стоимость бага снижается в 100 раз (найденный в CI vs найденный в продакшене)

Реальный расчёт для команды из 5 разработчиков:

Без CI/CD:

• Ручное тестирование: 2 часа/день × 5 человек = 10 часов/день
• Исправление багов в продакшене: 5 часов/неделю × 5 человек = 25 часов/неделю
• Итого потерь: ~60 часов/неделю

С CI/CD:

• Настройка: 8 часов (один раз)
• Поддержка: 2 часа/неделю
• Автоматизация экономит: ~58 часов/неделю
• ROI (возврат инвестиций): окупается за 1 неделю!

GitHub Actions: основы

Что такое GitHub Actions?

GitHub Actions — это встроенный в GitHub сервис автоматизации. Это как роботы-помощники, которые живут в вашем
репозитории и выполняют задачи при определённых событиях.

Аналогия: Представьте умный дом:

• \u200b\u200bДатчик движения (событие: `git push`) → включает свет (запускает тесты)
• Термостат (событие: `pull request`) → регулирует температуру (проверяет код)
• Таймер (событие: `schedule`) → поливает цветы (запускает бэкапы)

Где живут GitHub Actions?

Всё хранится в папке `.github/workflows/` вашего репозитория:

online-library/
├── .github/
│   └── workflows/
│       ├── ci.yml          ← Здесь живут workflows
│       ├── deploy.yml      ← Основной CI pipeline
│       └── security.yml    ← Деплой на сервер
├── catalog/                ← Проверка безопасности
├── booking/
├── tests/
└── docker-compose.yml

Workflows (Рабочие процессы)

Workflow — это YAML-файл с инструкциями для GitHub Actions.

Структура простейшего workflow:

# .github/workflows/hello.yml
name: Hello World                 # Название (видно в GitHub)

on: [push]                        # Когда запускать (при push)

jobs:                             # Что делать
  greet:                          # Имя задачи
    runs-on: ubuntu-latest        # На какой ОС запускать
    steps:                        # Шаги выполнения
      - name: Say hello           # Название шага
        run: echo "Hello, World!" # Команда для выполнения

Что произойдёт:

1. Вы делаете `git push`
2. GitHub видит файл `.github/workflows/hello.yml`
3. Создаёт виртуальную машину с Ubuntu
4. Выполняет команду `echo "Hello, World!"`
5. Показывает результат в интерфейсе

Где смотреть результаты:

• GitHub → ваш репозиторий → вкладка "Actions"
• Видите список всех запусков с зелёными ✅ или красными ❌

Jobs (Задачи)

Job — это набор шагов, которые выполняются на одной машине.

Пример с несколькими jobs:

```yaml
name: CI Pipeline

on: [push]

jobs:
  # Job 1: Тестирование
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run tests
        run: pytest tests/
          # Job 2: Линтинг (запустится параллельно с test)
  lint:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Check code style
        run: black --check .

  # Job 3: Деплой (запустится ТОЛЬКО если test и lint успешны)
  deploy:
    runs-on: ubuntu-latest
    needs: [test, lint]               # Зависит от других jobs
    steps:
      - name: Deploy to server
        run: echo "Deploying..."

Steps (Шаги)

Step — это отдельная команда или действие внутри job.

Два типа шагов:

`run`: Выполнение shell-команд

```yaml
- name: Install dependencies
  run: pip install -r requirements.txt

- name: Run tests
  run: |
    pytest tests/ --cov=.
        coverage report
# `uses`: Использование готовых действий из маркетплейса

- name: Checkout code
  uses: actions/checkout@v4        # Скачивает ваш код

- name: Setup Python
  uses: actions/setup-python@v4    # Устанавливает Python
  with:
    python-version: '3.12'

- name: Cache dependencies
  uses: actions/cache@v4           # Кэширует зависимости
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}

Пояснение:

• `actions/checkout@v4` — официальное действие от GitHub
• `@v4` — версия действия (как версия Docker образа)
• `with:` — параметры для действия

Secrets (Секреты)

Что это: Безопасное хранение паролей, API ключей и токенов.

Проблема без секретов:

# ❌ ОПАСНО! Пароль в публичном репозитории
- name: Deploy
  run: |
    sshpass -p "mypassword123" ssh user@server.com
    # Теперь весь мир знает ваш пароль!

Решение с секретами:

1. Добавляем секрет в GitHub:
• GitHub → Settings → Secrets and variables → Actions → New repository secret
• Name: SSH_PASSWORD
• Value: mypassword123

2. Используем в workflow:

# ✅ БЕЗОПАСНО! Секрет не виден в логах
- name: Deploy
  env:
    SSH_PASSWORD: ${{ secrets.SSH_PASSWORD }}
  run: |
    sshpass -p "$SSH_PASSWORD" ssh user@server.com
    # В логах будет: sshpass -p "***" ssh user@server.com

Важные секреты для нашей библиотеки:

secrets:
  DATABASE_URL: postgresql://user:***@server:5432/library_db
  SECRET_KEY: supersecret.jwtkey
  DOCKER_USERNAME: yourname
  DOCKER_PASSWORD: ***
  SSH_PRIVATE_KEY: -----BEGIN RSA PRIVATE KEY-----\n***

Triggers (Триггеры событий)

Что это: События, которые запускают workflow.

1. Push — при каждом коммите

on:
  push:
    branches:
      - main      # Только в ветку main
      - develop   # И в develop

Когда использовать: Для быстрых проверок (тесты, линтеры)

2. Pull Request — при создании/обновлении PR
on:
  pull_request:
    branches:
      - main      # При PR в main
    types:
      - opened      # Когда PR создан
      - synchronize # Когда добавлены новые коммиты

Когда использовать: Для полных проверок перед merge (тесты + нагрузка + безопасность)

3. Schedule — по расписанию (cron)

on:
  schedule:
    - cron: '0 2 * * *'  # Каждый день в 2:00 UTC

Когда использовать: Для периодических задач:

• Ночные бэкапы БД
• Проверка безопасности зависимостей
• Очистка старых логов

Примеры cron выражений:

'0 * * * *'      # Каждый час
'0 0 * * 0'      # Каждое воскресенье в полночь
'*/15 * * * *'   # Каждые 15 минут
'0 9-17 * * 1-5' # Каждый час с 9:00 до 17:00, пн-пт

4. Workflow Dispatch — ручной запуск

on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy'
        required: true
        default: 'staging'
        # type: choice
# options:
#   - staging
#   - production

# Когда использовать: Для ручного деплоя или запуска задач "по требованию"

# Как запустить:
# • GitHub → Actions → выбираете workflow → Run workflow → заполняете форму

# Комбинирование триггеров

name: Full CI/CD Pipeline

on:
  push:
    branches: [main, develop]    # быстрая проверка на каждый push

  pull_request:
    branches: [main]             # полная проверка для PR

  schedule:
    - cron: '0 3 * * *'          # ночные тесты безопасности

  workflow_dispatch:             # Ручной деплой
    inputs:
      environment:
        required: true
        type: choice
        options: [staging, production]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Run tests
        run: pytest tests/

  deploy:
  # if: github.event_name == 'workflow_dispatch'  # Только при ручном запуске
#     needs: test
#     runs-on: ubuntu-latest
#     steps:
#       - name: Deploy to ${{ github.event.inputs.environment }}
#         run: echo "Deploying to ${{ github.event.inputs.environment }}"

# Настройка CI pipeline для онлайн-библиотеки

# Теперь применим всё изученное к нашему реальному проекту!

# Структура нашего CI/CD

# Мы создадим три workflow:

# 1. ci.yml — быстрые проверки при каждом push (тесты, линтинг)
# 2. security.yml — глубокая проверка безопасности (раз в день)
# 3. deploy.yml — автоматический деплой на staging/production

# Workflow 1: Основной CI Pipeline

# Создайте файл .github/workflows/ci.yml:

name: CI Pipeline

# Когда запускать
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

# Основные переменные окружения
env:
  PYTHON_VERSION: '3.12'
  DATABASE_URL: postgresql://isa:ezerbaev@localhost:5432/test_db

jobs:
  # Job 1: Тестирование
  test:
      key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-

# Шаг 4: Устанавливаем зависимости
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    pip install pytest pytest-cov pytest-asyncio

# Шаг 5: Запускаем линтеры
- name: Lint with flake8
  run: |
    pip install flake8
    # Останавливаем сборку, если есть Python syntax ошибки или undefined names
    flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
    # Предупреждения (не останавливают сборку)
    flake8 . --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics

# Шаг 6: Проверяем форматирование
- name: Check code formatting with black
  run: |
    pip install black
    black --check .

# Шаг 7: Запускаем тесты с coverage
- name: Run tests with coverage
  env:
    DATABASE_URL: ${{ env.DATABASE_URL }}
    RABBITMQ_URL: amqp://guest:guest@localhost:5672/
  run: |
    pytest tests/ \
      --cov=. \
      --cov-report=xml \
      --cov-report=term-missing \
      --cov-fail-under=85 \
      -v

# Шаг 8: Загружаем отчёт coverage в Codecov (опционально)
- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v4
  with:
    file: ./coverage.xml
    fail_ci_if_error: false

# Шаг 9: Сохраняем артефакты (отчёты)
- name: Upload test results
  if: always()  # Запускается даже если тесты упали
  uses: actions/upload-artifact@v4
  with:
    name: test-results
    path: |
      htmlcov/
      coverage.xml

# Job 2: Линтинг (параллельно с тестами)
lint:
  name: Code Quality Checks
  runs-on: ubuntu-latest

  steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ env.PYTHON_VERSION }}

    - name: Install linting tools
      run: |
        pip install black flake8 mypy isort

    - name: Run black
      run: black --check .

    - name: Run isort
      run: isort --check-only .

    - name: Run mypy

    - name: Upload coverage to Codecov
  uses: codecov/codecov-action@v4
  with:
    file: ./coverage.xml
    fail_ci_if_error: false

# Шаг 9: Сохраняем артефакты (отчёты)
- name: Upload test results
  if: always()  # Запускается даже если тесты упали
  uses: actions/upload-artifact@v4
  with:
    name: test-results
    path: |
      htmlcov/
      coverage.xml

# Job 2: Линтинг (параллельно с тестами)
lint:
  name: Code Quality Checks
  runs-on: ubuntu-latest

  steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ env.PYTHON_VERSION }}

    - name: Install linting tools
      run: |
        pip install black flake8 mypy isort

    - name: Run black
      run: black --check .

    - name: Run isort
      run: isort --check-only .

    - name: Run mypy

          run: mypy . --ignore-missing-imports

# Job 3: Проверка Docker build
docker-build:
  name: Test Docker Build
  runs-on: ubuntu-latest

  steps:
    - uses: actions/checkout@v4

    - name: Build Docker images
      run: |
        docker compose build

    - name: Start services
      run: |
        docker compose up -d
        sleep 30  # Ждём запуска сервисов

    - name: Health check
      run: |
        curl -f http://localhost:8000/docs || exit 1
        curl -f http://localhost:8001/docs || exit 1

    - name: Stop services
      run: docker compose down

Детальное объяснение CI Pipeline

Секция services

services:
  postgres:
    image: postgres:15
    env:
      POSTGRES_USER: isa
      POSTGRES_PASSWORD: ezerbaev
      POSTGRES_DB: test_db

          options: >-
      --health-cmd pg_isready
      --health-interval 10s
      --health-timeout 5s
      --health-retries 5
    ports:
      - 5432:5432

Что происходит:

• GitHub Actions создаёт Docker-контейнер с PostgreSQL
• Ждёт, пока БД станет готова (`health-cmd`)
• Делает порт 5432 доступным для тестов
• После завершения job автоматически удаляет контейнер

Зачем: Интеграционные тесты могут использовать реальную БД, а не моки.

Кэширование зависимостей

- name: Cache dependencies
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-

Как работает:

1. Первый запуск:

  ◦ Устанавливает зависимости (2-3 минуты)
  ◦ Сохраняет их в кэш с ключом на основе хэша `requirements.txt`

2. Последующие запуски:

  ◦ Проверяет хэш `requirements.txt`
  ◦ Если не изменился → берёт из кэша (10 секунд!)
  ◦ Если изменился → устанавливает заново

Экономия: ~90% времени на установку зависимостей

    options: >-
      --health-cmd pg_isready
      --health-interval 10s
      --health-timeout 5s
      --health-retries 5
    ports:
      - 5432:5432

Что происходит:

• GitHub Actions создаёт Docker-контейнер с PostgreSQL
• Ждёт, пока БД станет готова (`health-cmd`)
• Делает порт 5432 доступным для тестов
• После завершения job автоматически удаляет контейнер

Зачем: Интеграционные тесты могут использовать реальную БД, а не моки.

Кэширование зависимостей

- name: Cache dependencies
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-

Как работает:

1. Первый запуск:

  ◦ Устанавливает зависимости (2-3 минуты)
  ◦ Сохраняет их в кэш с ключом на основе хэша `requirements.txt`

2. Последующие запуски:

  ◦ Проверяет хэш `requirements.txt`
  ◦ Если не изменился → берёт из кэша (10 секунд!)
  ◦ Если изменился → устанавливает заново

Экономия: ~90% времени на установку зависимостей

Условное выполнение

- name: Upload test results
  if: always()  # Запускается даже если тесты упали
  uses: actions/upload-artifact@v4

Доступные условия:

• `if: always()` — всегда выполнять
• `if: success()` — только если всё успешно (по умолчанию)
• `if: failure()` — только если что-то упало
• `if: github.ref == 'refs/heads/main'` — только в ветке main

Workflow 2: Проверка безопасности

Создайте `.github/workflows/security.yml`:

name: Security Scan

on:
  schedule:
    - cron: '0 3 * * *'  # Каждый день в 3:00 UTC
  workflow_dispatch:     # Можно запустить вручную

jobs:
  security:
    name: Security Analysis
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      # Проверка уязвимостей в зависимостях
            - name: Install Safety
        run: pip install safety

      - name: Check for vulnerabilities
        run: |
          pip install -r requirements.txt
          safety check --json > safety-report.json || true

      # Статический анализ кода
      - name: Run Bandit
        run: |
          pip install bandit
          bandit -r . -f json -o bandit-report.json || true

      # Проверка секретов в коде
      - name: Detect secrets
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD

      # Загружаем отчёты
      - name: Upload security reports
        uses: actions/upload-artifact@v4
        with:
          name: security-reports
          path: |
            safety-report.json
            bandit-report.json

      # Отправляем уведомление в Slack (опционально)
      - name: Notify Slack
        if: failure()
        uses: slackapi/slack-github-action@v1
        with:
          webhook-url: ${{ secrets.SLACK_WEBHOOK }}
          payload: |
            {
              "text": "Security scan found issues in library project!",
                            "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "Security scan failed for *${{ github.repository }}*\n<${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}|View details>"
                  }
                }
              ]
            }

Workflow 3: Автоматический деплой

Создайте `.github/workflows/deploy.yml`:

name: Deploy

on:
  push:
    branches:
      - main          # Автодеплой на staging при push в main
  workflow_dispatch:  # Ручной деплой на production
    inputs:
      environment:
        description: 'Environment to deploy to'
        required: true
        type: choice
        options:
          - staging
          - production

jobs:
  deploy:
    name: Deploy to ${{ github.event.inputs.environment || 'staging' }}
    runs-on: ubuntu-latest

    # Защита: деплой только если CI прошёл
    needs: []  # Можно добавить зависимость от другого workflow
        steps:
      - uses: actions/checkout@v4

      # Логинимся в Docker Hub
      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      # Собираем и пушим образы
      - name: Build and push Docker images
        run: |
          docker compose build
          docker tag library_catalog:latest ${{ secrets.DOCKER_USERNAME }}/library-catalog:${{ github.sha }}
          docker tag library_booking:latest ${{ secrets.DOCKER_USERNAME }}/library-booking:${{ github.sha }}
          docker push ${{ secrets.DOCKER_USERNAME }}/library-catalog:${{ github.sha }}
          docker push ${{ secrets.DOCKER_USERNAME }}/library-booking:${{ github.sha }}

      # Деплоим на сервер через SSH
      - name: Deploy to server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /opt/library

            # Скачиваем новые образы
            docker pull ${{ secrets.DOCKER_USERNAME }}/library-catalog:${{ github.sha }}
            docker pull ${{ secrets.DOCKER_USERNAME }}/library-booking:${{ github.sha }}

            # Обновляем docker-compose.yml
            export IMAGE_TAG=${{ github.sha }}
            docker compose up -d

            # Запускаем миграции
            docker compose exec -T catalog alembic upgrade head
            docker compose exec -T booking alembic upgrade head

                        # Проверяем health
            sleep 10
            curl -f http://localhost:8000/docs || exit 1

      # Откатываем при ошибке
      - name: Rollback on failure
        if: failure()
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /opt/library
            docker compose down
            docker compose up -d  # Вернёт предыдущую версию

      # Уведомление об успешном деплое
      - name: Notify success
        if: success()
        run: |
          echo "✅ Deploy successful!"
          echo "Environment: ${{ github.event.inputs.environment || 'staging' }}"
          echo "Commit: ${{ github.sha }}"

Практика: Настройка полного CI/CD для библиотеки

Шаг 1: Подготовка репозитория

# 1. Создаём структуру
mkdir -p .github/workflows
cd .github/workflows

# 2. Создаём все три workflow
touch ci.yml security.yml deploy.yml

# 3. Добавляем конфигурации
# (копируем примеры выше)
# (копируем примеры выше)

### Шаг 2: Настройка секретов

1. **GitHub -> Settings -> Secrets and variables -> Actions**

2. **Добавляем секреты:**
DATABASE_URL=postgresql://user:pass@host:5432/library_db
SECRET_KEY=your-jwt-secret-key
DOCKER_USERNAME=yourname
DOCKER_PASSWORD=***
SSH_PRIVATE_KEY=-----BEGIN RSA PRIVATE KEY-----...
SERVER_HOST=your-server.com
SERVER_USER=deploy
SLACK_WEBHOOK=https://hooks.slack.com/services/...
GRAFANA_TOKEN=***

Шаг 3: Первый запуск

# 1. Коммитим workflow файлы
git add .github/workflows/
git commit -m "Add CI/CD pipelines"
git push origin main

# 2. Идём в GitHub -> Actions
# Видим запущенный workflow

# 3. Кликаем на него -> видим логи в реальном времени

### Шаг 4: Анализ результатов
**Если всё прошло успешно ( ✅ ):**

✅ CI Pipeline completed in 3m 42s
├── ✅ test (2m 15s)
├── ✅ lint (1m 30s)
└── ✅ docker-build (2m 45s)

**Если есть проблемы ( ❌ ):**

❌ CI Pipeline failed in 1m 32s
├── ❌ test (1m 25s)
│   └── FAILED tests/test_validators.py::test_validate_isbn
│       AssertionError: assert False is True
├── ✅ lint (45s)
└── ⏭️ docker-build (skipped, test failed)

Кликаем на failed тест -> видим полный лог -> исправляем -> пушим снова.

Шаг 5: Настройка защиты веток

GitHub -> Settings -> Branches -> Add branch protection rule:

Branch name pattern: main

☑️ Require a pull request before merging
  ☑️ Require approvals (1)
  ☑️ Dismiss stale reviews

☑️ Require status checks to pass before merging
  ☑️ Require branches to be up to date
  Status checks:
    ☑️ test
    ☑️ lint
    ☑️ docker-build

☑️ Require conversation resolution before merging

☐ Allow force pushes (оставьте выключенным!)
Результат: Невозможно смержить PR, пока CI не пройдёт!

Шаг 6: Настройка автодеплоя

# В deploy.yml добавьте условие
jobs:
  deploy:
    # Деплоим только если это push в main И CI прошёл
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    needs: []  # Можно добавить зависимость от CI workflow

Шаг 7: Тестирование полного цикла

# 1. Создаём feature ветку
git checkout -b feature/add-genre-filter

# 2. Пишем код
# catalog/app.py
@app.get("/books/genre/{genre}")
async def get_books_by_genre(...):
    ...

# 3. Пишем тесты
# tests/test_catalog.py
def test_get_books_by_genre():
    ...

# 4. Коммитим
git add .
git commit -m "Add genre filter endpoint"
git push origin feature/add-genre-filter

# 5. Создаём Pull Request в GitHub
# CI автоматически запускается

# 6. Видим результат через 3-4 минуты:
#    ✅ All checks passed
#    Merge pull request (кнопка активна)
# 7. Мержим -> автоматически деплоится на staging

Оптимизация CI/CD

Ускорение сборки

1. Используйте кэширование агрессивно

- name: Cache Python packages
  uses: actions/cache@v4
  with:
    path: |
      ~/.cache/pip
      ~/.cache/pypoetry
    key: ${{ runner.os }}-python-${{ hashFiles('**/requirements.txt') }}

- name: Cache Docker layers
  uses: actions/cache@v4
  with:
    path: /tmp/.buildx-cache
    key: ${{ runner.os }}-docker-${{ hashFiles('**/Dockerfile') }}

2. Параллелизуйте независимые задачи

jobs:
  test:
    # Запускаются параллельно
  lint:
    # Запускаются параллельно
  security:
    # Запускаются параллельно

  deploy:
    needs: [test, lint, security]  # Только после успеха всех
3. Используйте условия для пропуска ненужных шагов

- name: Run integration tests
  if: contains(github.event.head_commit.message, '[integration]')
  run: pytest tests/integration/

- name: Deploy to staging
  if: github.ref == 'refs/heads/develop'
  run: ./deploy-staging.sh

Управление ресурсами

jobs:
  test:
    runs-on: ubuntu-latest

    # Ограничиваем ресурсы
    timeout-minutes: 10  # Убиваем зависшие тесты

    # Стратегия при ошибках
    strategy:
      fail-fast: false  # Продолжаем другие jobs при ошибке
      max-parallel: 3   # Максимум 3 параллельных jobs

Продвинутые техники

Динамические workflow

name: Smart CI

on: [push]

jobs:
  detect-changes:
    runs-on: ubuntu-latest
    outputs:
        catalog-changed: ${{ steps.changes.outputs.catalog }}
    booking-changed: ${{ steps.changes.outputs.booking }}

  steps:
    - uses: actions/checkout@v4

    - uses: dorny/paths-filter@v2
      id: changes
      with:
        filters: |
          catalog:
            - 'catalog/**'
          booking:
            - 'booking/**'

test-catalog:
  needs: detect-changes
  if: needs.detect-changes.outputs.catalog-changed == 'true'
  runs-on: ubuntu-latest
  steps:
    - name: Test catalog service
      run: pytest tests/catalog/

test-booking:
  needs: detect-changes
  if: needs.detect-changes.outputs.booking-changed == 'true'
  runs-on: ubuntu-latest
  steps:
    - name: Test booking service
      run: pytest tests/booking/

Результат: Тестируем только изменённые сервисы!

Self-Hosted Runners

Для больших проектов используйте свои серверы вместо GitHub-hosted runners:

jobs:
  test:
  runs-on: [self-hosted, linux, x64, gpu]  # Свой сервер с GPU

    steps:
      - name: Run ML tests
        run: pytest tests/ml/

Преимущества:

• Быстрее (нет холодного старта)
• Дешевле для больших проектов
• Доступ к специфичному оборудованию (GPU, большие БД)

Заключение

Что мы изучили

1. Концепции CI/CD:

  ◦ Continuous Integration — автоматические проверки
  ◦ Continuous Delivery — подготовка к деплою
  ◦ Continuous Deployment — автоматический деплой

2. GitHub Actions:

  ◦ Workflows, Jobs, Steps
  ◦ Триггеры и Секреты
  ◦ Кэширование и оптимизация

3. Практические навыки:

  ◦ Настройка CI pipeline для реального проекта
  ◦ Автоматизация тестирования
  ◦ Стратегии деплоя (Blue-Green, Canary, Rolling)

Экономическая выгода для команды

Наша библиотека ДО CI/CD:

• Ручное тестирование: 2 часа/день
• Баги в продакшене: 5 часов/неделю
• Деплой: 1 час (в выходные, ночью)
• Итого потерь: ~20 часов/неделю
После внедрения CI/CD:

• Автотесты: 3 минуты (автоматически)
• Баги: находятся за минуты, не часы
• Деплой: 5 минут (автоматически)
• Экономия: ~18 часов/неделю × $50/час = $900/неделю! """
