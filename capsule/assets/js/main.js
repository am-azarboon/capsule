// Create dynamic notification click button
const notifBtn = document.getElementById("notif-btn");

if (document.contains(notifBtn)) {
  notifBtn.addEventListener("click", function(){
    const notifMenu = document.getElementById("notif-menu");
    notifMenu.classList.toggle("hidden");
  
    if (notifMenu.classList.contains("hidden")) {
      // Clear notification counts
      document.getElementById("notif-count").innerHTML = "۰";
    }
  })
  
  // Hide opened menus if they are open when not focused
  notifBtn.addEventListener("focusout", function(){
    const notifMenu = document.getElementById("notif-menu");
  
    if (!notifMenu.classList.contains("hidden")) {
      notifMenu.classList.add("hidden");
      // Clear notification counts
      document.getElementById("notif-count").innerHTML = "۰";
    }
  })
}

// --------------------------------------------

// Sidebar section

const navBtn = document.getElementById("toggle");  
const sidebar = document.getElementById("sidebar");

// Open sidebar when click on button
function open_nav() {
  sidebar.classList.toggle("right-[-1000px]");
  navBtn.classList.toggle("right-0");
  navBtn.classList.toggle("right-64");
}

// Hide sidebar when click outside
if (document.contains(sidebar)) {
  document.onclick = function(e) {
    if (!sidebar.contains(e.target) && e.target.id !== "sidebar" && e.target.id !== "toggle") {
      if (!sidebar.classList.contains("right-[-1000px]")) {
        sidebar.classList.add("right-[-1000px]");
        navBtn.classList.toggle("right-64");
        navBtn.classList.toggle("right-0");
      }
    }
  }
}

// Generate random passwords
function generate_pass() {
  const allStrings = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$!?*"

  let randomString = "";
  for (let i = 0; i < 11; i++) {
    const randomStringNumber = Math.floor(1 + Math.random() * (allStrings.length - 1));
    randomString += allStrings.substring(randomStringNumber, randomStringNumber + 1);
  }
  document.getElementById("generate-pass").classList.add("hidden");
  document.getElementById("regenerate-pass").classList.remove("hidden");

  document.getElementById("pass-field").innerHTML = randomString;
}

// -------------------------------------------

// Add to archive button
async function archive(e, pk) {
  $.get(`/dashboard/archive/${pk}/`).then(response =>{
      if(response["response"] === "archived"){
          e.target.classList.toggle("bi-bookmark-fill");
          e.target.classList.toggle("bi-bookmark");
      }
      else{
          e.target.classList.toggle("bi-bookmark-fill");
          e.target.classList.toggle("bi-bookmark");
      }
  })
}

// Convert digits to persian digits
const farsiDigits = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];

let en_digits = document.querySelectorAll('.convert-digits');
for (let dt_el of en_digits) {
    let dt = dt_el.innerHTML || dt_el.value;
    dt_el.innerHTML = dt.toString().replace(/\d/g, x => farsiDigits[x]);
    dt_el.value = dt.toString().replace(/\d/g, x => farsiDigits[x]);
}
