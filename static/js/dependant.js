$(document).ready(function(){
    $("#country").change(function(){
        var country_id = $(this).val();
        var url ="/states/?country_id="+country_id;
        $.get(url, function(data, status){
            $("#state").html(data);
        });
    });
})


$(document).ready(function(){
    $("#state").change(function(){
        var state_id = $(this).val();
        var url ="/cities/?state_id="+state_id;
        $.get(url, function(data, status){
            $("#city").html(data);
        });
    });
})