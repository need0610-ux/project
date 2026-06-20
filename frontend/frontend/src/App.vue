<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div>
    <nav>
      <RouterLink to="/">홈</RouterLink>
      |
      <RouterLink to="/products">정기예금 상품</RouterLink>
    </nav>

    <RouterView />
  </div>
</template>