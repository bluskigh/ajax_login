const usernameInput = document.querySelector("form input");
const passwordInput = document.querySelector("input:nth-child(2)");

var checking = false;

function addGood(item) {
    item.classList.add("good-input");
    item.classList.remove("bad-input");
}
function removeGood(item) {
    item.classList.remove("good-input");
    item.classList.add("bad-input");
}

const checkUsername = async () => {
    checking = true;
    var result = await fetch('/username_exists/'+usernameInput.value);
    result = await result.json();
    result.exists ? addGood(usernameInput) : removeGood(usernameInput); 
    checking = false;
}

usernameInput.addEventListener("keyup", function() {
    this.value.length > 6 ? !checking ? checkUsername() : 0 : removeGood(username);
});
usernameInput.addEventListener("focusout", function() {
    checkUsername();
});

passwordInput.addEventListener("keyup", function() {
});
passwordInput.addEventListener("focusout", function() {
});

