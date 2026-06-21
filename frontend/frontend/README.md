# Frontend README

## 1. 프로젝트 개요

본 프론트엔드는 정기예금 추천 서비스의 사용자 화면입니다.

Vue 3 기반으로 구현하며, Django REST API와 연동하여 회원가입, 로그인, 정기예금 상품 조회, 상품 상세 조회, 관심상품 등록/삭제, 마이페이지, 주거래은행 추천, 게시판, 환율 계산기, 은행 지도 검색, 챗봇 기능을 제공합니다.

현재는 프론트 초기 세팅, 라우터 구성, 회원가입/로그인, Navbar 로그인 상태 반영, 정기예금 상품 목록/상세 조회, 관심상품 등록/삭제, 마이페이지 관심상품 조회 기능까지 구현했습니다.

---

## 2. 기술 스택

| 구분               | 기술         |
| ---------------- | ---------- |
| Framework        | Vue 3      |
| Build Tool       | Vite       |
| Routing          | Vue Router |
| State Management | Pinia      |
| HTTP Client      | Axios      |
| Code Quality     | ESLint     |
| Code Formatter   | Prettier   |

---

## 3. 프로젝트 구조

```text
frontend/
├─ public/
├─ src/
│  ├─ api/
│  │  ├─ accounts.js          # 회원가입, 로그인 API
│  │  ├─ products.js          # 정기예금 상품 API
│  │  └─ favorites.js         # 관심상품 API
│  ├─ assets/
│  ├─ components/
│  │  ├─ Navbar.vue           # 상단 네비게이션 바
│  │  └─ ChatbotFloatingButton.vue # 우측 하단 챗봇 버튼 예정
│  ├─ router/
│  │  └─ index.js             # 페이지 라우팅 설정
│  ├─ stores/                 # Pinia 상태 관리 예정
│  ├─ views/
│  │  ├─ HomeView.vue
│  │  ├─ LoginView.vue
│  │  ├─ SignupView.vue
│  │  ├─ ProductListView.vue
│  │  ├─ ProductDetailView.vue
│  │  ├─ BankTestView.vue
│  │  ├─ BankTestResultView.vue
│  │  ├─ ExchangeView.vue
│  │  ├─ MapView.vue
│  │  ├─ CommunityView.vue
│  │  ├─ PostDetailView.vue
│  │  └─ MyPageView.vue
│  ├─ App.vue
│  └─ main.js
├─ index.html
├─ package.json
├─ package-lock.json
├─ vite.config.js
└─ README.md
```

---

## 4. 실행 방법

### 4-1. 프론트엔드 폴더 이동

`package.json`이 있는 폴더로 이동합니다.

```bash
cd frontend
```

프로젝트 폴더 안에 `frontend/frontend` 구조로 생성된 경우에는 아래처럼 이동합니다.

```bash
cd frontend/frontend
```

### 4-2. 패키지 설치

```bash
npm install
```

### 4-3. 개발 서버 실행

```bash
npm run dev
```

실행 후 아래 주소로 접속합니다.

```text
http://localhost:5173/
```

---

## 5. 백엔드 서버 실행 필요

프론트엔드가 Django API를 호출하므로, 백엔드 서버도 함께 실행되어 있어야 합니다.

백엔드 실행 주소:

```text
http://127.0.0.1:8000/
```

프론트엔드 실행 주소:

```text
http://localhost:5173/
```

개발 중에는 터미널을 2개 열고 각각 실행합니다.

```bash
# backend
python manage.py runserver
```

```bash
# frontend
npm run dev
```

---

## 6. 주요 페이지

