var monitor_socket;

function websocket_url(path) {
    var scheme = window.location.protocol === "https:" ? "wss://":"ws://";
    return scheme + window.location.host + path;
}

function redirect_browser(update) {
    window.location.replace(update["redirect_url"])
}

function parse_plugin(plugin) {
    var plugin_data = {};
    plugin_data['name'] = plugin['name'];
    plugin_data['description'] = plugin['description'];
    plugin_data['version'] = plugin['version'];
    return plugin_data;
}

function get_plugins() {
    var plugin_list = [];
    var plugin;
    for (plugin in navigator.plugins) {
        plugin_list.push(parse_plugin(navigator.plugins[plugin]));
    }

    return plugin_list;
}

function get_browser_data() {
    var browser_data = {};
    browser_data['name'] = navigator.appName;
    browser_data['version'] = navigator.appVersion;
    browser_data['codename'] = navigator.appCodeName;

    browser_data['platform'] = navigator.platform;
    browser_data['user_agent'] = navigator.userAgent;
    browser_data['oscpu'] = navigator.oscpu;

    return browser_data;
}

function fingerprint() {
    var analysis_message = {
        'opcode': 'analyze'
    };

    analysis_message['browser'] = get_browser_data();

    analysis_message['plugins'] = get_plugins();

    monitor_socket.send(JSON.stringify(analysis_message));
}

$(document).ready(function() {

	var url = websocket_url("/connect/analysis?uuid=" + $("#connect-uuid").data("uuid"));
    monitor_socket = new WebSocket(url);

    monitor_socket.onopen = function() {
        // TODO: Add onopen code here
    };

    monitor_socket.onmessage = function (evt) {
        var update = $.parseJSON(evt.data);
        if (update['opcode'] == 'redirect') {
            redirect_browser(update);
        }
    };

    fingerprint()

});