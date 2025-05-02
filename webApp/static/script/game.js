function start() {
    $.ajaxSetup({
        async: false
    });
    $.getJSON(`/get_session_data/${session_id}`, function (data) {
    }).done(function (data) {
        colour = data.colour === 'white'
        g_board = data.board.replace('1', 'E').replace('2', 'EE').replace('3', 'EEE').replace('4', 'EEEE').replace('5', 'EEEEE').replace('6', 'EEEEEE').replace('7', 'EEEEEEE').replace('8', 'EEEEEEEE')
        whose_turn = data.whose_turn
    }).fail(function (jqXHR, textStatus, err) {
        console.log('error_start');
    });
    let col
    let row
    console.log(colour)
    console.log(g_board)
    if (colour) {
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
    for (let i of ids) {
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
    $.getJSON(`/get_board/${session_id}`, function (data) {
    }).done(function (data) {
        board_db = data.board.replace('1', 'E').replace('2', 'EE').replace('3', 'EEE').replace('4', 'EEEE').replace('5', 'EEEEE').replace('6', 'EEEEEE').replace('7', 'EEEEEEE').replace('8', 'EEEEEEEE')
    }).fail(function (jqXHR, textStatus, err) {
        console.log('error_waiting');
    });
    if (board_db !== g_board) {
        g_board = board_db
        update_board()
    }
    setTimeout(fetching_and_waiting, 1000)
}

function update_board() {
    for (let i of ids) {
        let colour
        if ((~~(i / 10) + i % 10) % 2 === 0) {
            colour = 'W'
        } else {
            colour = 'B'
        }
        let texture = g_board[~~(ids.indexOf(i) / 8) * 9 + ids.indexOf(i) % 8 - 1]
        document.getElementById(String(i)).style.backgroundImage = `url(${$SCRIPT_ROOT}static/img/not_good_figures/${colour}${texture}.png)`
    }
}

function pressed_fields(i) {
    if (whose_turn === colour) {
        if (pushed.length === 1) {
            let legit
            let mate
            let stalemate
            let check
            let draw
            $.getJSON(`/movement/${session_id}&${pushed[0]}&${i}`, function (data) {
            }).done(function (data) {
                legit = data.legit
                if (legit) {
                    mate = data.mate
                    stalemate = data.stalemate
                    check = data.check
                    draw = data.draw
                }
            }).fail(function (jqXHR, textStatus, err) {
                console.log('error_waiting');
            });
            if (legit) {
                // todo
                pushed = []
                if (whose_turn === 'white') {
                    whose_turn = 'black'
                } else {
                    whose_turn = 'white'
                }
            }
        } else {
            pushed.push(i)
        }
    }

}

let whose_turn
let colour
let g_board
let $SCRIPT_ROOT = document.getElementById('script-root').innerText.replaceAll('"', '');
let session_id = document.getElementById('session').innerText;
let ids = [11, 12, 13, 14, 15, 16, 17, 18, 21, 22, 23, 24, 25, 26, 27, 28, 31, 32, 33, 34, 35, 36, 37, 38, 41, 42, 43, 44, 45, 46, 47, 48, 51, 52, 53, 54, 55, 56, 57, 58, 61, 62, 63, 64, 65, 66, 67, 68, 71, 72, 73, 74, 75, 76, 77, 78, 81, 82, 83, 84, 85, 86, 87, 88];
let pushed = []
window.onload = start;
