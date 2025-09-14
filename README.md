[![Python Code Quality Checks](https://github.com/ZhikharevAl/interview/actions/workflows/code-quality.yaml/badge.svg)](https://github.com/ZhikharevAl/interview/actions/workflows/code-quality.yaml)
[![codecov](https://codecov.io/gh/ZhikharevAl/interview/branch/main/graph/badge.svg?token=bU6zfUsD9Z)](https://codecov.io/gh/ZhikharevAl/interview)
![Ruff](https://img.shields.io/badge/linting-Ruff-323330?logo=ruff) ![uv](https://img.shields.io/badge/dependencies-uv-FFA500)
![Pyright](https://img.shields.io/badge/typing-Pyright-007ACC)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/ZhikharevAl/interview)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

### Code Coverage

![Coverage Grid](https://codecov.io/gh/ZhikharevAl/interview/graphs/sunburst.svg?token=bU6zfUsD9Z)

# Interview Preparation App

A modern web application for creating and studying interview questions using interactive flashcards.

## Features

- 📚 **Interactive Flashcards**: Click to flip between questions and answers
![image](/attachment/frontend/frontend.png)
- 🏷️ **Category Management**: Organize questions by topics (JavaScript, Python, etc.)
- 📝 **Question Management**: Add, edit, and delete questions
- 🔀 **Shuffle Mode**: Randomize question order for better learning
- ➕ **Content Management**: Add new categories and questions through web interface
![image](/attachment/frontend/frontend_control.png)
- 🎨 **Modern UI**: Clean, responsive design with Tailwind CSS

## Tech Stack

- **Backend**: FastAPI (Python 3.13)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Frontend**: Vanilla JavaScript with Tailwind CSS
- **Package Management**: UV
- **Code Quality**: Ruff, Pyright, pre-commit hooks
- **Deployment**: Docker & Docker Compose

## Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/ZhikharevAl/interview.git
cd interview-prep-app

# Start the application
docker-compose up -d

# Access the app at http://localhost:8000
```

### Local Development

```bash
# Install dependencies
uv sync --group dev

# Run the development server
cd backend
uv run uvicorn app.main:app --reload

# Access the app at http://localhost:8000
```

## Usage

1. **Study Mode**: Select a category and click cards to reveal answers
2. **Management**: Add new categories and questions via the management tab
3. **Shuffle**: Randomize question order to test your knowledge

## API Endpoints

### Categories

- `GET /api/v1/categories/` - List all categories (with optional `skip` and `limit` parameters)
- `POST /api/v1/categories/` - Create a new category
- `GET /api/v1/categories/{category_id}` - Get category by ID
- `PATCH /api/v1/categories/{category_id}` - Update category by ID
- `DELETE /api/v1/categories/{category_id}` - Delete category by ID

### Questions

- `GET /api/v1/questions/` - List all questions (optional `?category_id=X` parameter)
- `POST /api/v1/questions/` - Create a new question
- `GET /api/v1/questions/{question_id}` - Get question by ID
- `PATCH /api/v1/questions/{question_id}` - Update question by ID
- `DELETE /api/v1/questions/{question_id}` - Delete question by ID

## Testing

The project includes comprehensive test suite with three levels of testing:

### Test Structure

```
tests/
├── unit/                   # Unit tests for services
├── integration/            # Integration tests with FastAPI TestClient
├── e2e/                    # End-to-end tests with Playwright
├── api/                    # API client classes
├── utils/                  # Test utilities and models
└── config/                 # Test configuration
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test type
uv run pytest tests/unit/           # Unit tests only
uv run pytest tests/integration/   # Integration tests only
uv run pytest tests/e2e/           # E2E tests only

# Run with coverage
uv run pytest --cov=backend/app --cov-report=html

# Run specific test file
uv run pytest tests/unit/test_category_service.py

# Run with Allure reporting
uv run pytest --alluredir=allure-results
allure serve allure-results
```

### Test Types

#### Unit Tests

- Test individual service functions in isolation
- Use in-memory SQLite database
- Fast execution, no external dependencies
- Coverage: `CategoryService`, `QuestionService`

#### Integration Tests

- Test complete API endpoints with FastAPI TestClient
- Test database interactions and business logic
- Validate HTTP status codes and response schemas
- Coverage: Categories API, Questions API, Health endpoints

#### End-to-End Tests

- Test complete user workflows using Playwright
- Real HTTP requests against running application
- Test API clients and error handling
- Coverage: Full API workflow testing

### Test Configuration

Tests use separate configuration via `tests/config/config.py`:

- Base URL: `http://localhost:8080` (configurable via `.env.test`)
- Timeout: 30 seconds
- Endpoints: `/api/v1/categories`, `/api/v1/questions`

### Test Utilities

- **API Clients**: High-level clients for Categories and Questions APIs
- **Fixtures**: Managed test data with automatic cleanup
- **Allure Integration**: Detailed test reporting with steps and attachments
- **Faker**: Random test data generation

## Development

```bash
# Install pre-commit hooks
pre-commit install

# Run linters
uvx ruff check .
uvx ruff format .
uv run pyright .

```

## License

MIT License - see [LICENSE](LICENSE) file for details.
