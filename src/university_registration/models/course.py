from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Course:
    """Represents an academic course offering."""

    id: str
    code: str
    title: str
    capacity: int
    professor_id: Optional[str] = None
    enrollments: List["Enrollment"] = field(default_factory=list)
