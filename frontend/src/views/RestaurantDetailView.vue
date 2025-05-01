<template>
  <BaseLayout>
    <div class="restaurant-detail">
      <div
        v-if="loading"
        class="d-flex justify-content-center align-items-center"
        style="height: 70vh"
      >
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Cargando...</span>
        </div>
      </div>

      <div v-else>
        <section class="restaurant-hero position-relative">
          <div class="cover-image-container">
            <img v-if="coverImageUrl" :src="coverImageUrl" alt="Pasta Palace" class="cover-image" />
            <div class="overlay"></div>
          </div>
          <div class="container position-relative z-1">
            <div class="restaurant-header">
              <h1 class="restaurant-name display-4 fw-bold text-white">{{ restaurant.name }}</h1>
              <div class="restaurant-badges">
                <span class="badge bg-success me-2">Open Now</span>
              </div>
            </div>
          </div>
        </section>
      </div>

      <!-- Main Content -->
      <section class="container py-5">
        <div class="row g-4">
          <!-- Left Column: Restaurant Info -->
          <div class="col-lg-8">
            <!-- About -->
            <div class="card shadow-sm mb-4">
              <div class="card-header bg-white">
                <h3 class="card-title h5 mb-0">Sobre {{ restaurant.name }}</h3>
              </div>
              <div class="card-body">
                <p class="description">{{ restaurant.description }}</p>
                <hr />
              </div>
            </div>

            <!-- Popular Dishes -->
            <div class="card shadow-sm mb-4">
              <div class="card-header bg-white d-flex justify-content-between align-items-center">
                <h3 class="card-title h5 mb-0">Platos Populares</h3>
                <span class="badge bg-primary">{{ menuItems.length }} platos</span>
              </div>
              <div class="card-body p-0">
                <div class="popular-dishes">
                  <!-- Loop through the menuItems and display each one -->
                  <div
                    v-for="(item, index) in menuItems"
                    :key="item.id"
                    class="dish-card p-3"
                    :class="{ 'border-bottom': index !== menuItems.length - 1 }"
                  >
                    <div class="dish-info">
                      <div class="d-flex justify-content-between align-items-start mb-2">
                        <h4 class="dish-name h6 mb-0 me-2">{{ item.name }}</h4>
                        <span class="dish-price badge bg-light text-dark"
                          >${{ item.price.toFixed(2) }}</span
                        >
                      </div>
                      <p class="dish-description mb-2">{{ item.description }}</p>
                      <div class="dish-tags" v-if="item.tags && item.tags.length">
                        <span
                          v-for="tag in item.tags"
                          :key="tag"
                          class="badge bg-secondary bg-opacity-10 text-secondary me-1"
                        >
                          {{ tag }}
                        </span>
                      </div>
                    </div>
                  </div>

                  <!-- Empty state when no menu items are available -->
                  <div v-if="menuItems.length === 0" class="p-4 text-center">
                    <i class="fas fa-utensils text-muted mb-3" style="font-size: 2rem"></i>
                    <p class="text-muted">No hay platos disponibles en este momento.</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Reviews -->
            <div class="card shadow-sm mb-4" v-if="reviews.length > 0">
              <div class="card-header bg-white d-flex justify-content-between align-items-center">
                <h3 class="card-title h5 mb-0">Reviews</h3>
                <span class="btn btn-sm btn-light disabled">{{ totalReviews }} total</span>
              </div>
              <div class="card-body pt-0">
                <div class="review-summary d-flex align-items-center my-3 p-3 bg-light rounded">
                  <div class="ratings-average text-center me-4">
                    <div class="display-4 fw-bold text-primary">{{ averageRating }}</div>
                    <div class="ratings-stars">
                      <i
                        v-for="n in 5"
                        :key="n"
                        :class="[
                          'fas',
                          n <= Math.round(averageRating)
                            ? 'fa-star text-warning'
                            : 'far fa-star text-warning',
                        ]"
                      ></i>
                    </div>
                    <small class="text-muted">{{ totalReviews }} reseñas</small>
                  </div>
                  <div class="ratings-breakdown flex-grow-1">
                    <div v-for="n in 5" :key="n" class="rating-bar d-flex align-items-center mb-1">
                      <span class="me-2">{{ 6 - n }}</span>
                      <div class="progress flex-grow-1 me-2">
                        <div
                          class="progress-bar"
                          :class="
                            6 - n >= 4 ? 'bg-success' : 6 - n === 3 ? 'bg-warning' : 'bg-danger'
                          "
                          :style="{
                            width: ((ratingCounts[6 - n] / totalReviews) * 100).toFixed(1) + '%',
                          }"
                        ></div>
                      </div>
                      <span class="text-muted small"
                        >{{ ((ratingCounts[6 - n] / totalReviews) * 100).toFixed(1) || 0 }}%</span
                      >
                    </div>
                  </div>
                </div>

                <div
                  v-for="review in reviews"
                  :key="review.id"
                  class="review-card p-3 border-bottom"
                >
                  <div class="d-flex mb-2">
                    <div
                      class="avatar me-3 bg-primary text-white rounded-circle text-center"
                      style="width: 40px; height: 40px; line-height: 40px"
                    >
                      {{ review.user_name.slice(0, 1).toUpperCase() }}
                    </div>
                    <div>
                      <h6 class="mb-0">{{ review.user_name }}</h6>
                      <div class="ratings-stars small">
                        <i
                          v-for="n in 5"
                          :key="n"
                          :class="[
                            'fas',
                            n <= Math.round(review.rating)
                              ? 'fa-star text-warning'
                              : 'far fa-star text-warning',
                          ]"
                        ></i>
                      </div>
                      <small class="text-muted">{{
                        new Date(review.created_at).toLocaleDateString('es-ES')
                      }}</small>
                    </div>
                  </div>
                  <p>{{ review.comment }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Right Column: Contact Info, Map, Hours -->
          <div class="col-lg-4">
            <!-- Contact Information -->
            <div class="card shadow-sm mb-4">
              <div class="card-header bg-white">
                <h3 class="card-title h5 mb-0">Información de Contacto</h3>
              </div>
              <ul class="list-group list-group-flush">
                <li class="list-group-item d-flex">
                  <i class="fas fa-map-marker-alt text-primary me-3 mt-1"></i>
                  <div>
                    <div class="fw-bold">Dirección</div>
                    <div>{{ restaurant.address }}</div>
                  </div>
                </li>
                <li class="list-group-item d-flex">
                  <i class="fas fa-phone text-primary me-3 mt-1"></i>
                  <div>
                    <div class="fw-bold">Teléfono</div>
                    <div>{{ restaurant.phone }}</div>
                  </div>
                </li>
                <li class="list-group-item d-flex">
                  <i class="fas fa-envelope text-primary me-3 mt-1"></i>
                  <div>
                    <div class="fw-bold">Email</div>
                    <div>{{ restaurant.email }}</div>
                  </div>
                </li>
                <li class="list-group-item d-flex">
                  <i class="fas fa-globe text-primary me-3 mt-1"></i>
                  <div>
                    <div class="fw-bold">Website</div>
                    <div>
                      <a href="#" class="text-primary">{{ restaurant.email }}</a>
                    </div>
                  </div>
                </li>
              </ul>
            </div>

            <!-- Opening Hours -->
            <div class="card shadow-sm mb-4">
              <div class="card-header bg-white">
                <h3 class="card-title h5 mb-0">Horario de apertura</h3>
              </div>
              <ul class="list-group list-group-flush">
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  <span>Lunes</span>
                  <span>11:00 AM - 10:00 PM</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  <span>Martes</span>
                  <span>11:00 AM - 10:00 PM</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  <span>Miercoles</span>
                  <span>11:00 AM - 10:00 PM</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  <span>Jueves</span>
                  <span>11:00 AM - 10:00 PM</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  <span>Viernes</span>
                  <span>11:00 AM - 11:00 PM</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  <span>Sábado</span>
                  <span>11:00 AM - 11:00 PM</span>
                </li>
                <li class="list-group-item d-flex justify-content-between align-items-center">
                  <span>Domingo</span>
                  <span>12:00 PM - 9:00 PM</span>
                </li>
              </ul>
            </div>

            <!-- Location Map -->
            <div v-if="restaurant.embedded_map" id="map" class="card shadow-sm mb-4">
              <div class="card-header bg-white">
                <h3 class="card-title h5 mb-0">Ubicación</h3>
              </div>
              <iframe
                v-if="restaurant.embedded_map"
                :src="restaurant.embedded_map"
                height="450"
                style="border: 0"
                allowfullscreen=""
                loading="lazy"
                referrerpolicy="no-referrer-when-downgrade"
              ></iframe>
            </div>
          </div>
        </div>
      </section>
    </div>
  </BaseLayout>
</template>

<script setup>
import BaseLayout from '@/views/layouts/BaseLayout.vue'
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { fetchRestaurantDetails } from '@/services/restaurantService'
import { fetchUnsplashImages } from '@/services/imageService'
import { fetchResturantReviews } from '@/services/reviewService'
import { fetchMenuByRestaurantId } from '@/services/menuService'

const route = useRoute()
const restaurantId = route.params.id
const menuItems = ref([])

const reviews = ref([])
const averageRating = ref(0)
const ratingCounts = ref({ 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 })
const totalReviews = ref(0)

const restaurant = ref({})
const loading = ref(true)
const coverImageUrl = ref('')

const calculateRatings = (reviewsList) => {
  const counts = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 }
  let total = 0

  reviewsList.forEach((review) => {
    const rating = Math.round(review.rating)
    counts[rating] = (counts[rating] || 0) + 1
    total += review.rating
  })

  totalReviews.value = reviewsList.length
  ratingCounts.value = counts
  averageRating.value = (total / reviewsList.length).toFixed(1)
}

