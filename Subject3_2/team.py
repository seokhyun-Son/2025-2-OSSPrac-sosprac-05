from flask import Flask, request, render_template, url_for, redirect, make_response
import json
import os
import datetime

app = Flask(__name__)

# 팀원 정보를 저장할 JSON 파일 경로
TEAM_JSON_FILE = 'team.json'
# 방문자 데이터를 저장할 파일 경로
VISITS_FILE = 'visits.txt'

def load_visits():
    """visits.txt 파일에서 방문자 데이터를 불러옵니다."""
    if not os.path.exists(VISITS_FILE):
        return {"total_visits": 0, "today_date": datetime.date.today().isoformat(), "today_visits": 0}
    try:
        with open(VISITS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {"total_visits": 0, "today_date": datetime.date.today().isoformat(), "today_visits": 0}

def save_visits(data):
    """방문자 데이터를 visits.txt 파일에 저장합니다."""
    with open(VISITS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

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

    ## 방문자 카운터 로직
    visits_data = load_visits()
    today = datetime.date.today().isoformat()
    
    ## 2. 날짜가 바뀌었는지 확인 (자정이 지나면 오늘 방문자 수 초기화)
    if visits_data['today_date'] != today:
        visits_data['today_date'] = today
        visits_data['today_visits'] = 0
    
    ## 3. 'visited_today' 쿠키 확인 (오늘 처음 방문했는지)
    # 쿠키가 없으면 is_first_visit_today = True
    is_first_visit_today = not request.cookies.get('visited_today')

    if is_first_visit_today:
        # 처음 방문했을 때만 전체 및 오늘 카운터 증가
        visits_data['total_visits'] += 1
        visits_data['today_visits'] += 1
        save_visits(visits_data) # 파일에 데이터 저장

    ## 4. 응답 객체 생성 및 템플릿 렌더링
    # make_response를 사용하여 응답 객체를 만든 후, 쿠키를 추가해야 합니다.
    response = make_response(render_template(
        'index.html', 
        teamMembers=team_members,
        totalVisits=visits_data['total_visits'],  # 전체 방문자 수
        todayVisits=visits_data['today_visits']   # 오늘 방문자 수
        # 만약 테마 기능도 구현했다면, 여기에 currentTheme도 추가해야 합니다.
    ))
    
    ## 5. 오늘 방문했음을 나타내는 쿠키 설정 (자정까지 유지)
    if is_first_visit_today:
        # 오늘 날짜의 23:59:59에 만료되도록 만료 시간 설정
        midnight = datetime.datetime.combine(
            datetime.date.today() + datetime.timedelta(days=1), datetime.time(0, 0)
        )
        expires_at = midnight.timestamp()
        
        # 'visited_today'라는 이름의 쿠키를 자정까지 유효하게 설정
        response.set_cookie('visited_today', 'yes', expires=expires_at)
        
    return response

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