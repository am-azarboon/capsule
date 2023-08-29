// Password hide/show button

const passToggleBtn = document.getElementById("pass-toggle-btn");

if (document.contains(passToggleBtn)) {
    passToggleBtn.addEventListener("click", function() {
        const password = document.getElementById("password");
        if(password.type === "password") {
            password.type = "text";
            passToggleBtn.classList.remove("bi-eye-fill");
            passToggleBtn.classList.add("bi-eye-slash-fill");
        }
        else {
            password.type = "password";
            passToggleBtn.classList.remove("bi-eye-slash-fill");
            passToggleBtn.classList.add("bi-eye-fill");
        }
    })
}

// Choose card/account form
function change_form(e) {
    if (e.target.value === "card") {
        console.log("Credit Card");
    }
    else {
        console.log("Account");
    }
}

// -----------------------------------------------

// Indetify bank type based on card number

// Bank cards' pre number
const bankPreCardNumbers = {
    627412: "بانک اقصاد نوین", 627381: "بانک انصار",
    505785: "بانک ایران زمین", 639347: "بانک پاسارگاد",
    622106: "بانک پارسیان", 846278: "بانک پارسیان", 627884: "بانک پارسیان",
    603799: "بانک ملی ایران", 589210: "بانک سپه",
    627648: "بانک توسعه صادرات", 207177: "بانک توسعه صادرات",
    603770: "بانک کشاورزی", 639217: "بانک کشاورزی",
    628023: "بانک مسکن", 627961: "بانک صنعت و معدن",
    627760: "پست بانک ایران", 502908: "بانک توسعه تعاون",
    502229: "بانک پاسارگاد", 627488: "بانک کارآفرین",
    502910: "بانک کارآفرین", 505416: "بانک گردشگری",
    621986: "بانک سامان", 639346: "بانک سینا",
    639607: "بانک سرمایه", 636214: "بانک تات",
    502806: "بانک شهر", 502706: "بانک شهر",
    502938: "بانک دی", 603769: "بانک صادرات",
    610433: "بانک ملت", 589463: "بانک رفاه",
    991975: "بانک ملت", 636795: "بانک مرکزی",
    385029: "بانک دی", 639370: "بانک مهر اقصاد",
    636949: "بانک حکمت ایرانیان", 628157: "موسسه اعتباری توسعه",
    505801: "موسسه اعتباری کوثر", 606373: "بانک قرض الحسنه مهر ایران",
    5041: "بانک قرض الحسنه رسالت",
}

const cardNumberInput = document.getElementById("card-number");
const bankNameInput = document.getElementById("bank");

if (document.contains(cardNumberInput)) {
    cardNumberInput.addEventListener("input", function(e) {
        input = e.target.value.replaceAll(" ", "");  // Remove all whitespaces
        let converted_input = Number(input);  // Conver number to integer

        if (isNaN(converted_input)){
            input = input.substring(0, input.length - 1);
            cardNumberInput.value = input;
        }
        else {
            // Add bank name at 4 or 6 character input
            if (input.length == 4 || input.length == 6) {
                if (converted_input in bankPreCardNumbers) {
                    bankNameInput.value = bankPreCardNumbers[converted_input];
                }
                else {
                    bankNameInput.value = "";
                }
            }
            else if (input.length == 5 || input.length < 4) {
                bankNameInput.value = "";  // Remove bank name before 6 or 4
            }

            let output = input.replace(/(.{4})/g, "$1 ");  // replace every 4 characters with the same characters plus a space
            output = output.trim();  // remove any whitespace from both ends of the output string
            cardNumberInput.value = output;
        }
    })
}


// Prevent user to input non-number in cvv2 filed
const cvv2Input = document.getElementById("cvv2");

if (document.contains(cvv2Input)) {
    cvv2Input.addEventListener("input", function(e) {
        let input = e.target.value;
        let converted_input = Number(input);  // Conver number to integer

        if (isNaN(converted_input) || input == " "){
            input = input.substring(0, input.length - 1);
            cvv2Input.value = input;
        }
    })
}

// Prevent user to input non-number in month-exp filed
const monthExp = document.getElementById("month-exp");

if (document.contains(monthExp)) {
    monthExp.addEventListener("input", function(e) {
        let input = e.target.value;
        let converted_input = Number(input);  // Conver number to integer

        if (isNaN(converted_input) || input == " "){
            input = input.substring(0, input.length - 1);
            monthExp.value = input;
        }
    })
}

// Prevent user to input non-number in cvv2 filed
const yearExp = document.getElementById("year-exp");

if (document.contains(yearExp)) {
    yearExp.addEventListener("input", function(e) {
        let input = e.target.value;
        let converted_input = Number(input);  // Conver number to integer

        if (isNaN(converted_input) || input == " "){
            input = input.substring(0, input.length - 1);
            yearExp.value = input;
        }
    })
}

// ----------------------------------------------------------