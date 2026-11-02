// ============================================================
// Global Typst table styling
// - Draw full cell boundaries (vertical + horizontal lines)
//   so no content visually overlaps between columns.
// - Compact font + tighter inset so wide tables fit A4 margins.
// - Light header-row shading, bold header text.
// ============================================================

#set table(
  inset: 5pt,
  stroke: 0.45pt + luma(70),
)

// Smaller, tighter text inside tables
#show table: set text(size: 0.85em)
#show table: set par(justify: false)

// Header row: light shading + bold
#set table(fill: (col, row) => if row == 0 { luma(238) })
#show table.cell.where(y: 0): set text(weight: "bold")