| Path                | Component                | 설명          |
| ------------------- | ------------------------ | ----------- |
| `/`                 | `HomeView.vue`           | 메인 화면       |
| `/login`            | `LoginView.vue`          | 로그인         |
| `/signup`           | `SignupView.vue`         | 회원가입        |
| `/products`         | `ProductListView.vue`    | 정기예금 상품 목록  |
| `/products/:id`     | `ProductDetailView.vue`  | 정기예금 상품 상세  |
| `/bank-test`        | `BankTestView.vue`       | 주거래은행 검사    |
| `/bank-test/result` | `BankTestResultView.vue` | 주거래은행 검사 결과 |
| `/exchange`         | `ExchangeView.vue`       | 환율 계산기      |
| `/map`              | `MapView.vue`            | 은행 지도       |
| `/community`        | `CommunityView.vue`      | 게시글 목록      |
| `/community/:id`    | `PostDetailView.vue`     | 게시글 상세 및 댓글 |
| `/mypage`           | `MyPageView.vue`         | 마이페이지       |

---

## 7. 현재 구현된 기능

### 7-1. 회원 기능

회원가입과 로그인 화면을 구현했습니다.

로그인 성공 시 백엔드에서 발급받은 Token을 `localStorage`에 저장합니다.

```text
localStorage token 저장
→ Navbar 로그인 상태 변경
→ 로그인/회원가입 버튼 숨김
→ 마이페이지/로그아웃 버튼 표시
```

구현된 기능:

* 회원가입
* 로그인
* 로그아웃
* 로그인 상태에 따른 Navbar 변경
* 새로고침 없이 로그인 상태 반영

---

### 7-2. 정기예금 상품 목록

Django 백엔드의 정기예금 상품 목록 API를 호출하여 상품 데이터를 화면에 출력합니다.

호출 API:

```text
GET /api/products/deposits/
```

출력 정보:

* 상품명
* 은행명
* 은행 코드
* 가입 방법
* 최고 금리
* 상세 보기 버튼
* 관심상품 등록/삭제 버튼

---

### 7-3. 정기예금 상품 상세

상품 목록 또는 마이페이지에서 상세 보기 버튼을 클릭하면 상품 상세 페이지로 이동합니다.

호출 API:

```text
GET /api/products/deposits/<product_id>/
```

출력 정보:

* 상품명
* 은행명
* 은행 코드
* 가입 방법
* 가입 대상
* 가입 한도
* 최고 금리
* 우대 조건
* 기타 유의사항
* 공시 시작일
* 공시 종료일
* 금리 옵션
* 관심상품 등록/삭제 버튼

---

### 7-4. 관심상품 기능

로그인한 사용자는 정기예금 상품을 관심상품으로 등록하거나 삭제할 수 있습니다.

관심상품 기능은 백엔드에서 POST 요청 하나로 추가/삭제를 함께 처리하는 toggle 방식입니다.

호출 API:

```text
GET /api/favorites/
POST /api/favorites/<product_id>/
```

구현된 기능:

* 상품 목록에서 관심상품 등록
* 상품 목록에서 관심상품 삭제
* 상품 상세에서 관심상품 등록
* 상품 상세에서 관심상품 삭제
* 이미 등록된 상품은 버튼 문구를 `관심상품 삭제`로 표시
* 등록되지 않은 상품은 버튼 문구를 `관심상품 등록`으로 표시
* 마이페이지에서 관심상품 목록 조회
* 마이페이지에서 관심상품 상세 보기 이동

---

### 7-5. 마이페이지

현재 마이페이지에서는 로그인한 사용자의 관심상품 목록을 조회합니다.

구현된 기능:

* 관심상품 목록 조회
* 관심상품 상품명 표시
* 은행명 표시
* 최고 금리 표시
* 상품 상세 페이지 이동

향후 추가 예정:

* 추천 이력 조회
* 주거래은행 검사 결과 조회
* 사용자 프로필 정보 표시

---

## 8. API 연동 현황

