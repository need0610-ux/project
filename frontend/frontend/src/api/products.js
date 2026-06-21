import api from './api'

// 예금 상품 목록 조회
export const getDepositProducts = () => {
  return api.get('/products/deposits/')
}

// 예금 상품 상세 조회
export const getDepositProductDetail = (productId) => {
  return api.get(`/products/deposits/${productId}/`)
}