function start() {
    $SCRIPT_ROOT = document.getElementById('script-root').innerText;
    session_id = document.getElementById('session').innerText;
    $.ajaxSetup({
        async: false
    });
    $.getJSON(`/get_session_data/${session_id}`, function (data) {
    }).done(function (data) {
        colour = data.colour;
        g_board = data.board.split('/');
        whose_turn = data.whose_turn;
        document.getElementById('enemy_nickname').innerText = 'Противник: ' + data.enemy
}).fail(function (jqXHR, textStatus, err) {
        console.log('error: get_session_data');
    });
    let col;
    let row;
    console.log(colour);
    console.log(g_board);
    if (colour === 'white') {
        col = function (i) {
            return (i % 10);
        };
        row = function (i) {
            return (9 - ~~(i / 10));
        };
    } else {
        col = function (i) {
            return (9 - i % 10)
        };
        row = function (i) {
            return (~~(i / 10))
        };
    }
    for (let i of ids) {
        let element = document.getElementById(String(i));
        element.style.gridColumn = String(col(i));
        element.style.gridRow = String(row(i));
        element.onclick = () => pressed_fields(i);
    }
    update_board();
    fetching_and_waiting();
}

function fetching_and_waiting() { // checks everytime if there was new move or
    let board_db;

    $.getJSON(`/get_board/${session_id}`, function (data) {
    }).done(function (data) {
        board_db = data.board.split('/');
    }).fail(function (jqXHR, textStatus, err) {
        console.log('error_waiting');
    });
    if (board_db.toString() !== g_board.toString()) {
        console.log(g_board);
        console.log(board_db);
        g_board = board_db;
        let mate;
        let shah;
        let stalemate;
        let draw;
        let to_who;
        $.getJSON(`/get_statement/${session_id}&${colour}`, function (data) {
        }).done(function (data) {
            mate = data.mate;
            shah = data.shah;
            stalemate = data.stalemate;
            draw = data.draw;
            to_who = data.to_who;
        }).fail(function (jqXHR, textStatus, err) {
            console.log('error: get_statement');
        });
        if (whose_turn === 'white') {
            whose_turn = 'black';
        } else {
            whose_turn = 'white';
        }
        console.log('whose_turn was changed');
        if (mate) {
            game_stopped = true;
            if (to_who === colour) {
                document.getElementById('statement').innerText = `Мат! Вы проиграли..`;
            } else {
                document.getElementById('statement').innerText = `Мат! Вы выйграли!`;
            }
        } else if (shah && to_who === colour) {
            document.getElementById('statement').innerText = `Шах! Ходите аккуратно.`;
        } else if (stalemate) {
            document.getElementById('statement').innerText = `Пат! Кому-то из вас сейчас очень обидно..`;
        } else if (draw) {
            document.getElementById('statement').innerText = `Ничья! Нечего говорить.`;
        } else {
            if (whose_turn === colour) {
                document.getElementById('statement').innerText = `Твой ход.`;
            } else {
                document.getElementById('statement').innerText = `Ждём хода противника...`;
            }
        }
        update_board();
    }
    setTimeout(fetching_and_waiting, 1000);
}

function update_board() {
    for (let i of ids) {
        let texture = g_board[8 - ~~(i / 10)][i % 10 - 1];
        if ((~~(i / 10) + i % 10) % 2 === 0) {
            document.getElementById(String(i)).style.backgroundImage = `url(${$SCRIPT_ROOT}static/img/W_field/${texture}.png)`;
        } else {
            document.getElementById(String(i)).style.backgroundImage = `url(${$SCRIPT_ROOT}static/img/B_field/${texture}.png)`;
        }
    }
}

function pressed_fields(i) { // if you pressed 2 valid fields and move is valid site makes move

    let field = document.getElementById(String(i)).style.backgroundImage.toString().split('/').at(-1).split('.')[0];
    let press = ((field.toUpperCase() === field) === (colour === 'white')); // нажимаю ли я на свою фигуру
    if (field === 'F') {
        press = false;
    }
    let is_first_push = pushed.length === 0;
    console.log('Мой ли ход:', whose_turn === colour, i, 'Первый ли ход:', is_first_push, 'На свою ли нажал:', press);
    if (whose_turn === colour && !(field === 'F' && is_first_push) && (press === is_first_push)) {
        if (!is_first_push) {
            let legit;
            $.getJSON(`/movement/${session_id}&${pushed[0]}&${i}`, function (daa) {
            }).done(function (data) {
                legit = data.legit;
            }).fail(function (jqXHR, textStatus, err) {
                console.log('error: movement');
            });
            if (legit) {
                pushed = [];
                console.log('movement was!');
            }
        } else {
            pushed.push(i);
        }
    } else {
        pushed = [];
        console.log('bad movement');
    }
}

let game_stopped = false;
let whose_turn;
let colour;
let g_board;
let $SCRIPT_ROOT;
let session_id;
let ids = [11, 12, 13, 14, 15, 16, 17, 18, 21, 22, 23, 24, 25, 26, 27, 28, 31, 32, 33, 34, 35, 36, 37, 38, 41, 42, 43, 44, 45, 46, 47, 48, 51, 52, 53, 54, 55, 56, 57, 58, 61, 62, 63, 64, 65, 66, 67, 68, 71, 72, 73, 74, 75, 76, 77, 78, 81, 82, 83, 84, 85, 86, 87, 88];
let pushed = [];
window.onload = start;
