//called when json link is clicked (assigned in dataTab.js)
function pop_json(file_target){
  $.get(file_target, function (data) {

    var jsondata = data;
    //Prepare the table to show in the popup
    var output_html = '<table class="table table-bordered"><thead><tr><th scope="col">Key</th><th scope="col">Value</th></tr></thead><tbody>'
    $.each(jsondata, function(key,value){
      output_html += '<tr> <td>' + key + '</td><td>' + value +'</td></tr>'
    });
    output_html +='</tbody></table>'

    //Set the table as popup body
    $('.modal-body').html(output_html);

    //Prepare the download data
    var download_data = "text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(jsondata));
    var download_element = $('#json-downloader-link');
    download_element.attr("href", "data:"+download_data);
    download_element.attr("download", file_target.substring(16) );
    $('#download-button').on('click',function(e){
      download_element[0].click();
    });
  });
  $('#jsonpop').modal('show');

}
