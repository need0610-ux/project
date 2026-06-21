# API 명세서

본 문서는 예적금 추천 서비스의 백엔드 API 명세를 정리한 문서이다.  
API는 Django REST Framework 기반으로 구현하며, 프론트엔드는 Vue에서 API를 호출하여 화면을 구성한다.

## 1. API 설계 기준

- Base URL: `/api/`
- 인증 방식: JWT 기반 인증
- 요청 및 응답 형식: JSON
- 로그인한 사용자만 이용 가능한 기능은 `Authorization` Header에 Access Token을 포함한다.

```http
Authorization: Bearer {access_token}
```

> 실제 Django `urls.py`에서 `/api/v1/`을 사용 중이라면 Base URL을 `/api/v1/`로 맞춘다.  
> 현재 프론트 연결 기준은 `/api/`로 작성한다.

---

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

---

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
| 지도 | GET | `/map/search/` | 은행 위치 검색 | X |
| 챗봇 | POST | `/chatbot/explain/` | 금융상품 및 금융용어 설명 요청 | X |
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

## 4.6 관심 상품 목록 조회

| 항목 | 내용 |
|---|---|
| Method | GET |
| URL | `/favorites/` |
| 인증 | O |
| 설명 | 로그인한 사용자가 저장한 관심 상품 목록을 조회한다. |

### Response

```json
{
  "success": true,
  "data": [
    {
      "favorite_id": 1,
      "product_id": 1,
      "bank_name": "국민은행",
      "product_name": "KB 정기예금",
      "product_type": "deposit",
      "max_rate": 3.7
    }
  ]
}
```

---

## 4.7 관심 상품 삭제

| 항목 | 내용 |
|---|---|
| Method | DELETE |
| URL | `/favorites/{favorite_id}/` |
| 인증 | O |
| 설명 | 로그인한 사용자가 저장한 관심 상품을 삭제한다. |

### Response

```json
{
  "success": true,
  "message": "관심 상품이 삭제되었습니다."
}
```

---

## 4.8 예적금 상품 추천 요청

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

## 4.9 추천 이력 조회

| 항목 | 내용 |
|---|---|
| Method | GET |
| URL | `/recommendations/history/` |
| 인증 | O |
| 설명 | 로그인한 사용자의 예적금 추천 이력을 조회한다. |

### Response

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "amount": 1000000,
      "term": 12,
      "product_type": "deposit",
      "recommended_product_name": "KB 정기예금",
      "bank_name": "국민은행",
      "created_at": "2026-06-20T10:00:00"
    }
  ]
}
```

---

## 4.10 주거래은행 진단 질문 조회

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

## 4.11 주거래은행 진단 결과 생성

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

## 4.12 내 진단 결과 조회

| 항목 | 내용 |
|---|---|
| Method | GET |
| URL | `/bank-test/my-result/` |
| 인증 | O |
| 설명 | 로그인한 사용자의 최근 주거래은행 진단 결과를 조회한다. |

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
    ],
    "created_at": "2026-06-20T10:00:00"
  }
}
```

---

## 4.13 환율 정보 조회

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

## 4.14 환율 계산

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

## 4.15 은행 위치 검색

| 항목 | 내용 |
|---|---|
| Method | GET |
| URL | `/map/search/` |
| 인증 | X |
| 설명 | 사용자의 검색어 또는 현재 위치를 기준으로 은행 위치를 검색한다. |

### Query Parameters

| 이름 | 타입 | 필수 | 설명 |
|---|---|---|---|
| query | string | O | 검색어, 예: 국민은행, 우리은행 |
| x | number | X | 경도 |
| y | number | X | 위도 |
| radius | integer | X | 검색 반경, 단위 m |

### Request Example

```http
GET /api/map/search/?query=국민은행&x=126.9780&y=37.5665&radius=2000
```

### Response

```json
{
  "success": true,
  "data": [
    {
      "place_name": "국민은행 광화문지점",
      "address_name": "서울 종로구 세종대로 172",
      "road_address_name": "서울 종로구 세종대로 172",
      "phone": "02-0000-0000",
      "x": "126.9780",
      "y": "37.5665",
      "place_url": "https://place.map.kakao.com/..."
    }
  ]
}
```

