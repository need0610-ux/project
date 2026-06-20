# Backend README

## 1. 프로젝트 개요

본 백엔드는 정기예금 추천 서비스의 API 서버입니다.  
Django와 Django REST Framework를 기반으로 구현했으며, 금융감독원 정기예금 API, 한국수출입은행 환율 API, 카카오 로컬 API를 연동합니다.

주요 기능은 다음과 같습니다.

- 정기예금 상품 데이터 저장 및 조회
- 회원가입, 로그인, 로그아웃, 프로필 조회
- 관심상품 추가/삭제 및 목록 조회
- 주거래은행 추천 기능
- 게시판 및 댓글 기능
- 환율 조회 및 환율 계산
- 금융 용어/상품 설명 챗봇
- 카카오 로컬 API 기반 은행 지점 검색

---

## 2. 기술 스택

| 구분 | 기술 |
|---|---|
| Language | Python |
| Framework | Django |
| API | Django REST Framework |
| Database | SQLite |
| External API | 금융감독원 금융상품 API, 한국수출입은행 환율 API, 카카오 로컬 API |
| Auth | Django 기본 User, Session/Basic Authentication |
| Environment | python-dotenv |

---

## 3. 프로젝트 구조

```text
backend/
├─ accounts/           # 회원가입, 로그인, 프로필
├─ products/           # 정기예금 상품 저장/조회
├─ favorites/          # 관심상품
├─ recommendations/    # 주거래은행 추천
├─ community/          # 게시판, 댓글
├─ exchanges/          # 환율 조회, 환율 계산
├─ chatbot/            # 금융용어 및 상품 설명 챗봇
├─ maps/               # 카카오 로컬 API 기반 은행 지점 검색
├─ config/             # Django 설정
├─ manage.py
├─ requirements.txt
├─ .env.example
└─ README.md
```

---

## 4. 실행 방법

### 4-1. 백엔드 폴더 이동

```bash
cd backend
```

### 4-2. 가상환경 생성

```bash
python -m venv venv
```

### 4-3. 가상환경 활성화

Git Bash 기준:

```bash
source venv/Scripts/activate
```

PowerShell 기준:

```powershell
venv\Scripts\activate
```

정상적으로 활성화되면 터미널 앞에 `(venv)`가 표시됩니다.

### 4-4. 패키지 설치

```bash
pip install -r requirements.txt
```

### 4-5. 마이그레이션 실행

```bash
python manage.py migrate
```

### 4-6. 서버 실행

```bash
python manage.py runserver
```

서버 실행 후 아래 주소로 접속합니다.

```text
http://127.0.0.1:8000/
```

---

## 5. 환경변수 설정

실제 API 키는 `.env` 파일에 저장합니다.  
`.env` 파일은 GitHub에 올리지 않습니다.

### 5-1. `.env` 파일 생성

`backend/.env` 파일을 생성하고 아래 내용을 작성합니다.

```env
FSS_API_KEY=금융감독원_금융상품_API_KEY
EXCHANGE_API_KEY=한국수출입은행_환율_API_KEY
KAKAO_REST_API_KEY=카카오_REST_API_KEY
```

### 5-2. `.env.example`

GitHub에는 실제 키 대신 `.env.example`을 올립니다.

```env
FSS_API_KEY=your_fss_api_key
EXCHANGE_API_KEY=your_exchange_api_key
KAKAO_REST_API_KEY=your_kakao_rest_api_key
```

### 5-3. `.gitignore`

```gitignore
.env
venv/
__pycache__/
*.pyc
db.sqlite3
```

---

## 6. 주요 앱 설명

### 6-1. products

금융감독원 정기예금 API를 호출하여 정기예금 상품 정보를 DB에 저장하고 조회합니다.

주요 모델:

- `Bank`
- `FinancialProduct`
- `ProductOption`

주요 기능:

- 정기예금 데이터 저장
- 정기예금 상품 목록 조회
- 정기예금 상품 상세 조회
- 상품별 금리 옵션 조회

---

### 6-2. accounts

Django 기본 User 모델을 사용하여 회원 기능을 구현했습니다.  
사용자는 이메일이 아닌 직접 정한 아이디인 `username`으로 로그인합니다.

주요 기능:

- 회원가입
- 로그인
- 로그아웃
- 프로필 조회

---

### 6-3. favorites

로그인한 사용자가 정기예금 상품을 관심상품으로 저장하거나 삭제할 수 있습니다.

주요 기능:

- 관심상품 추가
- 관심상품 삭제
- 내 관심상품 목록 조회

---

### 6-4. recommendations

사용자의 금융 성향 응답을 바탕으로 주거래은행을 추천합니다.  
현재는 규칙 기반 추천 로직으로 구현했습니다.

주요 기능:

- 주거래은행 추천
- 추천 이력 저장
- 내 추천 이력 조회

---

### 6-5. community

게시판과 댓글 기능을 제공합니다.

주요 기능:

- 게시글 목록 조회
- 게시글 작성
- 게시글 상세 조회
- 게시글 수정
- 게시글 삭제
- 댓글 작성
- 댓글 삭제

---

### 6-6. exchanges

