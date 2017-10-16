var O18PQuery = 'kauzoj18P'
var Ovr18P = {
  Allow:function(){
    this.SetAs(2);
  },
  Hide:function(){
    this.SetAs(1);
  },
  Check:function(){
    var choice = localStorage.getItem(O18PQuery);
    if (choice == null){
      return 0;
    } else {
      return choice;
    }
  },
  SetAs : function(value){
    localStorage.setItem(O18PQuery,value);
  },
  Remove: function(){
    localStorage.removeItem(O18PQuery);
  }
}
