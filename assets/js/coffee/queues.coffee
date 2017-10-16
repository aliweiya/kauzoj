authors = window.totaldata.Authors
pieces = window.totaldata.Pieces
queue = pieces.sort (a,b) ->
  a.Date - b.Date
unassigned = []
assigned = []
seencategories = []
while queue > 0
  current_category = queue[queue.length-1].Category
  if current_category not in seencategories
    seencategories.push(current_category)
  for author in authors
    if current_category in author.Allowed
      assigned.push(queue.shift())
      continue
  unassigned.push(queue.shift())

window.app = new Vue(
    el: '#app'
    data:
      categories: seencategories
      checkedCategories: []
      picked: "unassigned"
      assigned: assigned
      unassigned: unassigned
    computed:
      resultset () ->
        sorton = this[picked]
        results = []
        for item in sorton
          if item.Category in checkedCategories
            results.push(item)
        return results
    )
