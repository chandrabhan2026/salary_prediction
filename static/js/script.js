// ---------------- LOADING EFFECT ----------------
window.addEventListener("load", function () {
    document.body.classList.add("loaded");
});


// ---------------- FORM VALIDATION ----------------
document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");
    if (form) {
        form.addEventListener("submit", function (e) {

            const exp = document.querySelector("input[name='experience']");
            const edu = document.querySelector("select[name='education']");
            const job = document.querySelector("select[name='job']");

            if (exp && exp.value === "") {
                alert("Please select experience");
                e.preventDefault();
            }

            if (edu && edu.value === "") {
                alert("Please select education");
                e.preventDefault();
            }

            if (job && job.value === "") {
                alert("Please select job role");
                e.preventDefault();
            }

            // Show loading spinner if validation passed
            showLoader();
        });
    }
});


// ---------------- LOADER FUNCTION ----------------
function showLoader() {
    let loader = document.createElement("div");
    loader.id = "loader";
    loader.innerHTML = "Predicting Salary...";
    loader.style.position = "fixed";
    loader.style.top = "50%";
    loader.style.left = "50%";
    loader.style.transform = "translate(-50%, -50%)";
    loader.style.background = "#1f1f1f";
    loader.style.padding = "20px";
    loader.style.borderRadius = "10px";
    loader.style.color = "#00adb5";
    loader.style.boxShadow = "0 0 20px #00adb5";
    document.body.appendChild(loader);
}


// ---------------- SALARY COUNT ANIMATION ----------------
document.addEventListener("DOMContentLoaded", function () {

    const salaryText = document.querySelector(".result-card p");

    if (salaryText) {
        let finalValue = parseFloat(
            salaryText.innerText.replace(/[₹,]/g, "")
        );

        let current = 0;
        let increment = finalValue / 50;

        let counter = setInterval(() => {
            current += increment;
            if (current >= finalValue) {
                salaryText.innerText = "₹ " + finalValue.toLocaleString();
                clearInterval(counter);
            } else {
                salaryText.innerText = "₹ " + Math.floor(current).toLocaleString();
            }
        }, 30);
    }
});


// ---------------- SIDEBAR ACTIVE LINK ----------------
document.addEventListener("DOMContentLoaded", function () {
    let links = document.querySelectorAll(".sidebar a");
    links.forEach(link => {
        if (link.href === window.location.href) {
            link.style.background = "#333";
            link.style.color = "#00adb5";
        }
    });
});