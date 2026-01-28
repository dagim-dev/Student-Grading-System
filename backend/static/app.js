const API_BASE = "http://127.0.0.1:5000";


// --- Add Student ---
document.getElementById("add-student-btn").addEventListener("click", async () => {
    const name = document.getElementById("student-name").value.trim();
    const msgEl = document.getElementById("student-message");

    if (!name) return showMessage(msgEl, "Name cannot be empty!", "red");

    try {
        const res = await fetch(`${API_BASE}/students`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({name})
        });
        const data = await res.json();
        showMessage(msgEl, data.message, data.success ? "green" : "red");
        document.getElementById("student-name").value = "";
        refreshRankings();
    } catch { showMessage(msgEl, "Error connecting to server.", "red"); }
});

// --- Delete Student ---
document.getElementById("delete-student-btn").addEventListener("click", async () => {
    const name = document.getElementById("student-name").value.trim();
    const msgEl = document.getElementById("student-message");

    if (!name) return showMessage(msgEl, "Name cannot be empty!", "red");

    try {
        const res = await fetch(`${API_BASE}/students/${name}`, {method: "DELETE"});
        const data = await res.json();
        showMessage(msgEl, data.message, data.success ? "green" : "red");
        document.getElementById("student-name").value = "";
        refreshRankings();
    } catch { showMessage(msgEl, "Error connecting to server.", "red"); }
});

// --- Add Grades ---
document.getElementById("add-grade-btn").addEventListener("click", async () => {
    const name = document.getElementById("grade-student-name").value.trim();
    const subject = document.getElementById("grade-subject").value.trim();
    const gradesStr = document.getElementById("grade-values").value.trim();
    const msgEl = document.getElementById("grade-message");

    if (!name || !subject || !gradesStr) return showMessage(msgEl, "All fields required!", "red");

    const grades = gradesStr.split(",").map(g => parseFloat(g.trim())).filter(g => !isNaN(g));
    if (grades.length === 0) return showMessage(msgEl, "Enter valid numeric grades!", "red");

    try {
        const res = await fetch(`${API_BASE}/grades`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({name, subject, grades})
        });
        const data = await res.json();
        showMessage(msgEl, data.message, data.success ? "green" : "red");
        document.getElementById("grade-student-name").value = "";
        document.getElementById("grade-subject").value = "";
        document.getElementById("grade-values").value = "";
        refreshRankings();
    } catch { showMessage(msgEl, "Error connecting to server.", "red"); }
});

// --- Delete Grade ---
document.getElementById("delete-grade-btn").addEventListener("click", async () => {
    const name = document.getElementById("grade-student-name").value.trim();
    const subject = document.getElementById("grade-subject").value.trim();
    const gradesStr = document.getElementById("grade-values").value.trim();
    const msgEl = document.getElementById("grade-message");

    if (!name || !subject || !gradesStr) return showMessage(msgEl, "All fields required!", "red");

    const grades = gradesStr.split(",").map(g => parseFloat(g.trim())).filter(g => !isNaN(g));
    if (grades.length === 0) return showMessage(msgEl, "Enter valid numeric grades!", "red");

    try {
        for (const grade of grades) {
            const res = await fetch(`${API_BASE}/grades`, {
                method: "DELETE",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({name, subject, grade})
            });
            await res.json();
        }
        showMessage(msgEl, "Grades deleted successfully", "green");
        document.getElementById("grade-student-name").value = "";
        document.getElementById("grade-subject").value = "";
        document.getElementById("grade-values").value = "";
        refreshRankings();
    } catch { showMessage(msgEl, "Error connecting to server.", "red"); }
});


