<template>
  <div class="product-list-view">
    <h1>예금 상품 목록</h1>

    <p v-if="loading">상품을 불러오는 중입니다...</p>
    <p v-else-if="errorMessage">{{ errorMessage }}</p>

    <div v-else>
      <p v-if="products.length === 0">조회된 상품이 없습니다.</p>

      <div
        v-for="product in products"
        :key="product.id"
        class="product-card"
      >
        <h3>{{ product.name }}</h3>

        <p>은행명: {{ product.bank?.name }}</p>
        <p>은행 코드: {{ product.bank?.code }}</p>
        <p>가입 방법: {{ product.join_way }}</p>
        <p>최고 금리: {{ formatRate(product.max_interest_rate) }}</p>

        <div class="product-actions">
          <RouterLink :to="{ name: 'product-detail', params: { id: product.id } }">
            상세 보기
          </RouterLink>

          <button
            type="button"
            class="favorite-btn"
            :class="{ active: isFavorite(product.id) }"
            @click="handleToggleFavorite(product.id)"
          >
            {{ isFavorite(product.id) ? '관심상품 삭제' : '관심상품 등록' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getDepositProducts } from '@/api/products'
import { getFavorites, toggleFavoriteProduct } from '@/api/favorites'

const products = ref([])
const favoriteProductIds = ref([])
const loading = ref(false)
const errorMessage = ref('')

const formatRate = (rate) => {
  if (rate === null || rate === undefined || rate === '') {
    return '정보 없음'
  }

  return `${rate}%`
}

const isFavorite = (productId) => {
  return favoriteProductIds.value.includes(productId)
}

const fetchProducts = async () => {
  loading.value = true
  errorMessage.value = ''

  try {
    const response = await getDepositProducts()

    console.log('상품 목록 응답:', response.data)

    products.value = response.data
  } catch (error) {
    console.error(error)
    errorMessage.value = '상품 목록을 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

const fetchFavorites = async () => {
  const token = localStorage.getItem('token')

  if (!token) {
    favoriteProductIds.value = []
    return
  }

  try {
    const response = await getFavorites()

    console.log('관심상품 목록 응답:', response.data)

    favoriteProductIds.value = response.data.map((favorite) => {
      const product = favorite.product || favorite
      return product.id
    })
  } catch (error) {
    console.error(error)
    favoriteProductIds.value = []
  }
}

const handleToggleFavorite = async (productId) => {
  const token = localStorage.getItem('token')

  if (!token) {
    alert('로그인이 필요한 기능입니다.')
    return
  }

  try {
    const response = await toggleFavoriteProduct(productId)

    console.log('관심상품 토글 응답:', response.data)

    const isNowFavorite = response.data.is_favorite

    if (isNowFavorite) {
      favoriteProductIds.value.push(productId)
      alert('관심상품에 등록되었습니다.')
    } else {
      favoriteProductIds.value = favoriteProductIds.value.filter((id) => {
        return id !== productId
      })
      alert('관심상품에서 삭제되었습니다.')
    }
  } catch (error) {
    console.error(error)

    if (error.response?.status === 401 || error.response?.status === 403) {
      alert('로그인이 필요한 기능입니다.')
      return
    }

    alert('관심상품 처리에 실패했습니다.')
  }
}

onMounted(async () => {
  await fetchProducts()
  await fetchFavorites()
})
</script>

<style scoped>
.product-list-view {
  padding: 24px;
}

.product-card {
  padding: 16px;
  margin-bottom: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.product-actions {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-top: 16px;
}

.favorite-btn {
  padding: 8px 14px;
  border: 1px solid #bbb;
  border-radius: 6px;
  background-color: #fff;
  cursor: pointer;
}

.favorite-btn.active {
  background-color: #333;
  color: #fff;
  border-color: #333;
}
</style>