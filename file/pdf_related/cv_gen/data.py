from dataclasses import dataclass, field
from typing import List

@dataclass
class ColumnItem:
    """Generic item for column-based sections (languages, skills)"""
    title: str
    text: str

@dataclass
class ContactInfo:
    name: List[str] = field(default_factory=list)
    contacts: List[str] = field(default_factory=list)
    summaries: List[str] = field(default_factory=list)

