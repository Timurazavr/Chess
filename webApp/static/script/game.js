function dooo() {
    let ids = [11, 12, 13, 14, 15, 16, 17, 18, 21, 22, 23, 24, 25, 26, 27, 28, 31, 32, 33, 34, 35, 36, 37, 38, 41, 42, 43, 44, 45, 46, 47, 48, 51, 52, 53, 54, 55, 56, 57, 58, 61, 62, 63, 64, 65, 66, 67, 68, 71, 72, 73, 74, 75, 76, 77, 78, 81, 82, 83, 84, 85, 86, 87, 88];
    $SCRIPT_ROOT = document.getElementById('script-root').innerText;
    let is_white = true;
    $.getJSON('/get_colour', function (data) {
        is_white = data.colour === 'white'
    });
    console.log(is_white);
    if (is_white) {
        for (let i of ids) {
            let element = document.getElementById(String(i))
            element.style.gridColumn = String(i % 10);
            element.style.gridRow = String(9 - ~~(i / 10));
            element.innerText = i;
        }
    } else {
        for (let i of ids) {
            let element = document.getElementById(String(i))
            element.style.gridColumn = String(9 - i % 10);
            element.style.gridRow = String(~~(i / 10));
            element.innerText = String(i);
        }
    }
}

window.onload = dooo;
// for (let i in range(document.getElementById('board').innerHTML))
// window.onload = update_values;