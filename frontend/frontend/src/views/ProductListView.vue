<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/api'

const products = ref([])
const isLoading = ref(true)
const errorMessage = ref('')

onMounted(async () => {
  try {
    const response = await api.get('/products/deposits/')
    products.value = response.data
  } catch (error) {
    console.error(error)
    errorMessage.value = '정기예금 상품 목록을 불러오지 못했습니다.'
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <main>
    <h1>정기예금 상품 목록</h1>

    <p v-if="isLoading">상품을 불러오는 중입니다...</p>
    <p v-else-if="errorMessage">{{ errorMessage }}</p>

    <section v-else>
      <article v-for="product in products" :key="product.id">
        <h3>{{ product.name }}</h3>
        <p>은행: {{ product.bank.name }}</p>
        <p>가입방법: {{ product.join_way }}</p>
        <p>최고금리: {{ product.max_interest_rate }}%</p>
        <hr />
      </article>
    </section>
  </main>
</template>