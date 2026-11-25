const passwordInput = document.querySelector("#id_password");
const passwordToggle = document.querySelector(".password-toggle");

passwordToggle?.addEventListener("click", () => {
    const showingPassword = passwordInput.type === "password";
    passwordInput.type = showingPassword ? "text" : "password";
    passwordToggle.setAttribute("aria-pressed", String(showingPassword));
    passwordToggle.setAttribute(
        "aria-label",
        showingPassword ? "Hide password" : "Show password"
    );
    passwordToggle.innerHTML = showingPassword
        ? '<i class="fa-regular fa-eye-slash" aria-hidden="true"></i>'
        : '<i class="fa-regular fa-eye" aria-hidden="true"></i>';
});
