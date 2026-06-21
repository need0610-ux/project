import api from './api'

// 회원가입
export const signup = (signupData) => {
  return api.post('/accounts/signup/', signupData)
}

// 로그인
export const login = (loginData) => {
  return api.post('/accounts/login/', loginData)
}

// 프로필 조회
export const getProfile = () => {
  return api.get('/accounts/profile/')
}