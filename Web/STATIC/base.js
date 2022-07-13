$( document ).ready(function() {
    $(".btn-copy").click(function(){
        // If a button with the class "btn-copy" is clicked it will write the data stored in "data-copy" to the clipboard.
        navigator.clipboard.writeText($(this).data('copy'));
    }); 
});