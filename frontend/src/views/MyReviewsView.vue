<template>
  <main>
    <BaseLayout>
      <div class="container py-5">
        <h2 class="mb-4">Mis Reseñas</h2>

        <!-- Review Form -->
        <div class="card mb-4">
          <div class="card-body">
            <h5 class="card-title">{{ editingReview ? 'Editar Reseña' : 'Nueva Reseña' }}</h5>
            <form @submit.prevent="submitReview">
              <div class="mb-3">
                <label for="restaurant" class="form-label">Restaurante</label>
                <select v-model="form.restaurant_id" class="form-select" required>
                  <option disabled value="">Seleccione un restaurante</option>
                  <option v-for="r in restaurants" :key="r.id" :value="r.id">
                    {{ r.name }}
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">Calificación (1-5)</label>
                <input
                  type="number"
                  class="form-control"
                  v-model.number="form.rating"
                  min="1"
                  max="5"
                  required
                />
              </div>
              <div class="mb-3">
                <label class="form-label">Comentario</label>
                <textarea class="form-control" v-model="form.comment" rows="3" required></textarea>
              </div>
              <button type="submit" class="btn btn-primary">
                {{ editingReview ? 'Actualizar' : 'Crear' }}
              </button>
              <button
                v-if="editingReview"
                type="button"
                class="btn btn-secondary ms-2"
                @click="cancelEdit"
              >
                Cancelar
              </button>
            </form>
          </div>
        </div>

        <!-- Reviews List -->
        <div>
          <h4>Tus reseñas</h4>
          <div v-if="reviews.length">
            <div class="card mb-3" v-for="review in reviews" :key="review.id">
              <div class="card-body">
                <h5 class="card-title">{{ review.restaurant_name }}</h5>
                <p><strong>Calificación:</strong> {{ review.rating }}/5</p>
                <p>{{ review.comment }}</p>
                <button class="btn btn-sm btn-warning me-2" @click="editReview(review)">
                  Editar
                </button>
                <button class="btn btn-sm btn-danger" @click="removeReview(review.id)">
                  Eliminar
                </button>
              </div>
            </div>
          </div>
          <p v-else>No has escrito ninguna reseña aún.</p>
        </div>
      </div>
    </BaseLayout>
  </main>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import BaseLayout from '@/views/layouts/BaseLayout.vue'
import { useAuthStore } from '@/stores/auth'
import {
  fetchUserReviews,
  createReview,
  updateReview,
  deleteReview,
} from '@/services/reviewService'
import { fetchRestaurants } from '@/services/restaurantService'

// State
const authStore = useAuthStore()
const user = computed(() => authStore.user)

const reviews = ref([])
const restaurants = ref([])
const form = ref({ restaurant_id: '', rating: '', comment: '' })
const editingReview = ref(null)

const getRestaurants = async () => {
  restaurants.value = await fetchRestaurants()
}

const loadData = async () => {
  if (!user.value) return
  reviews.value = await fetchUserReviews(user.value.id)
  await getRestaurants()
}

onMounted(loadData)

// Submit (Create or Update)
const submitReview = async () => {
  try {
    if (editingReview.value) {
      await updateReview(editingReview.value.id, form.value)
    } else {
      await createReview({ ...form.value, user_id: user.value.id })
    }
    await loadData()
    cancelEdit()
  } catch (error) {
    // eslint-disable-next-line no-undef
    alert(error.message)
  }
}

// Edit a review
const editReview = (review) => {
  editingReview.value = review
  form.value = { ...review }
}

// Cancel edit
const cancelEdit = () => {
  editingReview.value = null
  form.value = { restaurant_id: '', rating: '', comment: '' }
}

// Delete
const removeReview = async (id) => {
  // eslint-disable-next-line no-undef
  if (confirm('¿Estás seguro de eliminar esta reseña?')) {
    await deleteReview(id)
    await loadData()
  }
}
</script>

<style scoped>
.card-body {
  background-color: #f8f9fa;
}
</style>
