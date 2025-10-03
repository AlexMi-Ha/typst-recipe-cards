#{
let recipes = json(sys.inputs.at("jsonPath", default:"recipes.json"))
  .map(r => {
    r.ingredients = r.ingredients.map(i => eval(i, mode: "markup"))
    r.steps = r.steps.map(i => eval(i, mode: "markup"))
    r.hints = r.hints.map(i => eval(i, mode: "markup"))
    return r
  });

  let format = sys.inputs.at("format", default: "cards")

  if(format == "a5") {
    import "template/a5.typ": printA5
    printA5(recipes: recipes, allowMultiplePagesPerRecipe: false)
  }else if(format == "cards") {
    import "template/cards.typ": printCards
    printCards(recipes: recipes)
  }else {
  }
}

