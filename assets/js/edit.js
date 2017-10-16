// Vue.use(VueClipboard.install)
var decrypted, editable, supreceed = true;
var showArticle = true;
var originalButton, editing, parentalControls, floodpages = false;
var ScrapePreventionChildProtection = "sgdhu0zJqMNwJMptmKK7,D2tD8NvxzqaOYTTsMyLF,GxE9O06PhZ76l26h3jWk,tbgpTwdRRrjPVatmRst0,Tjg05gCHSyVzwbdrDswZ,RYbgX8HE2RdJlucai4je,G68x6cY2lZlQmU1ndOEV,9gOCaOEkmcvwLFfgVLHb,PPJkVEbvB1WWx9YTUgIb,qTZGIfrqIv8FLSunL93A"
console.log(Ovr18P);
try {
  // grab "#source" div's content.
  var sourceDiv = document.getElementById("source");
  if (sourceDiv != null){
    console.log('attempt decrypt');
    var decrypted = XORCipher.decode(ScrapePreventionChildProtection,sourceDiv.value);
    showArticle = false;
    // parental nature:
    var parentalDiv = document.getElementById("parental");
    if (parentalDiv != null && parentalDiv.value == 'true'){
      var over18p = Ovr18P.Check();
      console.log('Local storate set to: ' + over18p);
      switch (over18p){
        case 0:
          console.log('parental controls are unset...');
          floodpages = true;
          parentalControls = true;
          break;
          ;;
        case 1:
          console.log('parental controls are ON...');
          parentalControls = true;
          break;
          ;;
        case 2:
          console.log('parental controls are OFF...');
          parentalControls = false;
          break;
          ;;
      }
    }
  } else {
    console.log('no hidden source, pumping cleartext into markdown.');
    var rendered = document.getElementById("article").innerHTML;
    var decrypted = toMarkdown(rendered);
    showArticle = false;
    originalButton = true;
  }
  // grab the #article div's content.
} catch (e){
  console.log(e);
  editable = false;
  supreceed = false;
}
console.log(floodpages);
console.log(showArticle);
var vm = new Vue({
    el: "#appt",
    data: {
        showedit: editable,
        copyalert: false,
        input: decrypted,
        output: '',
        sO18P: Ovr18P,
        editing: editing,
        floodpage: floodpages,
        showarticle: showArticle,
        showOriginalButton: originalButton,
        parentalControls: parentalControls
    },
    computed: {
      compiledMarkdown: function () {
        return marked(this.input, { sanitize: true })
      }
    },
    methods: {
      update: _.debounce(function (e) {
        this.input = e.target.value
        this.output = XORCipher.encode(ScrapePreventionChildProtection,this.input)
      }, 300),
      copySuccess: function (e){
        console.log('copy sucess')
        this.copyalert = true;
      },
      handlerL: function (){
        this.copyalert = false;
      },
      parental: function(value){
        if (value == 'on'){
          this.floodpage=false;
          this.parentalControls=true;
          this.sO18P.Hide();
          this.showarticle = false;
          this.supreceed = false;
          this.showedit = false;
          this.editing = false;
        } else {
          this.floodpage=false;
          this.parentalControls=false;
          this.sO18P.Show();
          this.showarticle = false;
          this.supreceed = true;
          this.showedit = true;
          this.editing = true;
        }
      }
    }
});
// posting still confuses me.
// https://github.com/mavoweb/mavo/tree/714ecd75389c8d9e4ff2a06d5351ed5d4e77f5aa/src
// how is that not insecure?
