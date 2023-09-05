// Get specific value from cookies (here is csrftoken)
function get_cookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    let cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
  }
  return cookieValue;
}

let csrftoken = get_cookie("csrftoken");

// ------------------------------------------------------------------------

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

// ---------------------------------------------------------

// Resend timer section
const ResendBtn = document.getElementById("resend-btn");
const ResendTimer = document.getElementById("resend-timer");

if (document.contains(ResendTimer)) {
  let time = [1, 59, 0];
  let timer_stop = false
  let interval = setInterval(timer, 10);

  // Resend otp-code function
  function send(e) {
    if (timer_stop) {
      let url = "/account/resend-code/"

      fetch(url, {
        method: "POST",
        headers: {
          "Content-type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({"send": true})
      }).then((res) => res.json())
          .then(function (data) {
            if (data["status"] === 200) {
              ResendBtn.classList.add("hidden");
              ResendTimer.classList.remove("hidden");

              time[0] = 1;
              timer_stop = false

              alertTimeout();  // Show alertDiv again for 10 sec
              interval = setInterval(timer, 10);
            }
            else {
              window.location = "/account/login/"
            }
          })
    }
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
          timer_stop = true;

          if (ResendBtn.classList.contains("hidden")){
            ResendBtn.classList.remove("hidden");
          }
          ResendTimer.classList.toggle("hidden");
        }
        time[1] = 59;
      }
    }
  }

  ResendBtn.addEventListener("click", send);
}
