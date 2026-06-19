# API 명세서

본 문서는 예적금 추천 서비스의 백엔드 API 명세를 정리한 문서이다.  
API는 Django REST Framework 기반으로 구현하며, 프론트엔드는 Vue에서 API를 호출하여 화면을 구성한다.

## 1. API 설계 기준

- Base URL: `/api/v1/`
- 인증 방식: JWT 기반 인증
- 요청 및 응답 형식: JSON
- 로그인한 사용자만 이용 가능한 기능은 `Authorization` Header에 Access Token을 포함한다.

```http
Authorization: Bearer {access_token}
```

## 2. 공통 응답 형식

### 성공 응답

```json
{
  "success": true,
  "data": {}
}
```

### 실패 응답

```json
{
  "success": false,
  "message": "오류 메시지"
}
```

## 3. API 목록

| 구분 | Method | URL | 설명 | 인증 |
|---|---|---|---|---|
| 회원 | POST | `/accounts/signup/` | 회원가입 | X |
| 회원 | POST | `/accounts/login/` | 로그인 | X |
| 회원 | POST | `/accounts/logout/` | 로그아웃 | O |
| 회원 | GET | `/accounts/me/` | 내 정보 조회 | O |
| 상품 | GET | `/products/` | 예적금 상품 목록 조회 | X |
| 상품 | GET | `/products/{product_id}/` | 예적금 상품 상세 조회 | X |
| 상품 | GET | `/banks/` | 은행 목록 조회 | X |
| 관심상품 | POST | `/favorites/` | 관심 상품 등록 | O |
| 관심상품 | GET | `/favorites/` | 관심 상품 목록 조회 | O |
| 관심상품 | DELETE | `/favorites/{favorite_id}/` | 관심 상품 삭제 | O |
| 추천 | POST | `/recommendations/` | 예적금 상품 추천 요청 | O |
| 추천 | GET | `/recommendations/history/` | 추천 이력 조회 | O |
| 주거래은행 진단 | GET | `/bank-test/questions/` | 진단 질문 조회 | X |
| 주거래은행 진단 | POST | `/bank-test/result/` | 진단 결과 생성 | O |
| 주거래은행 진단 | GET | `/bank-test/my-result/` | 내 진단 결과 조회 | O |
| 환율 | GET | `/exchange/rates/` | 환율 정보 조회 | X |
| 환율 | POST | `/exchange/calculate/` | 환율 계산 | X |
| 게시판 | GET | `/posts/` | 게시글 목록 조회 | X |
| 게시판 | GET | `/posts/{post_id}/` | 게시글 상세 조회 | X |
| 게시판 | POST | `/posts/` | 게시글 작성 | O |
| 게시판 | PUT | `/posts/{post_id}/` | 게시글 수정 | O |
| 게시판 | DELETE | `/posts/{post_id}/` | 게시글 삭제 | O |
| 댓글 | POST | `/posts/{post_id}/comments/` | 댓글 작성 | O |
| 댓글 | PUT | `/comments/{comment_id}/` | 댓글 수정 | O |
| 댓글 | DELETE | `/comments/{comment_id}/` | 댓글 삭제 | O |

---

## 4. 주요 API 상세

## 4.1 회원가입

| 항목 | 내용 |
|---|---|
| Method | POST |
| URL | `/accounts/signup/` |
| 인증 | X |
| 설명 | 아이디, 비밀번호, 닉네임을 입력하여 회원가입한다. |

### Request Body

```json
{
  "username": "user01",
  "password": "password123!",
  "password_confirm": "password123!",
  "nickname": "금융초보"
}
```

### Response

```json
{
  "success": true,
  "data": {
    "id": 1,
    "username": "user01",
    "nickname": "금융초보"
  }
}
```

---

## 4.2 로그인

| 항목 | 내용 |
|---|---|
| Method | POST |
| URL | `/accounts/login/` |
| 인증 | X |
| 설명 | 아이디와 비밀번호를 이용하여 로그인한다. |

### Request Body

```json
{
  "username": "user01",
  "password": "password123!"
}
```

### Response

```json
{
  "success": true,
  "data": {
    "access": "access_token",
    "refresh": "refresh_token",
    "user": {
      "id": 1,
      "username": "user01",
      "nickname": "금융초보"
    }
  }
}
```

