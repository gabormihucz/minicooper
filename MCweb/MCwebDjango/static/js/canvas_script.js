var pdf_canvas = $("#pdf-canvas")[0];
var drawing_canvas = $("#drawing-canvas")[0];
var drawable = drawing_canvas.getContext('2d');

//Setting up paper js and mouse event variables
paper.setup(drawing_canvas);
var bounds = 0;
var last_mousex = last_mousey = 0;
var mousex = mousey = 0;
var width = height = 0;
var drawing = false;
var animate = false;

//Temporary JSON to keep track of rectangle properties
var rectangles = {};

//Keep track of current rectangle object
var current_rectangle;

//temp rectangle for animation
var animation_rectangle = null;

//counter of rectangle object name and default name
var rectangle_counter = 0;
var name_counter = 0;

//Left click, track start location for mouse, set up offsets
$(drawing_canvas).on('mousedown', function(e) {
  if (drawing){
    canvasx = $(drawing_canvas).offset().left;
    canvasy = $(drawing_canvas).offset().top;
    bounds = e.target.getBoundingClientRect();
    last_mousex = parseInt(e.clientX- bounds.left);
    last_mousey = parseInt(e.clientY- bounds.top);
    animate = true;
  }
});

$(drawing_canvas).on('mousemove',function(e){
  if (drawing && animate){
    if (animation_rectangle != null){
      animation_rectangle.remove();
    }
    var animation_mousex = parseInt(e.clientX - bounds.left);
    var animation_mousey = parseInt(e.clientY - bounds.top);
    var animation_width = animation_mousex-last_mousex;
    var animaton_height = animation_mousey-last_mousey;
    animation_rectangle = new paper.Path.Rectangle(last_mousex, last_mousey, animation_width, animaton_height);
    animation_rectangle.strokeColor = "black";
  }
});

//Release mouse, create rectangle with end location for mouse
$(drawing_canvas).on('mouseup', function(e) {
  if (drawing){
    if (animation_rectangle != null){
      animation_rectangle.remove();
    }
    mousex = parseInt(e.clientX - bounds.left);
    mousey = parseInt(e.clientY - bounds.top);
    width = mousex-last_mousex;
    height = mousey-last_mousey;

    //Create rectangle with provided Xs and Ys, set up coloring for rectangle
    var rectangle = new paper.Path.Rectangle(last_mousex, last_mousey, width, height);
    var rectangle_name = "rect"+ rectangle_counter.toString();

    rectangle.name = rectangle_name;
    rectangle_counter++;

    rectangle.strokeColor = "blue";
    rectangle.fillColor = "blue";
    rectangle.fillColor.alpha = 0.25;

    //Set the current rectangle to the newly created rectangle and select it
    current_rectangle = rectangle;
    select_rectangle(current_rectangle);

    /*
      Update temporary JSON with rectangle name as key and a dictionary
      Containing name, mandatory status and its rectangle object as value
    */

    rectangles[rectangle_name]={};
    //Choose suitable default name for box to avoid conflict in temp JSON
    var proposed_default_name = "default" + name_counter.toString();
    while(check_box_label_exist(proposed_default_name,rectangles)){
      name_counter++;
      proposed_default_name = "default" + name_counter.toString();
    }
    rectangles[rectangle_name]["name"] = proposed_default_name;
    name_counter++;
    rectangles[rectangle_name]["mandatory"] = true;
    rectangles[rectangle_name]["object"] = rectangle;

    /*
      Attach event to rectangle, on click will select and
      set the current rectangle to this
      and display its properties on the side bar to be edited
    */
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
      rectangle.position = e.point;
      display_coordinates(this);
    }

    //Update sidebar on creation of the rectangle
    $("#box-label").val(rectangles[rectangle_name]["name"]);

    $("#mandatory-radio").prop("checked", true);
    display_coordinates(current_rectangle);
    disable_side_bar(false);

    //Stop drawing, reset draw button
    drawing = false;
    animate = false;
    $("#draw-btn").css("background-color","#007bff");
    $('html,body').css('cursor','default');

    //Focus on the sidebar name field
    $("#box-label").focus();
    $("#box-label").select();

  }
});

$("#delete-button").on('click', function(e){
  delete_current_rectangle();
});

$(document).on('keydown', function(e) {
  if (e.which == 46){
    delete_current_rectangle();
  }
});


/*
  Button will set the property of rectangle with the sidebar properties
  in the temp JSON if the name isnt already taken
*/
$("#set-button").on('click',function(){
  if (current_rectangle!=null){
    var proposed_box_label = $("#box-label").val();
    var selected_rectangles_key = rectangles[current_rectangle.name];

    //Allow if there is no clash, else, raise alert and focus on label box
    if ((!check_box_label_exist(proposed_box_label,rectangles) || proposed_box_label == selected_rectangles_key["name"]) && proposed_box_label.length != 0 ){
      selected_rectangles_key["name"] = $("#box-label").val();
      if($('#mandatory-radio').is(':checked'))  {
          selected_rectangles_key["mandatory"] = true;
      }
      else {
          selected_rectangles_key["mandatory"] = false;
      }

      resize_current_rectangle(current_rectangle);

    }else{
      alert("Label already exists or is empty");
      $("#box-label").focus();
      $("#box-label").select();
    }

  }
});


