import { defineStore } from 'pinia'
import { ref } from 'vue'
import { fetchReviews, createReview, updateReview, deleteReview } from '@/services/reviewService'

export const useReviewStore = defineStore('review', () => {
  const reviews = ref([])
  const loading = ref(false)
  const error = ref(null)

  const loadReviews = async () => {
    loading.value = true
    error.value = null
    try {
      const data = await fetchReviews()
      reviews.value = data
    } catch (err) {
      error.value = 'Error al cargar las reseñas.'
      console.error(err)
    } finally {
      loading.value = false
    }
  }

  const addReview = async (reviewData) => {
    const newReview = await createReview(reviewData)
    reviews.value.push(newReview)
  }

  const editReview = async (id, data) => {
    const updated = await updateReview(id, data)
    const index = reviews.value.findIndex((r) => r.id === id)
    reviews.value[index] = updated
  }

  const removeReview = async (id) => {
    await deleteReview(id)
    reviews.value = reviews.value.filter((r) => r.id !== id)
  }

  return {
    reviews,
    loading,
    error,
    loadReviews,
    addReview,
    editReview,
    removeReview,
  }
})
