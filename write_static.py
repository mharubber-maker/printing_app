import os

base = '/home/ghazal/printing_app'

files = {}

# ============================================================
files['static/css/tokens.css'] = """:root {
    --gold: #f5a623; --gold-dark: #c9820a; --gold-light: #ffd700;
    --gold-glow: rgba(245,166,35,0.4); --gold-subtle: rgba(245,166,35,0.1);
    --font-family: "Cairo", sans-serif;
    --text-xs: 11px; --text-sm: 13px; --text-base: 15px; --text-lg: 18px; --text-xl: 22px;
    --font-normal: 400; --font-bold: 700; --font-black: 900;
    --space-1:4px; --space-2:8px; --space-3:12px; --space-4:16px; --space-5:20px; --space-6:24px;
    --radius-sm:8px; --radius-md:12px; --radius-lg:16px; --radius-xl:20px; --radius-full:9999px;
    --transition-fast:150ms ease; --transition-base:300ms ease; --transition-slow:500ms ease;
    --shadow-sm:0 2px 8px rgba(0,0,0,0.06); --shadow-md:0 4px 16px rgba(0,0,0,0.10);
    --shadow-lg:0 8px 32px rgba(0,0,0,0.15);
    --shadow-gold:0 4px 20px var(--gold-glow); --shadow-glow:0 0 30px var(--gold-glow);
}
[data-theme="light"] {
    --bg-page:#faf6f0; --bg-card:#ffffff; --bg-card-hover:#fdf8f0;
    --bg-table-head:#fdf8f0; --bg-input:#ffffff; --bg-modal:#ffffff;
    --bg-overlay:rgba(0,0,0,0.6);
    --text-primary:#1a1008; --text-secondary:#555555; --text-muted:#999999;
    --border-color:#e8dcc8; --border-focus:var(--gold);
    --btn-primary-bg:linear-gradient(135deg,var(--gold),var(--gold-light));
    --btn-primary-fg:#1a1008;
    --badge-ongoing-bg:#fff8e8; --badge-ongoing-fg:#c9820a; --badge-ongoing-br:#f5d890;
    --badge-ready-bg:#e8fff5;   --badge-ready-fg:#00aa66;   --badge-ready-br:#90f5cc;
    --badge-done-bg:#e8f0ff;    --badge-done-fg:#4466cc;    --badge-done-br:#99aaee;
    --rainbow:linear-gradient(90deg,#ff0000,#ff8800,#ffff00,#00ff88,#0088ff,#8800ff);
}
[data-theme="dark"] {
    --bg-page:#0d0d1a; --bg-card:rgba(255,255,255,0.03); --bg-card-hover:rgba(255,255,255,0.05);
    --bg-table-head:rgba(0,0,0,0.3); --bg-input:rgba(255,255,255,0.05);
    --bg-modal:#0f0f1a; --bg-overlay:rgba(0,0,0,0.8);
    --text-primary:#ffffff; --text-secondary:rgba(255,255,255,0.6); --text-muted:rgba(255,255,255,0.35);
    --border-color:rgba(255,255,255,0.08); --border-focus:rgba(245,166,35,0.6);
    --btn-primary-bg:rgba(245,166,35,0.12); --btn-primary-fg:var(--gold-light);
    --badge-ongoing-bg:rgba(245,166,35,0.12); --badge-ongoing-fg:var(--gold);   --badge-ongoing-br:rgba(245,166,35,0.3);
    --badge-ready-bg:rgba(0,200,100,0.12);   --badge-ready-fg:#00dd88;          --badge-ready-br:rgba(0,200,100,0.3);
    --badge-done-bg:rgba(99,102,241,0.12);   --badge-done-fg:#818cf8;           --badge-done-br:rgba(99,102,241,0.3);
    --rainbow:linear-gradient(90deg,#ff0000,#ff8800,#ffff00,#00ff88,#0088ff,#8800ff);
}"""

# ============================================================
files['static/css/base.css'] = """*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
body{
    font-family:var(--font-family); background:var(--bg-page);
    color:var(--text-primary); min-height:100vh; padding:var(--space-4);
    direction:rtl; transition:background var(--transition-base),color var(--transition-base);
}
::-webkit-scrollbar{width:6px;}
::-webkit-scrollbar-track{background:var(--bg-card);}
::-webkit-scrollbar-thumb{background:var(--gold);border-radius:var(--radius-full);}
@keyframes fadeInUp{from{opacity:0;transform:translateY(16px);}to{opacity:1;transform:translateY(0);}}
@keyframes fadeIn{from{opacity:0;}to{opacity:1;}}
@keyframes pulseGold{0%,100%{box-shadow:var(--shadow-gold);}50%{box-shadow:0 0 40px rgba(245,166,35,0.7);}}
@keyframes rainbowFlow{0%{background-position:0% 0%;}100%{background-position:200% 0%;}}
@keyframes slideDown{from{opacity:0;transform:translateY(-10px);}to{opacity:1;transform:translateY(0);}}
.anim-fade-up{animation:fadeInUp var(--transition-slow) ease forwards;}
.anim-fade{animation:fadeIn var(--transition-base) ease forwards;}
.anim-slide{animation:slideDown var(--transition-base) ease forwards;}
.delay-1{animation-delay:0.1s;opacity:0;}
.delay-2{animation-delay:0.2s;opacity:0;}
.delay-3{animation-delay:0.3s;opacity:0;}
.rainbow-bar{
    height:3px; background:var(--rainbow);
    background-size:200% 100%;
    animation:rainbowFlow 3s linear infinite;
    border-radius:var(--radius-full);
}"""

