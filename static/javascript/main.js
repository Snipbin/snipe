function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

$(document).ready(function() {
    $("#search-help-tooltip").popover({
        trigger: 'hover',
        container: '.fa.fa-info'
    });

    var query = getParameterByName('query')
    if (query) {
        $("#snippet-search").attr('value', query);
    }

});
