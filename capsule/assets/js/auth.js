// Select the alert div element
const alertDiv = document.querySelector("#alert-1");

// Set a timeout function that will hide the alert div after 15 seconds
if (document.contains(alertDiv)) {
  setTimeout(function() {
    alertDiv.style.display = "none";
  }, 10000);
}

// setTimeout function for alertDiv
function alertTimeout() {
  alertDiv.style.display = "block";

  setTimeout(function() {
    alertDiv.style.display = "none";
  }, 10000);
}

// Resend timer section
const ResendBtn = document.getElementById("resend-btn");
const ResendTimer = document.getElementById("resend-timer");

if (document.contains(ResendTimer)) {
  let time = [1, 59, 0];
  let valid_send = false;
  let interval = setInterval(timer, 10);

  // Resend otp-code function
  function send(e) {
    ResendBtn.classList.toggle("hidden");
    ResendTimer.classList.toggle("hidden");
    time[0] = 1;

    alertTimeout();  // Show alertDiv again with timeout
    interval = setInterval(timer, 10);
  }


  // Timer function
  function timer() {
    ResendTimer.innerHTML = "(" + time[0] + ":" + time[1] + ")";
    time[2]++;

    if(time[2] >= 100){
      time[2] = 0;
      --time[1];

      if(time[1] < 0) {
        --time[0];

        if(time[0] < 0){
          clearInterval(interval);
          time[2] = 0;
          valid_send = true;
          ResendBtn.classList.toggle("hidden");
          ResendTimer.classList.toggle("hidden");
        }
        time[1] = 59;
      }
    }
  }

  ResendBtn.addEventListener("click", send);
}
