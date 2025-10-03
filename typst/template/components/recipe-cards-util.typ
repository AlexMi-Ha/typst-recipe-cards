#import "@preview/quick-cards:0.1.0": category, question, hint, answer

#let recipe-card(title: str, grouping: str, servings: int, prep_time:str, cook_time:str, ingredients: (), steps: ()) = {
  let servingsText = ""
  if(servings > 1) {
    servingsText = str(servings) + " Portionen";
  }else if(servings == 1) {
    servingsText = "1 Portion"
  }

  category[#title]
  question[#grouping $dot$ #servingsText \
  Vorbereitung: #prep_time $dot$ Kochzeit: #cook_time
  ]
  hint([
    //== Zutaten
    #columns(
      2,
      for ingredient in ingredients [
        #ingredient
      ]
    )
  ])
  answer(for step in steps [
    #step
  ])
}