setInterval(function() {
    $.ajax({
        type: "GET",
        url: "get_more_tables/",  // URL to your view that serves new info

    })
    .done(function(response) {
        $('#autotable').empty().append(response);
        
    });
}, 3000)

