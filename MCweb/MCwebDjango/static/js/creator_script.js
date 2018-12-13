// URL of PDF document
$('#upload_btn').on('click', function() {
    $('#file-input').trigger('click');
});

$( "#file-input" ).change(function() {
  console.log(this.files[0]);
  var reader = new FileReader();
  reader.readAsArrayBuffer(this.files[0]);
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

          // Get canvas#the-canvas
          var canvas = document.getElementById('the-canvas');

          // Fetch canvas' 2d context
          var context = canvas.getContext('2d');

          // Set dimensions to Canvas
          canvas.height = viewport.height;
          canvas.width = viewport.width;

          // Prepare object needed by render method
          var renderContext = {
            canvasContext: context,
            viewport: viewport
          };

          // Render PDF page
          page.render(renderContext);
        });
  }

});

// Asynchronous download PDF