| 기능         | Method | URL                                    | 상태                 |
| ---------- | ------ | -------------------------------------- | ------------------ |
| 회원가입       | POST   | `/api/accounts/signup/`                | 구현 완료              |
| 로그인        | POST   | `/api/accounts/login/`                 | 구현 완료              |
| 로그아웃       | POST   | `/api/accounts/logout/`                | 프론트 로컬 토큰 삭제 방식 구현 |
| 프로필 조회     | GET    | `/api/accounts/profile/`               | 추후 연결              |
| 정기예금 목록    | GET    | `/api/products/deposits/`              | 구현 완료              |
| 정기예금 상세    | GET    | `/api/products/deposits/<product_id>/` | 구현 완료              |
| 관심상품 목록    | GET    | `/api/favorites/`                      | 구현 완료              |
| 관심상품 추가/삭제 | POST   | `/api/favorites/<product_id>/`         | 구현 완료              |
| 주거래은행 추천   | POST   | `/api/recommendations/main-bank/`      | 추후 연결              |
| 전체 은행 추천   | POST   | `/api/recommendations/global-top/`     | 추후 연결              |
| 추천 이력 조회   | GET    | `/api/recommendations/history/`        | 추후 연결              |
| 게시글 목록     | GET    | `/api/community/`                      | 추후 연결              |
| 게시글 작성     | POST   | `/api/community/`                      | 추후 연결              |
| 게시글 상세     | GET    | `/api/community/<post_id>/`            | 추후 연결              |
| 댓글 작성      | POST   | `/api/community/<post_id>/comments/`   | 추후 연결              |
| 환율 조회      | GET    | `/api/exchange/rates/`                 | 추후 연결              |
| 은행 지점 검색   | GET    | `/api/map/search/`                     | 추후 연결              |
| 챗봇 설명      | POST   | `/api/chatbot/explain/`                | 추후 연결              |

---

## 9. 프론트엔드 구현 현황

* [x] Vue 3 프로젝트 생성
* [x] Vue Router 설정
* [x] Pinia 포함 프로젝트 생성
* [x] ESLint/Prettier 설정
* [x] Axios 설치
* [x] API 폴더 구성
* [x] HomeView 생성
* [x] Navbar 생성
* [x] 회원가입 화면 구현
* [x] 로그인 화면 구현
* [x] 로그인 성공 시 Token 저장
* [x] Navbar 로그인 상태 반영
* [x] 로그아웃 기능 구현
* [x] ProductListView 생성
* [x] 정기예금 상품 목록 API 연결
* [x] ProductDetailView 생성
* [x] 정기예금 상품 상세 API 연결
* [x] 관심상품 등록/삭제 API 연결
* [x] 상품 목록에서 관심상품 상태 반영
* [x] 상품 상세에서 관심상품 상태 반영
* [x] MyPageView 생성
* [x] 마이페이지 관심상품 목록 조회
* [ ] 마이페이지 추천 이력 조회
* [ ] 마이페이지 주거래은행 검사 결과 조회
* [ ] 주거래은행 검사 화면 구현
* [ ] 주거래은행 검사 결과 화면 구현
* [ ] 예적금 추천 화면 구현
* [ ] 게시판 목록 화면 구현
* [ ] 게시글 상세 및 댓글 화면 구현
* [ ] 글쓰기 화면 또는 글쓰기 폼 구현
* [ ] 환율 계산기 화면 구현
* [ ] 은행 지도 검색 화면 구현
* [ ] 우측 하단 챗봇 플로팅 버튼 구현
* [ ] 전체 화면 CSS 정리
* [ ] 최종 테스트 및 버그 수정

---

## 10. 앞으로 해야 할 일

### 10-1. 우선순위 1: 주거래은행 검사 기능

서비스의 핵심 차별화 기능이므로 우선 구현합니다.

해야 할 일:

* `BankTestView.vue`에서 검사 질문 화면 구현
* 사용자의 선택값 저장
* 검사 결과 계산 또는 백엔드 API 요청
* `BankTestResultView.vue`에서 결과 출력
* 검사 결과를 마이페이지에 표시

예상 작업 파일:

```text
src/views/BankTestView.vue
src/views/BankTestResultView.vue
src/views/MyPageView.vue
src/api/recommendations.js 또는 src/api/bankTest.js
```

---

### 10-2. 우선순위 2: 예적금 추천 기능

상품 목록 조회와 관심상품 기능이 연결되었으므로, 다음 단계로 추천 기능을 연결합니다.

해야 할 일:

* 추천 조건 입력 UI 구현
* 주거래은행 기준 추천 API 연결
* 전체 은행 기준 추천 API 연결
* 추천 결과 카드 출력
* 추천 이력 저장 여부 확인
* 마이페이지 추천 이력 조회 연결

