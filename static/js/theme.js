const THEME_KEY = "printing_app_theme";
function getTheme() { return localStorage.getItem(THEME_KEY) || "light"; }
function setTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem(THEME_KEY, theme);
    const btn = document.getElementById("theme-toggle");
    if (btn) btn.textContent = theme === "dark" ? "☀️ Light" : "🌙 Dark";
}
function toggleTheme() { setTheme(getTheme() === "dark" ? "light" : "dark"); }
document.addEventListener("DOMContentLoaded", () => setTheme(getTheme()));