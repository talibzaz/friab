$(document).on("keydown", ":input:not(textarea):not(:submit)", function(event) {
    return event.key != "Enter";
});