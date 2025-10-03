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
      // title
      set text(size: 14pt)
      align(center, category)
      v(-.7em)
      // subtitle
      set text(size: 10pt, fill: gray)
      align(center, question)
      line(length: 100%, stroke: gray)
      // ingredients
      set text(size: 10pt, fill: black)
      hint

      // pagenumber
      set text(size: 8pt, fill: black)
      align(bottom+right, "1/2")
    },
    back:{
      // title
      /*
      set text(size: 12pt)
      align(center, category)
      v(-.6em)
      line(length: 100%, stroke: gray)
      // steps
      set text(size: 8pt, fill: black)
      answer
      */

      // steps
      set text(size: 10pt, fill: black)
      answer

      // pagenumber
      set text(size: 8pt, fill: black)
      align(bottom+right, "2/2")
    }
)