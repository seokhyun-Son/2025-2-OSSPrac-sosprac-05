from flask import Flask, request, render_template, url_for, redirect
import json
import os

app = Flask(__name__)

# 팀원 정보를 저장할 JSON 파일 경로
TEAM_JSON_FILE = 'team.json'

def load_members():
    """team.json 파일에서 팀원 목록을 불러옵니다."""
    if not os.path.exists(TEAM_JSON_FILE):
        return []
    try:
        with open(TEAM_JSON_FILE, 'r', encoding='utf-8') as f:
            members = json.load(f)
            return members
    except json.JSONDecodeError:
        return []

def save_members(members):
    """팀원 목록을 team.json 파일에 저장합니다."""
    with open(TEAM_JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(members, f, ensure_ascii=False, indent=4)


# 1. '/' (메인 페이지) 
@app.route('/')
def index():
    team_members = load_members()
    # 팀장을 항상 맨 위로 정렬
    team_members.sort(key=lambda x: x['role'] != '팀장')
    return render_template('index.html', teamMembers=team_members)

# 2. '/input' (입력 페이지) 
@app.route('/input')
def input_page():
    return render_template('input.html')

# 김지훈 소개 홈페이지
@app.route('/kimjihun')
def kimjihun():
    return render_template('kimjihun.html')

# 장승열 소개 홈페이지
@app.route('/jang')
def jang():
    return render_template('jang.html')

# 나서윤 소개 홈페이지
@app.route('/na')
def na():
    return render_template('na.html')

# 손석현 소개 홈페이지
@app.route('/son')
def son():
    return render_template('son.html')

# 3. '/result' (결과 처리) 수정
@app.route('/result', methods=['POST'])
def result():
    # 폼에서 정보 가져오기 (기존과 동일)
    names = request.form.getlist('name[]')
    majors = request.form.getlist('major[]')
    roles = [request.form.get(f'role_{i}') for i in range(len(names))]
    phones = request.form.getlist('phone[]')
    email_locals = request.form.getlist('emailLocal[]')
    email_domains = request.form.getlist('emailDomain[]')

    # 현재 저장된 멤버 목록 불러오기
    team_members = load_members()

    # 새로 입력받은 멤버 정보 추가하기
    for i, (name, major, role, phone, email_local, email_domain) in enumerate(
            zip(names, majors, roles, phones, email_locals, email_domains)):

        if role == '팀장':
            profile_picture_url = url_for('static', filename='leader.png')
        else:
            profile_picture_url = url_for('static', filename='member.png')

        member = {
            'name': name,
            'major': major,
            'role': role,
            'phone': phone,
            'email': f"{email_local}@{email_domain}",
            'profilePicture': profile_picture_url
            # TODO: 필요하다면 여기에 '취미', '깃허브' 등도 추가
        }
        team_members.append(member) 


    save_members(team_members)

    # '새로고침' (메인 페이지로 리다이렉트)
    return redirect(url_for('index'))


# 4. '/contact' (비상 연락처) 
@app.route('/contact')
def contact():
    # URL에서 이메일과 전화번호 정보 가져오기
    email = request.args.get('email')
    phone = request.args.get('phone')

    # contact.html에 이메일과 전화번호 정보를 전달하여 렌더링
    return render_template('contact.html', email=email, phone=phone)


@app.route('/emergency')
def emergency_contact():
    name = "비상연락처"
    email = "emergency@email.com"
    phone = "010-9876-5432"
    
    return render_template('contact.html', name=name, email=email, phone=phone)

if __name__ == '__main__':
    app.run(debug=True)