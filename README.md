# Student Feedback Analysis System — Team 6

Class-based Flask + MySQL project with a simple frontend, anonymous ratings, analytics dashboard, and CSV export.

## Project files
- `app.py` — Flask backend; `Database` and `FeedbackService` classes; class-based views.
- `templates/` — HTML frontend pages.
- `static/style.css` — navy/teal responsive styling.
- `schema.sql` — database and sample courses.
- `requirements.txt` — Python dependencies.

## Run locally
1. Install Python 3.10+ and MySQL 8.
2. Create and activate a virtual environment:
   - Windows: `python -m venv venv` then `venv\\Scripts\\activate`
3. Install packages: `pip install -r requirements.txt`
4. In MySQL Workbench or MySQL command line, run `schema.sql`.
5. Set database credentials before running. In Windows PowerShell, for example:
   `$env:DB_USER="root"; $env:DB_PASSWORD="your_password"; $env:DB_NAME="student_feedback"`
6. Start: `python app.py`
7. Open `http://127.0.0.1:5000` in your browser.
8. Open `/dashboard` to view the summary; click Export CSV to download aggregated data.

## Important
- This is a student learning prototype, not a production deployment.
- Never collect student names or roll numbers in anonymous feedback.
- Before deployment, disable Flask debug mode, use a strong secret key, validate access to the dashboard, and configure secrets in the hosting provider's environment variables.
- The current version summarizes numeric ratings; it does not yet perform AI sentiment analysis on comments.
