const savedRole = localStorage.getItem("userRole");
if (savedRole === "teacher") {
    window.location.href = "/teacher";
} else if (savedRole === "student") {
    window.location.href = "/student";
}

initTheme();

document.getElementById("teacher-btn").addEventListener("click", () => {
    localStorage.setItem("userRole", "teacher");
    window.location.href = "/teacher";
});

document.getElementById("student-btn").addEventListener("click", () => {
    localStorage.setItem("userRole", "student");
    window.location.href = "/student";
});
