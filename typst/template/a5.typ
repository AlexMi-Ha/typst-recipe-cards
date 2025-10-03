#let getClosestNumbering(counter) = {
  let val = counter - 1;
  if (calc.odd(val)) {
    val += 1;
  }
  return val;
}

#let printA5(recipes: array, allowMultiplePagesPerRecipe: false, includeKeys: false) = {

  import "components/recipe-sheet.typ": recipeSheet
  set page(
    paper: "a5",
    margin: 1cm
  )

  let i = 0
  for recipe in recipes {
    if(allowMultiplePagesPerRecipe) {
      counter(page).update(1)
      set page(footer: context {
        set align(right)
        set text(size: 10pt)
        v(-.7em)
        numbering(
          "1/1",
          ..counter(page).get(),
          getClosestNumbering(counter(page).at(label("page-end-"+str(i))).first())
        )
      })
    }

    let key = ""
    if includeKeys and recipe.at("key", default: "") != "" {
      key = recipe.at("key", default: "")
    }

    recipeSheet(
      title: recipe.title,
      grouping: recipe.grouping,
      cook_time: recipe.cook_time,
      prep_time: recipe.prep_time,
      servings: recipe.servings,
      ingredients: recipe.ingredients,
      steps: recipe.steps,
      hints: recipe.hints,
      key: key
    )

    if(allowMultiplePagesPerRecipe) {
      pagebreak(weak: true, to: "odd")
      [
      #metadata("")
      #label("page-end-"+str(i))
      ]
    }
    pagebreak(weak: true)
    i = i+1;
  }
}