import { defineStore } from 'pinia'
import { ref } from 'vue'
import {
  fetchRestaurants,
  createRestaurant,
  updateRestaurant,
  deleteRestaurant,
} from '@/services/restaurantService'

export const useRestaurantStore = defineStore('restaurant', () => {
  const restaurants = ref([])
  const loading = ref(false)
  const error = ref(null)

  const loadRestaurants = async () => {
    loading.value = true
    error.value = null
    try {
      const data = await fetchRestaurants()
      console.log(data)
      restaurants.value = data
    } catch (err) {
      error.value = 'Error al cargar los restaurantes.'
      console.error(err)
    } finally {
      loading.value = false
    }
  }

  const addRestaurant = async (restaurantData) => {
    const newRestaurant = await createRestaurant(restaurantData)
    restaurants.value.push(newRestaurant)
  }

  const editRestaurant = async (id, data) => {
    const updated = await updateRestaurant(id, data)
    const index = restaurants.value.findIndex((r) => r.id === id)
    restaurants.value[index] = updated
  }

  const removeRestaurant = async (id) => {
    await deleteRestaurant(id)
    restaurants.value = restaurants.value.filter((r) => r.id !== id)
  }

  return {
    restaurants,
    loading,
    error,
    loadRestaurants,
    addRestaurant,
    editRestaurant,
    removeRestaurant,
  }
})
