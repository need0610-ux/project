<template>
  <div class="signup-view">
    <h1>회원가입</h1>

    <form class="signup-form" @submit.prevent="handleSignup">
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
        <label for="password1">비밀번호</label>
        <input
          id="password1"
          v-model="password1"
          type="password"
          placeholder="비밀번호를 입력하세요"
        >
      </div>

      <div>
        <label for="password2">비밀번호 확인</label>
        <input
          id="password2"
          v-model="password2"
          type="password"
          placeholder="비밀번호를 다시 입력하세요"
        >
      </div>

      <button type="submit">회원가입</button>
    </form>

    <p v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { signup } from '@/api/accounts'

const router = useRouter()

const username = ref('')
const password1 = ref('')
const password2 = ref('')
const errorMessage = ref('')

const handleSignup = async () => {
  errorMessage.value = ''

  if (!username.value || !password1.value || !password2.value) {
    errorMessage.value = '아이디와 비밀번호를 모두 입력해주세요.'
    return
  }

  if (password1.value !== password2.value) {
    errorMessage.value = '비밀번호가 일치하지 않습니다.'
    return
  }

  try {
    const response = await signup({
      username: username.value,
      password: password1.value,
      password_confirm: password2.value,
    })

    console.log('회원가입 응답:', response.data)

    alert('회원가입이 완료되었습니다.')

    router.push({ name: 'login' })
  } catch (error) {
    console.error(error)

    if (error.response?.data) {
      errorMessage.value = JSON.stringify(error.response.data)
      return
    }

    errorMessage.value = '회원가입 중 오류가 발생했습니다.'
  }
}
</script>

<style scoped>
.signup-view {
  padding: 24px;
}

.signup-form {
  max-width: 360px;
}

.signup-form div {
  margin-bottom: 12px;
}

.signup-form label {
  display: block;
  margin-bottom: 4px;
}

.signup-form input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}

.signup-form button {
  padding: 8px 16px;
  cursor: pointer;
}

.error-message {
  margin-top: 16px;
}
</style>