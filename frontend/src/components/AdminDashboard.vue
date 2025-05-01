<template>
  <div class="admin-dashboard">
    <img v-if="imageUrl" :src="imageUrl" alt="Dashboard Image" class="logo" />
    <h1>Bienvenido al Backoffice de Reserweb</h1>
    <p>Selecciona una sección en el menú para comenzar.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { fetchUnsplashImages } from '@/services/imageService'

const imageUrl = ref(null)

onMounted(async () => {
  try {
    const images = await fetchUnsplashImages('restaurant')
    if (images.length > 0) {
      imageUrl.value = images[0].urls.regular
    }
  } catch (error) {
    console.log(error)
    console.warn('No image loaded')
  }
})
</script>

<style scoped>
.admin-dashboard {
  text-align: center;
  margin-top: 60px;
  color: #333;
}

.logo {
  width: 100%;
  max-width: none;
  height: 300px;
  object-fit: cover;
  border-radius: 0;
  margin-bottom: 30px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
</style>
