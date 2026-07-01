from pathlib import Path

from flask import Blueprint, jsonify, request
from flasgger import swag_from

from university_registration.models.course import Course
from university_registration.services.course_service import (
    CourseNotFoundError,
    CourseService,
    DuplicateCourseError,
)

OPENAPI_DIR = Path(__file__).resolve().parents[4] / "docs" / "openapi"


def course_to_dict(course: Course) -> dict:
    return {
        "id": course.id,
        "code": course.code,
        "title": course.title,
        "capacity": course.capacity,
        "professor_id": course.professor_id,
        "enrollment_count": len(course.enrollments),
    }


def create_course_blueprint(service: CourseService) -> Blueprint:
    bp = Blueprint("courses", __name__, url_prefix="/courses")

    @bp.get("")
    @swag_from(str(OPENAPI_DIR / "list_courses.yml"))
    def list_courses():
        courses = [course_to_dict(course) for course in service.list_courses()]
        return jsonify(courses), 200

    @bp.post("")
    @swag_from(str(OPENAPI_DIR / "add_course.yml"))
    def add_course():
        payload = request.get_json(silent=True) or {}
        required = ("id", "code", "title", "capacity")
        missing = [field for field in required if field not in payload]
        if missing:
            return jsonify({"detail": f"Missing fields: {', '.join(missing)}"}), 400

        try:
            capacity = int(payload["capacity"])
        except (TypeError, ValueError):
            return jsonify({"detail": "capacity must be a positive integer"}), 400

        if capacity <= 0:
            return jsonify({"detail": "capacity must be a positive integer"}), 400

        course = Course(
            id=str(payload["id"]),
            code=str(payload["code"]),
            title=str(payload["title"]),
            capacity=capacity,
            professor_id=payload.get("professor_id"),
        )

        try:
            created = service.add_course(course)
        except DuplicateCourseError as exc:
            return jsonify({"detail": str(exc)}), 409

        return jsonify(course_to_dict(created)), 201

    @bp.get("/<course_id>")
    @swag_from(str(OPENAPI_DIR / "get_course.yml"))
    def get_course(course_id: str):
        try:
            course = service.get_course(course_id)
        except CourseNotFoundError as exc:
            return jsonify({"detail": str(exc)}), 404
        return jsonify(course_to_dict(course)), 200

    return bp
