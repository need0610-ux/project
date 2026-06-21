<template>
  <div class="product-detail-view">
    <h1>예금 상품 상세</h1>

    <p v-if="loading">상품 정보를 불러오는 중입니다...</p>
    <p v-else-if="errorMessage">{{ errorMessage }}</p>

    <div v-else-if="product" class="product-detail-card">
      <h2>{{ product.name }}</h2>

      <div class="product-info">
        <p>은행명: {{ product.bank?.name }}</p>
        <p>은행 코드: {{ product.bank?.code }}</p>
        <p>가입 방법: {{ product.join_way }}</p>
        <p>가입 대상: {{ product.join_member }}</p>
        <p>가입 한도: {{ product.max_limit || '정보 없음' }}</p>
        <p>최고 금리: {{ getProductMaxRate(product) }}</p>
        <p>우대 조건: {{ product.spcl_cnd }}</p>
        <p>기타 유의사항: {{ product.etc_note }}</p>
        <p>공시 시작일: {{ product.dcls_strt_day }}</p>
        <p>공시 종료일: {{ product.dcls_end_day || '없음' }}</p>
      </div>

      <button
        class="favorite-button"
        :class="{ active: isFavorite }"
        @click="handleFavoriteClick"
      >
        {{ isFavorite ? '관심상품 삭제' : '관심상품 등록' }}
      </button>

      <div v-if="product.options && product.options.length > 0" class="option-section">
        <h3>금리 옵션</h3>

        <table>
          <thead>
            <tr>
              <th>저축 기간</th>
              <th>기본 금리</th>
              <th>최고 우대 금리</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="option in product.options" :key="option.id">
              <td>{{ option.save_trm }}개월</td>
              <td>{{ formatRate(option.intr_rate) }}</td>
              <td>{{ formatRate(option.intr_rate2) }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <p v-else>금리 옵션 정보가 없습니다.</p>

      <RouterLink :to="{ name: 'products' }" class="back-link">
        목록으로 돌아가기
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getDepositProductDetail } from '@/api/products'
import { getFavorites, toggleFavoriteProduct } from '@/api/favorites'

const route = useRoute()

const product = ref(null)
const loading = ref(false)
const errorMessage = ref('')
const isFavorite = ref(false)

const formatRate = (rate) => {
  if (rate === null || rate === undefined || rate === '') {
    return '정보 없음'
  }

  return `${rate}%`
}

const getProductMaxRate = (product) => {
  if (!product) {
    return '정보 없음'
  }

  if (
    product.max_interest_rate !== null &&
    product.max_interest_rate !== undefined &&
    product.max_interest_rate !== ''
  ) {
    return `${product.max_interest_rate}%`
  }

  if (!product.options || product.options.length === 0) {
    return '정보 없음'
  }

  const rates = product.options
    .map((option) => Number(option.intr_rate2))
    .filter((rate) => !Number.isNaN(rate))

  if (rates.length === 0) {
    return '정보 없음'
  }

  return `${Math.max(...rates)}%`
}

const checkFavoriteStatus = async () => {
  const token = localStorage.getItem('token')

  if (!token || !product.value) {
    isFavorite.value = false
    return
  }

  try {
    const response = await getFavorites()

    const favorites = response.data

    isFavorite.value = favorites.some((favorite) => {
      const favoriteProduct = favorite.product || favorite
      return favoriteProduct.id === product.value.id
    })
  } catch (error) {
    console.error(error)
    isFavorite.value = false
  }
}

const handleFavoriteClick = async () => {
  if (!product.value) {
    return
  }

  const token = localStorage.getItem('token')

  if (!token) {
    alert('로그인이 필요한 기능입니다.')
    return
  }

  try {
    const response = await toggleFavoriteProduct(product.value.id)

    console.log('관심상품 응답:', response.data)

    isFavorite.value = response.data.is_favorite

    if (isFavorite.value) {
      alert('관심상품에 등록되었습니다.')
    } else {
      alert('관심상품에서 삭제되었습니다.')
    }
  } catch (error) {
    console.error(error)

    if (error.response?.status === 401 || error.response?.status === 403) {
      alert('로그인이 필요한 기능입니다.')
      return
    }

    alert('관심상품 처리 중 오류가 발생했습니다.')
  }
}

const fetchProductDetail = async () => {
  loading.value = true
  errorMessage.value = ''

  try {
    const productId = route.params.id

    const response = await getDepositProductDetail(productId)

    console.log('상품 상세 응답:', response.data)

    product.value = response.data

    await checkFavoriteStatus()
  } catch (error) {
    console.error(error)
    errorMessage.value = '상품 상세 정보를 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchProductDetail()
})
</script>

<style scoped>
.product-detail-view {
  padding: 24px;
}

.product-detail-card {
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.product-info {
  margin-bottom: 20px;
}

.product-info p {
  margin: 8px 0;
}

.favorite-button {
  padding: 10px 16px;
  margin-bottom: 24px;
  border: 1px solid #bbb;
  border-radius: 6px;
  background-color: #fff;
  cursor: pointer;
}

.favorite-button.active {
  background-color: #333;
  color: #fff;
  border-color: #333;
}

.option-section {
  margin-top: 16px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 16px 0;
}

th,
td {
  padding: 10px;
  border: 1px solid #ddd;
  text-align: center;
}

.back-link {
  display: inline-block;
  margin-top: 16px;
}
</style>