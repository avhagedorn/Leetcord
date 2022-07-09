$(document).ready(function($) {
    $("tbody tr").click(function() {
        if ($(this).data("href")){
            window.document.location = $(this).data("href");
        }
    });
});
