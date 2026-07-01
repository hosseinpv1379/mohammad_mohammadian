from pathlib import Path

from flask import Flask, jsonify, send_from_directory
from flasgger import Swagger

from university_registration.api.routes.courses import create_course_blueprint
from university_registration.models.course import Course
from university_registration.models.enrollment import Enrollment
from university_registration.services.course_service import CourseService

ROOT_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = ROOT_DIR / "frontend"
course_service = CourseService()


def seed_demo_data() -> None:
    """Populate in-memory storage with sample courses for demo screenshots."""
    if course_service.list_courses():
        return

    samples = [
        Course(
            id="cse101",
            code="CSE-101",
            title="آزمایشگاه مهندسی نرم‌افزار",
            capacity=40,
            professor_id="prof-rahimi",
            enrollments=[
                Enrollment(id="e1", student_id="s1001", course_id="cse101"),
                Enrollment(id="e2", student_id="s1002", course_id="cse101"),
                Enrollment(id="e3", student_id="s1003", course_id="cse101"),
            ],
        ),
        Course(
            id="math201",
            code="MATH-201",
            title="ریاضیات گسسته",
            capacity=50,
            professor_id="prof-karimi",
            enrollments=[
                Enrollment(id="e4", student_id="s1004", course_id="math201")
                for _ in range(38)
            ],
        ),
        Course(
            id="phy110",
            code="PHY-110",
            title="فیزیک عمومی ۱",
            capacity=35,
            professor_id="prof-ahmadi",
            enrollments=[
                Enrollment(id="e5", student_id="s1005", course_id="phy110")
                for _ in range(35)
            ],
        ),
        Course(
            id="eng205",
            code="ENG-205",
            title="اصول طراحی نرم‌افزار",
            capacity=30,
            professor_id="prof-hosseini",
            enrollments=[
                Enrollment(id="e6", student_id="s1006", course_id="eng205")
                for _ in range(22)
            ],
        ),
    ]

    for course in samples:
        # Fix enrollment ids to be unique
        for index, enrollment in enumerate(course.enrollments):
            enrollment.id = f"{course.id}-enr-{index + 1}"
            enrollment.student_id = f"s{1000 + index + 1}"
        course_service.add_course(course)


app = Flask(__name__)
Swagger(
    app,
    template_file=str(ROOT_DIR / "docs" / "openapi" / "swagger_definitions.yml"),
    config={
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs/",
    },
)
app.config["SWAGGER"] = {
    "title": "University Registration API",
    "description": (
        "REST API for the Software Engineering Lab project: "
        "University Registration System with Student, Course, Enrollment, and Professor."
    ),
    "version": "1.0.0",
}

seed_demo_data()
app.register_blueprint(create_course_blueprint(course_service))


@app.get("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.get("/assets/<path:filename>")
def frontend_assets(filename: str):
    return send_from_directory(FRONTEND_DIR, filename)


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(debug=True)
