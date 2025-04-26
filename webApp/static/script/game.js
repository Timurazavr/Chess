function start() {
    $SCRIPT_ROOT = document.getElementById('script-root').innerText.replaceAll('"', '');
    session_id = document.getElementById('session').innerText;
    ids = [11, 12, 13, 14, 15, 16, 17, 18, 21, 22, 23, 24, 25, 26, 27, 28, 31, 32, 33, 34, 35, 36, 37, 38, 41, 42, 43, 44, 45, 46, 47, 48, 51, 52, 53, 54, 55, 56, 57, 58, 61, 62, 63, 64, 65, 66, 67, 68, 71, 72, 73, 74, 75, 76, 77, 78, 81, 82, 83, 84, 85, 86, 87, 88];
    let is_white
    $.getJSON(`/get_session_data/${session_id}`, function (data) {
        is_white = data.colour === 'white'
        board = data.board.split("''")
    });
    let col
    let row
    console.log(board)
    if (is_white) {
        col = function (i) {
            return (~~(i / 10))
        }
        row = function (i) {
            return (9 - i % 10)
        }
    } else {
        col = function (i) {
            return (9 - ~~(i / 10))
        }
        row = function (i) {
            return (i % 10)
        }
    }
    for (let i of ids) {
        let element = document.getElementById(String(i))
        element.style.gridColumn = String(col(i));
        element.style.gridRow = String(row(i));
    }
    update_board()
    fetching_and_waiting()
}

function fetching_and_waiting() {
    let board_db = []
    $.getJSON(`/get_board/${session_id}`, function (data) {
        board_db = data.board.split("''")
        console.log(board_db)
    });
    if (board_db !== board) {
        board = board_db
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
        console.log(board, i, ids.indexOf(i))
        let texture = board[ids.indexOf(i)]
        if (texture === '--') {
            texture = 'F'
        }
        document.getElementById(String(i)).style.backgroundImage = `url(${$SCRIPT_ROOT}static/img/not_good_figures/${colour}${texture}.png)`
    }
}

let $SCRIPT_ROOT
let ids
let board=[]
let session_id
window.onload = start;