[![Python Code Quality Checks](https://github.com/ZhikharevAl/interview/actions/workflows/code-quality.yaml/badge.svg)](https://github.com/ZhikharevAl/interview/actions/workflows/code-quality.yaml)
[![codecov](https://codecov.io/gh/ZhikharevAl/interview/branch/main/graph/badge.svg?token=bU6zfUsD9Z)](https://codecov.io/gh/ZhikharevAl/interview)
![Ruff](https://img.shields.io/badge/linting-Ruff-323330?logo=ruff) ![uv](https://img.shields.io/badge/dependencies-uv-FFA500)
![Pyright](https://img.shields.io/badge/typing-Pyright-007ACC)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/ZhikharevAl/interview)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

### Покрытие кода

![Coverage Grid](https://codecov.io/gh/ZhikharevAl/interview/graphs/sunburst.svg?token=bU6zfUsD9Z)

# Приложение для подготовки к собеседованию

Современное веб-приложение для создания и изучения вопросов для интервью с использованием интерактивных карточек.

## Возможности

- 📚 **Интерактивные карточки**: Нажимайте, чтобы переключаться между вопросами и ответами
![image](/attachment/frontend/frontend.png)
- 🏷️ **Управление категориями**: Организуйте вопросы по темам (JavaScript, Python и др.)
- 📝 **Управление вопросами**: Добавляйте, редактируйте и удаляйте вопросы
- 🔀 **Режим перемешивания**: Рандомизируйте порядок вопросов для лучшего обучения
- ➕ **Управление контентом**: Добавляйте новые категории и вопросы через веб-интерфейс
![image](/attachment/frontend/frontend_control.png)
- 🎨 **Современный UI**: Чистый, адаптивный дизайн с Tailwind CSS

## Технологический стек

- **Backend**: FastAPI (Python 3.13)
- **База данных**: PostgreSQL с SQLAlchemy ORM
- **Frontend**: Vanilla JavaScript с Tailwind CSS
- **Управление пакетами**: UV
- **Качество кода**: Ruff, Pyright, pre-commit hooks
- **Развертывание**: Docker & Docker Compose

## Быстрый старт

### Используя Docker (Рекомендуется)

```bash
# Клонирование репозитория
git clone https://github.com/ZhikharevAl/interview.git
cd interview

# Запуск приложения
docker-compose up -d

# Доступ к приложению по адресу http://localhost:8080
```

### Локальная разработка

```bash
# Установка зависимостей
uv sync --group dev

# Запуск сервера разработки
cd backend
uv run uvicorn app.main:app --reload

# Доступ к приложению по адресу http://localhost:8000
```

## Использование

1. **Режим изучения**: Выберите категорию и нажимайте на карточки, чтобы увидеть ответы
2. **Управление**: Добавляйте новые категории и вопросы через вкладку управления
3. **Перемешивание**: Рандомизируйте порядок вопросов для проверки знаний

## API эндпоинты

### Категории

- `GET /api/v1/categories/` - Получить список всех категорий (с опциональными параметрами `skip` и `limit`)
- `POST /api/v1/categories/` - Создать новую категорию
- `GET /api/v1/categories/{category_id}` - Получить категорию по ID
- `PATCH /api/v1/categories/{category_id}` - Обновить категорию по ID
- `DELETE /api/v1/categories/{category_id}` - Удалить категорию по ID

### Вопросы

- `GET /api/v1/questions/` - Получить список всех вопросов (опциональный параметр `?category_id=X`)
- `POST /api/v1/questions/` - Создать новый вопрос
- `GET /api/v1/questions/{question_id}` - Получить вопрос по ID
- `PATCH /api/v1/questions/{question_id}` - Обновить вопрос по ID
- `DELETE /api/v1/questions/{question_id}` - Удалить вопрос по ID

### Система

- `GET /health` - Эндпоинт проверки состояния

## Тестирование

Проект включает комплексный набор тестов с тремя уровнями тестирования:

### Структура тестов

```
tests/
├── unit/                   # Юнит-тесты для сервисов
├── integration/            # Интеграционные тесты с FastAPI TestClient
├── e2e/                    # End-to-end тесты с Playwright
├── api/                    # Классы API клиентов
├── utils/                  # Утилиты и модели для тестов
└── config/                 # Конфигурация тестов
```

### Запуск тестов

```bash
# Запуск всех тестов
uv run pytest

# Запуск конкретного типа тестов
uv run pytest tests/unit/           # Только юнит-тесты
uv run pytest tests/integration/   # Только интеграционные тесты
uv run pytest tests/e2e/           # Только E2E тесты

# Запуск с покрытием
uv run pytest --cov=backend/app --cov-report=html

# Запуск конкретного тестового файла
uv run pytest tests/unit/test_category_service.py

# Запуск с отчетом Allure
uv run pytest --alluredir=allure-results
allure serve allure-results
```

### Типы тестов

#### Юнит-тесты

- Тестируют отдельные функции сервисов в изоляции
- Используют in-memory SQLite базу данных
- Быстрое выполнение, без внешних зависимостей
- Покрытие: `CategoryService`, `QuestionService`

#### Интеграционные тесты

- Тестируют полные API эндпоинты с FastAPI TestClient
- Тестируют взаимодействия с базой данных и бизнес-логику
- Проверяют HTTP статус коды и схемы ответов
- Покрытие: Categories API, Questions API, Health эндпоинты

#### End-to-End тесты

- Тестируют полные пользовательские сценарии с использованием Playwright
- Реальные HTTP запросы к работающему приложению
- Тестируют API клиенты и обработку ошибок
- Покрытие: Полное тестирование API workflow

### Конфигурация тестов

Тесты используют отдельную конфигурацию через `tests/config/config.py`:

- Base URL: `http://localhost:8080` (настраивается через `.env.test`)
- Timeout: 30 секунд
- Эндпоинты: `/api/v1/categories`, `/api/v1/questions`

### Утилиты для тестов

- **API клиенты**: Высокоуровневые клиенты для Categories и Questions API
- **Фикстуры**: Управляемые тестовые данные с автоматической очисткой
- **Интеграция с Allure**: Детальные отчеты тестов с шагами и вложениями
![Allure Report](./attachment/allure/allure%202025-09-15%20071638.png)
![Allure Report](./attachment/allure/allure%202025-09-15%20071815.png)
- **Faker**: Генерация случайных тестовых данных

## Разработка

```bash
# Установка pre-commit hooks
pre-commit install

# Запуск линтеров
uvx ruff check .
uvx ruff format .
uv run pyright .
```

## Лицензия

MIT License - смотрите файл [LICENSE](LICENSE) для подробностей.
