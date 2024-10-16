const video = document.getElementById('videoPlayer');
const playPauseBtn = document.getElementById('playPauseBtn');
const skipBackBtn = document.getElementById('skipBackBtn');
const skipForwardBtn = document.getElementById('skipForwardBtn');
const fullScreenBtn = document.getElementById('fullScreenBtn');

playPauseBtn.addEventListener('click', () => {
    if (video.paused) {
        video.play();
        playPauseBtn.textContent = 'Pause';
    } else {
        video.pause();
        playPauseBtn.textContent = 'Play';
    }
});

skipBackBtn.addEventListener('click', () => {
    video.currentTime -= 10;
});

skipForwardBtn.addEventListener('click', () => {
    video.currentTime += 10;
});

fullScreenBtn.addEventListener('click', () => {
    if (video.requestFullscreen) {
        video.requestFullscreen();
    } else if (video.mozRequestFullScreen) {
        video.mozRequestFullScreen();
    } else if (video.webkitRequestFullscreen) {
        video.webkitRequestFullscreen();
    } else if (video.msRequestFullscreen) {
        video.msRequestFullscreen();
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', (event) => {
    switch(event.code) {
        case 'Space':
            event.preventDefault();
            playPauseBtn.click();
            break;
        case 'ArrowLeft':
            skipBackBtn.click();
            break;
        case 'ArrowRight':
            skipForwardBtn.click();
            break;
    }
});
