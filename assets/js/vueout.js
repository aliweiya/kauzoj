Vue.use(VueFormWizard)
new Vue({
 el: '#helpwiz',
 methods: {
  onComplete: function(){
      alert('Yay. Done!');
   }
  }
})
