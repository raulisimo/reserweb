<template>
  <main>
    <BaseLayout>
      <component v-if="profileComponent" :is="profileComponent" />
      <div v-else class="text-center mt-5">
        <h4>Inicia sesión para ver tu perfil.</h4>
        <router-link to="/login" class="btn btn-primary mt-3">Ir al inicio de sesión</router-link>
      </div>
    </BaseLayout>
  </main>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

import BaseLayout from '@/views/layouts/BaseLayout.vue'
import ProfileClient from '@/components/ProfileClient.vue'
import ProfileRestaurant from '@/components/ProfileRestaurant.vue'

const authStore = useAuthStore()

const profileComponent = computed(() => {
  if (!authStore.user) return null
  return authStore.user.role === 'restaurant' ? ProfileRestaurant : ProfileClient
})
</script>
