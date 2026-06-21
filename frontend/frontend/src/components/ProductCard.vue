<template>
  <article class="product-card">
    <div class="logo-box">로고</div>

    <div class="product-main">
      <p class="bank-name">{{ product.bankName }}</p>
      <h4>{{ product.productName }}</h4>
    </div>

    <div class="product-meta">
      <div>
        <span>최고 금리</span>
        <strong>{{ product.maxRate }}</strong>
      </div>
      <div>
        <span>가입 기간</span>
        <strong>{{ product.term }}</strong>
      </div>
      <div>
        <span>가입 방식</span>
        <strong>{{ product.joinWay }}</strong>
      </div>
    </div>

    <div class="product-actions">
      <button type="button" class="favorite-btn" @click="$emit('toggle-favorite', product)">
        관심
      </button>

      <RouterLink :to="`/products/${product.id}`" class="detail-btn">
        상세보기
      </RouterLink>
    </div>
  </article>
</template>

<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  product: {
    type: Object,
    required: true,
  },
})

defineEmits(['toggle-favorite'])
</script>

<style scoped>
.product-card {
  display: grid;
  grid-template-columns: 72px minmax(180px, 1fr) auto auto;
  align-items: center;
  gap: 18px;
  padding: 14px;
  border: 1px solid #bfbfbf;
  background-color: #fff;
}

.logo-box {
  width: 60px;
  height: 44px;
  border: 1px solid #bfbfbf;
  background-color: #e6e6e6;
  color: #555;
  font-size: 13px;
  line-height: 44px;
  text-align: center;
}

.bank-name {
  margin: 0 0 6px;
  color: #777;
  font-size: 13px;
}

.product-main h4 {
  margin: 0;
  font-size: 15px;
}

.product-meta {
  display: flex;
  gap: 22px;
}

.product-meta div {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 60px;
}

.product-meta span {
  color: #666;
  font-size: 13px;
}

.product-meta strong {
  font-size: 15px;
}

.product-actions {
  display: flex;
  gap: 8px;
}

.favorite-btn,
.detail-btn {
  padding: 8px 12px;
  border: 1px solid #999;
  background-color: #fff;
  color: #222;
  font-size: 13px;
  text-decoration: none;
  cursor: pointer;
}

.favorite-btn:hover,
.detail-btn:hover {
  background-color: #f2f2f2;
}

@media (max-width: 900px) {
  .product-card {
    grid-template-columns: 60px 1fr;
  }

  .product-meta,
  .product-actions {
    grid-column: 1 / -1;
  }

  .product-meta {
    flex-wrap: wrap;
  }
}

@media (max-width: 520px) {
  .product-card {
    grid-template-columns: 1fr;
  }

  .logo-box {
    width: 100%;
  }

  .product-actions {
    flex-direction: column;
  }

  .favorite-btn,
  .detail-btn {
    text-align: center;
  }
}
</style>