# tests/test_parser.py
from mapper.parser import RecipeParser
import pytest

# region Testdata

# 1️⃣ Normal recipe
RECIPE_1 = """---
title: Pancakes
tags:
category: Breakfast
grouping: Sweet
prep_time: 10 min
cook_time: 15 min
servings: 4
source_url: http://example.com
last_modified: 2025-01-01
---
# Pancakes

## Zutaten
- Flour
- Milk

## Schritte
1. Mix ingredients.
2. Cook on pan.

## Hinweise
- Serve warm
- Optional: syrup

## Versionshistory
- 2025-01-01: Erstellt

<!-- MARKER FOR MAPPER SCRIPT -->"""

# 2️⃣ Recipe with missing optional fields (source_url, last_modified)
RECIPE_2 = """---
title: Omelette
tags:
category: Breakfast
grouping: Savory
prep_time: 5 min
cook_time: 5 min
servings: 1
---
# Omelette

## Zutaten
- Eggs
- Salt

## Schritte
1. Beat eggs.
2. Cook in pan.

## Hinweise
- Can add cheese

## Versionshistory
- 2025-01-02: Erstellt

<!-- MARKER FOR MAPPER SCRIPT -->"""

# 3️⃣ Recipe with multi-line step
RECIPE_3 = """---
title: Soup
tags:
category: Lunch
grouping: Starter
prep_time: 15 min
cook_time: 30 min
servings: 2
---
# Soup

## Zutaten
- Water
- Vegetables

## Schritte
1. Boil water.
   Add vegetables gradually.
2. Simmer for 30 minutes.

## Hinweise
- Season to taste

## Versionshistory
- 2025-01-03: Erstellt

<!-- MARKER FOR MAPPER SCRIPT -->"""

# 4️⃣ Recipe with empty hints section
RECIPE_4 = """---
title: Salad
tags:
category: Lunch
grouping: Side
prep_time: 5 min
cook_time: 0 min
servings: 2
---
# Salad

## Zutaten
- Lettuce
- Tomato

## Schritte
1. Chop ingredients.
2. Mix together.

## Hinweise

## Versionshistory
- 2025-01-04: Erstellt

<!-- MARKER FOR MAPPER SCRIPT -->"""

# 5️⃣ Recipe with only required fields
RECIPE_5 = """---
title: Toast
tags:
category: Breakfast
grouping: Quick
prep_time: 2 min
cook_time: 3 min
servings: 1
---
# Toast

## Zutaten
- Bread
- Butter

## Schritte
1. Toast bread.
2. Spread butter.

## Hinweise

## Versionshistory
- 2025-01-05: Erstellt

<!-- MARKER FOR MAPPER SCRIPT -->"""

# 6️⃣ Ingredients with subheadings
RECIPE_6 = """---
title: Complex Ingredients
tags:
category: Dinner
grouping: Main
prep_time: 20 min
cook_time: 40 min
servings: 4
---
# Complex Ingredients

## Zutaten
### Dry ingredients
- Flour
- Sugar
### Wet ingredients
- Milk
- Eggs

## Schritte
1. Mix dry ingredients.
2. Mix wet ingredients.
3. Combine all.

## Hinweise
- Be careful with lumps

## Versionshistory
- 2025-01-06: Erstellt

<!-- MARKER FOR MAPPER SCRIPT -->"""

# 7️⃣ Recipe with tags
RECIPE_7 = """---
title: Tagged Recipe
tags:
- easy
- quick
- vegetarian
category: Lunch
grouping: Main
prep_time: 15 min
cook_time: 20 min
servings: 2
source_url: http://example.com
last_modified: 2025-10-24
---
# Tagged Recipe

## Zutaten
- Ingredient A
- Ingredient B

## Schritte
1. Step 1
2. Step 2

## Hinweise
- Hint 1
- Hint 2

## Versionshistory
- 2025-10-24: Erstellt

<!-- MARKER FOR MAPPER SCRIPT -->"""

# endregion


@pytest.mark.parametrize("recipe_content,title,category,grouping,servings,ingredients,steps,hints", [
    (RECIPE_1, "Pancakes", "Breakfast", "Sweet", 4, ["- Flour", "- Milk"], ["+ Mix ingredients.", "+ Cook on pan."], ["- Serve warm", "- Optional: syrup"]),
    (RECIPE_2, "Omelette", "Breakfast", "Savory", 1, ["- Eggs", "- Salt"], ["+ Beat eggs.", "+ Cook in pan."], ["- Can add cheese"]),
    (RECIPE_3, "Soup", "Lunch", "Starter", 2, ["- Water", "- Vegetables"], ["+ Boil water.\nAdd vegetables gradually.", "+ Simmer for 30 minutes."], ["- Season to taste"]),
    (RECIPE_4, "Salad", "Lunch", "Side", 2, ["- Lettuce", "- Tomato"], ["+ Chop ingredients.", "+ Mix together."], []),
    (RECIPE_5, "Toast", "Breakfast", "Quick", 1, ["- Bread", "- Butter"], ["+ Toast bread.", "+ Spread butter."], []),
    (RECIPE_6, "Complex Ingredients", "Dinner", "Main", 4,
     ["=== Dry ingredients", "- Flour", "- Sugar", "=== Wet ingredients", "- Milk", "- Eggs"],
     ["+ Mix dry ingredients.", "+ Mix wet ingredients.", "+ Combine all."],
     ["- Be careful with lumps"])
])
def test_parse_recipes(recipe_content, title, category, grouping, servings, ingredients, steps, hints):
    parser = RecipeParser(recipe_content.splitlines(), title)
    recipe = parser.parse()

    assert recipe.title == title
    assert recipe.category == category
    assert recipe.grouping == grouping
    assert recipe.servings == servings
    assert recipe.ingredients == ingredients
    assert recipe.steps == steps
    assert recipe.hints == hints


def test_parse_recipe_with_tags():
    parser = RecipeParser(RECIPE_7.splitlines(), "RECIPE_7")
    recipe = parser.parse()

    assert recipe.title == "Tagged Recipe"
    assert recipe.category == "Lunch"
    assert recipe.grouping == "Main"
    assert recipe.servings == 2

    assert recipe.ingredients == ["- Ingredient A", "- Ingredient B"]
    assert recipe.steps == ["+ Step 1", "+ Step 2"]
    assert recipe.hints == ["- Hint 1", "- Hint 2"]

    assert recipe.tags == ["easy", "quick", "vegetarian"]
