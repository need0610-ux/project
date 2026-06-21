<template>
  <div class="app">
    <NavBar />

    <main class="main">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
</script>

<style scoped>
.app {
  min-height: 100vh;
  background-color: #ffffff;
  color: #222;
}

.main {
  width: 100%;
  max-width: 1440px;
  margin: 0 auto;
}
</style>