$(document).ready(function () {
    
    /* ----------------------- show aside menu in low resoulotion ----------------------- */
        $("button.menu").click(function () {
            $("aside.main-menu").fadeToggle(200);
        });
    /* ----------------------- show aside menu in low resoulotion ----------------------- */
    
    /* ----------------------- aside main-menu animation ----------------------- */
    $('aside.main-menu > nav > ul').each(function () {
        var current_ul = $(this);
        $("li",this).click(function () {
            if($(this).hasClass("active")){
                $("ul.hasUL > ul").slideUp(500);
                $("ul.hasUL > li.active").removeClass("active");
            }else{
                $("ul.hasUL > ul").slideUp(500);
                $("ul.hasUL > li.active").removeClass("active");
                $("ul",current_ul).slideDown(500);
                $(this).addClass("active");
            }
        });
    });
    /* ----------------------- aside main-menu animation ----------------------- */

});