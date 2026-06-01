# Horse-riding-tracker
<img width="581" height="470" alt="image" src="https://github.com/user-attachments/assets/48fc21c5-6b39-4cbe-9e77-9bf747590a7e" />

## API Documentation

This project provides a FastAPI-based REST API for a horse training planner.

### Prerequisites

- Python 3.9+
- pip (Python package installer)

### Setup & Configuration

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *Note: If you encounter issues with email validation, ensure you run `pip install "pydantic[email]"` which is included in the requirements.*

3. **Database Initialization:**
   The application uses a local SQLite database (`app.db`). The database schema and initial tables will be automatically created and populated upon the first application startup using the `DB_commands.sql` script.

### Running the Application

To run the API server locally on port 3000, execute:

```bash
uvicorn main:app --host 0.0.0.0 --port 3000 --reload
```

The API will be available at `http://localhost:3000`.

- **Interactive API docs (Swagger UI):** [http://localhost:3000/docs](http://localhost:3000/docs)
- **Alternative API docs (ReDoc):** [http://localhost:3000/redoc](http://localhost:3000/redoc)

### Running Tests

To run the unit tests, execute the following command:

```bash
pytest
```
