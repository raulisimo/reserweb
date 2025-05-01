<template>
  <div class="app-container">
    <Header />
    <main>
      <slot></slot>
    </main>
    <Footer />
  </div>
</template>

<script setup>
import Header from '@/components/TheHeader.vue'
import Footer from '@/components/TheFooter.vue'
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
main {
  flex: 1;
}
</style>
