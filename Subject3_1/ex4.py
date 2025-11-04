from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "replace-with-a-secure-secret"  # 로컬 테스트용, 실제 서비스에서는 안전하게 설정

@app.route("/", methods=["GET"])
def index():
    return render_template("input.html")

@app.route("/result", methods=["POST"])
def result():
    name = request.form.get("name", "").strip()
    student_number = request.form.get("StudentNumber", "").strip()
    major = request.form.get("Major", "").strip()
    gender = request.form.get("gender", "").strip()
    languages = request.form.getlist("languages")  # 체크박스 여러 값 받기

    missing = []
    if not name:
        missing.append("이름")
    if not student_number:
        missing.append("학번")
    if not major:
        missing.append("전공")
    if not gender:
        missing.append("성별")
    # 프로그래밍 언어는 선택 사항으로 둘 수 있으니 필수로 하려면 아래 검사 추가
    # if not languages:
    #     missing.append("프로그래밍 언어")

    if missing:
        flash("다음 항목을 채워주세요: " + ", ".join(missing))
        return redirect(url_for("index"))

    gender_map = {"M": "남", "F": "여"}
    gender_readable = gender_map.get(gender, gender)

    # languages는 리스트이므로 템플릿에 그대로 전달
    return render_template(
        "result.html",
        name=name,
        student_number=student_number,
        major=major,
        gender=gender_readable,
        languages=languages
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)

