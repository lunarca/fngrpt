var monitor_socket;

function websocket_url(path) {
    var scheme = window.location.protocol === "https:" ? "wss://":"ws://";
    return scheme + window.location.host + path;
}

$(document).ready(function() {

	var url = websocket_url("/connect/analysis/")

});