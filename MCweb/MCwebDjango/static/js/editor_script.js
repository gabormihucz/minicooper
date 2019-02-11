//Setting up canvas
var coordinates = document.getElementById("coordinates").value;
coordinates = JSON.parse(coordinates)

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
              var rectangle = new paper.Path.Rectangle(parseInt(values['x1']),
                parseInt(values['y1']),
                parseInt(values['x2']) - parseInt(values['x1']),
                parseInt(values['y2']) - parseInt(values['y1']));
              var rectangle_name = "rect"+ rectangle_counter.toString();

              rectangle.name = rectangle_name;
              rectangle_counter++;

              rectangle.strokeColor = "blue";
              rectangle.fillColor = "blue";
              rectangle.fillColor.alpha = 0.25;

              current_rectangle = rectangle;
              select_rectangle(current_rectangle);

              rectangles[rectangle_name]={};
              proposed_default_name = key;
              rectangles[rectangle_name]["name"] = proposed_default_name;

              rectangles[rectangle_name]["mandatory"] = values['mandatory'];
              rectangles[rectangle_name]["object"] = rectangle;

              //Re-assign events to rectangles
              rectangle.onClick = function(e){
                current_rectangle = this;
                select_rectangle(current_rectangle);
                $("#box-label").val(rectangles[current_rectangle.name]["name"]);
                if (rectangles[current_rectangle.name]["mandatory"]){
                  $("#mandatory-radio").prop("checked", true);
                }else{
                  $("#optional-radio").prop("checked", true);
                }
                display_coordinates(current_rectangle);
                disable_side_bar(false);

              }
              //Drag to move the rectangle around
              rectangle.onMouseDrag = function(e){
                this.position = e.point;
                display_coordinates(this);
              }

              //Update sidebar on creation of the rectangle
              $("#box-label").val(rectangles[current_rectangle.name]["name"]);
              if (rectangles[current_rectangle.name]["mandatory"]){
                $("#mandatory-radio").prop("checked", true);
              }else{
                $("#optional-radio").prop("checked", true);
              }

              display_coordinates(current_rectangle);
              disable_side_bar(false);
            }
          });
        }
    }
});
