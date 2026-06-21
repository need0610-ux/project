<template>
  <div class="mypage-view">
    <h1>마이페이지</h1>

    <section class="mypage-section">
      <h2>관심상품 목록</h2>

      <p v-if="loading">관심상품을 불러오는 중입니다...</p>
      <p v-else-if="errorMessage">{{ errorMessage }}</p>

      <div v-else>
        <p v-if="favoriteProducts.length === 0">
          등록된 관심상품이 없습니다.
        </p>

        <div
          v-for="favorite in favoriteProducts"
          :key="favorite.id"
          class="favorite-card"
        >
          <h3>{{ getProductName(favorite) }}</h3>

          <p>은행명: {{ getBankName(favorite) }}</p>
          <p>최고 금리: {{ formatRate(getMaxInterestRate(favorite)) }}</p>

          <RouterLink :to="{ name: 'product-detail', params: { id: getProductId(favorite) } }">
            상세 보기
          </RouterLink>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getFavoriteProducts } from '@/api/favorites'

const favoriteProducts = ref([])
const loading = ref(false)
const errorMessage = ref('')

const formatRate = (rate) => {
  if (rate === null || rate === undefined || rate === '') {
    return '정보 없음'
  }

  return `${rate}%`
}

const getProduct = (favorite) => {
  return favorite.product || favorite
}

const getProductId = (favorite) => {
  const product = getProduct(favorite)
  return product.id
}

const getProductName = (favorite) => {
  const product = getProduct(favorite)
  return product.name || '상품명 없음'
}

const getBankName = (favorite) => {
  const product = getProduct(favorite)
  return product.bank?.name || '은행명 없음'
}

const getMaxInterestRate = (favorite) => {
  const product = getProduct(favorite)
  return product.max_interest_rate
}

const fetchFavoriteProducts = async () => {
  loading.value = true
  errorMessage.value = ''

  try {
    const response = await getFavoriteProducts()

    console.log('관심상품 목록 응답:', response.data)

    favoriteProducts.value = response.data
  } catch (error) {
    console.error(error)

    if (error.response?.status === 401) {
      errorMessage.value = '로그인이 필요한 기능입니다.'
      return
    }

    errorMessage.value = '관심상품 목록을 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchFavoriteProducts()
})
</script>

<style scoped>
.mypage-view {
  padding: 24px;
}

.mypage-section {
  margin-top: 24px;
}

.favorite-card {
  padding: 16px;
  margin-bottom: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
}
</style>