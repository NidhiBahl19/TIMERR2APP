const timerDisplay = document.querySelector('.timer-display');
const startStopBtn = document.getElementById('startStopBtn');
const resetBtn = document.getElementById('resetBtn');
const lapBtn = document.getElementById('lapBtn');
const lapsList = document.querySelector('.laps');

let startTime;
let updatedTime;
let difference;
let tInterval;
let running = false;
let lapCounter = 0;

function startTimer() {
    if (!running) {
        startTime = new Date().getTime();
        tInterval = setInterval(getShowTime, 1);
        running = true;
        startStopBtn.textContent = 'Stop';
    }
}

function stopTimer() {
    if (running) {
        clearInterval(tInterval);
        running = false;
        startStopBtn.textContent = 'Start';
    }
}

function resetTimer() {
    clearInterval(tInterval);
    running = false;
    startStopBtn.textContent = 'Start';
    timerDisplay.textContent = '00:00:00.000';
    lapsList.innerHTML = '';
    lapCounter = 0;
}

function getShowTime() {
    updatedTime = new Date().getTime();
    difference = updatedTime - startTime;

    let hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    let minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
    let seconds = Math.floor((difference % (1000 * 60)) / 1000);
    let milliseconds = Math.floor((difference % 1000));

    hours = (hours < 10) ? "0" + hours : hours;
    minutes = (minutes < 10) ? "0" + minutes : minutes;
    seconds = (seconds < 10) ? "0" + seconds : seconds;
    milliseconds = (milliseconds < 100) ? (milliseconds < 10 ? "00" + milliseconds : "0" + milliseconds) : milliseconds;

    timerDisplay.textContent = `${hours}:${minutes}:${seconds}.${milliseconds}`;
}

function recordLap() {
    if (running) {
        lapCounter++;
        const li = document.createElement('li');
        li.textContent = `Lap ${lapCounter}: ${timerDisplay.textContent}`;
        lapsList.appendChild(li);
    }
}

startStopBtn.addEventListener('click', () => {
    if (running) {
        stopTimer();
    } else {
        startTimer();
    }
});

resetBtn.addEventListener('click', resetTimer);
lapBtn.addEventListener('click', recordLap);