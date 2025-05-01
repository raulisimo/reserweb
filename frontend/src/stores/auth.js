/* eslint-disable no-undef */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as loginService } from '@/services/authService'

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref(localStorage.getItem('access_token') || null)
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  const isAuthenticated = computed(() => !!accessToken.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isClient = computed(() => user.value?.role === 'client')
  const isRestaurant = computed(() => user.value?.role === 'restaurant')

  const userId = computed(() => user.value?.id)

  const login = async (credentials) => {
    const response = await loginService(credentials)

    accessToken.value = response.access_token
    user.value = response.user

    localStorage.setItem('access_token', response.access_token)
    localStorage.setItem('user', JSON.stringify(response.user))
  }

  const logout = () => {
    accessToken.value = null
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
  }

  return {
    userId,
    accessToken,
    user,
    isAuthenticated,
    isAdmin,
    isClient,
    isRestaurant,
    login,
    logout,
  }
})
