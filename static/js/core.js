document.addEventListener("DOMContentLoaded", () => {
    // ربط حساب المساحة
    const L = document.getElementById("length-input");
    const W = document.getElementById("width-input");
    if (L) L.addEventListener("input", calcArea);
    if (W) W.addEventListener("input", calcArea);

    // HTMX events
    document.body.addEventListener("htmx:afterRequest", e => {
        const path = e.detail.pathInfo?.requestPath || "";
        if (path === "/orders/add") {
            closeModal();
            resetForm("order-form");
            htmx.ajax("GET", "/stats", {target:"#stats-section", swap:"innerHTML"});
            showToast("✅ تم إضافة الطلب");
        }
        if (path.includes("/status")) {
            htmx.ajax("GET", "/stats", {target:"#stats-section", swap:"innerHTML"});
            showToast("✅ تم تحديث الحالة");
        }
    });
});