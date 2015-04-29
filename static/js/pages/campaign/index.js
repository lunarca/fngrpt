/**
 * Created by lunarca on 4/25/15.
 */

$(document).ready(function() {
    $("a[id^=view-campaign]").click(function() {
        window.location = "/campaigns/manage/" + $(this).data('uuid');
    });
});