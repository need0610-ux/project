<template>
  <div class="home-page">
    <section class="page-title">
      <p class="breadcrumb">화면 ① 서비스 진입점</p>
      <h1>1. 메인 화면</h1>
    </section>

    <section class="hero-section">
      <p class="hero-label">[ 메인 배너 영역 ]</p>
      <h2>
        나에게 맞는 예적금과 주거래은행을<br />
        한 번에 찾아보세요
      </h2>

      <div class="hero-buttons">
        <RouterLink to="/bank-test" class="primary-btn">
          주거래은행 추천 시작하기 →
        </RouterLink>
        <RouterLink to="/products" class="secondary-btn">
          예적금 상품 보러가기 →
        </RouterLink>
      </div>
    </section>

    <section class="feature-section">
      <h3>■ 주요 기능</h3>

      <div class="feature-grid">
        <RouterLink
          v-for="feature in features"
          :key="feature.title"
          :to="feature.path"
          class="feature-card"
        >
          <div class="feature-icon">아이콘</div>
          <strong>{{ feature.title }}</strong>
          <p>{{ feature.description }}</p>
        </RouterLink>
      </div>
    </section>

    <section class="preview-section">
      <h3>■ 인기 예금/적금 상품 미리보기</h3>

      <div class="preview-grid">
        <article
          v-for="product in previewProducts"
          :key="product.id"
          class="preview-card"
        >
          <p class="bank-name">{{ product.bankName }}</p>
          <h4>{{ product.productName }}</h4>

          <div class="rate-box"></div>

          <div class="product-info">
            <span>최고 금리</span>
            <strong>{{ product.rate }}</strong>
          </div>

          <RouterLink to="/products" class="detail-link">
            상품 보러가기
          </RouterLink>
        </article>
      </div>
    </section>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'

const features = [
  {
    title: '예적금 추천',
    description: '맞춤 상품 비교',
    path: '/products',
  },
  {
    title: '주거래은행 추천',
    description: '성향 검사 기반',
    path: '/bank-test',
  },
  {
    title: '환율 계산기',
    description: '실시간 환율',
    path: '/exchange',
  },
  {
    title: '커뮤니티',
    description: '정보 공유 게시판',
    path: '/community',
  },
  {
    title: '근처 은행 찾기',
    description: '지도 기반 검색',
    path: '/map',
  },
]

const previewProducts = [
  {
    id: 1,
    bankName: '국민은행',
    productName: 'KB Star 정기예금',
    rate: '3.85%',
  },
  {
    id: 2,
    bankName: '신한은행',
    productName: '신한 My플러스 적금',
    rate: '3.70%',
  },
  {
    id: 3,
    bankName: '하나은행',
    productName: '하나 급여우대 예금',
    rate: '3.60%',
  },
  {
    id: 4,
    bankName: '우리은행',
    productName: '우리 WON적금',
    rate: '3.95%',
  },
]
</script>

<style scoped>
.home-page {
  width: 100%;
  padding: clamp(16px, 3vw, 28px);
  box-sizing: border-box;
}

.page-title {
  padding-bottom: 14px;
  border-bottom: 1px solid #d9d9d9;
}

.breadcrumb {
  margin: 0 0 6px;
  color: #777;
  font-size: 13px;
}

.page-title h1 {
  margin: 0;
  font-size: clamp(18px, 2vw, 22px);
}

.hero-section {
  margin-top: 20px;
  padding: clamp(32px, 6vw, 56px) clamp(18px, 4vw, 40px);
  border: 1px solid #bfbfbf;
  background-color: #e2e2e2;
  text-align: center;
  box-sizing: border-box;
}

.hero-label {
  margin: 0 0 20px;
  color: #777;
  font-size: 13px;
}

.hero-section h2 {
  margin: 0;
  font-size: clamp(20px, 2.4vw, 28px);
  line-height: 1.6;
}

.hero-buttons {
  display: flex;
  justify-content: center;
  gap: 14px;
  margin-top: 28px;
  flex-wrap: wrap;
}

.primary-btn,
.secondary-btn {
  min-width: min(220px, 100%);
  padding: 14px 20px;
  border: 1px solid #333;
  font-weight: 700;
  text-align: center;
  text-decoration: none;
  box-sizing: border-box;
}

.primary-btn {
  background-color: #333;
  color: white;
}

.secondary-btn {
  background-color: white;
  color: #222;
}

.feature-section,
.preview-section {
  margin-top: 24px;
}

.feature-section h3,
.preview-section h3 {
  margin: 0 0 12px;
  font-size: 16px;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 14px;
}

.feature-card {
  min-height: 130px;
  padding: 18px;
  border: 1px solid #bfbfbf;
  color: #222;
  text-align: center;
  text-decoration: none;
  box-sizing: border-box;
}

.feature-icon {
  width: 60px;
  height: 60px;
  margin: 0 auto 12px;
  border: 1px solid #bfbfbf;
  background-color: #e6e6e6;
  line-height: 60px;
  font-size: 13px;
}

.feature-card strong {
  display: block;
  margin-bottom: 8px;
  font-size: 15px;
}

.feature-card p {
  margin: 0;
  color: #666;
  font-size: 13px;
}

.preview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 14px;
}

.preview-card {
  padding: 18px;
  border: 1px solid #bfbfbf;
  box-sizing: border-box;
}

.bank-name {
  margin: 0 0 8px;
  color: #666;
  font-size: 13px;
}

.preview-card h4 {
  margin: 0 0 16px;
  font-size: 15px;
}

.rate-box {
  height: 12px;
  margin-bottom: 16px;
  background-color: #ededed;
}

.product-info {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 14px;
  font-size: 14px;
}

.product-info strong {
  font-size: 18px;
  white-space: nowrap;
}

.detail-link {
  display: block;
  padding: 10px;
  border: 1px solid #bfbfbf;
  color: #222;
  text-align: center;
  text-decoration: none;
}

@media (max-width: 640px) {
  .home-page {
    padding: 14px;
  }

  .hero-section h2 br {
    display: none;
  }

  .primary-btn,
  .secondary-btn {
    width: 100%;
  }

  .product-info {
    flex-direction: column;
  }
}
</style>