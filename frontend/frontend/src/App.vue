<template>
  <div>
    <NavBar />

    <main>
      <RouterView />
    </main>

    <ChatBotButton />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import NavBar from '@/components/NavBar.vue'
import ChatBotButton from '@/components/ChatBotButton.vue'
</script>