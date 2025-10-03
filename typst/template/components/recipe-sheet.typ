#let contentWithMaxHeight(ratioToFullHeight:float, body:content) = context {
  let bodyScale = box(width: 128mm, body)

  let contentHeight = measure(bodyScale).height
  let height = calc.min(contentHeight, ratioToFullHeight * page.height)
  box(height: height, clip: false, bodyScale)
}

#let recipeSheet(title: str, grouping: str, servings: int, prep_time: str, cook_time: str, ingredients: array, steps: array, hints: array, key: str) = {
    let servingsText = ""
  if(servings > 1) {
    servingsText = str(servings) + " Portionen";
  }else if(servings == 1) {
    servingsText = "1 Portion"
  }

  if(key != "") {
    set text(size: 12pt)
    place(right, [*#key*])
  }

  set text(size: 20pt)
  align(center, title)
  v(-.7em)
  set text(size: 12pt, fill: gray)
  align(center, [
    #grouping $dot$ #servingsText \
  Vorbereitung: #prep_time $dot$ Kochzeit: #cook_time
  ])
  line(length: 100%, stroke: gray)
  set text(size: 12pt, fill: black)
  align(left, contentWithMaxHeight(ratioToFullHeight: 0.3, body:[
    == Zutaten
    #columns(
      2,
      for ingredient in ingredients [
        #ingredient
      ]
    )
  ]))

  align(left, [
    == Schritte
    #for step in steps [
      #step
    ]
  ])

  if(hints.len() > 0) {
    align(left, [
      == Hinweise
      #for hint in hints [
        #hint
      ]
    ])
  }
}