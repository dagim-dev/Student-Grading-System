initTheme();
initSwitchRole();

document.getElementById("add-student-btn").addEventListener("click", async () => {
    const name = document.getElementById("student-name").value.trim();
    const msgEl = document.getElementById("student-message");

    if (!name) return showMessage(msgEl, "Name cannot be empty!", "error");

    try {
        const res = await fetch("/students", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({name})
        });
        const data = await res.json();
        showMessage(msgEl, data.message, data.success ? "success" : "error");
        document.getElementById("student-name").value = "";
        refreshRankings();
    } catch { showMessage(msgEl, "Error connecting to server.", "error"); }
});

document.getElementById("delete-student-btn").addEventListener("click", async () => {
    const name = document.getElementById("student-name").value.trim();
    const msgEl = document.getElementById("student-message");

    if (!name) return showMessage(msgEl, "Name cannot be empty!", "error");

    try {
        const res = await fetch(`/students/${encodeURIComponent(name)}`, {method: "DELETE"});
        const data = await res.json();
        showMessage(msgEl, data.message, data.success ? "success" : "error");
        document.getElementById("student-name").value = "";
        refreshRankings();
    } catch { showMessage(msgEl, "Error connecting to server.", "error"); }
});

document.getElementById("add-grade-btn").addEventListener("click", async () => {
    const name = document.getElementById("grade-student-name").value.trim();
    const subject = document.getElementById("grade-subject").value.trim();
    const gradesStr = document.getElementById("grade-values").value.trim();
    const msgEl = document.getElementById("grade-message");

    if (!name || !subject || !gradesStr) return showMessage(msgEl, "All fields required!", "error");

    const grades = gradesStr.split(",").map(g => parseFloat(g.trim())).filter(g => !isNaN(g));
    if (grades.length === 0) return showMessage(msgEl, "Enter valid numeric grades!", "error");

    try {
        const res = await fetch("/grades", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({name, subject, grades})
        });
        const data = await res.json();
        showMessage(msgEl, data.message, data.success ? "success" : "error");
        document.getElementById("grade-student-name").value = "";
        document.getElementById("grade-subject").value = "";
        document.getElementById("grade-values").value = "";
        refreshRankings();
    } catch { showMessage(msgEl, "Error connecting to server.", "error"); }
});

document.getElementById("delete-grade-btn").addEventListener("click", async () => {
    const name = document.getElementById("grade-student-name").value.trim();
    const subject = document.getElementById("grade-subject").value.trim();
    const gradesStr = document.getElementById("grade-values").value.trim();
    const msgEl = document.getElementById("grade-message");

    if (!name || !subject || !gradesStr) return showMessage(msgEl, "All fields required!", "error");

    const grades = gradesStr.split(",").map(g => parseFloat(g.trim())).filter(g => !isNaN(g));
    if (grades.length === 0) return showMessage(msgEl, "Enter valid numeric grades!", "error");

    try {
        const res = await fetch("/grades", {
            method: "DELETE",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({name, subject, grades})
        });
        const data = await res.json();
        showMessage(msgEl, data.message, data.success ? "success" : "error");
        document.getElementById("grade-student-name").value = "";
        document.getElementById("grade-subject").value = "";
        document.getElementById("grade-values").value = "";
        refreshRankings();
    } catch { showMessage(msgEl, "Error connecting to server.", "error"); }
});

