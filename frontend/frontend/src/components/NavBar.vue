<template>
  <nav>
    <RouterLink to="/">홈</RouterLink>
    <RouterLink to="/products">예적금</RouterLink>
    <RouterLink to="/bank-test">주거래은행 검사</RouterLink>
    <RouterLink to="/exchange">환율 계산기</RouterLink>
    <RouterLink to="/community">커뮤니티</RouterLink>
    <RouterLink to="/login">로그인</RouterLink>
  </nav>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<style scoped>
nav {
  display: flex;
  gap: 16px;
  padding: 16px;
  border-bottom: 1px solid #ddd;
}

a {
  text-decoration: none;
  color: #333;
}
</style>