한국수출입은행 환율 API를 이용하여 환율 정보를 조회하고 원화 기준 환율 계산을 수행합니다.

주요 기능:

- 환율 목록 조회
- 원화 금액을 선택한 통화 기준으로 환산

---

### 6-7. chatbot

금융 용어 설명과 정기예금 상품 설명을 제공하는 챗봇 API입니다.

주요 기능:

- 금융 용어 설명
- 상품명 기반 정기예금 쉬운 설명
- 은행명 기반 상품 후보 안내

현재는 규칙 기반으로 구현했으며, 추후 AI API를 연동할 수 있도록 확장 가능합니다.

---

### 6-8. maps

카카오 로컬 API를 이용하여 은행 지점을 검색합니다.  
프론트엔드에서는 응답으로 받은 위도/경도 정보를 이용해 카카오맵에 마커를 표시할 수 있습니다.

주요 기능:

- 은행명 기반 지점 검색
- 지역명 + 은행명 기반 지점 검색
- 현재 위치 기준 주변 은행 검색

---

## 7. API 명세 요약

### 7-1. accounts

| Method | URL | 설명 | 인증 |
|---|---|---|---|
| POST | `/api/accounts/signup/` | 회원가입 | 불필요 |
| POST | `/api/accounts/login/` | 로그인 | 불필요 |
| POST | `/api/accounts/logout/` | 로그아웃 | 필요 |
| GET | `/api/accounts/profile/` | 내 정보 조회 | 필요 |

#### 회원가입 요청 예시

```json
{
  "username": "testuser",
  "password": "1234",
  "password_confirm": "1234",
  "email": "test@test.com"
}
```

#### 로그인 요청 예시

```json
{
  "username": "testuser",
  "password": "1234"
}
```

---

### 7-2. products

| Method | URL | 설명 | 인증 |
|---|---|---|---|
| GET | `/api/products/deposits/save/` | 금감원 정기예금 데이터 저장/갱신 | 불필요 |
| GET | `/api/products/deposits/` | 정기예금 상품 목록 조회 | 불필요 |
| GET | `/api/products/deposits/<product_id>/` | 정기예금 상품 상세 조회 | 불필요 |

#### 정기예금 데이터 저장 응답 예시

```json
{
  "message": "정기예금 상품 저장 완료",
  "saved_banks": 0,
  "saved_products": 0,
  "saved_options": 0,
  "total_base_count": 38,
  "total_option_count": 120
}
```

`save` API는 관리자/개발자용 데이터 갱신 API입니다.  
이미 저장된 상품은 중복 생성하지 않고 `update_or_create` 방식으로 갱신합니다.

---

### 7-3. favorites

| Method | URL | 설명 | 인증 |
|---|---|---|---|
| GET | `/api/favorites/` | 내 관심상품 목록 조회 | 필요 |
| POST | `/api/favorites/<product_id>/` | 관심상품 추가/삭제 토글 | 필요 |

#### 관심상품 추가 응답 예시

```json
{
  "message": "관심상품에 추가되었습니다.",
  "is_favorite": true
}
```

#### 관심상품 삭제 응답 예시

```json
{
  "message": "관심상품에서 삭제되었습니다.",
  "is_favorite": false
}
```

---

### 7-4. recommendations

| Method | URL | 설명 | 인증 |
|---|---|---|---|
| POST | `/api/recommendations/main-bank/` | 주거래은행 추천 | 필요 |
| GET | `/api/recommendations/history/` | 내 추천 이력 조회 | 필요 |

#### 주거래은행 추천 요청 예시

```json
{
  "access_preference": "mobile",
  "benefit_preference": "high_interest",
  "stability_preference": "internet_bank",
  "usage_purpose": "interest"
}
```

#### 응답 예시

```json
{
  "id": 1,
  "access_preference": "mobile",
  "benefit_preference": "high_interest",
  "stability_preference": "internet_bank",
  "usage_purpose": "interest",
  "recommended_bank": 3,
  "recommended_bank_name": "카카오뱅크",
  "reason": "모바일 접근성을 중요하게 생각하는 성향으로 보입니다. 비대면 가입과 앱 사용 편의성을 고려해 인터넷은행 계열 상품이 잘 맞을 수 있습니다.",
  "created_at": "2026-06-20T..."
}
```

---

### 7-5. community

| Method | URL | 설명 | 인증 |
|---|---|---|---|
| GET | `/api/community/` | 게시글 목록 조회 | 불필요 |
| POST | `/api/community/` | 게시글 작성 | 필요 |
| GET | `/api/community/<post_id>/` | 게시글 상세 조회 | 불필요 |
| PUT | `/api/community/<post_id>/` | 게시글 수정 | 작성자 필요 |
| DELETE | `/api/community/<post_id>/` | 게시글 삭제 | 작성자 필요 |
| POST | `/api/community/<post_id>/comments/` | 댓글 작성 | 필요 |
| DELETE | `/api/community/comments/<comment_id>/` | 댓글 삭제 | 작성자 필요 |

#### 게시글 작성 요청 예시

