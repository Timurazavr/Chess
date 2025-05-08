let dots = 0;
let cons = 'Ищем'

function update_values() {
    let element = document.getElementById("waiting");
    element.innerHTML = cons + '.'.repeat(dots + 1);
    $SCRIPT_ROOT = document.getElementById('script-root').innerText;
    $.getJSON("/check", function (data) {
        if (data.start_game) {
            cons = 'Найден противник: ' + data.enemy;
            window.location = $SCRIPT_ROOT + "session/" + data.session;
        } else if (data.black_id === -2) {
            let elem = document.getElementById('special_id')
            elem.hidden = false
            elem.innerText = 'Ваш Id игры по которому сможет подключится друг: ' + data.session.toString()
        }
    });
    dots = (dots + 1) % 3;
    setTimeout(update_values, 700);
}

window.onload = update_values;