const nameInput = document.querySelector("[name=username]");
const passwordInput = document.querySelector("[name=password]");
const confirmationInput = document.querySelector("[name=confirmation]");
const submitButton = document.querySelector("form button");
submitButton.disabled = true;
confirmationInput.disabled = true;

var checking = false;

const removeGoodInput = (item) => { item.classList.remove("good-input"); item.classList.add("bad-input"); }
const addGoodInput = (item) => { item.classList.add("good-input"); item.classList.remove("bad-input"); }

const checkUsername = async () => {
    console.log("started to check");
    checking = true; 
    var result = await fetch('/username_exists/'+nameInput.value);
    result = await result.json();
    console.log(result);
    console.log("got result");
    if (result.exists) {
        removeGoodInput(nameInput);
    } else {
        addGoodInput(nameInput);
    }
    console.log("done checking");
    checking = false;
}

// checking while typing
nameInput.addEventListener("keyup", function() {
    if (this.value.length > 6) {
        if (!checking) {
            // start checking the database
            checkUsername();
        } else { }
    } else { nameInput.classList.remove("bad-input"); nameInput.classList.remove("good-input"); } 
});

// one last check
nameInput.addEventListener("focusout", function() {
    checkUsername();
});



const pw_conditions = document.querySelector("#password_conditions");
const pw_length_cond = pw_conditions.querySelector("li");
const pw_special_cond = pw_conditions.querySelector("li:nth-child(2)");
const pw_capital_cond = pw_conditions.querySelector("li:nth-child(3)");

const addGood = (item) => {
    item.classList.remove("error_pw");
    item.classList.add("good_pw");
}
const removeGood = (item) => {
    item.classList.remove("good_pw");
    item.classList.add("error_pw");
}

const contains = (text) => {
    var pair = [false, false];
    for (const letter of text) {
        const code = letter.charCodeAt(0);
        if ((code >= 32 && code <= 47) || (code >= 58 && code <= 54) || (code >= 91 && code <= 96)) {
            pair[0] = true;
        }
        if (code >= 65 && code <= 90) {
            pair[1] = true;
        }
        if (pair[0] && pair[1])
            return pair;
    }
    return pair;
}

passwordInput.addEventListener("keyup", function() {
    if (this.value.length > 6) {
        addGood(pw_length_cond);
        const pair = contains(this.value);
        if (pair[0]) { addGood(pw_special_cond) } else { removeGood(pw_special_cond); return; }
        if (pair[1]) { addGood(pw_capital_cond) } else { removeGood(pw_capital_cond); return; }
        confirmationInput.disabled ? confirmationInput.disabled = false : 0; 
    } else {
        removeGood(pw_length_cond);
        removeGood(pw_special_cond);
        removeGood(pw_capital_cond);
        removeGoodInput(confirmationInput);
        confirmationInput.value = "";
        confirmationInput.disabled = true;
    }
});

passwordInput.addEventListener("focusout", function() {
    this.value.length < 6 ? removeGood(pw_length_cond) : 0;
    const pair = contains(this.value);
    !pair[0] ? removeGood(pw_special_cond) : 0;
    !pair[1] ? removeGood(pw_capital_cond) : 0;
    if (pair[0] && pair[1] && this.value.length > 6) {
        confirmationInput.disabled = false;
        submitButton.disabled = false;
    } else { submitButton.disabled = true; }
});

confirmationInput.addEventListener("keyup", function() {
    if (this.value == passwordInput.value) {
        addGoodInput(confirmationInput);
        submitButton.disabled = false;
    } else { removeGoodInput(confirmationInput); !submitButton.disabled ? submitButton.disabled = true : 0}
});