---

## 4.3 예적금 상품 목록 조회

| 항목 | 내용 |
|---|---|
| Method | GET |
| URL | `/products/` |
| 인증 | X |
| 설명 | 예적금 상품 목록을 조회한다. |

### Query Parameters

| 이름 | 타입 | 필수 | 설명 |
|---|---|---|---|
| type | string | X | 상품 유형, `deposit` 또는 `saving` |
| bank | string | X | 은행명 |
| term | integer | X | 가입 기간 |
| min_rate | number | X | 최소 금리 |

### Response

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "bank_name": "국민은행",
      "product_name": "KB 정기예금",
      "product_type": "deposit",
      "max_rate": 3.7,
      "min_term": 6,
      "max_term": 36
    }
  ]
}
```

---

## 4.4 예적금 상품 상세 조회

| 항목 | 내용 |
|---|---|
| Method | GET |
| URL | `/products/{product_id}/` |
| 인증 | X |
| 설명 | 특정 예적금 상품의 상세 정보와 금리 옵션을 조회한다. |

### Response

```json
{
  "success": true,
  "data": {
    "id": 1,
    "bank_name": "국민은행",
    "product_name": "KB 정기예금",
    "product_type": "deposit",
    "description": "목돈을 안정적으로 운용할 수 있는 정기예금 상품입니다.",
    "join_way": "영업점, 인터넷뱅킹, 모바일뱅킹",
    "special_condition": "우대 조건 충족 시 우대금리 제공",
    "options": [
      {
        "term": 6,
        "base_rate": 3.2,
        "prime_rate": 3.5
      },
      {
        "term": 12,
        "base_rate": 3.4,
        "prime_rate": 3.7
      }
    ]
  }
}
```

---

## 4.5 관심 상품 등록

| 항목 | 내용 |
|---|---|
| Method | POST |
| URL | `/favorites/` |
| 인증 | O |
| 설명 | 로그인한 사용자가 관심 있는 예적금 상품을 저장한다. |

### Request Body

```json
{
  "product_id": 1
}
```

### Response

```json
{
  "success": true,
  "message": "관심 상품으로 등록되었습니다."
}
```

---

## 4.6 예적금 상품 추천 요청

| 항목 | 내용 |
|---|---|
| Method | POST |
| URL | `/recommendations/` |
| 인증 | O |
| 설명 | 사용자가 입력한 조건을 바탕으로 예적금 상품을 추천한다. |

### Request Body

```json
{
  "amount": 1000000,
  "term": 12,
  "product_type": "deposit",
  "preferred_bank_id": 1
}
```

### Response

```json
{
  "success": true,
  "data": {
    "recommended_products": [
      {
        "rank": 1,
        "product_id": 1,
        "bank_name": "국민은행",
        "product_name": "KB 정기예금",
        "term": 12,
        "base_rate": 3.4,
        "prime_rate": 3.7,
        "expected_interest": 37000,
        "reason": "입력한 가입 기간과 금액 기준으로 우대금리가 높아 추천되었습니다."
      }
    ]
  }
}
```

---

## 4.7 주거래은행 진단 질문 조회

| 항목 | 내용 |
|---|---|
| Method | GET |
| URL | `/bank-test/questions/` |
| 인증 | X |
| 설명 | 주거래은행 성향 진단에 사용할 질문 목록을 조회한다. |

### Response

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "question": "은행을 선택할 때 가장 중요하게 생각하는 기준은 무엇인가요?",
      "choices": [
        {
          "id": 1,
          "content": "높은 금리"
        },
        {
          "id": 2,
          "content": "수수료 혜택"
        },
        {
          "id": 3,
          "content": "앱 사용 편의성"
        },
        {
          "id": 4,
          "content": "지점 접근성"
        }
      ]
    }
  ]
}
```

---

## 4.8 주거래은행 진단 결과 생성

| 항목 | 내용 |
|---|---|
| Method | POST |
| URL | `/bank-test/result/` |
| 인증 | O |
| 설명 | 사용자의 답변을 바탕으로 주거래은행 유형과 추천 은행을 반환한다. |

### Request Body

```json
{
  "answers": [
    {
      "question_id": 1,
      "choice_id": 1
    },
    {
      "question_id": 2,
      "choice_id": 3
    }
  ]
}
```

