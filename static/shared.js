function escapeHtml(str) {
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;");
}

function showMessage(el, text, type) {
    el.textContent = text;
    el.className = "message text-" + type;
}

function initTheme() {
    const themeToggle = document.getElementById("theme-toggle");
    if (!themeToggle) return;

    function applyTheme(theme) {
        document.documentElement.setAttribute("data-theme", theme);
        localStorage.setItem("theme", theme);
        themeToggle.textContent = theme === "dark" ? "Light mode" : "Dark mode";
        themeToggle.setAttribute("aria-label", theme === "dark" ? "Switch to light mode" : "Switch to dark mode");
    }

    applyTheme(document.documentElement.getAttribute("data-theme") || "light");

    themeToggle.addEventListener("click", () => {
        const next = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
        applyTheme(next);
    });
}

function initSwitchRole() {
    const switchRole = document.getElementById("switch-role");
    if (!switchRole) return;

    switchRole.addEventListener("click", () => {
        localStorage.removeItem("userRole");
        window.location.href = "/";
    });
}
