

function loadJson() {
  var linkElems = document.getElementsByTagName('a'),i;
  for (i in linkElems){
      if((" "+linkElems[i].className+" ") == " JSONFile "){
        var jsonVar = linkElems[i].href
        $.getJSON( jsonVar, function( data ) {
            //var items = [];
            //var data = '[{ "firstName": "John", "lastName": "Smith" }, { "firstName": "Peter", "lastName": "Jason" }, { "firstName": "Alice", "lastName": "Ray" }]'
            var table = '<table><thead><th>Label</th><th>Data</th></thead><tbody>';
            $.each( data, function( key, val ) {
              table += '<tr><td>' + key + '</td><td>' + val + '</td></tr>';
              //items.push( "<li id='" + key + "'>" + val + "</li>" );
            });
            table += '</tbody></table>';
            document.getElementById("datalist").innerHTML = table;
            /*
            $( "<ul/>", {
              "class": "my-new-list",
              html: items.join( "" )
            }).appendTo( "body" );*/
          });
      /*
        $.get(jsonVar, function(data) {
          var table = '<table><thead><th>Label</th><th>Data</th></thead><tbody>';
          var obj = $.parseJSON(data);
          for (const [key, value] of Object.entries(obj)) {
              table += '<tr><td>' + key + '</td><td>' + value + '</td></tr>';
          }
          table += '</tbody></table>';
          document.getElementById("datalist").innerHTML = table;
        });*/
    }
  }
}

window.onload = function (){
    loadJson();
}
