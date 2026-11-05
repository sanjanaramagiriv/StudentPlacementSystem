from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample student records
students = [
    {
        "name": "Rahul",
        "department": "CSE",
        "cgpa": 8.2,
        "aptitude": 75,
        "technical": 80,
        "communication": 70,
        "placed": True,
        "package": 6.0
    },
    {
        "name": "Priya",
        "department": "CSE",
        "cgpa": 9.1,
        "aptitude": 88,
        "technical": 92,
        "communication": 85,
        "placed": True,
        "package": 8.0
    },
    {
        "name": "Arjun",
        "department": "ECE",
        "cgpa": 7.0,
        "aptitude": 60,
        "technical": 65,
        "communication": 58,
        "placed": False,
        "package": 0
    }
]


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            name = request.form["name"].strip()
            department = request.form["department"].strip()
            cgpa = float(request.form["cgpa"])
            aptitude = int(request.form["aptitude"])
            technical = int(request.form["technical"])
            communication = int(request.form["communication"])
            placed = request.form["placed"] == "yes"
            package = float(request.form.get("package", 0) or 0)

            if not name or not department:
                return "Name and department are required.", 400

            if not 0 <= cgpa <= 10:
                return "CGPA must be between 0 and 10.", 400

            if not all(0 <= score <= 100 for score in
                       [aptitude, technical, communication]):
                return "Skill scores must be between 0 and 100.", 400

            if package < 0 or (not placed and package > 0):
                return "Enter a valid package for the placement status.", 400

            students.append({
                "name": name,
                "department": department,
                "cgpa": cgpa,
                "aptitude": aptitude,
                "technical": technical,
                "communication": communication,
                "placed": placed,
                "package": package if placed else 0
            })

            return redirect(url_for("home"))

        except (ValueError, KeyError):
            return "Please enter valid values in all fields.", 400

    total = len(students)
    placed_count = sum(student["placed"] for student in students)
    placement_rate = round(placed_count / total * 100, 1) if total else 0

    packages = [
        student["package"]
        for student in students
        if student["placed"] and student["package"] > 0
    ]
    average_package = round(sum(packages) / len(packages), 2) if packages else 0

    for student in students:
        student["readiness"] = round(
            student["cgpa"] * 4
            + student["aptitude"] * 0.20
            + student["technical"] * 0.25
            + student["communication"] * 0.15,
            1
        )

    return render_template(
        "index.html",
        students=students,
        total=total,
        placed_count=placed_count,
        placement_rate=placement_rate,
        average_package=average_package
    )


if __name__ == "__main__":
    app.run(debug=True)