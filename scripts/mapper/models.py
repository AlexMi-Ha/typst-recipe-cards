from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any
import re


LINK_PATTERN = re.compile("\[\[([^\[\]]+)\]\]")

@dataclass
class Recipe:
    title: str
    tags: List[str]
    category: str
    grouping: str
    prep_time: str
    cook_time: str
    servings: int
    source_url: str
    last_modified: str
    ingredients: List[str] = field(default_factory=list)
    steps: List[str] = field(default_factory=list)
    hints: List[str] = field(default_factory=list)
    key: str | None = None

    def set_key(self, category_id:str, grouping_id:str) -> None:
        self.key = f'{category_id.capitalize()}-{grouping_id.capitalize()}-{self.title[0].upper()}'
    
    def to_json(self) -> Dict[str, Any]:
        return asdict(self)
    
    def has_links(self) -> bool:
        return any(LINK_PATTERN.search(s) for s in (self.ingredients + self.steps + self.hints))