# Student Grading System

A grade management app written in Python. It tracks students, subjects, and grades, then calculates averages, letter grades, and class rankings. It can be used from a browser through a Flask web app or from the terminal through a menu-driven CLI. Both use the same core logic.

## Features

- Add and remove students, and add or remove grades by subject
- Per-subject and overall averages with letter grades (A+ to F)
- Class rankings, with tied averages sharing a rank
- Subject-wide averages across all students
- JSON persistence, with a timestamped backup written before every save

## Stack

- **Backend:** Python, Flask (REST API)
- **Frontend:** HTML, CSS, vanilla JavaScript
- **Storage:** JSON file (`students_data.json`) plus a `backups/` folder

## Run it

Requires Python 3.9 or newer.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Web app:**

```bash
python app.py
```

Then open `http://localhost:8000`.

**Command-line version:**

```bash
python firstProj.py
```

## API

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/students` | List all students |
| `POST` | `/students` | Add a student (`{"name": "..."}`) |
| `DELETE` | `/students/<name>` | Remove a student |
| `GET` | `/students/<name>` | One student's report |
| `GET` | `/search/<name>` | Search for a student |
| `POST` | `/grades` | Add grades (`{"name", "subject", "grades": [..]}`) |
| `DELETE` | `/grades` | Remove a grade (`{"name", "subject", "grade"}`) |
| `GET` | `/reports` | Reports for all students |
| `GET` | `/rankings` | Students ranked by overall average |
| `GET` | `/subjects/<subject>/average` | Class average for a subject |

## Project structure

```text
app.py            Flask app and REST routes
firstProj.py      Core grading logic, persistence, and the CLI menu
templates/        Web page
static/           Frontend JavaScript and CSS
```
