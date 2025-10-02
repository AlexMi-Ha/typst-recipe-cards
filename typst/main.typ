#import "@preview/quick-cards:0.1.0": *
#import "template/components/quick-cards/card-templates.typ": recipe-card-template
#import "template/components/recipe-cards-util.typ": recipe-card

#show: quick-cards-show.with(
  columns:2,                        // quick-cards does layout automatically i.e.
  rows:4,                           // questions and answers line up when printing twosided
  card-template: recipe-card-template, // there's predefined templates or create your own
  parse-body: true                  // enable Auto mode
)



#let recipes = json(sys.inputs.at("jsonPath", default:"recipes.json"));

#for recipe in recipes {
  recipe-card(
    title: recipe.title,
    grouping: recipe.grouping,
    prep_time: recipe.prep_time,
    cook_time: recipe.cook_time,
    servings: recipe.servings,
    ingredients: eval(recipe.ingredients, mode: "markup"),
    steps: eval(recipe.steps, mode: "markup")
  )
}