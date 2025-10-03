#let printCards(recipes: array) = {

  import "@preview/quick-cards:0.1.0": *
  import "components/quick-cards/card-templates.typ": recipe-card-template
  import "components/recipe-cards-util.typ": recipe-card

  show: quick-cards-show.with(
    columns:2,                        // quick-cards does layout automatically i.e.
    rows:4,                           // questions and answers line up when printing twosided
    card-template: recipe-card-template, // there's predefined templates or create your own
    parse-body: true                  // enable Auto mode

  )

  for recipe in recipes {
    recipe-card(
      title: recipe.title,
      grouping: recipe.grouping,
      prep_time: recipe.prep_time,
      cook_time: recipe.cook_time,
      servings: recipe.servings,
      ingredients: recipe.ingredients,
      steps: recipe.steps
    )
  }
}