const fetchRestaurant = async () => {
  try {
    const data = await fetchRestaurantDetails(restaurantId)
    restaurant.value = data

    // Fetch menu items after fetching restaurant
    menuItems.value = await fetchMenuByRestaurantId(restaurantId)
    console.log('Menu items:', menuItems.value)
    const images = await fetchUnsplashImages(data.name)
    if (images.length > 0) {
      coverImageUrl.value = images[0].urls.regular
    }
  } catch (error) {
    console.error('Error fetching restaurant details or menu items:', error)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await fetchRestaurant()
  try {
    const data = await fetchResturantReviews(restaurantId)
    reviews.value = data
    calculateRatings(data)
  } catch (err) {
    console.error('Error loading reviews:', err)
  }
})
</script>

<style scoped>
/* Hero Section Styles */
.restaurant-hero {
  height: 400px;
  margin-bottom: 2rem;
  display: flex;
  align-items: flex-end;
}

.cover-image-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}

.cover-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    0deg,
    rgba(0, 0, 0, 0.7) 0%,
    rgba(0, 0, 0, 0.3) 50%,
    rgba(0, 0, 0, 0.1) 100%
  );
}

.restaurant-header {
  padding: 2rem 0;
  position: relative;
  z-index: 1;
}

.z-1 {
  z-index: 1;
}

/* Card Styles */
.card {
  border: none;
  border-radius: 0.5rem;
  overflow: hidden;
}

.card-header {
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  padding: 1rem 1.25rem;
}

/* Map Styles */
.map-container {
  height: 250px;
  width: 100%;
}

.google-map {
  height: 100%;
  width: 100%;
  background-color: #f8f9fa; /* Placeholder color */
}

/* Avatar */
.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

/* Popular Dishes */
.popular-dishes {
  width: 100%;
}

.dish-card {
  display: flex;
  padding: 1rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.dish-card:last-child {
  border-bottom: none;
}

.dish-info {
  flex: 1;
}

.dish-name {
  margin-bottom: 0.25rem;
}

.dish-description {
  color: #6c757d;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.dish-price {
  font-weight: bold;
  color: #343a40;
}

/* Action Card */
.action-card {
  border-top: 4px solid #007bff;
}

/* Media Queries */
@media (max-width: 767.98px) {
  .restaurant-hero {
    height: 300px;
  }

  .restaurant-name {
    font-size: 2rem;
  }
}
</style>
