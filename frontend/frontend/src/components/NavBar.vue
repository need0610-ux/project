<template>
  <header class="navbar">
    <div class="nav-inner">
      <RouterLink to="/" class="logo">
        <span class="logo-icon">💰</span>
        <span>FinBank</span>
      </RouterLink>

      <nav class="nav-menu">
        <RouterLink to="/products">상품조회</RouterLink>
        <RouterLink to="/recommend">예적금 추천</RouterLink>
        <RouterLink to="/bank-test">주거래은행 추천</RouterLink>
        <RouterLink to="/exchange">환율 계산기</RouterLink>
        <RouterLink to="/community">커뮤니티</RouterLink>
        <RouterLink to="/map">지도</RouterLink>
      </nav>

      <div class="nav-actions">
        <template v-if="isLoggedIn">
          <RouterLink to="/mypage" class="mypage-btn">
            마이페이지
          </RouterLink>

          <button type="button" class="logout-btn" @click="handleLogout">
            로그아웃
          </button>
        </template>

        <template v-else>
          <RouterLink to="/login" class="login-btn">
            로그인
          </RouterLink>

          <RouterLink to="/signup" class="signup-btn">
            회원가입
          </RouterLink>
        </template>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink, useRouter } from 'vue-router'

const router = useRouter()

const isLoggedIn = ref(!!localStorage.getItem('token'))

const checkLoginStatus = () => {
  const token = localStorage.getItem('token')
  isLoggedIn.value = !!token
}

const handleLogout = () => {
  localStorage.removeItem('token')
  isLoggedIn.value = false

  alert('로그아웃되었습니다.')

  router.push({ name: 'home' })
}

onMounted(() => {
  checkLoginStatus()

  window.addEventListener('storage', checkLoginStatus)
  window.addEventListener('login-success', checkLoginStatus)
})
</script>

<style scoped>
.navbar {
  width: 100%;
  border-bottom: 1px solid #d9d9d9;
  background-color: #fff;
}

.nav-inner {
  display: flex;
  align-items: center;
  min-height: 64px;
  max-width: 1440px;
  margin: 0 auto;
  padding: 0 28px;
  gap: 32px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
  padding: 8px 12px;
  border: 1px solid #bfbfbf;
  color: #222;
  font-weight: 700;
  text-decoration: none;
}

.logo-icon {
  font-size: 18px;
}

.nav-menu {
  display: flex;
  align-items: center;
  gap: clamp(14px, 2.2vw, 34px);
  flex: 1;
  min-width: 0;
}

.nav-menu a {
  color: #222;
  font-size: 14px;
  white-space: nowrap;
  text-decoration: none;
}

.nav-menu a.router-link-active {
  font-weight: 700;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}

.login-btn,
.signup-btn,
.mypage-btn,
.logout-btn {
  padding: 9px 16px;
  border: 1px solid #bfbfbf;
  color: #222;
  font-size: 14px;
  white-space: nowrap;
  text-decoration: none;
  background-color: #fff;
  cursor: pointer;
}

.mypage-btn {
  background-color: #333;
  color: white;
  border-color: #333;
}

.logout-btn {
  background-color: #fff;
  color: #222;
}

@media (max-width: 900px) {
  .nav-inner {
    align-items: flex-start;
    flex-direction: column;
    padding: 16px 20px;
    gap: 14px;
  }

  .nav-menu {
    flex-wrap: wrap;
    gap: 12px 20px;
  }

  .nav-actions {
    width: 100%;
  }
}

@media (max-width: 520px) {
  .nav-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .login-btn,
  .signup-btn,
  .mypage-btn,
  .logout-btn {
    text-align: center;
  }
}
</style>