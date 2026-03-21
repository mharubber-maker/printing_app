function openModal(id="main-modal") {
    const m = document.getElementById(id);
    if (m) m.classList.remove("hidden");
}
function closeModal(id="main-modal") {
    const m = document.getElementById(id);
    if (m) m.classList.add("hidden");
}
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".modal-overlay").forEach(o => {
        o.addEventListener("click", e => {
            if (e.target === o) o.classList.add("hidden");
        });
    });
});