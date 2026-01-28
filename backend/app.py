from flask import Flask, request, jsonify, render_template

from firstProj import (
    students,          # the main dictionary
    load_data,         # to load students on startup
    save_data,         # to persist changes
    addStudent,        # POST /students
    setGrade,          # POST /grades
    removeGrade,       # DELETE /grades
    normalize_name,    # DELETE /students
    getStudentReport,  # GET /students/<name> and /search/<name>
    getRankings,       # GET /rankings
    getSubjectAverage  # GET /subjects/<subject>/average
)

app = Flask(__name__)

students.update(load_data())


@app.route("/")
def home():
    return render_template("index.html")





@app.route("/students", methods=["GET"])
def get_students():
    return jsonify(students)




@app.route("/students", methods=["POST"])
def create_student():
    data = request.json

    # Basic validation
    if not data or "name" not in data:
        return jsonify({
            "success": False,
            "message": "Student name is required"
        }), 400

    result = addStudent(data["name"])
    save_data(students)

    return jsonify(result), 201





@app.route("/grades", methods=["POST"])
def add_grade():
    data = request.json

    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400

    name = data.get("name")
    subject = data.get("subject")
    grades = data.get("grades")

    if not name or not subject or grades is None:
        return jsonify({
            "success": False,
            "message": "Missing required fields"
        }), 400

    result = setGrade(name, subject, grades)
    save_data(students)

    return jsonify(result), 201 if result["success"] else 400




@app.route("/students/<name>", methods=["GET"])
def student_report(name):
    report = getStudentReport(name)
    if not report.get("success"):
        return jsonify(report), 404
    return jsonify(report), 200


@app.route("/reports", methods=["GET"])
def all_student_reports():
    if not students:
        return jsonify({
            "success": False,
            "message": "No students found."
        }), 404

    all_reports = []

    for name in students:
        report = getStudentReport(name)
        if report.get("success"):
            all_reports.append(report)

    return jsonify({
        "success": True,
        "reports": all_reports
    }), 200



@app.route("/rankings", methods=["GET"])
def rankings():
    result = getRankings()
    if not result.get("success"):
        return jsonify(result), 404
    return jsonify(result), 200





@app.route("/grades", methods=["DELETE"])
def delete_grade():
    data = request.json

    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400

    name = data.get("name")
    subject = data.get("subject")
    grade = data.get("grade")

    if not name or not subject or grade is None:
        return jsonify({"success": False, "message": "Missing required fields: name, subject, grade"}), 400

    try:
        grade = float(grade)
    except ValueError:
        return jsonify({"success": False, "message": "Grade must be a number"}), 400

    removeGrade(name, subject, grade)
    save_data(students)

    return jsonify({"success": True, "message": f"Grade {grade} removed from {subject} for {name}"}), 200




@app.route("/students/<name>", methods=["DELETE"])
def delete_student(name):
    name = normalize_name(name)
    if name not in students:
        return jsonify({"success": False, "message": f"Student '{name}' not found."}), 404

    students.pop(name)
    save_data(students)
    return jsonify({"success": True, "message": f"Student '{name}' removed."}), 200




@app.route("/subjects/<subject>/average", methods=["GET"])
def subject_average(subject):
    result = getSubjectAverage(subject)
    if not result.get("success"):
        return jsonify(result), 404
    return jsonify(result), 200




@app.route("/search/<name>", methods=["GET"])
def search_student(name):
    report = getStudentReport(name)
    if not report.get("success"):
        return jsonify(report), 404
    return jsonify(report), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0")

