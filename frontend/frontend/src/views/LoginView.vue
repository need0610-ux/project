<template>
  <div class="login-view">
    <h1>로그인</h1>

    <form class="login-form" @submit.prevent="handleLogin">
      <div>
        <label for="username">아이디</label>
        <input
          id="username"
          v-model="username"
          type="text"
          placeholder="아이디를 입력하세요"
        >
      </div>

      <div>
        <label for="password">비밀번호</label>
        <input
          id="password"
          v-model="password"
          type="password"
          placeholder="비밀번호를 입력하세요"
        >
      </div>

      <button type="submit">로그인</button>
    </form>

    <p class="signup-link">
      아직 계정이 없으신가요?
      <RouterLink :to="{ name: 'signup' }">
        회원가입
      </RouterLink>
    </p>

    <p v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '@/api/accounts'

const router = useRouter()

const username = ref('')
const password = ref('')
const errorMessage = ref('')

const handleLogin = async () => {
  errorMessage.value = ''

  if (!username.value || !password.value) {
    errorMessage.value = '아이디와 비밀번호를 입력해주세요.'
    return
  }

  try {
    const response = await login({
      username: username.value,
      password: password.value,
    })

    console.log('로그인 응답:', response.data)

    const token = response.data.token

    if (!token) {
      errorMessage.value = '로그인 응답에서 토큰을 찾을 수 없습니다.'
      return
    }

    // 1. 토큰 저장
    localStorage.setItem('token', token)

    // 2. Navbar에게 로그인 상태가 바뀌었다고 알려주기
    window.dispatchEvent(new Event('login-success'))

    alert('로그인되었습니다.')

    // 3. 홈으로 이동
    router.push({ name: 'home' })
  } catch (error) {
    console.error(error)

    if (error.response?.data?.message) {
      errorMessage.value = error.response.data.message
    } else {
      errorMessage.value = '로그인에 실패했습니다. 아이디와 비밀번호를 확인해주세요.'
    }
  }
}
</script>

<style scoped>
.login-view {
  padding: 24px;
}

.login-form {
  max-width: 360px;
}

.login-form div {
  margin-bottom: 12px;
}

.login-form label {
  display: block;
  margin-bottom: 4px;
}

.login-form input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}

.login-form button {
  padding: 8px 16px;
  cursor: pointer;
}

.signup-link {
  margin-top: 16px;
}

.error-message {
  margin-top: 16px;
}
</style>