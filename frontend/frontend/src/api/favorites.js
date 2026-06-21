import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000/api/favorites/'

const getAuthHeaders = () => {
  const token = localStorage.getItem('token')

  return {
    headers: {
      Authorization: `Token ${token}`,
    },
  }
}

export const getFavorites = () => {
  return axios.get(API_URL, getAuthHeaders())
}

export const getFavoriteProducts = () => {
  return getFavorites()
}

export const addFavorite = (productId) => {
  return axios.post(`${API_URL}${productId}/`, {}, getAuthHeaders())
}

export const toggleFavoriteProduct = (productId) => {
  return axios.post(`${API_URL}${productId}/`, {}, getAuthHeaders())
}