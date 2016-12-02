$(document).ready(function() {
    console.log("dom is now ready");

    $.get("http://127.0.0.1:5000/", function(data) {
        console.log(data);
    });
});
