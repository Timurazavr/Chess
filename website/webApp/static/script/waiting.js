let dots = 0;

function update_values() {
    let element = document.getElementById("waiting");
    element.innerHTML = 'Ищем' + '.'.repeat(dots+1);
    $SCRIPT_ROOT = {{ request.script_root|tojson|safe }};
    $.getJSON($SCRIPT_ROOT + "/check", function (data) {
        if(data.start_game){
            element.innerHTML = 'Найден противник: '+data;
            sleep(2500);
            window.location = $SCRIPT_ROOT+"/session/"+data.session;
        }
    });
    dots = (dots + 1) % 3;
    setTimeout(update_values, 1000);
}

window.onload = update_values;