### Response

```json
{
  "success": true,
  "data": {
    "result_type": "금리추구형",
    "description": "금리 혜택과 우대 조건을 중요하게 생각하는 유형입니다.",
    "recommended_banks": [
      {
        "bank_id": 1,
        "bank_name": "국민은행",
        "reason": "예적금 상품 수가 많고 우대금리 조건이 다양합니다."
      }
    ]
  }
}
```

---

## 4.9 환율 정보 조회

| 항목 | 내용 |
|---|---|
| Method | GET |
| URL | `/exchange/rates/` |
| 인증 | X |
| 설명 | 외부 환율 API를 호출하여 주요 통화의 환율 정보를 조회한다. |

### Query Parameters

| 이름 | 타입 | 필수 | 설명 |
|---|---|---|---|
| currency | string | X | 조회할 통화 코드, 예: USD, JPY, EUR |

### Response

```json
{
  "success": true,
  "data": [
    {
      "currency": "USD",
      "currency_name": "미국 달러",
      "rate": 1380.5,
      "base_date": "2026-06-20"
    }
  ]
}
```

---

## 4.10 환율 계산

| 항목 | 내용 |
|---|---|
| Method | POST |
| URL | `/exchange/calculate/` |
| 인증 | X |
| 설명 | 입력 금액과 통화 정보를 기준으로 환전 금액을 계산한다. |

### Request Body

```json
{
  "from_currency": "KRW",
  "to_currency": "USD",
  "amount": 100000
}
```

### Response

```json
{
  "success": true,
  "data": {
    "from_currency": "KRW",
    "to_currency": "USD",
    "amount": 100000,
    "converted_amount": 72.43,
    "rate": 1380.5,
    "base_date": "2026-06-20"
  }
}
```

---

## 4.11 게시글 작성

| 항목 | 내용 |
|---|---|
| Method | POST |
| URL | `/posts/` |
| 인증 | O |
| 설명 | 로그인한 사용자가 커뮤니티 게시글을 작성한다. |

### Request Body

```json
{
  "title": "적금 추천 부탁드립니다.",
  "content": "사회초년생이 들기 좋은 적금이 궁금합니다."
}
```

### Response

```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "적금 추천 부탁드립니다.",
    "content": "사회초년생이 들기 좋은 적금이 궁금합니다.",
    "created_at": "2026-06-20T10:00:00"
  }
}
```

---

## 4.12 댓글 작성

| 항목 | 내용 |
|---|---|
| Method | POST |
| URL | `/posts/{post_id}/comments/` |
| 인증 | O |
| 설명 | 로그인한 사용자가 특정 게시글에 댓글을 작성한다. |

### Request Body

```json
{
  "content": "저는 12개월 적금을 추천합니다."
}
```

### Response

```json
{
  "success": true,
  "data": {
    "id": 1,
    "content": "저는 12개월 적금을 추천합니다.",
    "author": "user01",
    "created_at": "2026-06-20T10:20:00"
  }
}
```

---

## 5. 프론트엔드 구현 기능

아래 기능은 별도 백엔드 API 없이 프론트엔드에서 구현한다.

| 기능 | 구현 방식 |
|---|---|
| 챗봇 플로팅 버튼 | 모든 화면 오른쪽 하단에 고정 버튼으로 표시 |
| 금융용어 챗봇 | 키워드 기반으로 사전에 정의한 금융용어 설명 제공 |
| 지도 | 지도 SDK를 활용하여 은행 위치 검색 및 마커 표시 |

챗봇은 금융상품 설명과 금융용어 풀이를 위한 보조 기능으로 제공한다.  
초기 구현은 프론트엔드 규칙 기반 응답 방식으로 처리하며, 추후 AI API 연동 시 백엔드 API로 확장할 수 있다.

---

## 6. 구현 우선순위

다음 순서대로 구현한다.

| 우선순위 | 기능 |
| 1순위 | 회원가입, 로그인 |
| 2순위 | 예적금 상품 목록/상세 조회 |
| 3순위 | 관심 상품 |
| 4순위 | 예적금 추천 |
| 5순위 | 주거래은행 성향 진단 |
| 6순위 | 게시판, 댓글 |
| 7순위 | 환율 API |