---

## 4.16 금융 설명 챗봇

| 항목 | 내용 |
|---|---|
| Method | POST |
| URL | `/chatbot/explain/` |
| 인증 | X |
| 설명 | 사용자가 입력한 금융상품명 또는 금융용어를 백엔드 API로 전송하고, 백엔드는 쉬운 설명을 반환한다. |

### Request Body

```json
{
  "message": "예금자보호"
}
```

### Response - 금융용어 설명

```json
{
  "success": true,
  "data": {
    "type": "term",
    "question": "예금자보호",
    "answer": "예금자보호는 금융회사가 영업정지나 파산 등으로 예금을 돌려주기 어려운 경우, 일정 한도 내에서 예금자를 보호해주는 제도입니다."
  }
}
```

### Response - 금융상품 설명

```json
{
  "success": true,
  "data": {
    "type": "product",
    "question": "우리은행 WON플러스예금",
    "answer": "우리은행 WON플러스예금은 일정 기간 돈을 맡기고 약정된 금리를 받는 정기예금 상품입니다. 가입 기간과 금리 조건을 확인한 뒤 가입하는 것이 좋습니다.",
    "product": {
      "bank_name": "우리은행",
      "product_name": "WON플러스예금",
      "product_type": "deposit",
      "max_rate": 3.65
    }
  }
}
```

### Error Response

```json
{
  "success": false,
  "message": "설명할 내용을 입력해주세요."
}
```

---

## 4.17 게시글 목록 조회

| 항목 | 내용 |
|---|---|
| Method | GET |
| URL | `/posts/` |
| 인증 | X |
| 설명 | 커뮤니티 게시글 목록을 조회한다. |

### Response

```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "적금 추천 부탁드립니다.",
      "author": "user01",
      "created_at": "2026-06-20T10:00:00",
      "comment_count": 2
    }
  ]
}
```

---

## 4.18 게시글 상세 조회

| 항목 | 내용 |
|---|---|
| Method | GET |
| URL | `/posts/{post_id}/` |
| 인증 | X |
| 설명 | 특정 게시글의 상세 내용과 댓글 목록을 조회한다. |

### Response

```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "적금 추천 부탁드립니다.",
    "content": "사회초년생이 들기 좋은 적금이 궁금합니다.",
    "author": "user01",
    "created_at": "2026-06-20T10:00:00",
    "comments": [
      {
        "id": 1,
        "content": "저는 12개월 적금을 추천합니다.",
        "author": "user02",
        "created_at": "2026-06-20T10:20:00"
      }
    ]
  }
}
```

---

## 4.19 게시글 작성

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

## 4.20 게시글 수정

| 항목 | 내용 |
|---|---|
| Method | PUT |
| URL | `/posts/{post_id}/` |
| 인증 | O |
| 설명 | 로그인한 사용자가 자신이 작성한 게시글을 수정한다. |

### Request Body

```json
{
  "title": "적금 추천 다시 부탁드립니다.",
  "content": "12개월 기준으로 적금 추천을 받고 싶습니다."
}
```

### Response

```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "적금 추천 다시 부탁드립니다.",
    "content": "12개월 기준으로 적금 추천을 받고 싶습니다.",
    "updated_at": "2026-06-20T11:00:00"
  }
}
```

---

## 4.21 게시글 삭제

| 항목 | 내용 |
|---|---|
| Method | DELETE |
| URL | `/posts/{post_id}/` |
| 인증 | O |
| 설명 | 로그인한 사용자가 자신이 작성한 게시글을 삭제한다. |

### Response

```json
{
  "success": true,
  "message": "게시글이 삭제되었습니다."
}
```

---

## 4.22 댓글 작성

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

## 4.23 댓글 수정

| 항목 | 내용 |
|---|---|
| Method | PUT |
| URL | `/comments/{comment_id}/` |
| 인증 | O |
| 설명 | 로그인한 사용자가 자신이 작성한 댓글을 수정한다. |

### Request Body

```json
{
  "content": "저는 12개월 자유적금을 추천합니다."
}
```

