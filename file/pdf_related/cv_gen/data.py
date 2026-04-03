from dataclasses import dataclass, field
from typing import List

@dataclass
class ColumnItem:
    """Generic item for column-based sections (languages, skills)"""
    title: str
    text: str

@dataclass
class ContactInfo:
    name: List[str] = field(default=[])
    contacts: List[str] = field(default=[])
    summaries: List[str] = field(default=[])

