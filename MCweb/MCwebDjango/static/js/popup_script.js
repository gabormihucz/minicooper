
var matchClass=['popup'];

var popup = 'width=800,height=600,toolbar=0,menubar=0,location=0,status=1,scrollbars=1,resizable=1,left=20,top=20';

function eventHandler() {
  //var popupSpecs = 'width=800,height=600,toolbar=0,menubar=0,location=0,status=1,scrollbars=1,resizable=1,left=20,top=20'
  var popupSpecs = matchClass[0]
  //Create a "unique" name for the window using a random number
  var popurl = this.href;
  var popupName = Math.floor(Math.random()*10000001);
  //Opens the pop-up window according to the specified specs
  newwindow=window.open(popurl,popupName,eval(popupSpecs));
  return false;
}

//Attach the onclick event to all your links that have the specified CSS class names
function attachPopup(){
  var linkElems = document.getElementsByTagName('a'),i;
  for (i in linkElems){
      if((" "+linkElems[i].className+" ") == " popup "){
        linkElems[i].onclick = eventHandler;
  }
  }
}

//Call the function when the page loads
window.onload = function (){
    attachPopup();
}