document.getElementById("view-all-reports-btn").addEventListener("click", async () => {
    const container = document.getElementById("all-reports-container");
    container.innerHTML = "";

    try {
        const res = await fetch("/reports");
        const data = await res.json();

        if (!data.success) {
            container.innerHTML = `<p class="text-error">${escapeHtml(data.message)}</p>`;
            return;
        }

        let html = "";

        for (const report of data.reports) {
            html += `<h3>${escapeHtml(report.name)}</h3>`;
            html += `
                <table>
                    <tr>
                        <th>Subject</th>
                        <th>Grades</th>
                        <th>Average</th>
                        <th>Letter</th>
                    </tr>
            `;

            for (const [subject, info] of Object.entries(report.subjects)) {
                html += `
                    <tr>
                        <td>${escapeHtml(subject)}</td>
                        <td>${escapeHtml(info.grades.join(", "))}</td>
                        <td>${escapeHtml(info.average)}</td>
                        <td>${escapeHtml(info.letter)}</td>
                    </tr>
                `;
            }

            if (report.overall_average !== null) {
                html += `
                    <tr style="font-weight:bold">
                        <td colspan="2">Overall</td>
                        <td>${escapeHtml(report.overall_average)}</td>
                        <td>${escapeHtml(report.overall_letter)}</td>
                    </tr>
                `;
            }

            html += `</table><hr>`;
        }

        container.innerHTML = html;

    } catch {
        container.innerHTML = "<p class='text-error'>Server error.</p>";
    }
});

document.getElementById("view-report-btn").addEventListener("click", async () => {
    const name = document.getElementById("report-student-name").value.trim();
    const container = document.getElementById("report-container");
    container.innerHTML = "";
    if (!name) return container.innerHTML = `<p class="text-error">Enter a student name!</p>`;

    try {
        const res = await fetch(`/students/${encodeURIComponent(name)}`);
        const data = await res.json();
        if (!data.success) return container.innerHTML = `<p class="text-error">${escapeHtml(data.message)}</p>`;

        let html = `<h3>${escapeHtml(data.name)}'s Report</h3>`;
        html += "<table><tr><th>Subject</th><th>Grades</th><th>Average</th><th>Letter</th></tr>";
        for (const [subject, info] of Object.entries(data.subjects)) {
            html += `<tr>
                <td>${escapeHtml(subject)}</td>
                <td>${escapeHtml(info.grades.join(", "))}</td>
                <td>${escapeHtml(info.average)}</td>
                <td>${escapeHtml(info.letter)}</td>
            </tr>`;
        }
        if (data.overall_average !== null) {
            html += `<tr style="font-weight:bold">
                <td colspan="2">Overall</td>
                <td>${escapeHtml(data.overall_average)}</td>
                <td>${escapeHtml(data.overall_letter)}</td>
            </tr>`;
        }
        html += "</table>";
        container.innerHTML = html;

    } catch { container.innerHTML = "<p class='text-error'>Error connecting to server.</p>"; }
});

document.getElementById("view-rankings-btn").addEventListener("click", refreshRankings);

async function refreshRankings() {
    const container = document.getElementById("rankings-container");
    container.innerHTML = "";
    try {
        const res = await fetch("/rankings");
        const data = await res.json();
        if (!data.success) return container.innerHTML = `<p class="text-error">${escapeHtml(data.message)}</p>`;

        let html = "<table><tr><th>Rank</th><th>Name</th><th>Average</th><th>Letter</th></tr>";
        for (const student of data.rankings) {
            html += `<tr>
                <td>${escapeHtml(student.rank)}</td>
                <td>${escapeHtml(student.name)}</td>
                <td>${escapeHtml(student.average)}</td>
                <td>${escapeHtml(student.letter)}</td>
            </tr>`;
        }
        html += "</table>";
        container.innerHTML = html;

    } catch { container.innerHTML = "<p class='text-error'>Error connecting to server.</p>"; }
}

document.getElementById("view-subject-average-btn").addEventListener("click", async () => {
    const subject = document.getElementById("average-subject-name").value.trim();
    const container = document.getElementById("subject-average-container");
    container.innerHTML = "";
    if (!subject) return container.innerHTML = `<p class="text-error">Enter a subject!</p>`;

    try {
        const res = await fetch(`/subjects/${encodeURIComponent(subject)}/average`);
        const data = await res.json();
        if (!data.success) return container.innerHTML = `<p class="text-error">${escapeHtml(data.message)}</p>`;

        container.innerHTML = `<p>Average for <strong>${escapeHtml(data.subject)}</strong>: ${escapeHtml(data.average)} (${escapeHtml(data.letter)})</p>`;
    } catch { container.innerHTML = "<p class='text-error'>Error connecting to server.</p>"; }
});

refreshRankings();
