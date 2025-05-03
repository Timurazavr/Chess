let dots = 0;
let cons = 'Ищем'

function update_values() {
    let element = document.getElementById("waiting");
    element.innerHTML = cons + '.'.repeat(dots + 1);
    $SCRIPT_ROOT = document.getElementById('script-root').innerText.replaceAll('"', '');
    $.getJSON("/check", function (data) {
        if (data.start_game) {
            cons = 'Найден противник: ' + data.enemy;
            setTimeout(function () {
                window.location = $SCRIPT_ROOT + "session/" + data.session;
            }, 2000)
        }
    });
    dots = (dots + 1) % 3;
    setTimeout(update_values, 700);
}

window.onload = update_values;