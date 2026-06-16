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


### GUI

The project includes a browser GUI served by FastAPI from `gui.py`.

Run the application and open:

```bash
http://localhost:3000
```

The GUI stores the JWT token returned by login in browser `localStorage` and sends it as a Bearer token for protected API requests.

Implemented GUI actions cover 11 API endpoints:

| GUI action | API endpoint |
| --- | --- |
| Register user | `POST /api/users` |
| Login | `POST /api/auth/login` |
| Show horses | `GET /api/horses` |
| Show trainers | `GET /api/trainers` |
| Show training types | `GET /api/training-types` |
| Show trainings | `GET /api/trainings` |
| Browse trainings with pagination and filters | `GET /api/trainings/page?page=1&size=5&status=open&horse_id=1` |
| Create training | `POST /api/trainings` |
| Update training | `PUT /api/trainings/{id}` |
| Delete training | `DELETE /api/trainings/{id}` |
| Join training | `POST /api/trainings/{id}/join` |
| Show training participants | `GET /api/trainings/{id}/participants` |

Form input protection is handled with HTML validation attributes and JavaScript:

- `type="email"` protects email fields.
- `required`, `minlength`, `maxlength`, and `pattern` validate names and passwords.
- `type="number"`, `min`, `max`, and `step` validate numeric IDs and capacity.
- `type="datetime-local"` validates dates before converting them to ISO strings for the API.
- JavaScript prevents empty update requests and converts numeric/date inputs before sending JSON.

The "Browse trainings" page supports server-side filtering and pagination. It can filter by `status` and `horse_id`, choose a page size, and move through pages with Previous/Next buttons. Pagination is calculated after filters are applied, so a narrower filter returns a smaller result count and fewer pages.

The GUI is responsive: on small screens the two-column layout collapses to one column, filter controls stack vertically, and the trainings table scrolls horizontally when needed. The interface is organized into clear areas for account actions, quick lookups, paginated browsing, training management, and API responses.
### Running Tests

To run the unit tests, execute the following command:

```bash
pytest
```
