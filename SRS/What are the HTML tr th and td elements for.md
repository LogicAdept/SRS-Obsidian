<!--
reps: 0
priority: 0
-->
#DataFormats/Documents/HTML #SRS

# What are the HTML tr th and td elements for?

> [!abstract] Short answer
> **`<table>` represents two-dimensional tabular data; `<tr>` is a row, `<th>` a header cell, and `<td>` a data cell.** Headers get `scope` (or `headers`) so assistive technology can associate a cell with its column and row headings; `colspan` and `rowspan` merge cells across that grid.

## Anatomy

```html
<table>
  <caption>Course enrollment</caption>
  <thead>
    <tr><th scope="col">Person</th><th scope="col">Course</th></tr>
  </thead>
  <tbody>
    <tr><th scope="row">Chris</th><td>Web accessibility</td></tr>
    <tr><td>Dennis</td><td rowspan="2">HTML tables</td></tr>
    <tr><th scope="row">Mary</th></tr>
  </tbody>
</table>
```

**Listing 1.** caption, thead with column headers, tbody rows; rowspan merges one course cell across two rows.

The standard requires cells to be descendants of rows: `<table><tr><td>` without `tbody` still parses - the parser inserts a `tbody` automatically - but `<td>` directly holding a `<table>`-level role or a `<tr>` outside a table is a parse error. `th` may also be used for row headers (`scope="row"`), and the optional `tfoot` marks summary rows.

> [!warning] Tables are for data, not layout
> Before CSS, pages were built from nested layout tables; the practice survives in legacy code and is still wrong. A layout table poisons the accessibility tree - screen readers navigate it as a data grid with computed headers - and it breaks responsive design. When you *do* have real data, give the table a `caption` and header `scope` rather than styling bold first-row `td`s, which conveys nothing to machines.

`table` exists beside the list elements - see [[What are the HTML ol ul and li elements for]] for ordered collections and [[What are the HTML dl dt and dd elements for]] for key-value pairs - and the choices differ exactly in what structure they announce.

```d2
direction: right
table: "<table>" {
  width: 150
  height: 70
  style.fill: "#e3f2fd"
}
caption: "<caption>" {
  width: 150
  height: 70
  style.fill: "#fff3e0"
}
thead: "<thead>: tr > th scope=col" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
tbody: "<tbody>: tr > th scope=row, td" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
table -> caption
table -> thead
table -> tbody
```

**Fig. 1.** Table anatomy: the caption names the data, the head declares column headers, the body carries rows of header and data cells.

> [!tip] Interview answer
> **tr is a table row, th a header cell, td a data cell; thead/tbody/tfoot group rows and caption names the table. scope or headers links headers to cells for accessibility, and colspan/rowspan merge cells. Tables are strictly for two-dimensional data - never page layout.**
