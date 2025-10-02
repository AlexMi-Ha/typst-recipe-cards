// category: Main title
// title: category, prep time, cook time, total_time
// hint

#let recipe-card-template(
  question: [],
  answer: [],
  hint: [],
  category: "",
  numbering: "1/1",
  both: true,
)=(
    front:{
      set text(size: 12pt)
      align(center, category)
      v(-.7em)
      set text(size: 8pt, fill: gray)
      align(center, question)
      line(length: 100%, stroke: gray)
      set text(size: 8pt, fill: black)
      hint

      align(bottom+right, "1/2")
    },
    back:{
      set text(size: 12pt)
      align(center, category)
      v(-.6em)
      line(length: 100%, stroke: gray)
      set text(size: 10pt, fill: black)
      answer
      set text(size: 8pt, fill: black)
      align(bottom+right, "2/2")
    }
)