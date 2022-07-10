$( document ).ready(function() {
    $(".btn-copy").click(function(){
        navigator.clipboard.writeText($(this).data('copy'));
    }); 
});