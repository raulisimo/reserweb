<template>
  <section class="container my-5 py-4">
    <h2 class="text-center mb-4 display-5 fw-bold">Que dicen nuestros usuarios</h2>
    <p class="text-center text-muted mb-5">Encuentra opiniones contrastadas</p>

    <!-- Filter controls -->
    <div class="d-flex justify-content-between align-items-center mb-4 flex-wrap">
      <div class="mb-2 mb-md-0">
        <label for="sortReviews" class="me-2">Ordenar por:</label>
        <select
          id="sortReviews"
          class="form-select form-select-sm d-inline-block w-auto"
          v-model="sortOption"
        >
          <option value="newest">Más recientes</option>
          <option value="highest">Mayor puntuación</option>
          <option value="lowest">Menor puntuación</option>
        </select>
      </div>
      <div>
        <label class="me-2">Filtrar por puntuación:</label>
        <div class="btn-group" role="group">
          <button
            v-for="star in 5"
            :key="star"
            @click="toggleStarFilter(star)"
            class="btn btn-sm"
            :class="starFilters.includes(star) ? 'btn-warning' : 'btn-outline-warning'"
          >
            {{ star }}★
          </button>
          <button @click="resetFilters" class="btn btn-sm btn-outline-secondary ms-2">Reset</button>
        </div>
      </div>
    </div>

    <!-- Reviews grid -->
    <div class="row g-4">
      <div
        v-for="(review, index) in filteredAndSortedReviews"
        :key="index"
        class="col-12 col-md-6 col-lg-4 mb-4"
      >
        <div class="card h-100 shadow border-0 review-card">
          <div class="card-header bg-white border-0 pt-4 px-4">
            <div class="d-flex justify-content-between align-items-center">
              <div class="d-flex align-items-center">
                <div class="avatar me-3 bg-primary text-white rounded-circle">
                  {{ getInitials(review.user) }}
                </div>
                <div>
                  <h5 class="mb-0">{{ review.user }}</h5>
                  <small class="text-muted">{{ formatDate(review.date) }}</small>
                </div>
              </div>
              <span class="badge bg-primary">{{ review.rating.toFixed(1) }}</span>
            </div>
          </div>
          <div class="card-body px-4">
            <div class="mb-3 stars">
              <span
                v-for="n in 5"
                :key="n"
                :class="[
                  'star',
                  n <= review.rating ? 'filled' : '',
                  n > review.rating && n - 1 < review.rating ? 'half' : '',
                ]"
                >★</span
              >
            </div>
            <p class="card-text fs-5 mb-2 quote">{{ review.comment }}</p>
            <p class="card-text medium text-muted">
              <i>{{ review.restaurant }}</i>
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- No results message -->
    <div
      v-if="filteredAndSortedReviews.length === 0 && !loading"
      class="text-center py-5 text-muted"
    >
      <div class="mb-3 display-6">😕</div>
      <h5>No se han encontrado reseñas con tus filtros</h5>
      <button @click="resetFilters" class="btn btn-outline-primary mt-2">
        Restablecer filtros
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
      <p class="mt-3">Cargando reseñas...</p>
    </div>

    <!-- Pagination or Load More -->
    <div
      class="text-center mt-4"
      v-if="totalReviews > visibleCount && filteredAndSortedReviews.length > 0 && !loading"
    >
      <button class="btn btn-primary px-4" @click="loadMore">Cargar mas reviews</button>
      <p class="small text-muted mt-2">
        Mostrando {{ filteredAndSortedReviews.length }} de {{ totalFilteredReviews }} opiniones
      </p>
    </div>
  </section>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { fetchReviews } from '@/services/reviewService'

export default {
  setup() {
    const sortOption = ref('newest')
    const starFilters = ref([])
    const visibleCount = ref(6)
    const reviews = ref([])
    const loading = ref(false)
    const error = ref(null)

    const loadReviews = async () => {
      loading.value = true
      error.value = null
      try {
        const data = await fetchReviews()
        reviews.value = data.map((item) => ({
          id: item.id,
          user: item.user_name,
          restaurant: item.restaurant_name,
          comment: item.comment || 'No se ha proporcionado un comentario.',
          rating: item.rating,
          date: item.created_at,
        }))
      } catch (err) {
        console.error('Error fetching reviews:', err)
        error.value = 'Failed to load reviews'
      } finally {
        loading.value = false
      }
    }

    const totalReviews = computed(() => reviews.value.length)

    const getFilteredReviews = () => {
      if (starFilters.value.length === 0) {
        return [...reviews.value]
      }
      return reviews.value.filter((review) => {
        const roundedRating = Math.round(review.rating)
        return starFilters.value.includes(roundedRating)
      })
    }

    const getSortedReviews = (reviewsList) => {
      const sorted = [...reviewsList]
      switch (sortOption.value) {
        case 'newest':
          return sorted.sort((a, b) => new Date(b.date) - new Date(a.date))
        case 'highest':
          return sorted.sort((a, b) => b.rating - a.rating)
        case 'lowest':
          return sorted.sort((a, b) => a.rating - b.rating)
        default:
          return sorted
      }
    }

    const totalFilteredReviews = computed(() => getFilteredReviews().length)

    const filteredAndSortedReviews = computed(() => {
      const filtered = getFilteredReviews()
      const sorted = getSortedReviews(filtered)
      return sorted.slice(0, visibleCount.value)
    })

    const toggleStarFilter = (star) => {
      const index = starFilters.value.indexOf(star)
      if (index === -1) {
        starFilters.value.push(star)
      } else {
        starFilters.value.splice(index, 1)
      }
      visibleCount.value = 6
    }

    const resetFilters = () => {
      starFilters.value = []
      sortOption.value = 'newest'
      visibleCount.value = 6
    }

    const loadMore = () => {
      visibleCount.value += 3
      if (visibleCount.value > totalFilteredReviews.value) {
        visibleCount.value = totalFilteredReviews.value
      }
    }

    const getInitials = (name) => {
      return name
        .split(' ')
        .map((word) => word[0])
        .join('')
        .toUpperCase()
    }

    const formatDate = (dateString) => {
      const options = { year: 'numeric', month: 'short', day: 'numeric' }
      return new Date(dateString).toLocaleDateString(undefined, options)
    }

    onMounted(() => {
      loadReviews()
    })

    return {
      sortOption,
      starFilters,
      visibleCount,
      reviews,
      loading,
      error,
      fetchReviews,
      filteredAndSortedReviews,
      totalReviews,
      totalFilteredReviews,
      toggleStarFilter,
      resetFilters,
      loadMore,
      getInitials,
      formatDate,
    }
  },
}
</script>

<style scoped>
.review-card {
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
  border-radius: 12px;
  overflow: hidden;
}

.review-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1) !important;
}

.avatar {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.stars {
  color: #e0e0e0;
  font-size: 1.2rem;
}

.star.filled {
  color: #ffc107;
}

.star.half {
  position: relative;
  display: inline-block;
}

.star.half:after {
  content: '★';
  position: absolute;
  left: 0;
  top: 0;
  width: 50%;
  overflow: hidden;
  color: #ffc107;
}

.quote {
  position: relative;
  padding-left: 5px;
}

@media (max-width: 767px) {
  .review-card:hover {
    transform: none;
  }
}
</style>
