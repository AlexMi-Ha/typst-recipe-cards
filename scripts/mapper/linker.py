from typing import Dict, List
from .models import Recipe, LINK_PATTERN
import re

def replace_links(recipe: Recipe, file_to_recipe_mapper: Dict[str, Recipe]) -> None:
    def handle(m: re.Match[str]):
        filename = m.group(1)
        target_recipe = file_to_recipe_mapper.get(filename)
        if target_recipe is None:
            return m.group(0)
        return f"{target_recipe.title} (ref. {target_recipe.key})"
    
    recipe.ingredients = [LINK_PATTERN.sub(handle, s) for s in recipe.ingredients]
    recipe.steps = [LINK_PATTERN.sub(handle, s) for s in recipe.steps]
    recipe.hints = [LINK_PATTERN.sub(handle, s) for s in recipe.hints]

def link_buffer(buffer: List[Recipe], file_to_recipe_mapper: Dict[str, Recipe]) -> None:
    for r in buffer:
        replace_links(r, file_to_recipe_mapper)