const loginText = document.querySelector(".title-text .login");
const loginForm = document.querySelector("form.login");
const loginBtn = document.querySelector("label.login");
const signupBtn = document.querySelector("label.signup");
const signupLink = document.querySelector("form .signup-link a");
signupBtn.onclick = () => {
  loginForm.style.marginLeft = "-50%";
  loginText.style.marginLeft = "-50%";
};
loginBtn.onclick = () => {
  loginForm.style.marginLeft = "0%";
  loginText.style.marginLeft = "0%";
};
signupLink.onclick = () => {
  signupBtn.click();
  return false;
};

document.addEventListener("DOMContentLoaded", function () {
  function showError(message) {
    let errorBox = document.querySelector(".error-message");

    // Agar xato xabari hali bo‘lmasa, uni yaratamiz
    if (!errorBox) {
      errorBox = document.createElement("div");
      errorBox.classList.add("error-message");
      document.body.appendChild(errorBox);
    }

    errorBox.innerHTML = `<p>${message}</p>`;
    errorBox.classList.add("show");

    // 5 soniyadan keyin yo‘qolishi
    setTimeout(() => {
      errorBox.classList.add("hide");
      setTimeout(() => {
        errorBox.remove();
      }, 500); // Animatsiya tugaganidan keyin elementni butunlay o‘chirish
    }, 5000);
  }

  document.querySelectorAll("form").forEach(form => {
    form.addEventListener("submit", function (e) {
      let emptyFields = false;

      this.querySelectorAll("input").forEach(input => {
        if (input.type !== "hidden" && input.value.trim() === "") {
          emptyFields = true;
          input.parentElement.classList.add("error");
        }
      });

      if (emptyFields) {
        e.preventDefault();
        showError("Iltimos, barcha maydonlarni to'ldiring!");
      }
    });
  });
});
