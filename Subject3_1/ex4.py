from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>Student Info</title>
    </head>
    <body>
        <h2>Student Information Form</h2>
        <form method="POST" action="/result">
            <div>
                <label>Name :</label>
                <input type="text" name="name" required>
            </div>

            <div>
                <label>Student Number :</label>
                <input type="text" name="StudentNumber" required>
            </div>

            <div>
                <label>Major :</label>
                <input type="text" name="Major" required>
            </div>

            <fieldset>
                <legend>Gender</legend>
                <label><input type="radio" name="gender" value="M" required> 남</label>
                <label><input type="radio" name="gender" value="F"> 여</label>
            </fieldset>

            <button type="submit">Submit</button>
        </form>
    </body>
    </html>
    """

@app.route("/result", methods=["POST"])
def result():
    name = request.form.get("name", "").strip()
    student_number = request.form.get("StudentNumber", "").strip()
    major = request.form.get("Major", "").strip()
    gender = request.form.get("gender", "").strip()

    gender_map = {"M": "남", "F": "여"}
    gender_readable = gender_map.get(gender, gender)

    return f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>Result</title>
    </head>
    <body>
        <h2>Submission Result</h2>
        <p><strong>Name:</strong> {name}</p>
        <p><strong>Student Number:</strong> {student_number}</p>
        <p><strong>Major:</strong> {major}</p>
        <p><strong>Gender:</strong> {gender_readable}</p>

        <a href="/">돌아가기</a>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True, port=5000)
