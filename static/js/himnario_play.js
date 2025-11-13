// Constants
const LYRICS_SYNC_OFFSET_SECONDS = 1; // Offset for lyrics timing synchronization
const LYRICS_UPDATE_INTERVAL_MS = 500; // Interval for checking lyrics updates

// Initialize screenLock variable to null
let screenLock = null;

// Define release function to release screen lock
function release() {
  if (screenLock !== null) {
    screenLock.release().then(() => {
      if (typeof console !== "undefined") {
        console.log("Screen lock released");
      }
    });
    screenLock = null;
  }
}

// Define getScreenLock function to request screen lock
async function getScreenLock() {
  if ("wakeLock" in navigator) {
    try {
      screenLock = await navigator.wakeLock.request("screen");
      if (typeof console !== "undefined") {
        console.log("Screen lock acquired");
      }
    } catch (err) {
      if (typeof console !== "undefined") {
        console.error(`${err.name}, ${err.message}`);
      }
    }
  } else {
    if (typeof console !== "undefined") {
      console.error("Wake Lock API not supported");
    }
  }
}

// Call getScreenLock function to request screen lock
getScreenLock();

// Add event listener to listen for changes in visibility state of document
document.addEventListener("visibilitychange", async () => {
  // If screen lock is not null and document is visible, request screen lock
  if (screenLock !== null && document.visibilityState === "visible") {
    getScreenLock();
  }
});

// Add event listener to listen for end of audio playback
document.getElementById("audio").addEventListener("ended", async () => {
  // Release screen lock and redirect to himnario page
  release();
  window.location.href = "/himnario";
});

const audio = document.getElementById("audio");
const res = lyrics;

let i = 0;

const firstTime = res[0].timeStamp - LYRICS_SYNC_OFFSET_SECONDS;
let hasBreak = false;

// Add a timeupdate event listener to the audio element
audio.addEventListener(
  "timeupdate",
  async () => {
    // Get the current time of the audio in seconds
    const currentTime = Math.floor(audio.currentTime);

    // If the current time matches the timestamp of the first verse, hide the title and themes and show the lyrics
    if (currentTime === firstTime) {
      document.getElementById("title").hidden = true;
      document.getElementById("themes").hidden = true;
      document.getElementById("title-div").style.position = "fixed";
      document.getElementById("lyrics-div").style.position = "relative";
      document.getElementById("lyrics").hidden = false;
    }

    // Set an interval to update the lyrics
    const curInterval = setInterval(async () => {
      // If there are more verses to display and there is no break, check if the current time matches the timestamp of the next verse
      if (i < res.length && !hasBreak) {
        if (currentTime === res[i].timeStamp - LYRICS_SYNC_OFFSET_SECONDS) {
          // Update the lyrics and verse number
          document.getElementById("lyrics").innerHTML = res[i].line.replace(
            /(\.\s+|;\s+|!\s+|\?\s+)/g,
            "$1<br>",
          );
          let verseNumber = res[i].verseNumber;
          if (verseNumber === 0) {
            verseNumber = "Coro";
          }
          document.getElementById("verseno").innerHTML = verseNumber;

          // Move to the next verse
          i += 1;

          // If this is the last verse, show the end icon
          if (i === res.length) {
            document.getElementById("end_icon").hidden = false;
          }
        }
      } else {
        // If there are no more verses or there is a break, clear the interval
        clearInterval(curInterval);
      }
    }, LYRICS_UPDATE_INTERVAL_MS);
  },
  false,
);

// Get a reference to the document
const myDocument = document.documentElement;
// Get a reference to the fullscreen button
const fullScreenButton = document.getElementById("fullscreen-btn");

// Function to toggle fullscreen mode
function toggleFullscreen() {
  const docEl = document.documentElement;
  const isFullscreen =
    document.fullscreenElement ||
    document.webkitFullscreenElement ||
    document.mozFullScreenElement ||
    document.msFullscreenElement;

  // If not in fullscreen mode, request fullscreen
  if (!isFullscreen) {
    if (docEl.requestFullscreen) {
      docEl.requestFullscreen();
    } else if (docEl.webkitRequestFullscreen) {
      docEl.webkitRequestFullscreen();
    } else if (docEl.mozRequestFullScreen) {
      docEl.mozRequestFullScreen();
    } else if (docEl.msRequestFullscreen) {
      docEl.msRequestFullscreen();
    }
  } else {
    // If in fullscreen mode, exit fullscreen
    if (document.exitFullscreen) {
      document.exitFullscreen();
    } else if (document.webkitExitFullscreen) {
      document.webkitExitFullscreen();
    } else if (document.mozCancelFullScreen) {
      document.mozCancelFullScreen();
    } else if (document.msExitFullscreen) {
      document.msExitFullscreen();
    }
  }
}

