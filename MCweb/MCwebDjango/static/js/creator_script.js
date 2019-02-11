
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
