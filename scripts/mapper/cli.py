from typing import Dict, List
from pathlib import Path
import argparse
import json

from .io import search_recipes, read_lines
from .parser import RecipeParser, RecipeParserError
from .models import Recipe
from .linker import link_buffer
from .keygen import get_unique_keys_from_set, KeyGenError

def parse_args():
    parser = argparse.ArgumentParser(description="Obsidian Recipe to JSON converter")
    parser.add_argument("-i", "--input", required=True, help="Parent path where the recipe markdown files are located", type=Path)
    parser.add_argument("-o", "--output", required=True, help="Output path for recipe json files", type=Path)

    return parser.parse_args()


def export_categories(categories: Dict[str, List[Recipe]], out_path: Path) -> None:
    out_path.mkdir(parents=True, exist_ok=True)
    for category, recipes in categories.items():
        filename = out_path / f"{category}.json"
        print(f'Writing {category} to {filename}')
        
        json_content = json.dumps([f.to_json() for f in recipes], indent=2)
        filename.write_text(json_content, encoding='utf-8')

def main():
    args = parse_args()

    print('Welcome to the Obsidian to Typst Recipe converter!')
    print('Searching for recipes...')
    recipe_files = search_recipes(args.input)

    print(f'Found {len(recipe_files)} recipe files!')
    for recipe in recipe_files:
        print(f'\t{recipe.with_suffix('').name}')
    
    print('Parsing the recipes...')

    file_to_recipe: Dict[str, Recipe] = {}
    recipes: List[Recipe] = []
    buffer_with_links: List[Recipe] = []

    for p in recipe_files:
        try:
            lines = read_lines(p)
            parser = RecipeParser(lines, source=str(p))
            r = parser.parse()
            recipes.append(r)
            file_to_recipe[p.with_suffix('').name] = r
            if r.has_links():
                buffer_with_links.append(r)
        except RecipeParserError as e:
            print(f"Failed parsing recipe in {p}: {e}")
            raise

    categories: Dict[str, List[Recipe]] = {}
    for r in recipes:
        categories.setdefault(r.category, []).append(r)
    for cat, rs in categories.items():
        rs.sort(key=lambda r: (r.grouping, r.title))

    print(f'Parsed and grouped by {len(categories.keys())} categories!')
    print('Generating Keys...')

    try:
        category_keys = get_unique_keys_from_set(categories.keys())
        for cat, rs in categories.items():
            unique_groupings = set([r.grouping for r in rs])
            grouping_keys = get_unique_keys_from_set(unique_groupings)

            for r in rs:
                r.set_key(category_keys[r.category], grouping_keys[r.grouping])
        
    except KeyGenError as e:
        print(f"Failed generating Keys! {e}")
        raise

    print("Linking recipes...")
    link_buffer(buffer_with_links, file_to_recipe)

    print(f'Exporting json files to {args.output}...')
    export_categories(categories, args.output)

    print("All done!")