// Add a click event listener to the fullscreen button
fullScreenButton.addEventListener("click", toggleFullscreen);

// Add a keydown event listener to the document
myDocument.addEventListener("keydown", async (e) => {
  // If the "f" or "F" key is pressed, toggle fullscreen
  if (e.key === "f" || e.key === "F") {
    toggleFullscreen();
  }
  // If the "s" or "S" key is pressed, release the audio and redirect to the hymnario page
  if (e.key === "s" || e.key === "S") {
    release();
    window.location.href = "/himnario";
  }

  // If the "p", "P", or spacebar key is pressed, play or pause the audio
  if (e.key === "p" || e.key === "P" || e.key === " ") {
    play();
  }
});

// Get references to the left, right, and play buttons
const leftButton = document.getElementById("go-back");
const rightButton = document.getElementById("go-forward");
const playButton = document.getElementById("play");

// Initialize a flag to track whether the play button has been clicked before
let firstClick = false;

// Define a function to handle the play button click event
function play() {
  // If this is the first click, play the audio and set the firstClick flag to true
  if (!firstClick) {
    audio.play();
    firstClick = true;
  } else {
    // If this is not the first click, pause the audio and set the firstClick flag to false
    audio.pause();
    firstClick = false;
  }
}

function goBack() {
  // Set the hasBreak flag to true to indicate that there is a break in the lyrics
  hasBreak = true;

  // Hide the title and themes and show the lyrics
  document.getElementById("title").hidden = true;
  document.getElementById("themes").hidden = true;
  document.getElementById("title-div").style.position = "fixed";
  document.getElementById("lyrics-div").style.position = "relative";
  document.getElementById("lyrics").hidden = false;

  // Move to the previous verse
  if (i > 0) {
    i -= 1;
  }

  // Update the lyrics and verse number
  document.getElementById("lyrics").innerHTML = res[i].line.replace(
    /(\.\s+|;\s+|!\s+|\?\s+)/g,
    "$1<br>",
  );
  let verseNumber = res[i].verseNumber;
  if (verseNumber === 0) {
    verseNumber = "Coro";
  }
  document.getElementById("verseno").innerHTML = verseNumber;

  // Show or hide the end icon depending on whether this is the last verse
  if (i + 1 === res.length) {
    document.getElementById("end_icon").hidden = false;
  } else {
    document.getElementById("end_icon").hidden = true;
  }
}

function goForward() {
  // Set the hasBreak flag to true to indicate that there is a break in the lyrics
  hasBreak = true;

  // Hide the title and themes and show the lyrics
  document.getElementById("title").hidden = true;
  document.getElementById("themes").hidden = true;
  document.getElementById("title-div").style.position = "fixed";
  document.getElementById("lyrics-div").style.position = "relative";
  document.getElementById("lyrics").hidden = false;

  // Move to the next verse
  if (i < res.length && firstClick) {
    i += 1;
  } else if (i < res.length && !firstClick) {
    i = 0;
    firstClick = true;
  }

  // Update the lyrics and verse number
  document.getElementById("lyrics").innerHTML = res[i].line.replace(
    /(\.\s+|;\s+|!\s+|\?\s+)/g,
    "$1<br>",
  );
  let verseNumber = res[i].verseNumber;
  if (verseNumber === 0) {
    verseNumber = "Coro";
  }
  document.getElementById("verseno").innerHTML = verseNumber;

  // Show or hide the end icon depending on whether this is the last verse
  if (i + 1 === res.length) {
    document.getElementById("end_icon").hidden = false;
  } else {
    document.getElementById("end_icon").hidden = true;
  }
}

// Add click event listeners to the play, left, and right buttons
playButton.addEventListener("click", play);
leftButton.addEventListener("click", goBack);
rightButton.addEventListener("click", goForward);

// Add keydown event listener to the document
myDocument.addEventListener("keydown", async (e) => {
  // If the left arrow key is pressed, go back
  if (e.key === "ArrowLeft") {
    goBack();
  }
  // If the right arrow key is pressed, go forward
  if (e.key === "ArrowRight") {
    goForward();
  }
});
