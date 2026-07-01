from dataclasses import dataclass, field
from typing import List


@dataclass
class Professor:
    """Represents a faculty member who may teach courses."""

    id: str
    full_name: str
    department: str
    courses: List["Course"] = field(default_factory=list)
