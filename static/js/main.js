$(function(){
    
    $("div.option").on('click',function () {
        var choice = $(this).attr("value");
        $("#ans").attr("value", choice);
        $("#answer").submit();

    });

    $("svg.next").on('click',function () {
        var choice = $(this).attr("value");
        $("#ans").attr("value", choice);
        $("#answer").submit();

    });

});	