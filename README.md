# Interview Preparation App

A modern web application for creating and studying interview questions using interactive flashcards.

## Features

- 📚 **Interactive Flashcards**: Click to flip between questions and answers
- 🏷️ **Category Management**: Organize questions by topics (JavaScript, Python, etc.)
- 🔀 **Shuffle Mode**: Randomize question order for better learning
- ➕ **Content Management**: Add new categories and questions through web interface
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
git clone <your-repo-url>
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

- `GET /api/v1/categories/` - List all categories
- `POST /api/v1/categories/` - Create a new category
- `GET /api/v1/questions/` - List all questions (optional `?category_id=X`)
- `POST /api/v1/questions/` - Create a new question

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