### Response

```json
{
  "success": true,
  "data": {
    "id": 1,
    "content": "저는 12개월 자유적금을 추천합니다.",
    "updated_at": "2026-06-20T11:00:00"
  }
}
```

---

## 4.24 댓글 삭제

| 항목 | 내용 |
|---|---|
| Method | DELETE |
| URL | `/comments/{comment_id}/` |
| 인증 | O |
| 설명 | 로그인한 사용자가 자신이 작성한 댓글을 삭제한다. |

### Response

```json
{
  "success": true,
  "message": "댓글이 삭제되었습니다."
}
```

---

## 5. 프론트엔드 구현 및 API 연동 기준

아래 기능은 Vue 프론트엔드에서 화면과 사용자 인터랙션을 구현하고, 필요한 데이터는 백엔드 API를 호출하여 처리한다.

| 기능 | 프론트엔드 역할 | 백엔드 API 연동 |
|---|---|---|
| 챗봇 플로팅 버튼 | 모든 화면 오른쪽 하단에 고정 버튼 표시 | X |
| 챗봇 입력창 | 사용자 입력값 관리, 메시지 출력 | X |
| 금융 설명 챗봇 | 사용자 입력값을 API로 전송하고 응답 출력 | `/chatbot/explain/` |
| 지도 화면 | 검색창, 지도, 마커 표시 | `/map/search/` |
| 환율 계산 화면 | 금액, 통화 선택 입력 관리 | `/exchange/rates/`, `/exchange/calculate/` |
| 상품 목록 화면 | 필터, 목록 UI 표시 | `/products/` |
| 상품 상세 화면 | 상품 상세 정보 및 금리 옵션 표시 | `/products/{product_id}/` |
| 관심상품 | 관심상품 등록/조회/삭제 처리 | `/favorites/` |
| 게시판 | 게시글 목록, 상세, 작성, 수정, 삭제 처리 | `/posts/` |
| 댓글 | 댓글 작성, 수정, 삭제 처리 | `/comments/` |

챗봇은 모든 화면에서 접근할 수 있도록 `App.vue`에 플로팅 컴포넌트를 배치한다.  
사용자가 챗봇에 금융상품명 또는 금융용어를 입력하면 프론트엔드는 `/chatbot/explain/` API로 요청을 보내고, 응답받은 설명을 챗봇 창에 출력한다.

---

## 6. API Key 관리 기준

외부 API Key는 보안을 위해 프론트엔드 코드에 직접 작성하지 않는다.

| 구분 | 관리 위치 | 설명 |
|---|---|---|
| 금융감독원 API Key | Django `.env` | 예적금 상품 정보 조회 |
| 한국수출입은행 환율 API Key | Django `.env` | 환율 정보 조회 |
| 카카오 REST API Key | Django `.env` | 은행 위치 검색 |
| AI API Key | Django `.env` | 챗봇 설명 생성 기능 사용 시 |
| Vue API Base URL | Vue `.env` | 백엔드 서버 주소만 저장 |

### Backend `.env` 예시

```env
SECRET_KEY=django-secret-key
FSS_API_KEY=금융감독원_API_KEY
EXCHANGE_API_KEY=한국수출입은행_API_KEY
KAKAO_REST_API_KEY=카카오_REST_API_KEY
AI_API_KEY=AI_API_KEY
```

### Frontend `.env` 예시

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

프론트엔드에는 실제 외부 API Key를 저장하지 않는다.  
프론트엔드는 백엔드 API 주소만 알고, 백엔드가 외부 API와 통신한다.

---

## 7. 구현 우선순위

다음 순서대로 구현한다.

| 우선순위 | 기능 |
|---|---|
| 1순위 | 회원가입, 로그인 |
| 2순위 | 예적금 상품 목록/상세 조회 |
| 3순위 | 관심 상품 |
| 4순위 | 예적금 추천 |
| 5순위 | 주거래은행 성향 진단 |
| 6순위 | 게시판, 댓글 |
| 7순위 | 환율 API |
| 8순위 | 지도 API |
| 9순위 | 챗봇 API 연결 |