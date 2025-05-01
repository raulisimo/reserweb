<template>
  <main>
    <BaseLayout>
      <div class="container py-5">
        <h2 class="mb-4">Restaurantes</h2>

        <!-- Sorting dropdown -->
        <div class="mb-4 d-flex justify-content-end">
          <select class="form-select w-auto" v-model="sortOrder" @change="sortRestaurants">
            <option value="desc">⭐ Mejor puntuación</option>
            <option value="asc">⭐ Peor puntuación</option>
          </select>
        </div>

        <!-- Loading Spinner -->
        <div v-if="loading" class="d-flex align-items-center mb-3">
          <div class="spinner-border text-primary me-2" role="status"></div>
          <span>Cargando restaurantes...</span>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="alert alert-danger">{{ error }}</div>

        <!-- Restaurant Cards -->
        <div class="row">
          <div
            v-for="restaurant in sortedRestaurants"
            :key="restaurant.id"
            class="col-md-6 col-lg-4 mb-4"
          >
            <router-link :to="`/restaurant/${restaurant.id}`" class="card-link">
              <div class="card restaurant-card h-100 p-4 position-relative">
                <!-- Score badge -->
                <div v-if="restaurant.avg_score !== null" class="score-badge">
                  ⭐ {{ restaurant.avg_score.toFixed(1) }}
                </div>

                <div class="d-flex flex-column h-100">
                  <div class="mb-3">
                    <h5 class="fw-bold text-dark mb-1">{{ restaurant.name }}</h5>
                    <p class="text-muted small mb-0">{{ restaurant.description }}</p>
                  </div>

                  <div class="mt-auto">
                    <div class="mb-2">
                      <span class="fw-semibold text-dark">Dirección:</span>
                      <div class="text-muted small">{{ restaurant.address }}</div>
                    </div>

                    <div>
                      <span class="fw-semibold text-dark">Teléfono:</span>
                      <div class="text-muted small">{{ restaurant.phone }}</div>
                    </div>
                  </div>
                </div>
              </div>
            </router-link>
          </div>
        </div>
      </div>
    </BaseLayout>
  </main>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import BaseLayout from '@/views/layouts/BaseLayout.vue'
import { fetchRestaurantswithScore } from '@/services/restaurantService.js'

const restaurants = ref([])
const loading = ref(true)
const error = ref(null)
const sortOrder = ref('desc')

onMounted(async () => {
  try {
    const data = await fetchRestaurantswithScore()
    restaurants.value = data
  } catch (err) {
    console.log(err)
    error.value = 'No se pudieron cargar los restaurantes.'
  } finally {
    loading.value = false
  }
})

const sortedRestaurants = computed(() => {
  const sorted = [...restaurants.value]
  sorted.sort((a, b) => {
    const aScore = a.avg_score ?? 0
    const bScore = b.avg_score ?? 0
    return sortOrder.value === 'asc' ? aScore - bScore : bScore - aScore
  })
  return sorted
})

function sortRestaurants() {
  // Trigger re-computation (already reactive)
}
</script>

<style scoped>
.restaurant-card {
  background-color: #fff;
  border-radius: 12px;
  border: 1px solid #eee;
  transition:
    transform 0.25s ease,
    box-shadow 0.25s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.restaurant-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
}

.card-link {
  text-decoration: none;
  color: inherit;
  display: block;
  height: 100%;
}

/* Score badge */
.score-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  background-color: #e8e5e2;
  color: #000;
  padding: 4px 10px;
  font-size: 0.875rem;
  border-radius: 20px;
  font-weight: 600;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
}
</style>