# ============================================================
files['static/css/components.css'] = """.card{background:var(--bg-card);border-radius:var(--radius-xl);border:1px solid var(--border-color);box-shadow:var(--shadow-sm);transition:background var(--transition-base),border-color var(--transition-base);}
.btn{display:inline-flex;align-items:center;gap:var(--space-2);padding:10px 18px;border-radius:var(--radius-md);border:none;cursor:pointer;font-family:var(--font-family);font-size:var(--text-sm);font-weight:var(--font-bold);transition:all var(--transition-base);white-space:nowrap;}
.btn-primary{background:var(--btn-primary-bg);color:var(--btn-primary-fg);border:1px solid rgba(245,166,35,0.4);box-shadow:var(--shadow-gold);}
.btn-primary:hover{transform:translateY(-2px);box-shadow:0 6px 25px var(--gold-glow);}
.btn-danger{background:none;color:rgba(255,100,100,0.5);font-size:18px;padding:4px 8px;border:none;cursor:pointer;}
.btn-danger:hover{color:rgba(255,80,80,0.9);}
.badge{display:inline-block;padding:3px 12px;border-radius:var(--radius-full);font-size:var(--text-xs);font-weight:var(--font-bold);border:1px solid transparent;white-space:nowrap;}
.badge-ongoing{background:var(--badge-ongoing-bg);color:var(--badge-ongoing-fg);border-color:var(--badge-ongoing-br);}
.badge-ready{background:var(--badge-ready-bg);color:var(--badge-ready-fg);border-color:var(--badge-ready-br);}
.badge-done{background:var(--badge-done-bg);color:var(--badge-done-fg);border-color:var(--badge-done-br);}
.form-input{width:100%;background:var(--bg-input);border:1px solid var(--border-color);border-radius:var(--radius-md);padding:10px 16px;color:var(--text-primary);font-family:var(--font-family);font-size:var(--text-sm);text-align:right;outline:none;transition:border-color var(--transition-fast),box-shadow var(--transition-fast);}
.form-input:focus{border-color:var(--border-focus);box-shadow:0 0 0 3px rgba(245,166,35,0.12);}
.form-input::placeholder{color:var(--text-muted);}
.form-label{display:block;font-size:var(--text-xs);font-weight:var(--font-bold);color:var(--text-secondary);margin-bottom:var(--space-1);}
.stat-card{border-radius:var(--radius-lg);padding:var(--space-4);position:relative;overflow:hidden;}
.stat-card .stat-num{font-size:36px;font-weight:var(--font-black);line-height:1;}
.stat-card .stat-lbl{font-size:var(--text-xs);color:var(--text-muted);margin-top:var(--space-2);}
.data-table{width:100%;border-collapse:separate;border-spacing:0;}
.data-table .col-headers{background:var(--bg-table-head);}
.data-table .col-th{font-size:var(--text-xs);font-weight:var(--font-bold);color:var(--gold-dark);padding:10px 16px;}
.data-table .data-row{border-bottom:1px solid var(--border-color);transition:background var(--transition-fast);}
.data-table .data-row:hover{background:var(--bg-card-hover);}
.data-table td{padding:12px 16px;}
.modal-overlay{position:fixed;inset:0;background:var(--bg-overlay);backdrop-filter:blur(8px);display:flex;align-items:center;justify-content:center;z-index:50;padding:var(--space-4);animation:fadeIn var(--transition-fast) ease;}
.modal-card{background:var(--bg-modal);border:1px solid var(--border-color);border-radius:var(--radius-xl);box-shadow:var(--shadow-lg);padding:var(--space-6);width:100%;max-width:460px;animation:slideDown var(--transition-base) ease;}
.toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:var(--bg-modal);border:1px solid rgba(245,166,35,0.4);border-radius:var(--radius-lg);padding:12px 24px;font-size:var(--text-sm);font-weight:var(--font-bold);color:var(--text-primary);box-shadow:var(--shadow-gold);z-index:100;animation:fadeInUp var(--transition-base) ease;}
.logo-ring{border-radius:50%;object-fit:cover;border:3px solid var(--gold);box-shadow:var(--shadow-glow);animation:pulseGold 3s ease-in-out infinite;}
.status-select{border:none;border-radius:var(--radius-full);padding:4px 12px;font-family:var(--font-family);font-size:var(--text-xs);font-weight:var(--font-bold);cursor:pointer;outline:none;transition:all var(--transition-fast);}"""

# ============================================================
files['static/js/theme.js'] = """const THEME_KEY = "printing_app_theme";
function getTheme() { return localStorage.getItem(THEME_KEY) || "light"; }
function setTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem(THEME_KEY, theme);
    const btn = document.getElementById("theme-toggle");
    if (btn) btn.textContent = theme === "dark" ? "☀️ Light" : "🌙 Dark";
}
function toggleTheme() { setTheme(getTheme() === "dark" ? "light" : "dark"); }
document.addEventListener("DOMContentLoaded", () => setTheme(getTheme()));"""

# ============================================================
files['static/js/modal.js'] = """function openModal(id="main-modal") {
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
});"""

# ============================================================
files['static/js/utils.js'] = """function calcArea() {
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
}"""

# ============================================================
files['static/js/core.js'] = """document.addEventListener("DOMContentLoaded", () => {
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
});"""

# ============================================================
# كتابة الملفات
for path, content in files.items():
    full_path = os.path.join(base, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    lines = content.count('\n') + 1
    print(f"✅ {lines:3d} سطر ← {path}")

print("\n🎉 كل الملفات اتكتبت بنجاح")
base = '/home/ghazal/printing_app'