/*
  Draw button, if not drawing, will set to draw mode,
  if already drawing will cancel the draw mode
*/
$("#draw-btn").on('click',function(){
  if (drawing){
    drawing = false;
    $("#draw-btn").css("background-color","#007bff");
    $('html,body').css('cursor','default');
  }else{
    drawing = true;
    $("#draw-btn").css("background-color","grey");
    $('html,body').css('cursor','crosshair');
  }
});

$('#upload-btn').on('click', function() {
    $('#file-input').trigger('click');
});

$( document ).ready(function() {
    $("#box-label").val("");
    $("#draw-btn").prop('disabled',true);
    disable_side_bar(true);
    $("#template-name-label").val("");
    $("#x1-label").val("");
    $("#y1-label").val("");
    $("#x2-label").val("");
    $("#y2-label").val("");
});

//Additional helper functions
function check_box_label_exist(boxLabel, rectangle_JSON){
  var duplicate_name_flag = false;

  //Check if name already exist
  for (var key in rectangle_JSON) {
    var name = rectangle_JSON[key]["name"];
    if (name == boxLabel){
      duplicate_name_flag = true;
    }
  }
  return duplicate_name_flag;
}

//Deselect all items and select targeted item
function select_rectangle(rectangle){
  var children = paper.project.activeLayer.children;
  for (var i = 0; i < children.length; i++) {
  	var child = children[i];
    child.selected = false;
  }
  rectangle.selected = true;
}

//function to delete currently selected rectangle
function delete_current_rectangle(){
  if (current_rectangle != null){
    delete rectangles[current_rectangle.name];
    current_rectangle.remove();
    current_rectangle == null;

    $("#box-label").val("");
    $("#x1-label").val("");
    $("#y1-label").val("");
    $("#x2-label").val("");
    $("#y2-label").val("");
    disable_side_bar(true);
  }
}

//Set the sidebar to disabled or enabled
function disable_side_bar(state){
  $("#box-label").prop('disabled', state);
  $("#mandatory-radio").prop('disabled', state);
  $("#optional-radio").prop('disabled', state);
  $("#set-button").prop('disabled',state);
  $("#delete-button").prop('disabled',state);
  $("#x1-label").prop('disabled',state);
  $("#y1-label").prop('disabled',state);
  $("#x2-label").prop('disabled',state);
  $("#y2-label").prop('disabled',state);
}

function resize_current_rectangle(rectangle){
  //Check if any resizing field is empty, if it is not then reassign bounds for rectangle
  var coordinateArray = [$("#x1-label").val(),$("#y1-label").val(),$("#x2-label").val(),$("#y2-label").val()];
  var emptyfound = false;
  for (var i = 0; i < coordinateArray.length; i++){
    if (coordinateArray[i] == ""){
      emptyfound = true;
      break;
    }
  }
  if (!emptyfound){
    var x1 = parseInt(coordinateArray[0]);
    var y1 = parseInt(coordinateArray[1]);
    var x2 = parseInt(coordinateArray[2]);
    var y2 = parseInt(coordinateArray[3]);
    rectangle.bounds = new paper.Rectangle(new paper.Point(x1,y1), new paper.Size(x2-x1,y2-y1));
  }else{
    alert("At least one coordinate field is empty");
  }

}

function display_coordinates(rectangle){
  $("#x1-label").val(rectangle.bounds.topLeft._x.toFixed(0));
  $("#y1-label").val(rectangle.bounds.topLeft._y.toFixed(0));
  $("#x2-label").val(rectangle.bounds.bottomRight._x.toFixed(0));
  $("#y2-label").val(rectangle.bounds.bottomRight._y.toFixed(0));
}

//Convert temp json object into a template object
function convert_to_save_format(temp_json_object){
  var result = {};
  var boxes = {};
  var name;
  var mandatory;
  var temp_rect;

  result["template_name"] = $("#template-name-label").val();
  //Convert temp JSON to template JSON format
  for (var key in temp_json_object) {
    name = temp_json_object[key]["name"];
    mandatory = temp_json_object[key]["mandatory"];
    temp_rect = temp_json_object[key]["object"];
    boxes[name] = {};
    boxes[name]["x1"] = temp_rect.bounds.topLeft._x;
    boxes[name]["y1"] = temp_rect.bounds.topLeft._y;
    boxes[name]["x2"] = temp_rect.bounds.bottomRight._x;
    boxes[name]["y2"] = temp_rect.bounds.bottomRight._y;
    boxes[name]["mandatory"] = mandatory;
  }
  boxes["size"] = {};
  boxes["size"]["x"] = bounds.right - bounds.left
  boxes["size"]["y"] = bounds.bottom - bounds.top
  result['rectangles'] = boxes;

  return result;
}
