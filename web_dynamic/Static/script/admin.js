function hideMessage(messageType) {
    var messageDiv = document.getElementsByClassName(`${messageType}Div`)[0];

    if (messageDiv) {
        messageDiv.classList.remove("visible");
        setTimeout(function () {
            messageDiv.style.display = "none";
        }, 500);
    }
}

function showMessage(messageType) {
    var messageDiv = document.getElementsByClassName(`${messageType}Div`)[0];

    if (messageDiv) {
        messageDiv.style.display = "flex";
        setTimeout(function () {
            messageDiv.classList.add("visible");
        }, 10);
    }
}

var closeIcon = document.getElementById("closeIcon");
if (closeIcon) {
    closeIcon.addEventListener("click", function () {
        hideMessage("success");
        hideMessage("error");
    });
}
function showSideBar() {
    var burgerNav = document.getElementById("burgerNav");
    var sidebar = document.getElementById("sideBar");
    if (burgerNav) {
        burgerNav.addEventListener("click", () => {
            sidebar.style.display = "block";
            sidebar.classList.add("visible");
        });
    }
}

function hideSideBar() {
    var closeIcon = document.getElementById("closeIcon2");
    var sidebar = document.getElementById("sideBar");

    if (closeIcon) {
        closeIcon.addEventListener("click", () => {
            sidebar.classList.remove("visible");
        });
    }
}

showMessage("success");
showMessage("error");
showSideBar();
hideSideBar();
