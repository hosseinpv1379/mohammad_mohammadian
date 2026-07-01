import pytest

from university_registration.models.course import Course
from university_registration.services.course_service import (
    CourseNotFoundError,
    CourseService,
    DuplicateCourseError,
)


@pytest.fixture
def service() -> CourseService:
    svc = CourseService()
    yield svc
    svc.clear()


def test_add_course_persists_new_course(service: CourseService) -> None:
    # Arrange
    course = Course(
        id="cse101",
        code="CSE-101",
        title="Software Engineering Lab",
        capacity=35,
        professor_id="prof-1",
    )

    # Act
    created = service.add_course(course)

    # Assert
    assert created.id == "cse101"
    assert len(service.list_courses()) == 1
    assert service.get_course("cse101").title == "Software Engineering Lab"


def test_get_course_returns_existing_course(service: CourseService) -> None:
    # Arrange
    service.add_course(
        Course(id="math201", code="MATH-201", title="Discrete Math", capacity=50)
    )

    # Act
    found = service.get_course("math201")

    # Assert
    assert found.code == "MATH-201"
    assert found.capacity == 50


def test_get_course_raises_when_id_missing(service: CourseService) -> None:
    # Arrange
    missing_id = "unknown-course"

    # Act & Assert
    with pytest.raises(CourseNotFoundError, match="not found"):
        service.get_course(missing_id)
