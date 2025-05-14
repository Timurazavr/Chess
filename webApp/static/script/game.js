function start() {
    $SCRIPT_ROOT = document.getElementById('script-root').innerText;
    session_id = document.getElementById('session').innerText;
    document.getElementById('resign').onclick = resign;
    document.getElementById('walkback').onclick = () => {
        window.location = $SCRIPT_ROOT
    };
    $.ajaxSetup({
        async: false
    });
    $.getJSON(`/get_session_data/${session_id}`, function (data) {
    }).done(function (data) {
        if (!data.legit) {
            window.location = $SCRIPT_ROOT + "error";
        }
        colour = data.colour;
        g_board = data.board.split('/');
        whose_turn = data.whose_turn;
        if (whose_turn === colour) {
            document.getElementById('statement').innerText = `Твой ход.`;
        } else {
            document.getElementById('statement').innerText = `Ждём ход противника...`;
        }
        document.getElementById('enemy_nickname').innerText = 'Противник: ' + data.enemy
    }).fail(function (jqXHR, textStatus, err) {
        console.log('error: get_session_data');
        window.location = $SCRIPT_ROOT + "error";
    });
    let col;
    let row;
    console.log(colour);
    console.log(g_board);
    if (colour === 'white') {
        col = function (i) {
            return (~~(i / 10));
        };
        row = function (i) {
            return (9 - i % 10);
        };
    } else {
        col = function (i) {
            return (9 - ~~(i / 10))
        };
        row = function (i) {
            return (i % 10)
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


async function fetching_and_waiting() { // checks everytime if there was new move or
    $.ajaxSetup({
        async: false
    });
    if (!game_stopped) {
        $.getJSON(`/is_finished/${session_id}`, function (data) {
        }).done(function (data) {
            if (data.is_finished) {
                if (whose_turn === colour) {
                    $('statement').text('Вы сдались.')
                } else {
                    $('statement').text('Противник сдался.')
                }
                game_stopped = true
            }
        }).fail(function (jqXHR, textStatus, err) {
            console.log('error: is_finished');
        });
        let board_db;
        $.getJSON(`/get_board/${session_id}`, function (data) {
        }).done(function (data) {
            if (!data.legit) {
                window.location = $SCRIPT_ROOT + "error";
            }
            if (data.end) {
                game_stopped = true
            }
            board_db = data.board.split('/');
        }).fail(function (jqXHR, textStatus, err) {
            console.log('error: get_board');
            window.location = $SCRIPT_ROOT + "error";
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
                if (!data.legit) {
                    window.location = $SCRIPT_ROOT + "error";
                }
                mate = data.mate;
                shah = data.shah;
                stalemate = data.stalemate;
                draw = data.draw;
                to_who = data.to_who;
            }).fail(function (jqXHR, textStatus, err) {
                console.log('error: get_statement');
                window.location = $SCRIPT_ROOT + "error";
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
                    document.getElementById('statement').innerText = `Ждём ход противника...`;
                }
            }
            update_board();
        }
        if (game_stopped) {
            document.getElementById('walkback').removeAttribute('hidden');
            await ending();
        } else {
            setTimeout(fetching_and_waiting, 333);
        }
    }
}

function update_board() {
    for (let i of ids) {
        let texture = g_board[8 - i % 10][~~(i / 10) - 1];
        if ((~~(i / 10) + i % 10) % 2 === 0) {
            document.getElementById(String(i)).style.backgroundImage = `url(${$SCRIPT_ROOT}static/img/W_field/${texture}.png)`;
        } else {
            document.getElementById(String(i)).style.backgroundImage = `url(${$SCRIPT_ROOT}static/img/B_field/${texture}.png)`;
        }
    }
}

function pressed_fields(i) { // if you pressed 2 valid fields and move is valid site makes move
    if (!game_stopped) {
        $.ajaxSetup({
            async: false
        });
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
                    window.location = $SCRIPT_ROOT + "error";
                });
                let elem = document.getElementById(String(pushed[0]))
                elem.style.boxShadow = ''
                elem.style.zIndex = ''
                pushed = [];
                if (legit) {
                    console.log('movement was!');
                } else {
                    console.log('bad movement, logic said that');
                }
            } else {
                pushed.push(i);
                let elem = document.getElementById(String(i))
                elem.style.boxShadow = '5px 5px 4px 1px #ffffffff, -5px -5px 4px 1px #ffffffff, -5px 5px 4px 1px #ffffffff, 5px -5px 4px 1px #ffffffff'
                elem.style.zIndex = '1'
            }
        } else {
            let elem = document.getElementById(String(pushed[0]))
            elem.style.boxShadow = ''
            elem.style.zIndex = ''
            pushed = [];
            console.log('bad movement');
        }
    }
}

function resign() {
    if (!game_stopped) {
        if (whose_turn === colour) {
            $.ajaxSetup({
                async: false
            });
            $.getJSON(`/resign/${session_id}`, function (daa) {
            }).done(function (data) {

            }).fail(function (jqXHR, textStatus, err) {
                console.log('error: movement');
            });
        }
    }
}

function ending() {
    return new Promise((resolve) => {  // Возвращаем Promise
        let text = $('statement').text();
        let elem = document.getElementById('statement');
        let numb = 30;
        let dots = 0;

        function doit() {
            elem.innerText = text + ` Выход через ${Math.ceil(numb / 3)}${'.'.repeat(dots + 1)}`;
            dots = (dots + 1) % 3;
            numb = numb - 1;
            console.log(text + ` Выход через ${Math.ceil(numb / 3)}${'.'.repeat(dots + 1)}`);

            if (numb > 0) {
                setTimeout(doit, 333);
            } else {
                window.location = $SCRIPT_ROOT;
                resolve();  // Говорим, что всё завершено
            }
        }

        doit();
    });
}


function pause(milliseconds) {
    let dt = new Date();
    while ((new Date()) - dt <= milliseconds) { /* Do nothing */
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
