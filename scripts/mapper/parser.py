from __future__ import annotations
from typing import List, Dict, Any
from .models import Recipe

class RecipeParserError(Exception):
    pass

class RecipeParser:
    def __init__(self, lines: List[str], source: str = "<memory>"):
        self.lines = [l.rstrip("\n") for l in lines]
        self.path = source
        self.properties: Dict[str, Any] = {"tags": []}
        self.ingredients: List[str] = []
        self.steps: List[str] = []
        self.hints: List[str] = []
        self.line_ptr = 0

    def _eof(self) -> bool:
        return self.line_ptr >= len(self.lines)
    
    def _current(self) -> str:
        while not self._eof() and self.lines[self.line_ptr].strip() == "":
            self.line_ptr += 1
        if self._eof():
            raise RecipeParserError(f"Unexpected EOF in {self.path}")
        return self.lines[self.line_ptr].strip()
    
    def _next(self) -> None:
        if self._eof():
            raise RecipeParserError(f"Unexpected EOF in {self.path}")
        self.line_ptr += 1

    def _line_equals(self, equals: str) -> bool:
        return self._current() == equals.strip()
    
    def _line_starts_with(self, starts_with: str) -> bool:
        return self._current().startswith(starts_with)
    
    def _assert_line_equals(self, equals: str) -> None:
        if self._line_equals(equals):
            return
        raise RecipeParserError(f"Unexpected line in {self.path}. Expected: '{equals}'; Got: '{self._current()}'")
    
    def _assert_line_starts_with(self, starts_with: str) -> None:
        if self._line_starts_with(starts_with):
            return
        raise RecipeParserError(f"Unexpected start of line in {self.path}. Expected: '{starts_with}'; Got: '{self._current()}'")
    
    def parse(self) -> Recipe:
        self._expect_and_parse_section('---', self._parse_props)
        self._assert_required_props()
        
        # Title
        self._assert_line_starts_with('# ')
        self.properties['title'] = self._current()[2:].strip()
        self._next()

        self._expect_and_parse_section('## Zutaten', self._parse_ingredients)
        self._expect_and_parse_section('## Schritte', self._parse_steps)
        self._expect_and_parse_section('## Hinweise', self._parse_hints)

        return Recipe(
            title=self.properties['title'],
            tags=self.properties.get('tags', []),
            category=self.properties['category'],
            grouping=self.properties['grouping'],
            prep_time=self.properties['prep_time'],
            cook_time=self.properties['cook_time'],
            servings=int(self.properties['servings']),
            source_url=self.properties.get('source_url', ''),
            last_modified=self.properties.get('last_modified', ''),
            ingredients=self.ingredients,
            steps=self.steps,
            hints=self.hints
        )
    
    def _expect_and_parse_section(self, header: str, func):
        self._assert_line_equals(header)
        func()

    def _parse_props(self):
        self._next()
        while not self._line_equals('---'):
            if self._line_starts_with('tags:'):
                # tags header -> Collect following lines of tags
                self._next()
                while self._line_starts_with('- '):
                    self.properties['tags'].append(self._current()[1:].strip())
                    self._next()
                continue
            if ':' not in self._current():
                self._next()
                continue

            key, val = self._current().split(':', 1)
            self.properties[key.strip()] = val.strip().strip('"')
            self._next()

        self._assert_line_equals('---')
        self._next()

    def _assert_required_props(self):
        required = ('title', 'category', 'grouping', 'servings', 'prep_time', 'cook_time')
        missing = [k for k in required if k not in self.properties]
        if missing:
            raise RecipeParserError(f"Missing required properties in recipe at {self.path}: {missing}\nFound only {self.properties}")
        if not self.properties['servings'].isdigit():
            raise RecipeParserError(f"Invalid value for servings in recipe at {self.path}: {self.properties['servings']}")
        
    def _parse_ingredients(self):
        # current line '## Zutaten'
        self._next()
        while not self._eof() and (self._line_starts_with('- ') or self._line_starts_with('### ')):
            cur = self._current()
            if self._line_starts_with('### '):
                cur = '===' + cur[3:]
            self.ingredients.append(cur)
            self._next()

        self._assert_line_starts_with('## ')

    def _parse_steps(self):
        # current line '## Schritte'
        self._next()
        cur_step = 1
        while not self._eof() and not self._line_starts_with('## '):
            cur = self._current()
            if self._line_starts_with(f'{cur_step}.'):
                cur = '+ ' + cur[len(f'{cur_step}.'):].strip()
                self.steps.append(cur)
                cur_step += 1
            else:
                if not self.steps:
                    self.steps.append(cur)
                else:
                    self.steps[-1] += "\n" + cur
            
            self._next()

        self._assert_line_starts_with('## ')

    def _parse_hints(self):
        # current line '## Hinweise'
        self._next()
        while not self._eof() and not self._line_starts_with('## '):
            self.hints.append(self._current())
            self._next()