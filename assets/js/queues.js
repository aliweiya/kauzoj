// Generated by CoffeeScript 1.12.7
(function() {
  var assigned, author, authors, current_category, i, len, pieces, queue, seencategories, unassigned,
    indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

  authors = window.totaldata.Authors;

  pieces = window.totaldata.Pieces;

  queue = pieces.sort(function(a, b) {
    return a.Date - b.Date;
  });

  unassigned = [];

  assigned = [];

  seencategories = [];

  while (queue > 0) {
    current_category = queue[queue.length - 1].Category;
    if (indexOf.call(seencategories, current_category) < 0) {
      seencategories.push(current_category);
    }
    for (i = 0, len = authors.length; i < len; i++) {
      author = authors[i];
      if (indexOf.call(author.Allowed, current_category) >= 0) {
        assigned.push(queue.shift());
        continue;
      }
    }
    unassigned.push(queue.shift());
  }

  window.app = new Vue({
    el: '#app',
    data: {
      categories: seencategories,
      checkedCategories: [],
      picked: "unassigned",
      assigned: assigned,
      unassigned: unassigned
    },
    computed: resultset(function() {
      var item, j, len1, ref, results, sorton;
      sorton = this[picked];
      results = [];
      for (j = 0, len1 = sorton.length; j < len1; j++) {
        item = sorton[j];
        if (ref = item.Category, indexOf.call(checkedCategories, ref) >= 0) {
          results.push(item);
        }
      }
      return results;
    })
  });

}).call(this);
