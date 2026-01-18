document.write('<button id="timer" class="timer_start" style="position:fixed; top:0.5em; left:1em; color:white; background:none; border:none">Start</button>');
var timer = document.getElementById('timer');
var seconds = 15 * 60;
seconds--;

timer.addEventListener('click',function(){
    timer.disabled = 'disabled';
    setTimeout(displayTime,1000);
});
function displayTime(){
    var min = Math.floor(seconds/60),
        sec = seconds % 60;
    timer.innerHTML = min + ':' + sec;
    seconds--;
    if(seconds >= 0){
        setTimeout(displayTime,1000);
    }   
}