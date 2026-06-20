<template>
  <div class="product-card">
    <div class="card-header">
      <p class="bank-name">{{ bankName }}</p>
      <h3 class="product-name">{{ productName }}</h3>
    </div>

    <div class="rate-box">
      <div>
        <span class="label">기본 금리</span>
        <strong>{{ baseRate }}%</strong>
      </div>
      <div>
        <span class="label">최고 금리</span>
        <strong>{{ maxRate }}%</strong>
      </div>
    </div>

    <p class="description">
      {{ description }}
    </p>

    <button class="detail-button">
      자세히 보기
    </button>
  </div>
</template>

<script setup>
defineProps({
  bankName: {
    type: String,
    default: '은행명',
  },
  productName: {
    type: String,
    default: '상품명',
  },
  baseRate: {
    type: [String, Number],
    default: '0.00',
  },
  maxRate: {
    type: [String, Number],
    default: '0.00',
  },
  description: {
    type: String,
    default: '상품 설명이 들어갑니다.',
  },
})
</script>

<style scoped>
.product-card {
  width: 100%;
  padding: 20px;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  background-color: #ffffff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.card-header {
  margin-bottom: 16px;
}

.bank-name {
  margin: 0 0 6px;
  font-size: 14px;
  color: #6b7280;
}

.product-name {
  margin: 0;
  font-size: 20px;
  color: #111827;
}

.rate-box {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.rate-box div {
  flex: 1;
  padding: 12px;
  border-radius: 12px;
  background-color: #f3f4f6;
}

.label {
  display: block;
  margin-bottom: 4px;
  font-size: 13px;
  color: #6b7280;
}

strong {
  font-size: 18px;
  color: #2563eb;
}

.description {
  margin-bottom: 16px;
  font-size: 14px;
  color: #374151;
  line-height: 1.5;
}

.detail-button {
  width: 100%;
  padding: 10px 0;
  border: none;
  border-radius: 10px;
  background-color: #2563eb;
  color: white;
  font-weight: 600;
  cursor: pointer;
}

.detail-button:hover {
  background-color: #1d4ed8;
}
</style>