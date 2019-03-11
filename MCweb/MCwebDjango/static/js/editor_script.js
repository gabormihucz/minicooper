/*
  Converts the temporary JSON to our template format and
  provide error message appropriately
*/
var originalTempID = document.getElementById("tempID").value;
$("#save-button").on('click',function(){
  //Check if template is given a name
  if ($("#template-name-label").val() == ""){
    alert("Please input template name");
    $("#template-name-label").focus();
  }else{
    //Then check if template has content
    if (Object.keys(rectangles).length === 0){
      alert("The template is empty, please create some boxes");
    }else{
      //Convert temp JSON object into template JSON format
      result = convert_to_save_format(rectangles);
      result['template_id'] = tempID;
      console.log(result);
      // Sending and receiving data in JSON format using POST method

      var xhr = new XMLHttpRequest();
      var url = "http://127.0.0.1:8000/template_editor/"+originalTempID;

      function getCookie(c_name)

       {
           if (document.cookie.length > 0)
           {
               c_start = document.cookie.indexOf(c_name + "=");
               if (c_start != -1)
               {
                   c_start = c_start + c_name.length + 1;
                   c_end = document.cookie.indexOf(";", c_start);
                   if (c_end == -1) c_end = document.cookie.length;
                   return unescape(document.cookie.substring(c_start,c_end));
               }
           }
           return "";
        }

      var response ;
      xhr.onreadystatechange = function() {
          if (xhr.readyState == XMLHttpRequest.DONE) {
              response = xhr.responseText;
              if(response.substr(0,2) == "OK"){
                alert("Template has been overwritten");
                window.location = response.substr(2);
              }else{
                alert(response);
              }
              // console.log(response)
          }
      }

      xhr.open("POST", url, true);
      xhr.setRequestHeader("Content-Type", "application/json");
      xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
      xhr.send(JSON.stringify(result));
      console.log("post_sent");
    }
  }
});

//Setting up canvas
var coordinates = document.getElementById("coordinates").value;
var originalTempName = document.getElementById("tempName").value;
var tempID = document.getElementById("tempID").value;

coordinates = JSON.parse(coordinates);

//Set PDF as background and update the dimensions of canvas
$( "#file-input" ).change(function() {
  var uploaded_file = this.files[0];
  var pdf_regex = /^([a-zA-Z0-9\s_\\.\-:])+(.pdf)$/;

  //Check if file provided is a pdf file
  if (!pdf_regex.test(uploaded_file["name"])){
    alert("Invalid PDF file");
  }else{
    var reader = new FileReader();
    reader.readAsArrayBuffer(uploaded_file);
    reader.onload = function(){
        var arrayBuffer = reader.result
        var bytes = new Uint8Array(arrayBuffer);

        pdfjsLib.getDocument(bytes)
          .then(function(pdf) {
            return pdf.getPage(1);
          })
          .then(function(page) {
            // Set scale (zoom) level
            var scale = 1;

            // Get viewport (dimensions)
            var viewport = page.getViewport(scale);

            // Fetch canvas' 2d context
            var context = pdf_canvas.getContext('2d');

            // Set dimensions to Canvas
            pdf_canvas.height = viewport.height;
            pdf_canvas.width = viewport.width;
            drawing_canvas.height = viewport.height;
            drawing_canvas.width = viewport.width;
            paper.setup(drawing_canvas);
            $("#canvas-container").height(viewport.height + 30);

            // Prepare object needed by render method
            var renderContext = {
              canvasContext: context,
              viewport: viewport
            };

            page.render(renderContext);
            $("#draw-btn").prop('disabled', false);

            //Load template upon uploading PDF background
            rectangles = {};

            //Translate template back into temporary JSON
            for (var key in coordinates){
              var values = coordinates[key];
              new_box_element(parseInt(values['x1']),
                parseInt(values['y1']),
                parseInt(values['x2']) - parseInt(values['x1']),
                parseInt(values['y2']) - parseInt(values['y1']),
                key,values['mandatory']
              );
            }
          });
        }
    }
});
