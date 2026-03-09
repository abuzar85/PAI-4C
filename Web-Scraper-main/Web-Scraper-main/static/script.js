// ================= LOADER FUNCTIONS =================

function startSingleLoader() {
    const overlay = document.getElementById("loader-overlay");
    const bar = document.getElementById("progress-bar");

    if (!overlay || !bar) return;

    overlay.style.display = "flex";
    bar.style.width = "100%";
}

function startExcelLoader() {
    const overlay = document.getElementById("loader-overlay");
    const bar = document.getElementById("progress-bar");

    if (!overlay || !bar) return;

    overlay.style.display = "flex";

    let progress = 0;

    const interval = setInterval(() => {
        progress += Math.random() * 15;

        if (progress >= 100) {
            progress = 100;
            clearInterval(interval);
        }

        bar.style.width = progress + "%";
    }, 400);
}


// ================= CLEAR RESULTS =================

function clearResults() {
    document.getElementById("results-table")?.remove();
    document.getElementById("action-buttons")?.remove();
    document.getElementById("no-email-message")?.remove();

    const overlay = document.getElementById("loader-overlay");
    const bar = document.getElementById("progress-bar");

    if (overlay) overlay.style.display = "none";
    if (bar) bar.style.width = "0%";
}
