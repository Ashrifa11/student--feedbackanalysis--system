import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask.views import MethodView
import mysql.connector
from mysql.connector import Error
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-secret-key")


class Database:
    """Creates MySQL connections using environment variables."""
    @staticmethod
    def connect():
        return mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "student_feedback")
        )


class FeedbackService:
    """Contains the project's feedback and analytics operations."""
    @staticmethod
    def get_courses():
        conn = Database.connect()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, course_name FROM courses ORDER BY course_name")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def submit(course_id, rating, comment):
        if not course_id:
            raise ValueError("Please select a course.")
        try:
            rating = int(rating)
        except (TypeError, ValueError):
            raise ValueError("Rating must be a whole number from 1 to 5.")
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5.")

        conn = Database.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO feedback (course_id, rating, comment) VALUES (%s, %s, %s)",
                (int(course_id), rating, (comment or "").strip() or None)
            )
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_summary():
        conn = Database.connect()
        try:
            query = """
                SELECT c.course_name, COUNT(f.id) AS response_count,
                       ROUND(AVG(f.rating), 2) AS average_rating
                FROM courses c
                LEFT JOIN feedback f ON f.course_id = c.id
                GROUP BY c.id, c.course_name
                ORDER BY c.course_name
            """
            df = pd.read_sql(query, conn)
            return df.fillna({"response_count": 0, "average_rating": 0}).to_dict("records")
        finally:
            conn.close()

    @staticmethod
    def export_csv():
        rows = FeedbackService.get_summary()
        return pd.DataFrame(rows, columns=["course_name", "response_count", "average_rating"]).to_csv(index=False)


class HomeView(MethodView):
    def get(self):
        try:
            courses = FeedbackService.get_courses()
            return render_template("index.html", courses=courses)
        except Error:
            flash("Cannot connect to MySQL. Check your database settings and run schema.sql.", "error")
            return render_template("index.html", courses=[])


class SubmitFeedbackView(MethodView):
    def post(self):
        try:
            FeedbackService.submit(
                request.form.get("course_id"),
                request.form.get("rating"),
                request.form.get("comment")
            )
            flash("Thank you! Your anonymous feedback was submitted.", "success")
        except ValueError as exc:
            flash(str(exc), "error")
        except Error:
            flash("Database error. Check that MySQL is running and schema.sql was executed.", "error")
        return redirect(url_for("home"))


class DashboardView(MethodView):
    def get(self):
        try:
            summary = FeedbackService.get_summary()
            return render_template("dashboard.html", summary=summary)
        except (Error, Exception):
            flash("Could not load analytics. Check MySQL and the database schema.", "error")
            return render_template("dashboard.html", summary=[])


class ExportCSVView(MethodView):
    def get(self):
        from flask import Response
        try:
            csv_data = FeedbackService.export_csv()
            return Response(
                csv_data,
                mimetype="text/csv",
                headers={"Content-Disposition": "attachment; filename=feedback_summary.csv"}
            )
        except Exception:
            flash("Could not export CSV. Check database and analytics dependencies.", "error")
            return redirect(url_for("dashboard"))


app.add_url_rule("/", view_func=HomeView.as_view("home"))
app.add_url_rule("/submit", view_func=SubmitFeedbackView.as_view("submit_feedback"), methods=["POST"])
app.add_url_rule("/dashboard", view_func=DashboardView.as_view("dashboard"))
app.add_url_rule("/export.csv", view_func=ExportCSVView.as_view("export_csv"))


if __name__ == "__main__":
    app.run(debug=True)