예상 작업 파일:

```text
src/views/ProductListView.vue
src/views/MyPageView.vue
src/api/recommendations.js
```

---

### 10-3. 우선순위 3: 커뮤니티 기능

프로젝트 필수 기능인 게시판과 댓글 기능을 구현합니다.

해야 할 일:

* 게시글 목록 조회
* 게시글 작성
* 게시글 상세 조회
* 댓글 목록 조회
* 댓글 작성
* 로그인 사용자만 글쓰기/댓글 작성 가능하게 처리

예상 작업 파일:

```text
src/views/CommunityView.vue
src/views/PostDetailView.vue
src/api/community.js
```

---

### 10-4. 우선순위 4: 환율 계산기

환율 API와 연동하여 환율 조회 및 계산 기능을 구현합니다.

해야 할 일:

* 통화 선택 UI 구현
* 금액 입력 UI 구현
* 환율 목록 조회 API 연결
* 계산 결과 출력
* 환율 API 응답 실패 시 예외 처리

예상 작업 파일:

```text
src/views/ExchangeView.vue
src/api/exchange.js
```

---

### 10-5. 우선순위 5: 은행 지도 검색

카카오 로컬 API를 사용하는 백엔드 지도 검색 API와 연결합니다.

해야 할 일:

* 검색어 입력
* 현재 위치 또는 기본 위치 기준 은행 검색
* 은행 목록 출력
* 지도 표시
* 은행명, 주소, 거리 정보 표시

예상 작업 파일:

```text
src/views/MapView.vue
src/api/map.js
```

---

### 10-6. 우선순위 6: 챗봇 플로팅 버튼

챗봇은 상단 Navbar가 아니라 모든 화면의 오른쪽 하단에 고정합니다.

해야 할 일:

* `ChatbotFloatingButton.vue` 생성
* App.vue에 전역 배치
* 버튼 클릭 시 채팅창 열기/닫기
* 사용자 질문 입력
* 챗봇 API 연결
* 금융상품 설명 또는 금융용어 설명 응답 출력

예상 작업 파일:

```text
src/components/ChatbotFloatingButton.vue
src/App.vue
src/api/chatbot.js
```

---

### 10-7. 우선순위 7: 화면 디자인 정리

기능 연결 후 전체 화면의 스타일을 통일합니다.

해야 할 일:

* Navbar 간격 정리
* 버튼 스타일 통일
* 상품 카드 스타일 통일
* 마이페이지 카드 스타일 정리
* 모바일 화면 대응
* 와이어프레임과 화면 구성 맞추기

---

## 11. 개발 메모

현재 관심상품 API는 REST 방식의 DELETE 요청이 아니라 POST 요청 하나로 추가와 삭제를 함께 처리하는 toggle 방식입니다.

```text
POST /api/favorites/<product_id>/
```

동작 방식:

```text
관심상품에 없는 상품이면 추가
이미 관심상품에 있는 상품이면 삭제
```

따라서 프론트엔드에서는 관심상품 등록과 삭제 모두 같은 API 함수를 사용합니다.

```javascript
toggleFavoriteProduct(productId)
```

---

## 12. 다음 작업 체크리스트

* [ ] BankTestView 검사 질문 UI 구현
* [ ] BankTestResultView 검사 결과 UI 구현
* [ ] 주거래은행 검사 결과를 마이페이지에 연결
* [ ] 예적금 추천 API 연결
* [ ] 추천 결과 화면 구현
* [ ] 추천 이력 마이페이지 연결
* [ ] CommunityView 게시글 목록 API 연결
* [ ] PostDetailView 게시글 상세 API 연결
* [ ] 댓글 작성 기능 구현
* [ ] ExchangeView 환율 계산 API 연결
* [ ] MapView 은행 검색 API 연결
* [ ] ChatbotFloatingButton 구현
* [ ] App.vue에 챗봇 플로팅 버튼 전역 배치
* [ ] 전체 CSS 정리
* [ ] 최종 발표용 화면 캡처 정리
* [ ] README와 실제 구현 상태 동기화