```json
{
  "title": "정기예금 가입 전에 뭘 봐야 하나요?",
  "content": "금리 말고도 우대조건이나 가입기간을 봐야 하는지 궁금합니다.",
  "category": "product"
}
```

#### 댓글 작성 요청 예시

```json
{
  "content": "최고금리만 보지 말고 우대조건 충족 가능 여부도 같이 보는 게 좋아요."
}
```

---

### 7-6. exchanges

| Method | URL | 설명 | 인증 |
|---|---|---|---|
| GET | `/api/exchanges/rates/` | 환율 목록 조회 | 불필요 |
| POST | `/api/exchanges/calculate/` | 환율 계산 | 불필요 |

#### 환율 계산 요청 예시

```json
{
  "amount": 100000,
  "currency": "USD"
}
```

#### 응답 예시

```json
{
  "amount_krw": 100000.0,
  "currency": "USD",
  "currency_name": "미국 달러",
  "rate": 1380.5,
  "converted_amount": 72.44
}
```

---

### 7-7. chatbot

| Method | URL | 설명 | 인증 |
|---|---|---|---|
| POST | `/api/chatbot/` | 금융 용어/상품 설명 챗봇 | 불필요 |

#### 금융 용어 질문 예시

```json
{
  "message": "우대금리가 뭐야?"
}
```

#### 상품 설명 질문 예시

```json
{
  "message": "WON플러스예금 쉽게 설명해줘"
}
```

#### 응답 예시

```json
{
  "answer": "우리은행의 \"WON플러스예금\"은 정기예금 상품입니다. 정기예금은 일정 기간 돈을 맡기고 만기 때 원금과 이자를 받는 상품입니다...",
  "type": "product"
}
```

---

### 7-8. maps

| Method | URL | 설명 | 인증 |
|---|---|---|---|
| GET | `/api/maps/banks/?keyword=하나은행` | 은행 지점 검색 | 불필요 |
| GET | `/api/maps/banks/?keyword=광주 하나은행` | 지역 + 은행명 검색 | 불필요 |
| GET | `/api/maps/banks/?keyword=하나은행&x=126.9780&y=37.5665&radius=3000` | 현재 위치 기준 주변 은행 검색 | 불필요 |

#### 응답 예시

```json
{
  "keyword": "하나은행",
  "count": 3,
  "branches": [
    {
      "place_name": "하나은행 광주지점",
      "address_name": "광주광역시 ...",
      "road_address_name": "광주광역시 ...",
      "phone": "062-...",
      "x": "126.XXXX",
      "y": "35.XXXX",
      "place_url": "https://place.map.kakao.com/...",
      "distance": ""
    }
  ]
}
```

---

## 8. 개발 메모

### 8-1. 금감원 정기예금 데이터 처리

금감원 API는 정기예금 데이터를 다음과 같이 제공합니다.

```text
baseList    상품 기본 정보
optionList  상품별 금리 옵션
```

따라서 DB 모델도 다음과 같이 분리했습니다.

```text
Bank
  └─ FinancialProduct
        └─ ProductOption
```

이 구조를 통해 하나의 상품이 여러 기간별 금리 옵션을 가질 수 있도록 설계했습니다.

---

### 8-2. 챗봇 구현 방식

현재 챗봇은 규칙 기반으로 구현했습니다.

```text
금융 용어 질문
→ 미리 정의한 용어 설명 반환

상품 설명 질문
→ products DB에서 상품 검색
→ 가입방법, 가입대상, 최고금리, 우대조건을 쉬운 문장으로 변환
```

향후 AI API를 연동할 경우, DB에서 조회한 상품 정보를 AI에게 전달하고 해당 정보만 근거로 설명하게 하는 방식으로 확장할 수 있습니다.

---

### 8-3. 지도 기능 구현 방식

백엔드는 카카오 로컬 API로 은행 지점 데이터를 조회하고, 프론트엔드는 응답받은 좌표 정보를 이용해 카카오맵에 마커를 표시합니다.

```text
Vue
→ 검색어/좌표를 Django API로 전달
→ Django가 카카오 로컬 API 호출
→ 은행 지점 목록 반환
→ Vue가 지도에 마커 표시
```

---

## 9. 백엔드 구현 완료 기능

- [x] Django 프로젝트 초기 설정
- [x] 가상환경 설정
- [x] 환경변수 관리
- [x] 금융감독원 정기예금 API 연동
- [x] 정기예금 상품 저장
- [x] 정기예금 상품 목록 조회
- [x] 정기예금 상품 상세 조회
- [x] 회원가입
- [x] 로그인
- [x] 로그아웃
- [x] 프로필 조회
- [x] 관심상품 추가/삭제
- [x] 관심상품 목록 조회
- [x] 주거래은행 추천
- [x] 추천 이력 조회
- [x] 게시글 작성
- [x] 게시글 목록 조회
- [x] 게시글 상세 조회
- [x] 게시글 수정
- [x] 게시글 삭제
- [x] 댓글 작성
- [x] 댓글 삭제
- [x] 환율 목록 조회
- [x] 환율 계산
- [x] 금융용어 설명 챗봇
- [x] 정기예금 상품 설명 챗봇
- [x] 카카오 로컬 API 기반 은행 지점 검색