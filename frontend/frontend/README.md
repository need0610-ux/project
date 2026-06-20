# Frontend README

## 1. 프로젝트 개요

본 프론트엔드는 정기예금 추천 서비스의 사용자 화면입니다.  
Vue 3 기반으로 구현하며, Django REST API와 연동하여 정기예금 상품 조회, 회원 기능, 관심상품, 주거래은행 추천, 게시판, 환율 계산, 지도 검색, 챗봇 기능을 제공합니다.

현재는 프론트 초기 세팅과 정기예금 상품 목록 API 연결을 우선 구현했습니다.

---

## 2. 기술 스택

| 구분 | 기술 |
|---|---|
| Framework | Vue 3 |
| Build Tool | Vite |
| Routing | Vue Router |
| State Management | Pinia |
| HTTP Client | Axios |
| Code Quality | ESLint |
| Code Formatter | Prettier |

---

## 3. 프로젝트 구조

```text
frontend/
├─ public/
├─ src/
│  ├─ api/
│  │  └─ api.js              # Django API 요청 공통 설정
│  ├─ assets/
│  ├─ components/
│  │  └─ ChatbotFloating.vue # 우측 하단 챗봇 버튼 예정
│  ├─ router/
│  │  └─ index.js            # 페이지 라우팅 설정
│  ├─ stores/                # Pinia 상태 관리
│  ├─ views/
│  │  ├─ HomeView.vue
│  │  └─ ProductListView.vue
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

정기예금 상품 목록 화면은 아래 주소에서 확인할 수 있습니다.

```text
http://localhost:5173/products
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

즉, 개발 중에는 터미널을 2개 열고 각각 실행합니다.

```bash
# backend
python manage.py runserver
```

```bash
# frontend
npm run dev
```

---

## 6. Axios API 설정

Django 백엔드 API 호출을 위해 `src/api/api.js`를 생성했습니다.

```javascript
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
})

export default api
```

사용 예시:

```javascript
import api from '@/api/api'

const response = await api.get('/products/deposits/')
```

---

## 7. 라우터 설정

현재 등록된 주요 라우트는 다음과 같습니다.

| Path | Component | 설명 |
|---|---|---|
| `/` | `HomeView.vue` | 메인 화면 |
| `/products` | `ProductListView.vue` | 정기예금 상품 목록 |

라우터 설정 예시:

```javascript
import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import ProductListView from '../views/ProductListView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/products',
      name: 'products',
      component: ProductListView,
    },
  ],
})

export default router
```

---

## 8. 현재 구현 화면

### 8-1. HomeView

서비스 소개 및 정기예금 상품 목록 화면으로 이동하는 링크를 제공합니다.

주요 내용:

- 서비스 소개
- 정기예금 상품 목록 이동 링크

---

### 8-2. ProductListView

Django 백엔드의 정기예금 상품 목록 API를 호출하여 상품 데이터를 화면에 출력합니다.

호출 API:

```text
GET /api/products/deposits/
```

출력 정보:

- 상품명
- 은행명
- 가입방법
- 최고금리

---

## 9. 앞으로 구현할 화면

향후 구현 예정 화면은 다음과 같습니다.

```text
LoginView.vue           로그인
SignupView.vue          회원가입
ProductDetailView.vue   정기예금 상품 상세
FavoriteView.vue        관심상품 목록
RecommendationView.vue  주거래은행 추천
CommunityView.vue       게시판/댓글
ExchangeView.vue        환율 계산기
MapView.vue             은행 지점 지도 검색
ChatbotFloating.vue     우측 하단 플로팅 챗봇
```

---

## 10. 백엔드 API 연동 예정 목록

| 기능 | Method | URL |
|---|---|---|
| 회원가입 | POST | `/api/accounts/signup/` |
| 로그인 | POST | `/api/accounts/login/` |
| 프로필 조회 | GET | `/api/accounts/profile/` |
| 정기예금 목록 | GET | `/api/products/deposits/` |
| 정기예금 상세 | GET | `/api/products/deposits/<product_id>/` |
| 관심상품 목록 | GET | `/api/favorites/` |
| 관심상품 추가/삭제 | POST | `/api/favorites/<product_id>/` |
| 주거래은행 추천 | POST | `/api/recommendations/main-bank/` |
| 추천 이력 조회 | GET | `/api/recommendations/history/` |
| 게시글 목록 | GET | `/api/community/` |
| 게시글 작성 | POST | `/api/community/` |
| 댓글 작성 | POST | `/api/community/<post_id>/comments/` |
| 환율 목록 조회 | GET | `/api/exchanges/rates/` |
| 환율 계산 | POST | `/api/exchanges/calculate/` |
| 챗봇 | POST | `/api/chatbot/` |
| 은행 지점 검색 | GET | `/api/maps/banks/?keyword=하나은행` |

---

## 11. 프론트엔드 구현 현황

- [x] Vue 3 프로젝트 생성
- [x] Vue Router 설정
- [x] Pinia 포함 프로젝트 생성
- [x] ESLint/Prettier 설정
- [x] Axios 설치
- [x] 공통 API 파일 생성
- [x] HomeView 생성
- [x] ProductListView 생성
- [x] 정기예금 상품 목록 API 연결
- [ ] 로그인 화면 구현
- [ ] 회원가입 화면 구현
- [ ] 상품 상세 화면 구현
- [ ] 관심상품 화면 구현
- [ ] 주거래은행 추천 화면 구현
- [ ] 게시판/댓글 화면 구현
- [ ] 환율 계산 화면 구현
- [ ] 지도 검색 화면 구현
- [ ] 우측 하단 챗봇 UI 구현