document.getElementById("view-all-reports-btn")
    .addEventListener("click", async () => {

    const container = document.getElementById("all-reports-container");
    container.innerHTML = "";

    try {
        const res = await fetch(`${API_BASE}/reports`);
        const data = await res.json();

        if (!data.success) {
            container.innerHTML = `<p style="color:red">${data.message}</p>`;
            return;
        }

        let html = "";

        for (const report of data.reports) {
            html += `<h3>${report.name}</h3>`;
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
                        <td>${subject}</td>
                        <td>${info.grades.join(", ")}</td>
                        <td>${info.average}</td>
                        <td>${info.letter}</td>
                    </tr>
                `;
            }

            if (report.overall_average !== null) {
                html += `
                    <tr style="font-weight:bold">
                        <td colspan="2">Overall</td>
                        <td>${report.overall_average}</td>
                        <td>${report.overall_letter}</td>
                    </tr>
                `;
            }

            html += `</table><hr>`;
        }

        container.innerHTML = html;

    } catch {
        container.innerHTML = "<p style='color:red'>Server error.</p>";
    }
});




// --- View Student Report ---
document.getElementById("view-report-btn").addEventListener("click", async () => {
    const name = document.getElementById("report-student-name").value.trim();
    const container = document.getElementById("report-container");
    container.innerHTML = "";
    if (!name) return container.innerHTML = `<p style="color:red">Enter a student name!</p>`;

    try {
        const res = await fetch(`${API_BASE}/students/${name}`);
        const data = await res.json();
        if (!data.success) return container.innerHTML = `<p style="color:red">${data.message}</p>`;

        let html = `<h3>${data.name}'s Report</h3>`;
        html += "<table><tr><th>Subject</th><th>Grades</th><th>Average</th><th>Letter</th></tr>";
        for (const [subject, info] of Object.entries(data.subjects)) {
            html += `<tr>
                <td>${subject}</td>
                <td>${info.grades.join(", ")}</td>
                <td>${info.average}</td>
                <td>${info.letter}</td>
            </tr>`;
        }
        if (data.overall_average !== null) {
            html += `<tr style="font-weight:bold">
                <td colspan="2">Overall</td>
                <td>${data.overall_average}</td>
                <td>${data.overall_letter}</td>
            </tr>`;
        }
        html += "</table>";
        container.innerHTML = html;

    } catch { container.innerHTML = "<p style='color:red'>Error connecting to server.</p>"; }
});

// --- View Rankings ---
document.getElementById("view-rankings-btn").addEventListener("click", refreshRankings);
async function refreshRankings() {
    const container = document.getElementById("rankings-container");
    container.innerHTML = "";
    try {
        const res = await fetch(`${API_BASE}/rankings`);
        const data = await res.json();
        if (!data.success) return container.innerHTML = `<p style="color:red">${data.message}</p>`;

        let html = "<table><tr><th>Rank</th><th>Name</th><th>Average</th><th>Letter</th></tr>";
        for (const student of data.rankings) {
            html += `<tr>
                <td>${student.rank}</td>
                <td>${student.name}</td>
                <td>${student.average}</td>
                <td>${student.letter}</td>
            </tr>`;
        }
        html += "</table>";
        container.innerHTML = html;

    } catch { container.innerHTML = "<p style='color:red'>Error connecting to server.</p>"; }
}

// --- View Subject Average ---
document.getElementById("view-subject-average-btn").addEventListener("click", async () => {
    const subject = document.getElementById("average-subject-name").value.trim();
    const container = document.getElementById("subject-average-container");
    container.innerHTML = "";
    if (!subject) return container.innerHTML = `<p style="color:red">Enter a subject!</p>`;

    try {
        const res = await fetch(`${API_BASE}/subjects/${subject}/average`);
        const data = await res.json();
        if (!data.success) return container.innerHTML = `<p style="color:red">${data.message}</p>`;

        container.innerHTML = `<p>Average for <strong>${data.subject}</strong>: ${data.average} (${data.letter})</p>`;
    } catch { container.innerHTML = "<p style='color:red'>Error connecting to server.</p>"; }
});

// --- Utility function ---
function showMessage(el, text, color) {
    el.textContent = text;
    el.style.color = color;
}

// --- Initial load ---
refreshRankings();
