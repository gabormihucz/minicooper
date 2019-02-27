
//loads Json file and puts in a table which is inserted into the html
function loadJson() {
  var linkElems = document.getElementsByClassName('JSONFile'),i;
  for (i in linkElems){
        var jsonVar = linkElems[i].href
        $.getJSON( jsonVar, function( data ) {
            var table = '<table><thead><th>Label</th><th>Data</th></thead><tbody>';
            $.each( data, function( key, val ) {
              table += '<tr><td>' + key + '</td><td>' + val + '</td></tr>';

            });
            table += '</tbody></table>';
            document.getElementById("datalist").innerHTML = table;
          });
  }
}

window.onload = function (){
    loadJson();
}
