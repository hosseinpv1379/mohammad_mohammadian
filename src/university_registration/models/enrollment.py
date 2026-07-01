from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Enrollment:
    """Links a student to a course for a specific registration."""

    id: str
    student_id: str
    course_id: str
    status: str = "active"
    tuition_waived: bool = False
    enrolled_at: Optional[datetime] = None
