from dataclasses import dataclass, field
from typing import List


@dataclass
class Student:
    """Represents a university student."""

    id: str
    full_name: str
    student_number: str
    major: str
    scholarship: bool = False
    enrollments: List["Enrollment"] = field(default_factory=list)
