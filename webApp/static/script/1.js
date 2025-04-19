function update_values() {
    $SCRIPT_ROOT = {
    {
        request.script_root | tojson | safe
    }
}
    ;
    $.getJSON($SCRIPT_ROOT + "/waiting_for_players",
        function (data) {
            $("#waiting").text(data.cpu + " %")
        });
}