# Student Grading System

A web application for managing student records, grades, reports, and class rankings. Teachers can add students, record grades by subject, view individual or class-wide reports, and rank students by overall average.

The same core logic also powers an interactive command-line interface for local use without a browser.

## Tech Stack

- **Backend:** Python 3.9+, Flask 3.x
- **Frontend:** HTML, CSS, vanilla JavaScript
- **Storage:** JSON file (`students_data.json`) with automatic backups in `backups/`

## Setup

1. Clone the repository and enter the project directory.

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   # venv\Scripts\activate    # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Running Locally

### Web UI

Start the Flask server:

```bash
python app.py
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

### CLI

Run the menu-driven terminal interface:

```bash
python firstProj.py
```

## Project Structure

```
student_grading_website/
├── app.py              # Flask web server and REST API routes
├── firstProj.py        # Core grading logic and CLI menu
├── students_data.json  # Persistent student/grade data
├── backups/            # Auto-generated JSON backups (local, gitignored)
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Main web page
└── static/
    ├── app.js          # Frontend API calls and UI logic
    └── style.css       # Styles
```

## Key Features

- **Students:** Add and remove students
- **Grades:** Add and remove grades by subject (supports comma-separated values)
- **Reports:** View a single student's report or all student reports
- **Rankings:** Rank students by overall grade average (ties share the same rank)
- **Subject averages:** Calculate the class-wide average for a subject
- **Letter grades:** Automatic letter-grade conversion (A+ through F)
- **Backups:** Previous data is backed up to `backups/` before each save when content changes

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Web UI |
| GET | `/students` | List all students and grades |
| POST | `/students` | Add a student (`{"name": "..."}`) |
| GET | `/students/<name>` | Student report |
| DELETE | `/students/<name>` | Remove a student |
| POST | `/grades` | Add grades (`{"name", "subject", "grades": [...]}`) |
| DELETE | `/grades` | Remove grade(s) (`{"name", "subject", "grade"}` or `"grades": [...]`) |
| GET | `/reports` | All student reports |
| GET | `/rankings` | Student rankings |
| GET | `/subjects/<subject>/average` | Subject class average |
| GET | `/search/<name>` | Student report (alias) |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8000` | Port for the Flask development server |
| `FLASK_DEBUG` | `0` | Set to `1` to enable Flask debug mode |

Example:

```bash
PORT=8080 FLASK_DEBUG=1 python app.py
```

No API keys or external services are required.

## Known Limitations

- Data is stored in a single JSON file — suitable for small datasets and single-user use
- No authentication or authorization
- Concurrent writes (multiple tabs or processes) are not safe and may corrupt data
- Backup files accumulate in `backups/` over time; clean up periodically if disk space is a concern
- The Flask development server is not intended for production deployment

## Letter Grade Scale

| Average | Letter |
|---------|--------|
| 90+ | A+ |
| 85–89 | A |
| 80–84 | A- |
| 75–79 | B+ |
| 70–74 | B |
| 65–69 | C+ |
| 60–64 | C |
| 50–59 | D |
| Below 50 | F |
