const clockSpan = document.getElementById('time-span');


const Format = (num) => {
    if (num < 10) return '0' + num; else return num;
};

const Clock = () => {
    const now = new Date();
    let hours = now.getHours();
    let minutes = Format(now.getMinutes());
    clockSpan.innerText = `${hours}:${minutes}`;
};

clockInterval = setInterval(Clock, 1000);
