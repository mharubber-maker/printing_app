function calcArea() {
    const l = parseFloat(document.getElementById("length-input")?.value) || 0;
    const w = parseFloat(document.getElementById("width-input")?.value)  || 0;
    const el = document.getElementById("area-result");
    if (!el) return;
    if (l > 0 && w > 0) {
        const a = l * w;
        el.textContent = (a === Math.floor(a))
            ? Math.floor(a) + " م²"
            : a.toFixed(2) + " م²";
    } else {
        el.textContent = "-- م²";
    }
}
function showToast(msg, ms=3000) {
    const t = document.getElementById("toast");
    if (!t) return;
    t.textContent = msg;
    t.classList.remove("hidden");
    setTimeout(() => t.classList.add("hidden"), ms);
}
function resetForm(id) {
    const f = document.getElementById(id);
    if (f) f.reset();
    const a = document.getElementById("area-result");
    if (a) a.textContent = "-- م²";
}