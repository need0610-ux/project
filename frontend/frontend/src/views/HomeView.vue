<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <main>
    <h1>예적금 추천 서비스</h1>
    <p>정기예금 상품 조회, 주거래은행 추천, 환율 계산, 금융 챗봇 기능을 제공합니다.</p>

    <RouterLink to="/products">
      정기예금 상품 보러가기
    </RouterLink>
  </main>
</template>