from typing import Dict, List, Optional

from university_registration.models.course import Course


class CourseNotFoundError(Exception):
    """Raised when a course id does not exist in storage."""


class DuplicateCourseError(Exception):
    """Raised when attempting to create a course with an existing id."""


class CourseService:
    """In-memory course management service."""

    def __init__(self) -> None:
        self._courses: Dict[str, Course] = {}

    def list_courses(self) -> List[Course]:
        return list(self._courses.values())

    def get_course(self, course_id: str) -> Course:
        course = self._courses.get(course_id)
        if course is None:
            raise CourseNotFoundError(f"Course '{course_id}' not found.")
        return course

    def add_course(self, course: Course) -> Course:
        if course.id in self._courses:
            raise DuplicateCourseError(f"Course with id '{course.id}' already exists.")
        self._courses[course.id] = course
        return course

    def clear(self) -> None:
        """Reset storage; useful for tests."""
        self._courses.clear()
