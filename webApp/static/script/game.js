function start() {
    $.ajaxSetup({
        async: false
    });
    window.g_board = []
    window.$SCRIPT_ROOT = document.getElementById('script-root').innerText.replaceAll('"', '');
    window.session_id = document.getElementById('session').innerText;
    window.ids = [11, 12, 13, 14, 15, 16, 17, 18, 21, 22, 23, 24, 25, 26, 27, 28, 31, 32, 33, 34, 35, 36, 37, 38, 41, 42, 43, 44, 45, 46, 47, 48, 51, 52, 53, 54, 55, 56, 57, 58, 61, 62, 63, 64, 65, 66, 67, 68, 71, 72, 73, 74, 75, 76, 77, 78, 81, 82, 83, 84, 85, 86, 87, 88];
    let is_white
    $.getJSON(`/get_session_data/${window.session_id}`, function (data) {
    }).done(function (data) {
        is_white = data.colour === 'white'
        window.g_board = data.board.split("''")
    }).fail(function (jqXHR, textStatus, err) {
        console.log('error_start');
    });
    let col
    let row
    console.log(is_white)
    console.log(window.g_board)
    if (is_white) {
        col = function (i) {
            return (i % 10)
        }
        row = function (i) {
            return (9 - ~~(i / 10))
        }
    } else {
        col = function (i) {
            return (9 - i % 10)
        }
        row = function (i) {
            return (~~(i / 10))
        }
    }
    for (let i of window.ids) {
        let element = document.getElementById(String(i))
        element.style.gridColumn = String(col(i));
        element.style.gridRow = String(row(i));
        element.onclick = pressed_fields(i)
    }
    update_board()
    fetching_and_waiting()
}

function fetching_and_waiting() {
    let board_db = []
    $.getJSON(`/get_board/${window.session_id}`, function (data) {
    }).done(function (data) {
        board_db = data.board.split("''")
    }).fail(function (jqXHR, textStatus, err) {
        console.log('error_waiting');
    });
    if (board_db !== window.g_board) {
        window.g_board = board_db
        update_board()
    }
    setTimeout(fetching_and_waiting, 1000)
}

function update_board() {
    for (let i of window.ids) {
        let colour
        if ((~~(i / 10) + i % 10) % 2 === 0) {
            colour = 'W'
        } else {
            colour = 'B'
        }
        let texture = window.g_board[window.ids.indexOf(i)]
        if (texture === '--') {
            texture = 'F'
        }
        document.getElementById(String(i)).style.backgroundImage = `url(${window.$SCRIPT_ROOT}static/img/not_good_figures/${colour}${texture}.png)`
    }
}

function pressed_fields(i) {
    if (pushed.length === 1) {
        let legit
        let mate
        let stalemate
        let check
        $.getJSON(`/movement/${window.session_id}&${pushed[0]}&${i}`, function (data) {
        }).done(function (data) {
            legit = data.legit
            if (legit) {
                mate = data.mate
                stalemate = data.stalemate
                check = data.check
            }
        }).fail(function (jqXHR, textStatus, err) {
            console.log('error_waiting');
        });
        if (legit) {
            return
        }
    } else {
        pushed.push(i)
    }

}

let pushed = []
window.onload = start;
