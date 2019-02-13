/*
  Converts the temporary JSON to our template format and
  provide error message appropriately
*/
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
      console.log(result);
      // Sending and receiving data in JSON format using POST method
      var xhr = new XMLHttpRequest();
      var url = "http://127.0.0.1:8000/save_template/";

      var response ;
      xhr.onreadystatechange = function() {
          if (xhr.readyState == XMLHttpRequest.DONE) {
              response = xhr.responseText;
              // console.log(response)
              if(response == "Post request parsed succesfully"){
                alert("Template saved succesfully")
              }else{
                alert("Something went wrong, try again")
              }
          }
      }

      xhr.open("POST", url, true);
      xhr.setRequestHeader("Content-Type", "application/json");
      xhr.send(JSON.stringify(result));
      console.log("post_sent");
    }
  }
});



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
            // Render PDF page
            page.render(renderContext);
            $("#draw-btn").prop('disabled', false);
            rectangles = {};
          });
        }
    }
});
