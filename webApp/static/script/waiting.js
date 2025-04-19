let dots = 0

function update_values() {
    let element = document.getElementById("waiting"); // Найти элемент с id="clock"// Получить текущее время
    element.innerHTML = 'Ищем' + '.'.repeat(dots+1);
    dots = (dots + 1) % 3
    console.log(dots)
    setTimeout(update_values, 1000)
}

window.onload = update_values