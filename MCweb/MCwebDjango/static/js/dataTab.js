var table = $('#resultTable').dataTable( {
"order": [[ 5, "desc" ]],

"ajax": {"url":'get_more_tables',
"type":"GET",
"dataSrc":""
},

 "columns": [
         { "data": "fields.pdf_name" },
         { "data": "fields.file_name" },
         { "data": "fields.status_string" },
         { "data": "fields.template_name" },
         { "data": "fields.template_user" },
         { "data": "fields.upload_date" }
     ],

"columnDefs": [
            {
                
                targets:0,
                render: function ( data, type, row, meta ) {
                    if(type === 'display'){
                        data = '<a href="media/pdfFiles/' + data + '.pdf">' + data + '</a>';
                    }

                    return data;
                }
            },

            {          
                targets:1,
                render: function ( data, type, row, meta ) {
                    if(type === 'display'){
                        data = '<a href="media/' + data + '">' + data.substring(10, data.length-5) + '</a>';
                    }

                    return data;
                }
            }

        ],

} );


setInterval( function () {
    table.api().ajax.reload( null, false ); // user paging is not reset on reload
}, 1000 );



//jquery function for the datepicker dropdown
$( function() {
    $( ".datepicker" ).datepicker();
} );

//helper function to format django's datetimefield to javascript date
function formattedDate(date) {
	var months={
		"Jan.": "01",
		"Feb.": "02",
		"March": "03",
		"April": "04",
		"May": "05",
		"June": "06",
		"July": "07",
		"Aug.": "08",
		"Sept.": "09",
		"Oct.": "10",
		"Nov.": "11",
		"Dec.":  "12"
	}
	var split_date = date.split(" ");
	var day = split_date[1].slice(0, -1);
	if (day.length===1){
		day= "0"+day;
	}
	var temp_month = split_date[0];
	var month = months[temp_month];
	var year = split_date[2].slice(0, -1);
	return month + "/" +  day + "/" + year;

}

//
function getMinusDaysDate(numDays){
    var date = new Date();
    var last = new Date(date.getTime() - (numDays * 24 * 60 * 60 * 1000));
    return last

}


/* Custom filtering function which will search data in column five between two values */
$(document).ready(function () {
    var flag = true
    $.fn.dataTable.ext.search.push(
        function (settings, data, dataIndex) {
            var min = $('#min').datepicker( "getDate");
            var max = $('#max').datepicker("getDate");
            // need to change str order before making  date obect since it uses a new Date("mm/dd/yyyy") format for short date.
            var startDate = new Date(data[5]);

            if (min === null && max === null) { return true; }
            if (min === null && startDate <= max) { return true;}
            if(max === null && startDate >= min) {return true;}
            if (startDate <= max && startDate >= min) { return true; }
            return false;
        }
    );
    if (flag){
        $( "#min" ).datepicker( "setDate" , getMinusDaysDate(7));
        table.api().ajax.reload( null, false ); 
        flag=false;
    }
    $("#min").datepicker({ onSelect: function () { table.draw(); }, changeMonth: true, changeYear: true , dateFormat:"dd/mm/yy"});
    $("#max").datepicker({ onSelect: function () { table.draw(); }, changeMonth: true, changeYear: true, dateFormat:"dd/mm/yy" });



    // Event listener to the two range filtering inputs to redraw on input
    $('#min, #max').change(function () {
        table.api().ajax.reload( null, false );
    });

    //Set color of status according to its value
    $( ".status" ).each(function( ) {
      if ($(this).text() == "Pass"){
        $(this).css("color","green");
      }else{
        $(this).css("color","red");
      }
    });

});
