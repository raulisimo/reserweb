<template>
  <BaseLayout>
    <div class="not-found text-center">
      <h1 class="display-1 text-danger">404</h1>
      <h2 class="text-secondary">No encontramos lo que buscas</h2>
      <p class="mt-3">
        <RouterLink to="/" class="btn btn-primary mt-3">Vuelve al inicio</RouterLink>
      </p>
    </div>
  </BaseLayout>
</template>

<script setup>
import BaseLayout from '@/views/layouts/BaseLayout.vue'
</script>

<style scoped>
.not-found {
  margin-top: 100px;
}
h1 {
  font-size: 10rem;
  font-weight: 700;
}
h2 {
  font-size: 2rem;
  color: #6c757d;
}
</style>
