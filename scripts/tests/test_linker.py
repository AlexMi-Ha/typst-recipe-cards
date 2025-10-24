import pytest
from mapper.models import Recipe
from mapper.linker import link_buffer, replace_links

BASE_RECIPE = Recipe(
    title="BaseRecipe",
    tags=[],
    category="Cat",
    grouping="Grp",
    prep_time="10 min",
    cook_time="20 min",
    servings=2,
    source_url="",
    last_modified="",
    ingredients=["Flour", "Milk"],
    steps=["Mix ingredients."],
    hints=["Serve warm"]
)
BASE_RECIPE.set_key("C", "G")

LINKING_RECIPE = Recipe(
    title="LinkedRecipe",
    tags=[],
    category="Cat",
    grouping="Grp",
    prep_time="15 min",
    cook_time="25 min",
    servings=2,
    source_url="",
    last_modified="",
    ingredients=["- [[BaseRecipe]]", "- Sugar"],
    steps=["+ Prepare [[BaseRecipe]]", "+ Add Sugar"],
    hints=["- See [[BaseRecipe]]"]
)

def test_replace_links():
    filename_mapper = {"BaseRecipe": BASE_RECIPE, "LinkedRecipe": LINKING_RECIPE}

    replace_links(LINKING_RECIPE, filename_mapper)

    expanded_link = f"{BASE_RECIPE.title} (ref. {BASE_RECIPE.key})"

    assert LINKING_RECIPE.ingredients[0] == f"- {expanded_link}"
    assert LINKING_RECIPE.ingredients[1] == "- Sugar"

    assert LINKING_RECIPE.steps[0] == f"+ Prepare {expanded_link}"
    assert LINKING_RECIPE.steps[1] == "+ Add Sugar"

    assert LINKING_RECIPE.hints[0] == f"- See {expanded_link}"