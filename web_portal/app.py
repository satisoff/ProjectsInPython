from __future__ import annotations

import logging
import os
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from flask_cors import CORS

from .config import load_settings
from .db import init_database
from .repository import FeeRepository
from .services import FeeService, ValidationError


load_dotenv()


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("authenticated"):
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    settings = load_settings()

    app.secret_key = settings.secret_key
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_SECURE"] = os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true"

    CORS(app, resources={r"/api/*": {"origins": os.getenv("CORS_ORIGINS", "*")}})

    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))

    init_database(settings)
    service = FeeService(FeeRepository(settings))

    @app.get("/")
    def root():
        if session.get("authenticated"):
            return redirect(url_for("dashboard"))
        return redirect(url_for("login"))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        error = None
        if request.method == "POST":
            username = request.form.get("username", "")
            password = request.form.get("password", "")
            if username == settings.app_username and password == settings.app_password:
                session["authenticated"] = True
                return redirect(url_for("dashboard"))
            error = "Invalid credentials"
        return render_template("login.html", error=error)

    @app.get("/logout")
    def logout():
        session.clear()
        return redirect(url_for("login"))

    @app.get("/dashboard")
    @login_required
    def dashboard():
        adm_no = request.args.get("adm_no")
        student = None
        if adm_no and adm_no.isdigit():
            student = service.get_student(int(adm_no))
        return render_template("dashboard.html", student=student)

    @app.route("/students/add", methods=["GET", "POST"])
    @login_required
    def add_student():
        error = None
        student = None
        if request.method == "POST":
            try:
                student = service.add_student(request.form.to_dict())
            except ValidationError as exc:
                error = str(exc)
            except Exception:
                app.logger.exception("Failed to add student")
                error = "Internal server error"
        return render_template("add_student.html", error=error, student=student)

    @app.get("/students/<int:adm_no>")
    @login_required
    def student_details(adm_no: int):
        student = service.get_student(adm_no)
        if not student:
            return render_template("student_details.html", student=None, error="Student not found"), 404
        return render_template("student_details.html", student=student, error=None)

    @app.route("/students/<int:adm_no>/submit-fee", methods=["GET", "POST"])
    @login_required
    def submit_fee(adm_no: int):
        error = None
        result = None
        if request.method == "POST":
            amount = request.form.get("paid_amount", "0")
            try:
                result = service.submit_fee(adm_no, int(amount))
            except (ValidationError, ValueError) as exc:
                error = str(exc)
            except Exception:
                app.logger.exception("Failed to submit fee")
                error = "Internal server error"
        return render_template("submit_fee.html", adm_no=adm_no, error=error, result=result)

    @app.route("/students/<int:adm_no>/update", methods=["GET", "POST"])
    @login_required
    def update_student(adm_no: int):
        error = None
        student = service.get_student(adm_no)
        if not student:
            return render_template("update_student.html", student=None, error="Student not found"), 404

        if request.method == "POST":
            updates = {
                key: request.form.get(key)
                for key in ["st_name", "class", "sec", "cont_no"]
                if request.form.get(key)
            }
            try:
                student = service.update_student(adm_no, updates)
            except ValidationError as exc:
                error = str(exc)
            except Exception:
                app.logger.exception("Failed to update student")
                error = "Internal server error"

        return render_template("update_student.html", student=student, error=error)

    @app.post("/students/<int:adm_no>/delete")
    @login_required
    def delete_student(adm_no: int):
        deleted = service.delete_student(adm_no)
        if not deleted:
            return render_template("dashboard.html", student=None, error="Student not found")
        return redirect(url_for("dashboard"))

    @app.post("/api/login")
    def api_login():
        payload = request.get_json(silent=True) or {}
        if payload.get("username") == settings.app_username and payload.get("password") == settings.app_password:
            session["authenticated"] = True
            return jsonify({"ok": True})
        return jsonify({"ok": False, "error": "invalid credentials"}), 401

    def _api_guard():
        if not session.get("authenticated"):
            return jsonify({"error": "unauthorized"}), 401
        return None

    @app.post("/api/students")
    def api_add_student():
        unauthorized = _api_guard()
        if unauthorized:
            return unauthorized
        payload = request.get_json(silent=True) or {}
        try:
            return jsonify(service.add_student(payload)), 201
        except ValidationError:
            return jsonify({"error": "invalid request data"}), 400
        except Exception:
            app.logger.exception("Failed to add student via API")
            return jsonify({"error": "internal server error"}), 500

    @app.get("/api/students/<int:adm_no>")
    def api_get_student(adm_no: int):
        unauthorized = _api_guard()
        if unauthorized:
            return unauthorized
        student = service.get_student(adm_no)
        if not student:
            return jsonify({"error": "student not found"}), 404
        return jsonify(student)

    @app.patch("/api/students/<int:adm_no>")
    def api_update_student(adm_no: int):
        unauthorized = _api_guard()
        if unauthorized:
            return unauthorized
        payload = request.get_json(silent=True) or {}
        try:
            return jsonify(service.update_student(adm_no, payload))
        except ValidationError:
            return jsonify({"error": "invalid request data"}), 400
        except Exception:
            app.logger.exception("Failed to update student via API")
            return jsonify({"error": "internal server error"}), 500

    @app.delete("/api/students/<int:adm_no>")
    def api_delete_student(adm_no: int):
        unauthorized = _api_guard()
        if unauthorized:
            return unauthorized
        deleted = service.delete_student(adm_no)
        if not deleted:
            return jsonify({"error": "student not found"}), 404
        return jsonify({"ok": True})

    @app.post("/api/students/<int:adm_no>/submit-fee")
    def api_submit_fee(adm_no: int):
        unauthorized = _api_guard()
        if unauthorized:
            return unauthorized
        payload = request.get_json(silent=True) or {}
        try:
            paid_amount = int(payload.get("paid_amount"))
            return jsonify(service.submit_fee(adm_no, paid_amount))
        except (ValidationError, ValueError):
            return jsonify({"error": "invalid request data"}), 400
        except Exception:
            app.logger.exception("Failed to submit fee via API")
            return jsonify({"error": "internal server error"}), 500

    return app


app = create_app()
